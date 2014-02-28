from fields import Field

_models = {}

# Abstract classes

class ModelMetaclass(type):
    """
    This metaclass registers models
    and creates a Meta class with some default values (if necessary)
    """
    def __new__(mcs, name, bases, attrs):
        # mcs is ModelMetaclass, an instance of `type`

        # Need to check this because this also gets called
        # creating the Model class itself
        if name is not 'Model':
            # Find everything that inherits from Field
            # and put it in a list called `fields`
            fields = {}
            for attr_name, attr in attrs.items():
                if issubclass(type(attr), Field):
                    # print '%s is a field' % str(attr)
                    attr._name = attr_name
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
