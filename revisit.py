from typing import List
import json
import copy
from itertools import permutations


class Study:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if hasattr(self, 'sequence'):
            self.__components_raw__ = self.sequence.get_components()
            # Creates dict object using the given name as the key and the jsonified object as the value.
            self.components = json.dumps(
                {f"{comp.__name__}": json.loads(comp.json()) for comp in self.__components_raw__}, indent=4
            )

    def __str__(self):
        return str(self.json())

    def json(self):
        current_dict = {}

        if hasattr(self, 'sequence'):
            self.__components_raw__ = self.sequence.get_components()

            # Apply response context to each response in each component
            if hasattr(self, '__context__'):
                for type, data in self.__context__.items():
                    for comp in self.__components_raw__:
                        for response in comp.response:
                            if response.type == type or type == 'all':
                                response.data(
                                    overwrite=False,
                                    **data
                                )

            self.components = json.dumps(
                {f"{comp.__name__}": json.loads(comp.json()) for comp in self.__components_raw__}, indent=4
            )

        for attr, value in vars(self).items():
            if not attr.startswith('__'):
                if isinstance(value, UIConfig):
                    value = json.loads(value.json())
                if isinstance(value, Sequence):
                    value = json.loads(value.json())
                if isinstance(value, StudyMetadata):
                    value = json.loads(value.json())
                if attr == 'components':
                    value = json.loads(value)

                current_dict[attr] = value
        return json.dumps(current_dict, indent=4)

    def response_context(self, **kwargs):
        self.__context__ = kwargs
        return self

    def save(self, file_path):
        """Save the object data to a file in JSON format."""
        with open(file_path, 'w') as json_file:
            json.dump(json.loads(self.json()), json_file, indent=4)


class TopLevel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return str(self.json())

    def json(self):
        current_dict = {}
        for attr, value in vars(self).items():
            current_dict[attr] = value

        return json.dumps(current_dict, indent=4)


class Response:
    def __init__(self, **kwargs):

        if 'base' in kwargs.keys():
            for key, value in vars(kwargs['base']).items():
                setattr(self, key, copy.deepcopy(value))

        for key, value in kwargs.items():
            if key != 'base':
                setattr(self, key, value)

    def __str__(self):
        return str(self.json())

    def json(self):
        current_dict = {}
        for attr, value in vars(self).items():
            current_dict[attr] = value
        return json.dumps(current_dict, indent=4)

    def data(self, overwrite=True, **kwargs):
        for key, value in kwargs.items():
            if key != 'base':
                if overwrite is True or (overwrite is False and not hasattr(self, key)):
                    setattr(self, key, value)
        return self


class Checkbox(Response):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'checkbox'


class Component:
    def __init__(self, **kwargs):
        if '__name__' not in kwargs.keys():
            raise ValueError('Attribute "__name__" is required in component.')

        self.response = []

        if 'base' in kwargs.keys():
            for key, value in vars(kwargs['base']).items():
                setattr(self, key, copy.deepcopy(value))

        for key, value in kwargs.items():
            if key == 'response':
                new_response_list = [response(**curr_item) for curr_item in value]
                setattr(self, key, new_response_list)
            elif key != 'base':
                setattr(self, key, value)

    def __str__(self):
        return str(self.json())

    def __add__(self, other):
        if isinstance(other, Response):
            self.response.append(other)
            return self
        return NotImplemented

    def json(self):

        current_dict = {}
        for attr, value in vars(self).items():
            if not attr.startswith('__'):
                if attr == 'response':
                    value = [json.loads(r.json()) for r in self.response]
                current_dict[attr] = value

        return json.dumps(current_dict, indent=4)

    def responses(self, responses: List[Response]) -> None:
        for item in responses:
            if not isinstance(item, Response):
                raise ValueError(f'Expecting type Response got {type(item)}')
        self.response = responses
        return self

    def get_response(self, id: str) -> Response | None:
        for response in self.response:
            if response.id == id:
                return response
        return None

    def edit_response(self, id: str, **kwargs) -> 'Component':
        for response in self.response:
            if response.id == id:
                response.data(**kwargs)
                return self

        raise ValueError('No response with given ID found.')

    def response_context(self, **kwargs):
        self.__context__ = kwargs

        for type, data in self.__context__.items():
            for response in self.response:
                if response.type == type or type == 'all':
                    response.data(
                        overwrite=False,
                        **data
                    )

        return self


class Sequence:
    def __init__(self, **kwargs):
        if 'order' not in kwargs.keys():
            raise ValueError('order must be defined in a sequence.')
        self.components = []

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __add__(self, other):
        if isinstance(other, Sequence) or isinstance(other, Component):
            self.components.append(other)
            return self
        return NotImplemented

    def __str__(self):
        return str(self.json())

    def json(self):

        components_data = [
            item.__name__ if isinstance(item, Component) else json.loads(item.json()) for item in self.components
        ]

        current_dict = {
            'order': self.order,
            'components': components_data
        }

        return json.dumps(current_dict, indent=4)

    def get_components(self, component_list: List[Component] = []):
        for comp in self.components:
            if isinstance(comp, Component):
                component_list.append(comp)
            elif isinstance(comp, Sequence):
                comp.get_components(component_list)

        return component_list


class StudyMetadata(TopLevel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UIConfig(TopLevel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Components(TopLevel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# -----------------------------------
# Factory Functions
# -----------------------------------
def component(**kwargs):
    return Component(**kwargs)


def sequence(**kwargs):
    return Sequence(**kwargs)


def study(**kwargs):
    return Study(**kwargs)


def studyMetadata(**kwargs):
    return StudyMetadata(**kwargs)


def uiConfig(**kwargs):
    return UIConfig(**kwargs)


def response(**kwargs):
    return Response(**kwargs)


def checkbox(**kwargs):
    return Checkbox(**kwargs)

# -----------------------------------
# -----------------------------------


def from_response(response: Response):
    return copy.deepcopy(response)


def permute(items: List[str]):
    return set(permutations(items))
