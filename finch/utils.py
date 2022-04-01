import logging


def update_test_result(result, test, checkpoint, checkpoint_result, checkpoint_comment=None):
    """
    Update case result and add comment if any.
    """
    temp = {}
    index = -1
    for item in result:
        if item['id'] == test:
            temp = item
            index = result.index(item)
            break
    if index == -1:
        temp['id'] = test
        temp['checkpoint'] = {}
    if checkpoint not in temp['checkpoint']:
        temp['checkpoint'][checkpoint] = {}
    temp['checkpoint'][checkpoint]['result'] = checkpoint_result
    if checkpoint_comment:
        temp['checkpoint'][checkpoint]['comments'] = checkpoint_comment
    if index == -1:
        result.append(temp)
    else:
        result[index] = temp


def get_test_result(result):
    """
    Give a brief summary of test results.
    """
    fail = 0
    total = len(result)

    for test in result:
        is_fail = False
        for checkpoint in test['checkpoint']:
            if test['checkpoint'][checkpoint]['result'] != 'pass':
                is_fail = True
                break
        if is_fail:
            fail += 1
    pass_rate = 1 - (fail / total)
    logging.info('Run %d cases with %d failed' % (total, fail))
    return fail > 0, [pass_rate, fail, total]
