from django.utils.importlib import import_module

def firstof(l):
    """Return first item in sequence where f(item) == True."""
    try:
        return next(v for i,v in enumerate(l) if v is not None)
    except StopIteration:
        return None


def import_object(dottedpath):
    """
    Load a class/object from a module in dotted-path notation.
    E.g.: load_class("package.module.class").
    """
    splitted_path = dottedpath.split('.')
    module = '.'.join(splitted_path[:-1])
    obj = splitted_path[-1]
    
    module = import_module(module)
    
    return getattr(module, obj)
