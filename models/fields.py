

# Abstract classes

class Field(object):
    pass


# Fields

class GUIDField(Field):
    pass

class DateField(Field):
    pass

class UIntField(Field):
    pass

class FloatField(Field):
    pass

class ArrayField(Field):
    def __init__(self, type=None):
        self.type_klass = type

class StringField(Field):
    pass

class BooleanField(Field):
    pass

class UrlField(Field):
    pass

class EnumField(Field):
    def __init__(self, choices):
        # Choices is a dict or a list
        self.choices = choices

# Reference fields

class EmbeddedField(Field):
    def __init__(self, model):
        self.model_klass = model

