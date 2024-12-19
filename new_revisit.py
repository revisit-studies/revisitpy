from __future__ import annotations
import json
import models as rvt_models
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, get_args, Any


# Private
class _WrappedResponse(BaseModel):
    root: rvt_models.Response

    def model_post_init(self, __context: Any) -> None:
        # Sets the root to be the instantiation of the individual response type instead
        # of the union response type
        self.root = self.root.root

    def __str__(self):
        return json.dumps(json.loads(self.root.model_dump_json(exclude_none=True)), indent=4)

    def data(self, overwrite=True, **kwargs):
        for key, value in kwargs.items():
            if key != 'base':
                if overwrite is True or (overwrite is False and getattr(self.root, key) is None):
                    setattr(self.root, key, value)
        return self


# Private
class _WrappedComponent(BaseModel):
    component_name__: str
    base__: Optional[_WrappedComponent] = None
    context__: Optional[dict] = None
    root: rvt_models.IndividualComponent

    def model_post_init(self, __context: Any) -> None:
        # Sets the root to be the instantiation of the individual response type instead
        # of the union response type
        self.root = self.root.root

    def __str__(self):
        return json.dumps(json.loads(self.root.model_dump_json(exclude_none=True)), indent=4)

    def responses(self, responses: List[_WrappedResponse]) -> None:
        for item in responses:
            if not isinstance(item, _WrappedResponse):
                raise ValueError(f'Expecting type Response got {type(item)}')
        self.root.response = responses
        return self

    def get_response(self, id: str) -> _WrappedResponse | None:
        for response in self.root.response:
            if response.id == id:
                return response
        return None

    def edit_response(self, id: str, **kwargs) -> _WrappedComponent:
        for response in self.root.response:
            if response.id == id:
                response.data(**kwargs)
                return self

        raise ValueError('No response with given ID found.')

    def response_context(self, **kwargs):
        self.context__ = kwargs

        for type, data in self.context__.items():
            for response in self.response:
                if response.type == type or type == 'all':
                    response.data(
                        overwrite=False,
                        **data
                    )

        return self

# # -----------------------------------
# # Factory Functions
# # -----------------------------------

# Component factory function
# Allows additional items to be sent over to our Component model while keeping restrictions
# for the model that is auto-generated.


def component(**kwargs):

    # Inherit base
    base_component = kwargs.get('base__', None)
    if base_component:
        base_fields = vars(base_component.root)
        for key, value in base_fields.items():
            if key not in kwargs:
                kwargs[key] = value
    possible_components = get_args(rvt_models.IndividualComponent.__fields__.get('root').annotation)

    # Iterates over all possible fields for passing to Individual Component
    valid_fields = set()
    for model in possible_components:
        valid_fields.update(model.model_fields.keys())

    filter_kwargs = {key: value for key, value in kwargs.items() if key in valid_fields}

    base_model = rvt_models.IndividualComponent(**filter_kwargs)
    return _WrappedComponent(**kwargs, root=base_model)

# Response factory function


def response(**kwargs):
    possible_components = get_args(rvt_models.Response.__fields__.get('root').annotation)

    # Iterates over all possible fields for passing to Individual Component
    valid_fields = set()
    for model in possible_components:
        valid_fields.update(model.model_fields.keys())

        filter_kwargs = {key: value for key, value in kwargs.items() if key in valid_fields}

    base_model = rvt_models.Response(**filter_kwargs)
    return _WrappedResponse(**kwargs, root=base_model)
