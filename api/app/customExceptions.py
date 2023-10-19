def custom_exceptions(exe) -> list:
    """ custom exceptions
       return string 
    """
    exceptions = []
    if isinstance(exe, TypeError):
        exceptions.append('Type error! given type is not vaild.')

    if isinstance(exe, SyntaxError):
        exceptions.append('Syntax error! syntax is not valid.')

    if isinstance(exe, NameError):
        exceptions.append('Variable is out of scope or does not exists.')

    
    return exceptions