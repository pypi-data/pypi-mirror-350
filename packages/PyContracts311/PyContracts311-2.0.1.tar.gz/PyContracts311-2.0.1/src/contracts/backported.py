import sys
from inspect import getfullargspec
from inspect import signature
from collections import namedtuple

if sys.version_info[0] >= 3:  # pragma: no cover
    unicode = str

# Modern Python 3.x implementation
def getargspec(function):
    """Get argument specification for a function."""
    sig = signature(function)
    args = []
    varargs = None
    varkw = None
    defaults = None
    
    # Collect parameters
    parameters = sig.parameters
    positional_args = []
    keyword_args = []
    
    for name, param in parameters.items():
        if param.kind == param.POSITIONAL_ONLY:
            positional_args.append(name)
        elif param.kind == param.POSITIONAL_OR_KEYWORD:
            positional_args.append(name)
            if param.default is not param.empty:
                keyword_args.append(name)
        elif param.kind == param.VAR_POSITIONAL:
            varargs = name
        elif param.kind == param.KEYWORD_ONLY:
            keyword_args.append(name)
        elif param.kind == param.VAR_KEYWORD:
            varkw = name
    
    # Create defaults tuple
    if keyword_args:
        defaults = tuple(
            parameters[arg].default 
            for arg in positional_args[-len(keyword_args):]
            if parameters[arg].default is not parameters[arg].empty
        )
    
    return namedtuple('ArgSpec', 'args varargs keywords defaults')(
        args=positional_args,
        varargs=varargs,
        keywords=varkw,
        defaults=defaults
    )

# Modern Python 3.x implementation
def getfullargspec(function):
    """Get full argument specification for a function."""
    sig = signature(function)
    args = []
    varargs = None
    varkw = None
    defaults = None
    kwonlyargs = []
    kwonlydefaults = {}
    annotations = {}
    
    # Collect parameters
    parameters = sig.parameters
    for name, param in parameters.items():
        args.append(name)
        if param.kind == param.VAR_POSITIONAL:
            varargs = name
        elif param.kind == param.VAR_KEYWORD:
            varkw = name
        elif param.kind == param.KEYWORD_ONLY:
            kwonlyargs.append(name)
            if param.default is not param.empty:
                kwonlydefaults[name] = param.default
        if param.annotation is not param.empty:
            annotations[name] = param.annotation
    
    # Create defaults tuple
    if parameters:
        defaults = tuple(
            param.default 
            for param in parameters.values() 
            if param.default is not param.empty
        )
    
    return namedtuple('FullArgSpec', 'args varargs varkw defaults kwonlyargs kwonlydefaults annotations')(
        args=args,
        varargs=varargs,
        varkw=varkw,
        defaults=defaults,
        kwonlyargs=kwonlyargs,
        kwonlydefaults=kwonlydefaults,
        annotations=annotations
    )

# Modern Python 3.x implementation
def getcallargs(func, *positional, **named):
    """Get the mapping of arguments to values."""
    sig = signature(func)
    bound = sig.bind(*positional, **named)
    return bound.arguments

# Always use the modern implementation
getcallargs = getcallargs
getargspec = getargspec
getfullargspec = getfullargspec
