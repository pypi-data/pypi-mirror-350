from dataclasses import dataclass, asdict, is_dataclass
from functools import wraps
from typing import Type
import json

"""
Example usage:

    @extendable_dataclass(keep_others=True)
    class Person(JsonSerializable):
        name: str
        age: int


    p1 = Person(name='Alice', age=30, occupation='Engineer', dog_name="Gamine")
    p2 = Person(name='John', age=33, occupation='Journalist')
    print(p1)
    print(p1.to_json())
    print(p1._others)

"""


class JsonSerializable:
    def to_json(self):
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        # Check for nested dataclasses and handle them
        for field, field_type in cls.__annotations__.items():
            if is_dataclass(field_type) and isinstance(data.get(field), dict):
                data[field] = field_type(**data[field])
        return cls(**data)


def extendable_dataclass(_cls=None, *, keep_others: bool = True):
    def inner_decorator(cls: Type):
        decorated_dataclass = dataclass(cls)
        original_init = decorated_dataclass.__init__

        @wraps(original_init)
        def new_init(self, *args, **kwargs):
            filtered_kwargs = {}
            others = {}
            for k, v in kwargs.items():
                if k in cls.__dataclass_fields__:
                    filtered_kwargs[k] = v
                elif keep_others:
                    others[k] = v

            if keep_others:
                self._others = others

            original_init(self, *args, **filtered_kwargs)

        cls.__init__ = new_init
        return decorated_dataclass

    if _cls is None:
        return inner_decorator
    else:
        return inner_decorator(_cls)
