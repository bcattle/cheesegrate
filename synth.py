#!/usr/bin/env python
import argparse
import pkgutil
import importlib

# Load the list of adapters
adapters = [pkg[1] for pkg in pkgutil.iter_modules(path=['adapters'])]

# Add arguments for those adapters
parser = argparse.ArgumentParser(description='Generates different representations of our data models')
parser.add_argument('adapter',  choices=adapters, help='Run a specified adapter')
parser.add_argument('path', help='The classpath to the model(s) of interest, e.g. phone_models.User')
parser.add_argument('factory_path', nargs='?', default='',      # <- makes it optional
                    help='The classpath to a factory or factories for the models')

parsed_args = parser.parse_args()

# Import the adapter they asked for
adapter_klass = importlib.import_module('adapters.%s' % parsed_args.adapter)

def get_class_or_module_for_classpath(classpath):
    """
    For a `classpath` like modules.stuff, import as a module
    for a `classpath` like modules.MyClass, import the class

    Returns: module, class

    """
    module_and_maybe_class = classpath.rsplit('.', 1)
    if module_and_maybe_class[-1].isupper():
        # It is a class.
        # Import the module and pull the class from it
        module, class_name = module_and_maybe_class
        model_module = importlib.import_module(module)
        model_klass = getattr(model_module, class_name)

        # Return
        return model_module, model_klass

    else:
        # It's a module path only, import it
        model_module = importlib.import_module(parsed_args.path)
        return model_module, None


# Did they ask for a factory or factories?
factories = None
if parsed_args.factory_path:
    factory_module_name, factory_class_name = get_class_or_module_for_classpath(parsed_args.factory_path)
    # If they specified a class, import it
    factory_module = importlib.import_module(factory_module_name)
    factory_klass = None
    if factory_class_name:
        factory_klass = getattr(factory_module, factory_class_name)
    else:
        # Load the factories which were registered by the metaclass
        from factory.base import _factories
        factories = _factories

# Import the models' classpath
model_module, model_klass = get_class_or_module_for_classpath(parsed_args.path)
if model_klass is None:
    # The user specified a module
    # Since it was imported, the full list
    # of modules is now stored in `base`!
    import base

    # Run the adapter on each class
    for name, model_klass in base._models.items():
        adapter = adapter_klass(model_klass, factories)
        pass

else:
    # The user specified a specific class
    # Run the adapter
    adapter = adapter_klass(model_klass, factories)
    pass

