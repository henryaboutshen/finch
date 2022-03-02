import logging


def update_test_result(result, test, checkpoint, checkpoint_result, checkpoint_comment=None):
    """
    Update case result and add comment if any.
    """
    if test not in result:
        result[test] = {}
    if checkpoint not in result[test]:
        result[test][checkpoint] = {}
    result[test][checkpoint]['result'] = checkpoint_result
    if checkpoint_comment:
        result[test][checkpoint]['comments'] = checkpoint_comment


def get_test_result(result):
    """
    Give a brief summary of test results.
    """
    fail = 0
    total = len(result)

    for test in result:
        is_fail = False
        for checkpoint in result[test]:
            if result[test][checkpoint]['result'] != 'pass':
                is_fail = True
                break
        if is_fail:
            fail += 1
    pass_rate = 1 - (fail / total)
    logging.info('Run %d cases with %d failed' % (total, fail))
    return fail > 0, [pass_rate, fail, total]


def get_keys(env, test, *args):
    """
    Extract the value you want.
    :param test:
    :param env:
    :param args: field name(s)
    :return: return default if current env is not customized.
    """
    values = []
    for key in args:
        if isinstance(test[key], dict) and test[key].get('default') is not None:
            if test[key].get(env) is not None:
                values.append(test[key][env])
            else:
                values.append(test[key]['default'])
        else:
            values.append(test[key])
    return tuple(values)


def get_value(dict_data, key, default=None):
    """
    get value of key recursively in a dict.
    """
    if isinstance(dict_data, dict):
        temp = dict_data
        for k, v in temp.items():
            if k == key:
                return v
            else:
                val = get_value(v, key)
                if val is not default:
                    return val
        return default
    if isinstance(dict_data, (list, tuple)):
        for item in dict_data:
            val = get_value(item, key)
            if val is not default:
                return val
    if isinstance(dict_data, str):
        return default
