from warnings import warn


def deprecate_function():
    warn("This function is deprecated", DeprecationWarning, stacklevel=2)
