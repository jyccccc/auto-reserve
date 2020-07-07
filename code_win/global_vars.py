def _init():
    global _global_dict
    _global_dict = {}


def set_value(key,value):
    _global_dict[key] = value


def set_values(keys,values):
	for i in range(len(keys)):
		_global_dict[keys[i]] = values[i]


def get_value(key,defValue=''):
    try:
        return _global_dict[key]
    except KeyError:
        return defValue
