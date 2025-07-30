# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args

ComponentType = typing.Union[
    str,
    int,
    float,
    Component,
    None,
    typing.Sequence[typing.Union[str, int, float, Component, None]],
]

NumberType = typing.Union[
    typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
]


class Loader(Component):
    """A Loader component.
Component to serve as Loader for Graphs

Keyword arguments:

- id (string; required):
    Unique ID to identify this component in Dash callbacks.

- output (string; required):
    element that should be extracted from the request result.

- request (boolean | number | string | dict | list; required):
    url to load the data.

- url (string; required):
    url to load the data."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dashpool_components'
    _type = 'Loader'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        url: typing.Optional[str] = None,
        request: typing.Optional[typing.Any] = None,
        output: typing.Optional[str] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'output', 'request', 'url']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'output', 'request', 'url']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'output', 'request', 'url']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Loader, self).__init__(**args)

setattr(Loader, "__init__", _explicitize_args(Loader.__init__))
