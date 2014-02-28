from base import Model
from fields import GUIDField, DateField, UIntField, ArrayField, \
    StringField, BooleanField, UrlField, EmbeddedField, FloatField, \
    EnumField

# The list of models lives in `base._models`


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

