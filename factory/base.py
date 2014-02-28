from fields import FactoryField

_factories = {}

class FactoryMetaclass(type):
    """
    This metaclass registers factories
    """
    def __new__(mcs, name, bases, attrs):
        # Need to check this because this also gets called
        # creating the Model class itself
        if name is not 'Factory':
            # Find everything that inherits from FactoryField
            # and put it in a list called `fields`
            fields = {}
            for attr_name, attr in attrs.items():
                if issubclass(type(attr), FactoryField):
                    # print '%s is a field' % str(attr)
                    attr._name = attr_name
                    fields[attr_name] = attr
            attrs['_fields'] = fields

        new_class = super(FactoryMetaclass, mcs).__new__(mcs, name, bases, attrs)

        if name is not 'Factory':
            # Register this class with the module-level
            # list of factories
            _factories[name] = new_class

        return new_class


class Factory(object):
    __metaclass__ = FactoryMetaclass

    def __call__(self, *args, **kwargs):
        # Generate the model
        pass

