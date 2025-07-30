import json

from datetime import datetime


def validate_args(spider_name, args, sel, args_spec_path):
    def date(wh):
        return datetime.strptime(wh, "%Y-%m-%d %H:%M:%S")

    def arr(val):
        val = str(val)
        try:
            val = json.loads(val)
            print(val)
            if not isinstance(val, list):
                raise ValueError
        except Exception:
            sep = ','
            if val.find('\n') != -1:
                sep = '\n'
            val = val.split(sep)
        return val

    type_validators = {
        'int': int,
        'float': float,
        'boolean': bool,
        'date': date,
        'string': str,
        'array': arr,
        'object': json.loads
    }
    with open(args_spec_path) as args_spec_file:
        args_spec = json.load(args_spec_file)
    args_spec = args_spec["_common"][sel] + args_spec[spider_name][sel]
    data = {}
    for key in range(len(args_spec)):
        name = args_spec[key]['name']
        typ = args_spec[key]['type']
        default = args_spec[key]['default']
        required = args_spec[key]['required']
        no_error = True
        value = args[name]
        try:
            value = type_validators[typ](value)
        except Exception:
            no_error = False
        if no_error or not required:
            if not no_error and default is not None:
                value = default
                no_error = True
            if no_error:
                data.update({name: value})
            else:
                raise ValueError
        else:
            raise ValueError
    return data


def validate_input(path="args_and_settings.json"):
    def func_call(spider_instantiation):
        def prep(cls, crawler, *args, **kwargs):
            aux = validate_args(cls.name, crawler.settings, "settings", path)
            crawler.settings.frozen = False
            for key in aux.keys():
                crawler.settings.set(key, aux[key])
            crawler.settings.freeze()
            aux = validate_args(cls.name, kwargs, "args", path)
            for key in aux.keys():
                kwargs.update({key: aux[key]})
            return spider_instantiation(cls, crawler, *args, **kwargs)
        return prep
    return func_call
