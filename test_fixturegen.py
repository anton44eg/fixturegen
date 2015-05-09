from functools import partial
import sqlite3
import os
import os.path
import sys
import unittest

from click.testing import CliRunner

import fixturegen
import fixturegen.cli
import fixturegen.exc
import fixturegen.generator


PATH = os.path.dirname(os.path.abspath(__file__))

_TEST_DB = '{0}/test.db'.format(PATH)
_SQLITE_DSN = 'sqlite:///{0}'.format(_TEST_DB)

PY2 = sys.version_info[0] == 2
PY26 = sys.version_info[0] == 2 and sys.version_info[1] == 6

class FixturegenTestCase(unittest.TestCase):
    def setUp(self):
        connection = sqlite3.connect(_TEST_DB)
        try:
            connection.execute('CREATE TABLE empty_table (id PRIMARY KEY , name TEXT)')
            connection.execute('CREATE TABLE user (id PRIMARY KEY , name TEXT)')
            connection.execute('CREATE TABLE user_without_id (name TEXT)')
            connection.execute('CREATE TABLE user_with_spaced_name (id PRIMARY KEY , name TEXT)')
            data = (
                (1, 'first'),
                (2, 'second'),
                (3, 'third'),
            )
            cursor = connection.cursor()
            cursor.executemany('INSERT INTO user VALUES (?, ?)', data)
            cursor.execute('INSERT INTO user_with_spaced_name VALUES (?, ?)', (1, 'first name'))
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
        if PY26:
            self.assertRaises(fixturegen.exc.WrongDSN, fixturegen.generator.sqlalchemy_data, '', '')
        else:
            with self.assertRaises(fixturegen.exc.WrongDSN):
                fixturegen.generator.sqlalchemy_data('', '')

    def test_sqlaclhemy_data_wrong_table(self):
        if PY26:
            self.assertRaises(fixturegen.exc.NoSuchTable, fixturegen.generator.sqlalchemy_data,
                              '', _SQLITE_DSN)
        else:
            with self.assertRaises(fixturegen.exc.NoSuchTable):
                fixturegen.generator.sqlalchemy_data('', _SQLITE_DSN)

    def test_sqlaclhemy_data_empty_table(self):
        self.assertEqual(fixturegen.generator.sqlalchemy_data('empty_table', _SQLITE_DSN),
                          ('empty_table', ('id', 'name'), tuple()))

    def test_sqlaclhemy_data(self):
        user_data = partial(fixturegen.generator.sqlalchemy_data, 'user', _SQLITE_DSN)

        data = user_data()
        self.assertEqual(data[0], 'user')
        self.assertEqual(data[1], ('id', 'name'))
        self.assertEqual(len(data[2]), 3)
        self.assertEqual(data[2][0], (1, 'first'))

        # Test limit
        data = user_data(limit=2)
        self.assertEqual(len(data[2]), 2)
        self.assertEqual(data[2][0], (1, 'first'))

        # Test order
        data = user_data(order_by='id DESC')
        self.assertEqual(data[2][0], (3, 'third'))

        # Test where
        data = user_data(where='name = "second"')
        self.assertEqual(len(data[2]), 1)
        self.assertEqual(data[2][0], (2, 'second'))

        # Put it all together
        data = user_data(limit=2, order_by='id DESC', where='id > 1')
        self.assertEqual(len(data[2]), 2)
        self.assertEqual(data[2][0], (3, 'third'))
        self.assertEqual(data[2][1], (2, 'second'))

    def test_generator(self):
        data = 'user', ('id', 'name'), ((1, u'first'), (2, u'second'),
                                        (3, u'third'))
        result = fixturegen.generator.generate(*data)
        self.assertTrue('from fixture import DataSet' in result)
        self.assertTrue('class UserData' in result)
        self.assertTrue('class user_1:' in result)
        self.assertTrue('id = 1' in result)
        if PY2:
            self.assertTrue("name = u'first'" in result)
        else:
            self.assertIn("name = 'first'", result)

        # Test default row class naming
        result = fixturegen.generator.generate('user', ('id', 'name'), ((1, u'first'),))
        self.assertTrue('class user_1:' in result)

        # Test id row class naming
        result = fixturegen.generator.generate('user', ('id', 'name'), ((1, u'first'),), row_naming_columns=['id'])
        self.assertTrue('class user_1:' in result)

        # Test empty row class naming
        result = fixturegen.generator.generate('user', ('id', 'name'), ((1, u'first'),), row_naming_columns=[])
        self.assertTrue('class user_1:' in result)

        # Test wrong row class naming
        if PY26:
            self.assertRaises(fixturegen.exc.WrongNamingColumn,
                              fixturegen.generator.generate,
                              'user', ('id', 'name'), ((1, u'first'),),
                              row_naming_columns=['non_existent_column'])
        else:
            with self.assertRaises(fixturegen.exc.WrongNamingColumn):
                fixturegen.generator.generate('user', ('id', 'name'), ((1, u'first'),),
                                              row_naming_columns=['non_existent_column'])

        # Test table without id column
        if PY26:
            self.assertRaises(fixturegen.exc.WrongNamingColumn, fixturegen.generator.generate,
                              'user_without_id', ('name',), ())
        else:
            with self.assertRaises(fixturegen.exc.WrongNamingColumn):
                fixturegen.generator.generate('user_without_id', ('name',), (),)

        # Test multiple columns
        result = fixturegen.generator.generate('user', ('id', 'name'), ((1, u'first'),),
                                               row_naming_columns=['id', 'name'])
        self.assertTrue('class user_1_first:' in result)

        # Test without import
        result = fixturegen.generator.generate(*data, with_import=False)
        self.assertFalse('from fixture import DataSet' in result)

        # Test custom fixture class name
        result = fixturegen.generator.generate(*data,
                                               fixture_class_name='TestClass')
        self.assertTrue('class TestClass(DataSet)' in result)

    def test_cli(self):
        runner = CliRunner()
        result = runner.invoke(fixturegen.cli.sqlalchemy)
        self.assertTrue('Error: Missing argument "dsn"' in result.output)
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(fixturegen.cli.sqlalchemy, [_SQLITE_DSN])
        self.assertTrue('Error: Missing argument "table"' in result.output)
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(fixturegen.cli.sqlalchemy, [_SQLITE_DSN, 'user'])
        self.assertTrue('class UserData(DataSet):' in result.output)
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(fixturegen.cli.sqlalchemy, [_SQLITE_DSN, 'user', '--naming-row-columns=id'])
        self.assertTrue('class UserData(DataSet):' in result.output)
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(fixturegen.cli.sqlalchemy, [_SQLITE_DSN, 'non_existent_table'])
        self.assertTrue('No such table' in result.output)
        self.assertEqual(result.exit_code, 1)

        result = runner.invoke(fixturegen.cli.sqlalchemy, ['wrong_dsn', 'user'])
        self.assertTrue('Wrong DSN' in result.output)
        self.assertEqual(result.exit_code, 1)

        result = runner.invoke(fixturegen.cli.sqlalchemy, [_SQLITE_DSN, 'user_with_spaced_name',
                                                           '--naming-row-columns=id,name'])
        self.assertTrue('NonValidRowClassName:' in result.output)
        self.assertTrue('user_with_spaced_name_1_first name' in result.output)
        self.assertEqual(result.exit_code, 1)
