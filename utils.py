import re
import importlib
import os
import glob

# https://raw.github.com/fabric/fabric/master/fabric/colors.py
def _wrap_with(code):
    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner

red = _wrap_with('31')
green = _wrap_with('32')
yellow = _wrap_with('33')
blue = _wrap_with('34')
magenta = _wrap_with('35')
cyan = _wrap_with('36')
white = _wrap_with('37')


def decamel(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def to_camel(s):
    return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s)


def get_class_or_module_for_classpath(classpath):
    """
    For a `classpath` like modules.stuff, import as a module
    for a `classpath` like modules.MyClass, import the class

    Returns: module, class

    """
    module_and_maybe_class = classpath.rsplit('.', 1)
    if module_and_maybe_class[-1][0].isupper():
        # It is a class.
        # Import the module and pull the class from it
        module, class_name = module_and_maybe_class
        model_module = importlib.import_module(module)
        model_klass = getattr(model_module, class_name)

        # Return
        return model_module, model_klass

    else:
        # It's a module path only, import it
        model_module = importlib.import_module(classpath)
        return model_module, None


def get_subpackages(module):
    # http://stackoverflow.com/a/832040/1161906
    dir = os.path.dirname(module.__file__)
    def is_package(d):
        d = os.path.join(dir, d)
        return os.path.isdir(d) and glob.glob(os.path.join(d, '__init__.py*'))

    return filter(is_package, os.listdir(dir))