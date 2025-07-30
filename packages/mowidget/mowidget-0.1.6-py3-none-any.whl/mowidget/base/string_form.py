"""A simple string form."""

from __future__ import annotations

import pathlib
import warnings

import anywidget
import traitlets

warnings.simplefilter('always', DeprecationWarning)


class StringForm(anywidget.AnyWidget):
    """
    A widget that creates a dynamic form for string inputs.

    This widget allows users to create a form with multiple string input
    fields. The fields are generated based on the provided default values.

    Args:
        default (dict[str, str], optional):
            A dictionary containing initial form field values.
            Default is None.

    Attributes:
        default_keys (list[str]):
            The list of keys used to generate form fields.
        form_data (dict):
            A dictionary containing the form field values.

    Examples:
        >>> StringForm(default={"name": "Alex", "age": "22"})
    """

    _esm = pathlib.Path(__file__).parent.parent / "frontend/js/string-form.js"
    _css = (
        pathlib.Path(__file__).parent.parent / "frontend/css/string-form.css"
    )

    form_data = traitlets.Dict().tag(sync=True)

    _default_keys: list[str]

    def __init__(
        self,
        default: dict[str, str] | None = None,
        default_keys: list[str] | None = None,
    ) -> None:
        super().__init__()
        self.default_keys = default_keys or []
        self.form_data = default or {}
        for key in self.default_keys:
            if key not in self.form_data:
                self.form_data[key] = ""

    @property
    def default_keys(self) -> list[str]:
        return self._default_keys

    @default_keys.setter
    def default_keys(self, value: list[str]) -> None:
        warnings.warn(
            "`default_keys` will be removed in v0.4.0, use `default` instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self._default_keys = value
