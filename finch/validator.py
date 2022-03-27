import logging

from .utils import update_test_result


async def test_count(test, results, client):
    """
    Count documents in collection
    """
    logging.debug('Checkpoint: count, test: %s' % test)
    client = client
    db = client.bondsolution
    n = await db.bond.count_documents({})
    result = 'pass' if n > 0 else 'fail'
    message = None if n > 0 else 'count: %d' % n
    update_test_result(results, test, 'count', result, message)


async def test_find(test, results, client):
    """
    Find document in collection
    """
    logging.debug('Checkpoint: find, test: %s' % test)
    client = client
    db = client.bondsolution
    n = await db.bond.find_one({})
    result = 'pass' if n else 'fail'
    message = None if n else 'find: %s' % n
    update_test_result(results, test, 'find', result, message)
