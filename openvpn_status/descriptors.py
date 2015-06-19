from __future__ import unicode_literals, absolute_import

from six import iteritems


class LabelProperty(object):
    """The property with label name."""

    def __init__(self, label, default_factory=None):
        self.label = label
        self.default_factory = default_factory

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.__name__ in instance.__dict__:
            return instance.__dict__[self.__name__]
        elif self.default_factory is not None:
            value = self.default_factory()
            instance.__dict__[self.__name__] = value
            return value
        else:
            names = (owner.__name__, self.__name__)
            raise AttributeError('%r object has no attribute %r' % names)

    def __set__(self, instance, value):
        instance.__dict__[self.__name__] = value


def name_descriptors(cls):
    for name, value in iter_descriptors(cls):
        if not hasattr(value, '__name__'):
            value.__name__ = name
    return cls


def iter_descriptors(cls):
    for name, value in iteritems(cls.__dict__):
        if name.startswith('__'):
            continue
        if hasattr(value, '__get__') or hasattr(value, '__set__'):
            yield name, value
