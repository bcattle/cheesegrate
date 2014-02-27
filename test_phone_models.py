#!/usr/bin/env python

# List of models
_models = {}

# Abstract classes

class Field(object):
    pass


class ModelMetaclass(type):
    # def __new__(mcs, *args, **kwargs):
    def __new__(mcs, name, bases, attrs):
        # mcs is ModelMetaclass, an instance of `type`
        # print name
        # print bases
        # # print attrs
        # print ''

        # Need to check this because this also gets called
        # creating the Model class itself
        if name is not 'Model':
            # Find everything that inherits from Field
            # and put it in a list called `fields`
            fields = {}
            for attr_name, attr in attrs.items():
                if issubclass(type(attr), Field):
                    # print '%s is a field' % str(attr)
                    fields[attr_name] = attr
            attrs['_fields'] = fields

            # Grab the Meta class from the superclass, if needed
            if not 'Meta' in attrs:
                attrs['Meta'] = bases[0].Meta
                # Reset this, since we copied it over
                attrs['Meta'].abstract = False

            # Set default variables for any Meta values
            if not hasattr(attrs['Meta'], 'abstract'):
                setattr(attrs['Meta'], 'abstract', False)

        new_class = super(ModelMetaclass, mcs).__new__(mcs, name, bases, attrs)

        if name is not 'Model' and not attrs['Meta'].abstract:
            # Register this class with the module-level
            # list of models
            _models[name] = new_class

        return new_class


class Model(object):
    __metaclass__ = ModelMetaclass

    class Meta:
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

# Abstract model

class BaseModel(Model):            # --> ISBaseModel
    id = GUIDField()
    created_at = DateField()
    updated_at = DateField()

    class Meta:
        abstract = True


# Concrete models

class HeatmapDatapoint(Model):
    up_votes = UIntField()
    down_votes = UIntField()


class Heatmap(BaseModel):
    datapoints = ArrayField(type=HeatmapDatapoint)


class User(BaseModel):
    name = StringField()
    is_followed = BooleanField()
    profile_pic_small = UrlField()

class Comment(BaseModel):
    user = EmbeddedField(model=User)
    text = StringField()
    video_time_secs = FloatField()
    up_votes = UIntField()
    down_votes = UIntField()

class Episode(BaseModel):
    pass


EpisodeStarChoices = []

class EpisodeStar(User):
    role_1 = EnumField(choices=EpisodeStarChoices)
    role_2 = EnumField(choices=EpisodeStarChoices)


import ipdb
ipdb.set_trace()


pass
