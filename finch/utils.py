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
