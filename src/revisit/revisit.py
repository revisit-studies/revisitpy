from __future__ import annotations
import json
from . import models as rvt_models
from pydantic import BaseModel, ValidationError  # type: ignore
from typing import List, Literal, get_origin, Optional, get_args, Any, Unpack, overload, get_type_hints
from enum import Enum
import csv
from dataclasses import make_dataclass
import re
import os
import shutil
from . import widget as _widget


__all__ = [
    "component",
    "sequence",
    "response",
    "uiConfig",
    "studyMetadata",
    "studyConfig",
    "data",
    "widget"
]


class _JSONableBaseModel(BaseModel):
    def __str__(self):
        return json.dumps(
            json.loads(
                self.root.model_dump_json(
                    exclude_none=True, by_alias=True
                )),
            indent=4
        )


# Private
class _WrappedResponse(_JSONableBaseModel):
    root: rvt_models.Response

    def model_post_init(self, __context: Any) -> None:
        # Sets the root to be the instantiation of the individual response type instead
        # of the union response type
        self.root = self.root.root

    def set(self, overwrite=True, **kwargs) -> _WrappedResponse:
        for key, value in kwargs.items():
            # Disallow changing type
            if key == 'type':
                if getattr(self.root, key) != value:
                    raise RevisitError(message=f"Cannot change type from {getattr(self.root, key)} to {value}")
            elif key != 'base':
                if overwrite is True or (overwrite is False and getattr(self.root, key) is None):
                    setattr(self.root, key, value)

        # Re-validates the model. Returns the new model.
        self.root = _validate_response(self.root.__dict__)
        return self

    def clone(self):
        return response(**self.root.__dict__)


# Private
class _WrappedComponent(_JSONableBaseModel):
    component_name__: str
    base__: Optional[_WrappedComponent] = None
    context__: Optional[dict] = None
    root: rvt_models.IndividualComponent

    def model_post_init(self, __context: Any) -> None:
        # Sets the root to be the instantiation of the individual response type instead
        # of the union response type
        self.root = self.root.root

    def responses(self, responses: List[_WrappedResponse]) -> _WrappedComponent:
        for item in responses:
            if not isinstance(item, _WrappedResponse):
                raise ValueError(f'Expecting type Response got {type(item)}')
        self.root.response = responses
        return self

    def get_response(self, id: str) -> _WrappedResponse | None:
        for response in self.root.response:
            if response.root.id == id:
                return response
        return None

    def edit_response(self, id: str, **kwargs) -> _WrappedComponent:
        for r in self.root.response:
            if r.root.id == id:
                # Get dict 
                response_dict = r.root.__dict__
                # Create new response
                new_response = response(**response_dict)
                # Set with new values
                new_response.set(**kwargs)
                # Filter out old response
                self.root.response = [_r for _r in self.root.response if _r.root.id != id]
                # Add new response
                self.root.response.append(new_response)
                # Return component
                return self

        raise ValueError('No response with given ID found.')

    def response_context(self, **kwargs):
        self.context__ = kwargs

        for type, data in self.context__.items():
            for response in self.root.response:
                if response.root.type == type or type == 'all':
                    response.set(
                        overwrite=False,
                        **data
                    )

        return self

    def clone(self, component_name__):
        return component(**self.root.__dict__, component_name__=component_name__)


class _WrappedStudyMetadata(_JSONableBaseModel):
    root: rvt_models.StudyMetadata


class _WrappedUIConfig(_JSONableBaseModel):
    root: rvt_models.UIConfig


class _WrappedComponentBlock(_JSONableBaseModel):
    root: rvt_models.ComponentBlock
    component_objects__: List[_WrappedComponent]

    def __add__(self, other):
        """Allows addition operator to append to sequence components list."""
        if isinstance(other, _WrappedComponent):
            self.component_objects__.append(other)
            self.root.components.append(other.component_name__)
            return self
        elif isinstance(other, _WrappedComponentBlock):
            # Extend existing list of components with new set of components for tracking
            self.component_objects__.extend(other.component_objects__)

            # Add root object to components
            self.root.components.append(other.root)
            return self
        return NotImplemented

    def from_data(self, data_list) -> DataIterator:
        if not isinstance(data_list, list):
            raise RevisitError(
                message="'from_data' must take in a list of data rows. Use reVISit's 'data' method to parse a CSV file into a valid input."
            )
        return DataIterator(data_list, self)


class _WrappedStudyConfig(_JSONableBaseModel):
    root: rvt_models.StudyConfig


class _StudyConfigType(rvt_models.StudyConfigType):
    components: List[_WrappedComponent]


class DataIterator:
    def __init__(self, data_list: List, parent_class: _WrappedComponentBlock):
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
                            param_datum_value = _extract_datum_value(param_value)
                            if param_datum_value is not None:
                                param_dict[param_key] = getattr(datum, param_datum_value)
                            else:
                                param_dict[param_key] = value
                        else:
                            param_dict[param_key] = value
                    current_dict[key] = param_dict
                else:
                    if type(value) is str:
                        datum_value = _extract_datum_value(value)
                        if datum_value is not None:
                            if key == 'component_name__':
                                current_dict[key] = str(getattr(datum, datum_value))
                            else:
                                current_dict[key] = getattr(datum, datum_value)
                        else:
                            current_dict[key] = value
                    else:
                        current_dict[key] = value
            curr_component = component(**current_dict)
            self.parent_class = self.parent_class + curr_component
        # Return the parent class calling iterator when component is finished.
        return self.parent_class


# # -----------------------------------
# # Factory Functions
# # -----------------------------------

# Component factory function
# Allows additional items to be sent over to our Component model while keeping restrictions
# for the model that is auto-generated.

@overload
def component(**kwargs: Unpack[rvt_models.MarkdownComponentType]) -> _WrappedComponent: ...
@overload
def component(**kwargs: Unpack[rvt_models.ReactComponentType]) -> _WrappedComponent: ...
@overload
def component(**kwargs: Unpack[rvt_models.ImageComponentType]) -> _WrappedComponent: ...
@overload
def component(**kwargs: Unpack[rvt_models.WebsiteComponentType]) -> _WrappedComponent: ...
@overload
def component(**kwargs: Unpack[rvt_models.QuestionnaireComponentType]) -> _WrappedComponent: ...
@overload
def component(**kwargs: Any) -> _WrappedComponent: ...


def component(**kwargs) -> _WrappedComponent:
    # Inherit base
    base_component = kwargs.get('base__', None)
    if base_component:
        base_fields = vars(base_component.root)
        for key, value in base_fields.items():
            if key not in kwargs:
                kwargs[key] = value
    # Get kwargs to pass to individual component
    filter_kwargs = _get_filtered_kwargs(rvt_models.IndividualComponent, kwargs)
    # Grab response list
    response = filter_kwargs.get('response')

    # Sets default response list
    valid_response = []
    # If response present
    if response is not None:
        for r in response:

            # Prevent dict input
            if isinstance(r, dict):
                raise RevisitError(message='Cannot pass a dictionary directly into "Response" list.')

            response_type_hint = get_type_hints(rvt_models.Response).get('root')
            response_types = get_args(response_type_hint)

            # If wrapped, get root
            if isinstance(r, _WrappedResponse):
                valid_response.append(r.root)

            # If not wrapped but is valid response, append to list
            elif r.__class__ in response_types:
                valid_response.append(r)

            # If other unknown type, raise error
            else:
                raise RevisitError(message=f'Invalid type {type(r)} for "Response" class.')

    filter_kwargs['response'] = valid_response

    # Validate component
    _validate_component(filter_kwargs)
    base_model = rvt_models.IndividualComponent(**filter_kwargs)

    try:
        return _WrappedComponent(**kwargs, root=base_model)
    except ValidationError as e:
        raise RevisitError(e.errors())


# Response factory function
@overload
def response(**kwargs: Unpack[rvt_models.NumericalResponseType]) -> _WrappedResponse: ...
@overload
def response(**kwargs: Unpack[rvt_models.ShortTextResponseType]) -> _WrappedResponse: ...
@overload
def response(**kwargs: Unpack[rvt_models.LongTextResponseType]) -> _WrappedResponse: ...
@overload
def response(**kwargs: Unpack[rvt_models.LikertResponseType]) -> _WrappedResponse: ...
@overload
def response(**kwargs: Unpack[rvt_models.DropdownResponseType]) -> _WrappedResponse: ...
@overload
def response(**kwargs: Unpack[rvt_models.SliderResponseType]) -> _WrappedResponse: ...
@overload
def response(**kwargs: Unpack[rvt_models.RadioResponseType]) -> _WrappedResponse: ...
@overload
def response(**kwargs: Unpack[rvt_models.CheckboxResponseType]) -> _WrappedResponse: ...
@overload
def response(**kwargs: Unpack[rvt_models.IFrameResponseType]) -> _WrappedResponse: ...
@overload
def response(**kwargs: Unpack[rvt_models.MatrixResponseType]) -> _WrappedResponse: ...
@overload
def response(**kwargs: Any) -> _WrappedResponse: ...


def response(**kwargs) -> _WrappedResponse:
    filter_kwargs = _get_filtered_kwargs(rvt_models.Response, kwargs)
    _validate_response(filter_kwargs)
    base_model = rvt_models.Response(**filter_kwargs)
    # We've validated the response for a particular type. Now, how do we validate the wrapped component correctly?
    try:
        return _WrappedResponse(**kwargs, root=base_model)
    except ValidationError as e:
        raise RevisitError(e.errors())


def studyMetadata(**kwargs: Unpack[rvt_models.StudyMetadataType]):
    filter_kwargs = _get_filtered_kwargs(rvt_models.StudyMetadata, kwargs)
    base_model = rvt_models.StudyMetadata(**filter_kwargs)
    return _WrappedStudyMetadata(**kwargs, root=base_model)


def uiConfig(**kwargs: Unpack[rvt_models.UIConfigType]):
    filter_kwargs = _get_filtered_kwargs(rvt_models.UIConfig, kwargs)
    base_model = rvt_models.UIConfig(**filter_kwargs)
    return _WrappedUIConfig(**kwargs, root=base_model)


def sequence(**kwargs: Unpack[rvt_models.ComponentBlockType]):
    filter_kwargs = _get_filtered_kwargs(rvt_models.ComponentBlock, kwargs)
    valid_component_names = []
    valid_components = []
    components = filter_kwargs.get('components')
    if components is not None:
        for c in components:

            # Prevent dict input
            if isinstance(c, dict):
                raise RevisitError(message='Cannot pass a dictionary directly into "Component" list.')

            # If wrapped, get root
            if isinstance(c, _WrappedComponent):
                valid_component_names.append(c.component_name__)
                valid_components.append(c)

            # If other unknown type, raise error
            else:
                raise RevisitError(message=f'Invalid type {type(c)} for "Component" class.')

    filter_kwargs['components'] = valid_component_names
    base_model = rvt_models.ComponentBlock(**filter_kwargs)
    return _WrappedComponentBlock(**kwargs, root=base_model, component_objects__=valid_components)


@overload
def studyConfig(**kwargs: Unpack[_StudyConfigType]) -> _WrappedStudyConfig: ...
@overload
def studyConfig(**kwargs: Any) -> _WrappedStudyConfig: ...


def studyConfig(**kwargs: Unpack[_StudyConfigType]) -> _WrappedStudyConfig:
    filter_kwargs = _get_filtered_kwargs(rvt_models.StudyConfig, kwargs)

    root_list = ['studyMetadata', 'uiConfig', 'sequence']
    un_rooted_kwargs = {x: (y.root if x in root_list and hasattr(y, 'root') else y) for x, y in filter_kwargs.items()}

    study_sequence = filter_kwargs['sequence']

    # Merges components from the components list given and the components that are stored in the sequence
    un_rooted_kwargs['components'] = {
        comp.component_name__: comp.root for comp in un_rooted_kwargs.get('components', [])
    } | {
        comp.component_name__: comp.root for comp in study_sequence.component_objects__
    }

    base_model = rvt_models.StudyConfig(**un_rooted_kwargs)
    return _WrappedStudyConfig(**kwargs, root=base_model)


# Function to parse the CSV and dynamically create data classes
def data(file_path: str) -> List[Any]:
    # Read the first row to get the headers
    with open(file_path, mode='r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        headers = csv_reader.fieldnames
        if not headers:
            raise RevisitError(message="No headers found in CSV file.")

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


def widget(study: _WrappedStudyConfig, revisitPath: str):
    if not os.path.isdir(revisitPath):
        raise RevisitError(message=f'"{revisitPath}" does not exist.')

    extracted_paths = []

    for component in study.root.components.values():
        if hasattr(component.root, 'path'):

            fileName = component.root.path.split('/')[-1]

            if component.root.type == 'react-component':
                dest = f"{revisitPath}/src/public/__revisit-widget/assets/{fileName}"
            else:
                dest = f"{revisitPath}/public/__revisit-widget/assets/{fileName}"

            extracted_paths.append({
                "src": component.root.path,
                "dest": dest
            })

            newPath = f"__revisit-widget/assets/{fileName}"
            component.root.path = newPath

    uiConfig = study.root.uiConfig
    if uiConfig.helpTextPath is not None:

        fileName = uiConfig.helpTextPath.split('/')[-1]
        dest = f"{revisitPath}/public/__revisit-widget/assets/{fileName}"

        extracted_paths.append({
            "src": uiConfig.helpTextPath,
            "dest": dest
        })

        newPath = f"__revisit-widget/assets/{fileName}"
        uiConfig.helpTextPath = newPath

    if uiConfig.logoPath is not None:

        fileName = uiConfig.logoPath.split('/')[-1]

        dest = f"{revisitPath}/public/__revisit-widget/assets/{fileName}"

        extracted_paths.append({
            "src": uiConfig.logoPath,
            "dest": dest
        })

        newPath = f"__revisit-widget/assets/{fileName}"
        uiConfig.logoPath = newPath

    # Copy all files
    for item in extracted_paths:
        _copy_file(item['src'], item['dest'])

    w = _widget.Widget()
    w.config = json.loads(study.__str__())
    return w


# ------- PRIVATE FUNCTIONS ------------ #

def _validate_component(kwargs: dict):
    component_mapping = _generate_possible_component_types()[1]
    if 'type' not in kwargs:
        raise RevisitError(message='"Type" is required on Component.')
    elif component_mapping.get(kwargs['type']) is None:
        raise RevisitError(message=f'Unexpected component type: {kwargs['type']}')

    try:
        return rvt_models.IndividualComponent.model_validate(kwargs).root
    except ValidationError as e:
        temp_errors = []

        for entry in e.errors():
            if entry['loc'][0] == component_mapping[kwargs['type']]:
                temp_errors.append(entry)

        if len(temp_errors) > 0:
            raise RevisitError(temp_errors)
        else:
            raise RevisitError(
                message='Unexpected error occurred during Component instantiation.'
            )


# Call validate response when creating response component.
def _validate_response(kwargs: dict):
    response_mapping = _generate_possible_response_types()[1]
    if 'type' not in kwargs:
        raise RevisitError(message='"Type" is required on Response.')
    else:

        type_value = kwargs.get('type')

        # Handles enum class type
        if isinstance(kwargs.get('type'), Enum):
            type_value = type_value.value

        if response_mapping.get(type_value) is None:
            raise RevisitError(message=f'Unexpected type: {type_value}')

        try:
            return rvt_models.Response.model_validate(kwargs).root
        except ValidationError as e:
            temp_errors = []
            for entry in e.errors():
                if entry['loc'][0] == response_mapping[type_value]:
                    temp_errors.append(entry)

            if len(temp_errors) > 0:
                raise RevisitError(temp_errors)
            else:
                raise RevisitError(
                    message='Unexpected error occurred during Response instantiation'
                )


def _generate_possible_response_types():
    return _generate_possible_types(rvt_models.Response)


def _generate_possible_component_types():
    return _generate_possible_types(rvt_models.IndividualComponent)


# Generates mappings between the response class name and the
# type string literal. Creates the reversed mapping as well.
def _generate_possible_types(orig_cls):
    type_hints = get_type_hints(orig_cls).get('root')
    types = get_args(type_hints)
    type_hints = {}
    type_hints_reversed = {}
    for cls in types:
        # If class is the union of two separate classes,
        # need to get types from root
        if get_type_hints(cls).get('root') is not None:
            test = get_type_hints(cls).get('root')
            for item in get_args(test):
                curr_type = get_type_hints(item).get('type')
                type_hints[cls.__name__] = set([get_args(curr_type)[0]])
                type_hints_reversed[get_args(curr_type)[0]] = cls.__name__
        else:
            curr_type = get_type_hints(cls).get('type')
            curr_origin = get_origin(get_type_hints(cls).get('type'))
            if curr_origin is Literal:
                type_hints[cls.__name__] = set([get_args(curr_type)[0]])
                type_hints_reversed[get_args(curr_type)[0]] = cls.__name__
            elif isinstance(curr_type, type) and issubclass(curr_type, Enum):
                enum_list = [member.value for member in curr_type]
                type_hints[cls.__name__] = set(enum_list)
                for item in enum_list:
                    type_hints_reversed[item] = cls.__name__
    return (type_hints, type_hints_reversed)


# Custom exception
class RevisitError(Exception):
    def __init__(self, errors=None, message=None):
        # Case 1: Validation Errors From Pydantic
        # Case 2: Standard Error Message
        super().__init__('There was an error.')
        if message is None:
            pretty_message_list = pretty_error(errors)
            self.message = \
                f'There was an error. \n' \
                f'----------------------------------------------------' \
                f'\n\n' \
                f'{'\n\n'.join(pretty_message_list)}' \
                f'\n'
        else:
            self.message = \
                f'There was an error. \n' \
                f'----------------------------------------------------' \
                f'\n\n' \
                f'{message}' \
                f'\n'

    def __str__(self):
        return self.message


def pretty_error(errors):
    custom_messages = {
        'missing': 'Field is missing'
    }
    new_error_messages = []
    for error in errors:
        custom_message = custom_messages.get(error['type'])
        if custom_message:
            new_error_messages.append(f'Location: {error['loc']}\nError: Field "{error['loc'][-1]}" is required.')
        else:
            new_error_messages.append(f'Location: {error['loc']}\nError: {error['msg']}')
    return new_error_messages


def _get_filtered_kwargs(class_type: Any, kwargs):
    try:
        possible_items = get_args(class_type.model_fields.get('root').annotation)
    except AttributeError:
        possible_items = [class_type]

    valid_fields = set()
    for model in possible_items:
        if 'root' in model.model_fields.keys():
            unioned_classes = (get_args(get_type_hints(model).get('root')))
            for cls in unioned_classes:
                valid_fields.update(cls.model_fields.keys())
                
        valid_fields.update(model.model_fields.keys())

    return {key: value for key, value in kwargs.items() if key in valid_fields}


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


def _extract_datum_value(text: str) -> str:
    # Use regex to match 'datum:thing' and capture 'thing'
    match = re.match(r'^datum:(\w+)$', text)
    if match:
        return match.group(1)  # Return the captured part (i.e., 'thing')
    return None  # Return None if the pattern doesn't match


def _copy_file(src: str, dest: str):
    # Check if file exists
    if not os.path.exists(src):
        raise RevisitError(message=f'File "{src}" not found.')

    os.makedirs(os.path.dirname(dest), exist_ok=True)

    print(f'Copying file from {src} to {dest}')
    shutil.copyfile(src, dest)
