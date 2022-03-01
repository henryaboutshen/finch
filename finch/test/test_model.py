import unittest

from finch import model


class TestLoader(unittest.TestCase):

    def test_query_global_data(self):
        env = 'PRODUCTION_CV2'
        model.connect_db()
        self.assertEqual(model.query_global_data(env, param='env'), env)
        self.assertEqual(model.query_global_data(env, param=['env']), {'env': env})
        self.assertEqual(type(model.query_global_data(env)), dict)
        self.assertRaises(TypeError, model.query_global_data, env, {'env': env})
