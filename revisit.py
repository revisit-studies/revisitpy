from typing import List, Any
import json
import copy
from itertools import permutations
import csv
from dataclasses import make_dataclass
import re

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
        print(f"Wrote study config to {file_path}")


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

    def from_data(self, data_list: list):
        return DataIterator(data_list, self)


class StudyMetadata(TopLevel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UIConfig(TopLevel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Components(TopLevel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DataIterator:
    def __init__(self, data_list: List, parent_class: Sequence):
        self.data = data_list
        self.parent_class = parent_class

    def component(self, **kwargs):
        for datum in self.data:
            current_dict = {}
            for key, value in kwargs.items():
                if key == 'parameters':
                    param_dict = {}
                    for param_key, param_value in value.items():
                        if type(param_value) is str:
                            param_datum_value = extract_datum_value(param_value)
                            if param_datum_value is not None:
                                param_dict[param_key] = getattr(datum, param_datum_value)
                            else:
                                param_dict[param_key] = value
                        else:
                            param_dict[param_key] = value
                    current_dict[key] = param_dict
                else:
                    if type(value) is str:
                        datum_value = extract_datum_value(value)
                        if datum_value is not None:
                            if key == '__name__':
                                current_dict[key] = str(getattr(datum, datum_value))
                            else:
                                current_dict[key] = getattr(datum, datum_value)
                        else:
                            current_dict[key] = value
                    else:
                        current_dict[key] = value
            curr_component = Component(**current_dict)
            self.parent_class = self.parent_class + curr_component

        # Return the parent class calling iterator when component is finished.
        return self.parent_class


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


# Function to parse the CSV and dynamically create data classes
def data(file_path: str) -> List[Any]:
    # Read the first row to get the headers
    with open(file_path, mode='r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        headers = csv_reader.fieldnames
        if not headers:
            raise ValueError("CSV file has no headers.")

        # Create a data class with attributes based on the headers
        DataRow = make_dataclass("DataRow", [(header, Any) for header in headers])

        # Parse each row into an instance of the dynamically created data class
        data_rows = []
        for row in csv_reader:
            # Convert the row values to the appropriate types (e.g., int, float, bool)
            data = {key: _convert_value(value) for key, value in row.items()}
            data_row = DataRow(**data)
            data_rows.append(data_row)

    return data_rows


def _convert_value(value: str) -> Any:
    """Helper function to convert string values to appropriate data types."""
    value = value.strip()
    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    try:
        if '.' in value:
            return float(value)
        else:
            return int(value)
    except ValueError:
        return value  # Return as string if it cannot be converted


def extract_datum_value(text: str) -> str:
    # Use regex to match 'datum:thing' and capture 'thing'
    match = re.match(r'^datum:(\w+)$', text)
    if match:
        return match.group(1)  # Return the captured part (i.e., 'thing')
    return None  # Return None if the pattern doesn't match
