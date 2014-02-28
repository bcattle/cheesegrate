<img src="http://img3.wikia.nocookie.net/__cb20130927013726/battlefordreamislandfanfiction/images/c/c4/Cheese_Grater.png" width=100></img> cheesegrate
============

Cheesegrate is a centralized place to model the data in your application,
and generate a variety of representations of it. 
Model once, use often. 

Picture an iOS app backed by an a Java backend, persisting to [Cassandra](http://cassandra.apache.org/).

You model your data, something like 

``` python
class User(BaseModel):
    name = StringField()
    is_followed = BooleanField()
    profile_pic_small = UrlField()
```

From this data model, you could 

1. Generate Objective-C data model classes that use [Mantle](https://github.com/MantleFramework/Mantle/)
2. Generate Java ([POJO](http://en.wikipedia.org/wiki/Plain_Old_Java_Object)) data model classes for use in the backend
2. Generate JSON fixtures, populated with random or sequential data using a rich Factory syntax
3. Generate [Gatling](http://gatling-tool.org/) Scala scripts that exercise the app's REST endpoints
4. Generate unit tests that verify HTTP authentication/authorization rules are working
3. Generate a Objective-C data controller that exercises the REST, exposing methods like `[dataController getUsersWithSuccessHandler:^{ ... }];`
4. Generate Java validation code using XXX
5. Generate Cassandra CQL commands to build the database schema
6. Define denormalized data "views" of the data in the datastore. For example imagine two tables, "users by ID" and "users by timestamp". 
7. Data views need to be synchronized in schema and data. Persisting a single `User` object should automatically update "users by ID" and "users by timestamp". Generate the code to make this happen.
7. Generate URL routes for the backend
8. Generate HTML documentation of the HTTP API, database schemas, and Objective-C models and data controller


## Data model

``` python
class User(BaseModel):
    name = StringField()
    is_followed = BooleanField()
    profile_pic_small = UrlField()
```

### Fields

* `UIntField`
* `FloatField`
* `StringField`
* `BooleanField`
* `UrlField`
* `EnumField`
* `DateField`
* `GUIDField`

#### Reference fields

* `EmbeddedField`
* `ArrayField`


## Factories

Something like 

``` python
class UserFactory(Factory):
    name = IndexedChoiceField(sequence=user_names_and_pics, seq_index=0)
    profile_pic_small = IndexedChoiceField(sequence=user_names_and_pics, seq_index=1)
    is_followed = RandomBooleanField()
```

### Fields

* `ChoiceField`
* `IndexedChoiceField`
* `RandomBooleanField`
* `RandomIntField`
* `RandomFloatField`
* `DateNowUTCField`
* `RandomGuidField`
* `ArrayOfModelsField`

## Adapters

Classes that describe how to convert 
* data model -> Objective-C model class
* data model -> Java model (POJO)
* data model -> Cassandra CQL

etc.
