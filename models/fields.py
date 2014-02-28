

# Abstract classes

class Field(object):
    def blank_value(self):
        return ''


# Fields

class GUIDField(Field):
    def blank_value(self):
        return '00000000-0000-0000-0000-000000000000'

class DateField(Field):
    def blank_value(self):
        # ISO 8601
        return "2000-01-01'T'00:00:00Z"

class UIntField(Field):
    def blank_value(self):
        return 0

class FloatField(Field):
    def blank_value(self):
        return 0.0

class ArrayField(Field):
    def __init__(self, type=None):
        self.type_klass = type

    def blank_value(self):
        return []

class StringField(Field):
    pass

class BooleanField(Field):
    def blank_value(self):
        return False

class UrlField(Field):
    def blank_value(self):
        return 'http://example.com/blog/'

class EnumField(Field):
    def __init__(self, choices):
        # Choices is a dict or a list
        self.choices = choices

    def blank_value(self):
        return self.choices[0]

# Reference fields

class EmbeddedField(Field):
    def __init__(self, model):
        self.model_klass = model

    def blank_value(self):
        return {}