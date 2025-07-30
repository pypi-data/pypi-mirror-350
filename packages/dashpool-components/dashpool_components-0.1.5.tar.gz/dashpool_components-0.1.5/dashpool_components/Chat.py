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


class Chat(Component):
    """A Chat component.
Component to serve as Loader for Graphs

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

- dashpoolEventOnClick (boolean; default True):
    flag if a dashpool event should be fired on click on a reference.

- messages (list of boolean | number | string | dict | lists; optional):
    default messages.

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

- referenceTarget (string; default undefined):
    targent if a reference is clicked and as a link.

- showClearButton (boolean; default False):
    flag if the clear button should be shown.

- showReportButton (boolean; default False):
    flag if the report button should be shown.

- title (boolean | number | string | dict | list; default 'Dashpool Chat AI'):
    title of the chat.

- url (string; default ''):
    url to load the data."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dashpool_components'
    _type = 'Chat'
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
        url: typing.Optional[str] = None,
        messages: typing.Optional[typing.Sequence[typing.Any]] = None,
        title: typing.Optional[typing.Any] = None,
        nodeChangeEvent: typing.Optional["NodeChangeEvent"] = None,
        dashpoolEvent: typing.Optional["DashpoolEvent"] = None,
        style: typing.Optional[typing.Any] = None,
        showReportButton: typing.Optional[bool] = None,
        showClearButton: typing.Optional[bool] = None,
        dashpoolEventOnClick: typing.Optional[bool] = None,
        referenceTarget: typing.Optional[str] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'dashpoolEvent', 'dashpoolEventOnClick', 'messages', 'nodeChangeEvent', 'referenceTarget', 'showClearButton', 'showReportButton', 'style', 'title', 'url']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'dashpoolEvent', 'dashpoolEventOnClick', 'messages', 'nodeChangeEvent', 'referenceTarget', 'showClearButton', 'showReportButton', 'style', 'title', 'url']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Chat, self).__init__(**args)

setattr(Chat, "__init__", _explicitize_args(Chat.__init__))
