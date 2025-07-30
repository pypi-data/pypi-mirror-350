_memorized = {}


def run_once(parameter_match: list[str]):
    """Ensure the class is only called once based on input parameters
    If it has already run, return the cached results

    Args:
        parameter_match: the list of argument keys to use as match if the function was already executed
    """

    def inner(func):
        def wrapper(*args, **kwargs):
            key = func.__name__
            for match in parameter_match:
                val = None
                try:  # do not complain if key does not exist, it may be optional
                    val = kwargs[match]
                except KeyError:
                    pass
                # sort list if key is a list, to better match for duplicates, the result passes to function is unsorted
                if isinstance(val, list):
                    val = sorted(val)
                key = key + f"_{str(val).lower()}"
            # print(f"key: {key}")
            if key not in _memorized:
                # print(f"calling func with args:{args} and kwargs:{kwargs}")
                _memorized[key] = func(*args, **kwargs)
                # print(f"new key {key}: {type(_memorized[key])}")
                return _memorized[key]

            # print(f"existing key {key}: {type(_memorized[key])}")
            return _memorized[key]

        return wrapper

    # returning inner function
    return inner
