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


class Explorer(Component):
    """An Explorer component.
A component to mimic a file explorer

Keyword arguments:

- id (string; required):
    Unique ID to identify this component in Dash callbacks.

- dashpoolEvent (dict; optional):
    latest Dashpool Event.

    `dashpoolEvent` is a dict with keys:

    - timestamp (dict; required)

        `timestamp` is a dict with keys:

        - toString (optional):
            Returns a string representation of an object.
            @,param,radix, ,Specifies a radix for converting numeric
            values to strings. This value is only used for numbers.

        - toFixed (required):
            Returns a string representing a number in fixed-point
            notation. @,param,fractionDigits, ,Number of digits after
            the decimal point. Must be in the range 0 - 20, inclusive.

        - toExponential (required):
            Returns a string containing a number represented in
            exponential notation. @,param,fractionDigits, ,Number of
            digits after the decimal point. Must be in the range 0 -
            20, inclusive.

        - toPrecision (required):
            Returns a string containing a number represented either in
            exponential or fixed-point notation with a specified
            number of digits. @,param,precision, ,Number of
            significant digits. Must be in the range 1 - 21,
            inclusive.

        - valueOf (optional):
            Returns the primitive value of the specified object.

        - toLocaleString (dict; optional):
            Converts a number to a string by using the current or
            specified locale. @,param,locales, ,A locale string or
            array of locale strings that contain one or more language
            or locale tags. If you include more than one locale
            string, list them in descending order of priority so that
            the first entry is the preferred locale. If you omit this
            parameter, the default locale of the JavaScript runtime is
            used. @,param,options, ,An object that contains one or
            more properties that specify comparison options.
            @,param,locales, ,A locale string, array of locale
            strings, Intl.Locale object, or array of Intl.Locale
            objects that contain one or more language or locale tags.
            If you include more than one locale string, list them in
            descending order of priority so that the first entry is
            the preferred locale. If you omit this parameter, the
            default locale of the JavaScript runtime is used.
            @,param,options, ,An object that contains one or more
            properties that specify comparison options.

            `toLocaleString` is a dict with keys:


    - type (string; required)

    - data (boolean | number | string | dict | list; optional)

- n_refreshed (number; optional):
    : An integer that represents the number of times that this element
    has been refreshed.

- n_saved (number; optional):
    : An integer that represents the number of times the layout has
    been saved.

- nodeChangeEvent (dict; optional):
    Event if a Tree Node changes.

    `nodeChangeEvent` is a dict with keys:

    - id (string; required)

    - type (string; required)

    - label (string; required)

    - app (boolean | number | string | dict | list; optional)

    - shared (list of strings; optional)

    - icon (string; optional)

    - frame (string; optional)

    - data (boolean | number | string | dict | list; optional)

    - parent (string; optional)

    - layout (string; optional)

- nodes (list of dicts; required):
    Array of nodes shown in the Tree View.

    `nodes` is a list of dicts with keys:

    - id (string; required)

    - type (string; required)

    - label (string; required)

    - app (boolean | number | string | dict | list; optional)

    - shared (list of strings; optional)

    - icon (string; optional)

    - frame (string; optional)

    - data (boolean | number | string | dict | list; optional)

    - parent (string; optional)

    - layout (string; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dashpool_components'
    _type = 'Explorer'
    Nodes = TypedDict(
        "Nodes",
            {
            "id": str,
            "type": str,
            "label": str,
            "app": NotRequired[typing.Any],
            "shared": NotRequired[typing.Sequence[str]],
            "icon": NotRequired[str],
            "frame": NotRequired[str],
            "data": NotRequired[typing.Any],
            "parent": NotRequired[str],
            "layout": NotRequired[str]
        }
    )

    NodeChangeEvent = TypedDict(
        "NodeChangeEvent",
            {
            "id": str,
            "type": str,
            "label": str,
            "app": NotRequired[typing.Any],
            "shared": NotRequired[typing.Sequence[str]],
            "icon": NotRequired[str],
            "frame": NotRequired[str],
            "data": NotRequired[typing.Any],
            "parent": NotRequired[str],
            "layout": NotRequired[str]
        }
    )

    DashpoolEventTimestampToLocaleString = TypedDict(
        "DashpoolEventTimestampToLocaleString",
            {

        }
    )

    DashpoolEventTimestamp = TypedDict(
        "DashpoolEventTimestamp",
            {
            "toString": NotRequired[typing.Any],
            "toFixed": typing.Any,
            "toExponential": typing.Any,
            "toPrecision": typing.Any,
            "valueOf": NotRequired[typing.Any],
            "toLocaleString": NotRequired["DashpoolEventTimestampToLocaleString"]
        }
    )

    DashpoolEvent = TypedDict(
        "DashpoolEvent",
            {
            "timestamp": "DashpoolEventTimestamp",
            "type": str,
            "data": NotRequired[typing.Any]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        nodes: typing.Optional[typing.Sequence["Nodes"]] = None,
        n_refreshed: typing.Optional[NumberType] = None,
        n_saved: typing.Optional[NumberType] = None,
        nodeChangeEvent: typing.Optional["NodeChangeEvent"] = None,
        dashpoolEvent: typing.Optional["DashpoolEvent"] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'dashpoolEvent', 'n_refreshed', 'n_saved', 'nodeChangeEvent', 'nodes']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'dashpoolEvent', 'n_refreshed', 'n_saved', 'nodeChangeEvent', 'nodes']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'nodes']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Explorer, self).__init__(**args)

setattr(Explorer, "__init__", _explicitize_args(Explorer.__init__))
