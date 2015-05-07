from functools import partial
import sqlite3
import os
import os.path
import unittest

import fixturegen
import fixturegen.cli
import fixturegen.exc
import fixturegen.generator


PATH = os.path.dirname(os.path.abspath(__file__))

_TEST_DB = '{}/test.db'.format(PATH)


class FixturegenTestCase(unittest.TestCase):
    def setUp(self):
        try:
            connection = sqlite3.connect(_TEST_DB)
            connection.execute('CREATE TABLE empty_table (id PRIMARY KEY , name TEXT)')
            connection.execute('CREATE TABLE user (id PRIMARY KEY , name TEXT)')
            data = (
                (1, 'first'),
                (2, 'second'),
                (3, 'third'),
            )
            cursor = connection.cursor()
            for row in data:
                cursor.execute('INSERT INTO user VALUES (?, ?)', row)
            connection.commit()
        except:
            try:
                os.remove(_TEST_DB)
            except OSError:
                pass
            raise
        finally:
            connection.close()

    def tearDown(self):
        try:
            os.remove(_TEST_DB)
        except OSError:
            pass

    def test_entry_points(self):
        fixturegen
        fixturegen.cli
        fixturegen.exc
        fixturegen.generator

    def test_sqlaclhemy_data_wrong_dsn(self):
        with self.assertRaises(fixturegen.exc.WrongDSN):
            fixturegen.generator.sqlalchemy_data('', '')

    def test_sqlaclhemy_data_wrong_table(self):
        with self.assertRaises(fixturegen.exc.NoSuchTable):
            fixturegen.generator.sqlalchemy_data('', 'sqlite:///{}'.format(_TEST_DB))

    def test_sqlaclhemy_data_empty_table(self):
        self.assertEquals(fixturegen.generator.sqlalchemy_data('empty_table', 'sqlite:///{}'.format(_TEST_DB)),
                          ('empty_table', ('id', 'name'), tuple()))

    def test_sqlaclhemy_data(self):
        user_data = partial(fixturegen.generator.sqlalchemy_data, 'user', 'sqlite:///{}'.format(_TEST_DB))

        data = user_data()
        self.assertEquals(data[0], 'user')
        self.assertEquals(data[1], ('id', 'name'))
        self.assertEquals(len(data[2]), 3)
        self.assertEquals(data[2][0], (1, 'first'))

        # Test limit
        data = user_data(limit=2)
        self.assertEquals(len(data[2]), 2)
        self.assertEquals(data[2][0], (1, 'first'))

        # Test order
        data = user_data(order_by='id DESC')
        self.assertEquals(data[2][0], (3, 'third'))

        # Test where
        data = user_data(where='name = "second"')
        self.assertEquals(len(data[2]), 1)
        self.assertEquals(data[2][0], (2, 'second'))

        # Put it all together
        data = user_data(limit=2, order_by='id DESC', where='id > 1')
        self.assertEquals(len(data[2]), 2)
        self.assertEquals(data[2][0], (3, 'third'))
        self.assertEquals(data[2][1], (2, 'second'))

    def test_generator(self):
        data = 'user', ('id', 'name'), ((1, u'first'), (2, u'second'),
                                        (3, u'third'))
        result = fixturegen.generator.generate(*data)
        self.assertIn('from fixture import DataSet', result)
        self.assertIn('class UserData', result)
        self.assertIn('class user_1:', result)
        self.assertIn('id = 1', result)
        self.assertIn("name = u'first'", result)

        # Test default row class naming
        result = fixturegen.generator.generate('user', ('id', 'name'), ((1, u'first'),))
        self.assertIn('class user_1:', result)

        # Test id row class naming
        result = fixturegen.generator.generate('user', ('id', 'name'), ((1, u'first'),), row_naming_columns=['id'])
        self.assertIn('class user_1:', result)

        # Test empty row class naming
        result = fixturegen.generator.generate('user', ('id', 'name'), ((1, u'first'),), row_naming_columns=[])
        self.assertIn('class user_1:', result)

        # Test wrong row class naming
        with self.assertRaises(fixturegen.exc.WrongNamingColumn):
            fixturegen.generator.generate('user', ('id', 'name'), ((1, u'first'),),
                                          row_naming_columns=['non_existent_column'])

        # Test multiple columns
        result = fixturegen.generator.generate('user', ('id', 'name'), ((1, u'first'),),
                                               row_naming_columns=['id', 'name'])
        self.assertIn('class user_1_first:', result)

        # Test without import
        result = fixturegen.generator.generate(*data, with_import=False)
        self.assertNotIn('from fixture import DataSet', result)

        # Test custom fixture class name
        result = fixturegen.generator.generate(*data,
                                               fixture_class_name='TestClass')
        self.assertIn('class TestClass(DataSet)', result)
