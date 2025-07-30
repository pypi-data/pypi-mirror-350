from dataclasses import fields
from pprint import pformat

def pprint_repr(cls):
    def __repr__(self):
        cls_name = self.__class__.__name__
        indent = ' ' * (len(cls_name) + 1)
        field_reprs = []
        for field in fields(self):
            if not field.repr:
                continue
            value = getattr(self, field.name)
            value_repr = pformat(value, width=1)
            lines = value_repr.split('\n')
            if len(lines) > 1:
                white_space_name = " "* (len(field.name) + 1)
                value_repr = '\n'.join([lines[0]] + [indent + white_space_name + line for line in lines[1:]])
            field_reprs.append(f"{field.name}={value_repr}")
        return f"{cls_name}(" + f",\n{indent}".join(field_reprs) + f"\n{' ' * len(cls_name)})"

    cls.__repr__ = __repr__
    return cls