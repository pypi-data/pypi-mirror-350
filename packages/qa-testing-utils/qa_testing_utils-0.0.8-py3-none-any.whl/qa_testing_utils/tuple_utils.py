# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from dataclasses import is_dataclass, replace, fields
from typing import Any, Self, Tuple, Type


class FromTupleMixin:
    """
    Class decorator adding a `from_tuple` method allowing instantiation from
    a tuple matching the order of decorated class fields.

    Works with frozen dataclasses too.
    """
    @classmethod
    def from_tuple(cls: Type[Self], data: Tuple[Any, ...]) -> Self:
        if is_dataclass(cls):
            # Retrieve all fields, including inherited ones
            cls_fields = [f.name for f in fields(cls)]

            # Create a dictionary of field names to values from the tuple
            field_values = {name: value for name,
                            value in zip(cls_fields, data)}

            # Create a new instance using `__new__`
            instance = cls.__new__(cls)

            # If the dataclass is frozen, use `replace` to set the attributes
            if getattr(cls, '__dataclass_params__').frozen:
                return replace(instance, **field_values)
            else:
                # If the dataclass is not frozen, use setattr to set attributes
                for key, value in field_values.items():
                    setattr(instance, key, value)

                # Call __init__ if defined
                instance.__init__(*data)
                return instance
        else:
            # For vanilla classes, assume fields are defined in __init__
            # Using `__init__` directly as the custom initializer
            instance = cls.__new__(cls)
            for attr, value in zip(cls.__annotations__.keys(), data):
                setattr(instance, attr, value)

            # Call __init__ if it expects parameters
            instance.__init__(*data)
            return instance
