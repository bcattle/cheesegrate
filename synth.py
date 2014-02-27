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

parsed_args = parser.parse_args()

# Import the adapter they asked for
adapter = importlib.import_module('adapters.%s' % parsed_args.adapter)

# Import the classpath
# We expect the syntax "module.module.module" or "module.Class"
module_and_maybe_class = parsed_args.path.rsplit('.', 1)
if module_and_maybe_class[-1].isupper():
    # It is a class,
    # import the module and pull the class from it
    module, class_name = module_and_maybe_class
    model_module = importlib.import_module(module)
    model_klass = getattr(model_module, class_name)

    # Run the adapter
    pass

else:
    # It's a module path only, import it
    model_module = importlib.import_module(parsed_args.path)
    # The full list of modules is now stored in `base`!
    import base

    # Run the adapter on each class
    for name, model in base._models.items():
        pass

