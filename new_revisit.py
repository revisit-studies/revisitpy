from __future__ import annotations
import json
import models as rvt_models
from pydantic import BaseModel, parse_obj_as
from typing import List, Optional, get_args, Any, Unpack, overload, Union


def _get_filtered_kwargs(class_type: Any, kwargs):
    try:
        possible_items = get_args(class_type.__fields__.get('root').annotation)
    except AttributeError:
        possible_items = [class_type]

    valid_fields = set()
    for model in possible_items:
        valid_fields.update(model.model_fields.keys())

    return {key: value for key, value in kwargs.items() if key in valid_fields}


class _JSONableBaseModel(BaseModel):
    def __str__(self):
        return json.dumps(json.loads(self.root.model_dump_json(exclude_none=True, by_alias=True)), indent=4)


# Private
class _WrappedResponse(_JSONableBaseModel):
    root: rvt_models.Response

    def model_post_init(self, __context: Any) -> None:
        # Sets the root to be the instantiation of the individual response type instead
        # of the union response type
        self.root = self.root.root

    def data(self, overwrite=True, **kwargs) -> _WrappedResponse:
        for key, value in kwargs.items():
            # Disallow changing type
            if key == 'type':
                if getattr(self.root, key) != value:
                    raise ValueError(f"Cannot change type from {getattr(self.root, key)} to {value}")
            elif key != 'base':
                if overwrite is True or (overwrite is False and getattr(self.root, key) is None):
                    setattr(self.root, key, parse_obj_as(type(getattr(self.root, key)), value))
        return self


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
        for response in self.root.response:
            if response.root.id == id:
                response.data(**kwargs)
                return self

        raise ValueError('No response with given ID found.')

    def response_context(self, **kwargs):
        self.context__ = kwargs

        for type, data in self.context__.items():
            for response in self.root.response:
                if response.root.type == type or type == 'all':
                    response.data(
                        overwrite=False,
                        **data
                    )

        return self


class _WrappedStudyMetadata(_JSONableBaseModel):
    root: rvt_models.StudyMetadata


class _WrappedUIConfig(_JSONableBaseModel):
    root: rvt_models.UIConfig


class _WrappedComponentBlock(_JSONableBaseModel):
    root: rvt_models.ComponentBlock


class _WrappedStudyConfig(_JSONableBaseModel):
    root: rvt_models.StudyConfig


class _StudyConfigType(rvt_models.StudyConfigType):
    components: List[_WrappedComponent]


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

    filter_kwargs = _get_filtered_kwargs(rvt_models.IndividualComponent, kwargs)

    base_model = rvt_models.IndividualComponent(**filter_kwargs)
    return _WrappedComponent(**kwargs, root=base_model)


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
    base_model = rvt_models.Response(**filter_kwargs)
    return _WrappedResponse(**kwargs, root=base_model)


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
    base_model = rvt_models.ComponentBlock(**filter_kwargs)
    return _WrappedComponentBlock(**kwargs, root=base_model)


@overload
def studyConfig(**kwargs: Unpack[_StudyConfigType]) -> _WrappedStudyConfig: ...
@overload
def studyConfig(**kwargs: Any) -> _WrappedStudyConfig: ...


def studyConfig(**kwargs: Unpack[_StudyConfigType]) -> _WrappedStudyConfig:
    filter_kwargs = _get_filtered_kwargs(rvt_models.StudyConfig, kwargs)

    root_list = ['studyMetadata', 'uiConfig', 'sequence']
    unrooted_kwargs = {x: (y.root if x in root_list else y) for x, y in filter_kwargs.items()}

    unrooted_kwargs['components'] = {comp.component_name__: comp.root for comp in unrooted_kwargs.get('components', [])}

    base_model = rvt_models.StudyConfig(**unrooted_kwargs)
    return _WrappedStudyConfig(**kwargs, root=base_model)
