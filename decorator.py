import os
import random
import string
import warnings


def temp_file(func):
    allow_output_names = ['output', 'file_output', 'output_file']
    outputs_params = list(set(func.func_code.co_varnames).intersection(allow_output_names))
    assert outputs_params, 'Your function must have one param named {}'.format(allow_output_names)

    arg_name = outputs_params[0]
    arg_position = func.func_code.co_varnames.index(arg_name)

    if len(outputs_params) > 1:
        warnings.warn('Function has some ambiguous argument names, {param} will be used'.format(param=arg_name),
                      UserWarning)

    def decorator(*args, **kwargs):
        if arg_name in kwargs:
            output_original = kwargs[arg_name]
        else:
            output_original = args[arg_position]
            args = tuple([value for index, value in enumerate(args) if index != arg_position])

        extension_file = os.path.splitext(output_original)[1]
        dir_name = os.path.dirname(output_original)
        output_temp = os.path.join(dir_name,
                                   '{name}{extension}'.format(name=get_random_string(), extension=extension_file))

        kwargs[arg_name] = output_temp
        result = func(*args, **kwargs)
        os.rename(output_temp, output_original)
        return result

    return decorator


def get_random_string(length=32):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
