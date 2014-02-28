from factory.base import BaseFactory
from factory.fields import RandomGuidField, DateNowUTCField, RandomIntField, \
    ArrayOfModelsField,  IndexedChoiceField, RandomBooleanField, \
    ChoiceField, RandomFloatField

class DefaultFactory(BaseFactory):
    """
    You can specify defaults by
      field type or field name

    Anything here will be applied to all models

    The most specific constraint will be used, i.e.
    if there's a default StringField, and a default for `name`
    the latter will be used.
    """
    type_defaults = {
        'GUIDField': RandomGuidField,
        'DateField': DateNowUTCField,
    }


class HeatmapDatapointFactory(BaseFactory):
    up_votes = RandomIntField(max=400)
    down_votes = RandomIntField(max=100)


class HeatmapFactory(BaseFactory):
    datapoints = ArrayOfModelsField(length_min=10, length_max=40)


# Data sources:
#   list of profile pic urls
#   list of user names


user_names_and_pics = [
    ('The Brown Mamba', 'http://localhost:8080/koowalla/'),
    ('', ''),
    ('', ''),
    ('', ''),
]

class UserFactory(BaseFactory):
    name = IndexedChoiceField(sequence=user_names_and_pics, seq_index=0)
    profile_pic_small = IndexedChoiceField(sequence=user_names_and_pics, seq_index=1)
    is_followed = RandomBooleanField()


comments = [
    'Christine you look so hott!',
    '',
    '',
    '',
]

class CommentFactory(BaseFactory):
    # `user` is an EmbeddedField to the `User` model
    #   that model's Factory will be used by default
    text = ChoiceField(comments)
    video_time_secs = RandomFloatField(max=60.0)
    up_votes = RandomIntField(max=40)
    down_votes = RandomIntField(max=10)


class EpisodeStartFactory(BaseFactory):
    # Automatically resolves the superclass dependency
    # and runs UserFactory

    # Fields with defined `choices` by default
    # are chosen at random

    pass


# Print warnings for any fields that are undefined

