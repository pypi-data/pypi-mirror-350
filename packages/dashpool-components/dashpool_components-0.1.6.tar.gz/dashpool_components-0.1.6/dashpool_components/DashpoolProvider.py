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


class DashpoolProvider(Component):
    """A DashpoolProvider component.
Context provider for easy interaction between Dashpool components

Keyword arguments:

- children (list of a list of or a singular dash component, string or numbers; required):
    Array of children.

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

- defaultReload (boolean; default True):
    default reload after login.

- dragElement (boolean | number | string | dict | list; optional):
    The last drag element.

- initialData (boolean | number | string | dict | list; optional):
    The initial state for the user. Note! Not everything is reactive.

- requireLogin (boolean; default True):
    require login.

- sharedData (dict; optional):
    the shared data.

    `sharedData` is a dict with keys:

    - dragElement (boolean | number | string | dict | list; optional)

    - apps (list of dicts; optional)

        `apps` is a list of dicts with keys:

        - name (string; required)

        - group (string; required)

        - url (string; required)

        - icon (string; required)

    - frames (list of dicts; optional)

        `frames` is a list of dicts with keys:

        - name (string; required)

        - id (string; required)

        - icon (string; required)

        - group (string; required)

        - url (string; required)

    - activeFrame (boolean | number | string | dict | list; optional)

    - users (list of strings; optional)

    - groups (list of dicts; optional)

        `groups` is a list of dicts with keys:

        - name (string; required)

        - id (string; required)

- widgetEvent (boolean | number | string | dict | list; optional):
    widget events."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dashpool_components'
    _type = 'DashpoolProvider'
    SharedDataApps = TypedDict(
        "SharedDataApps",
            {
            "name": str,
            "group": str,
            "url": str,
            "icon": str
        }
    )

    SharedDataFrames = TypedDict(
        "SharedDataFrames",
            {
            "name": str,
            "id": str,
            "icon": str,
            "group": str,
            "url": str
        }
    )

    SharedDataGroups = TypedDict(
        "SharedDataGroups",
            {
            "name": str,
            "id": str
        }
    )

    SharedData = TypedDict(
        "SharedData",
            {
            "dragElement": NotRequired[typing.Any],
            "apps": NotRequired[typing.Sequence["SharedDataApps"]],
            "frames": NotRequired[typing.Sequence["SharedDataFrames"]],
            "activeFrame": NotRequired[typing.Any],
            "users": NotRequired[typing.Sequence[str]],
            "groups": NotRequired[typing.Sequence["SharedDataGroups"]]
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
        children: typing.Optional[ComponentType] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        dragElement: typing.Optional[typing.Any] = None,
        initialData: typing.Optional[typing.Any] = None,
        sharedData: typing.Optional["SharedData"] = None,
        widgetEvent: typing.Optional[typing.Any] = None,
        dashpoolEvent: typing.Optional["DashpoolEvent"] = None,
        requireLogin: typing.Optional[bool] = None,
        defaultReload: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['children', 'id', 'dashpoolEvent', 'defaultReload', 'dragElement', 'initialData', 'requireLogin', 'sharedData', 'widgetEvent']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'dashpoolEvent', 'defaultReload', 'dragElement', 'initialData', 'requireLogin', 'sharedData', 'widgetEvent']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        if 'children' not in _explicit_args:
            raise TypeError('Required argument children was not specified.')

        super(DashpoolProvider, self).__init__(children=children, **args)

setattr(DashpoolProvider, "__init__", _explicitize_args(DashpoolProvider.__init__))
