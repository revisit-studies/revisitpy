from typing import List, Dict
import json
import copy
from itertools import permutations


class Study:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if self.sequence is not None:
            self.components = json.loads(self.sequence.generate_components())

    def __str__(self):
        return str(self.json())

    def json(self):
        current_dict = {}
        for attr, value in vars(self).items():
            if isinstance(value, UIConfig):
                value = json.loads(value.json())
            if isinstance(value, Sequence):
                value = json.loads(value.json())
            if isinstance(value, StudyMetadata):
                value = json.loads(value.json())

            current_dict[attr] = value
        return json.dumps(current_dict, indent=4)


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

    def data(self, **kwargs):
        for key, value in kwargs.items():
            if key != 'base':
                setattr(self, key, value)
        return self


class Checkbox(Response):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'checkbox'


class Component:
    def __init__(self, **kwargs):
        if 'name' not in kwargs.keys():
            raise ValueError('Name is required in component.')

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
            item.name if isinstance(item, Component) else json.loads(item.json()) for item in self.components
        ]

        current_dict = {
            'order': self.order,
            'components': components_data
        }

        return json.dumps(current_dict, indent=4)

    def generate_components(self, component_dict: Dict = None):
        if component_dict is None:
            component_dict = {}

        for comp in self.components:
            if isinstance(comp, Component):
                component_dict[comp.name] = json.loads(comp.json())
            elif isinstance(comp, Sequence):
                comp.generate_components(component_dict)

        return json.dumps(component_dict, indent=4)


class StudyMetadata(TopLevel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UIConfig(TopLevel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Components(TopLevel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# Factory function for Component
def component(**kwargs):
    return Component(**kwargs)


# Factory function for Checkbox
def checkbox(**kwargs):
    return Checkbox(**kwargs)


def sequence(**kwargs):
    return Sequence(**kwargs)


def study(**kwargs):
    return Study(**kwargs)


def from_response(response: Response):
    return copy.deepcopy(response)


def response(**kwargs):
    return Response(**kwargs)


def permute(items: List[str]):
    return set(permutations(items))


def studyMetadata(**kwargs):
    return StudyMetadata(**kwargs)


def uiConfig(**kwargs):
    return UIConfig(**kwargs)
