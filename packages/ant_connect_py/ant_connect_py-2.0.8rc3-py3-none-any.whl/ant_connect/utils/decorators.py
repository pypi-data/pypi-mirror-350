""" This module contains the decorators used in the ant_connect package. """

import functools
import inspect

from ant_connect.config import empty_default


def preprocess_arguments(cls_method):
    """Decorator to preprocess the arguments of a class method."""

    @functools.wraps(cls_method)
    def wrapper(cls, *args, **kwargs):
        """Wrapper function to preprocess the arguments of a class method."""

        # get the parameters of the method
        signature = inspect.signature(cls_method)
        parameters = signature.parameters

        # make a dict with the class arguments and default values
        class_args_dict = {value.name: value.default for value in parameters.values()}

        # make a list of the dict keys, which are the class arguments
        class_names_list = list(class_args_dict.keys())

        # remove the first element and key of the list and dict which is the class itself
        del class_args_dict["cls"]
        class_names_list.pop(0)

        if args:
            # if args, then make them kwargs with the class names
            new_kwargs = {class_names_list[i]: args[i] for i in range(len(args))}
            # combine both kwargs and new_kwargs
            kwargs.update(new_kwargs)

        # add default values to kwargs if they are not provided by user and default is None
        for argument in class_names_list:
            if argument not in kwargs and class_args_dict[argument] is None:
                kwargs[argument] = empty_default

        return cls_method(cls, **kwargs)

    return wrapper
