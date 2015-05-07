Fixture Generator for `Fixture <https://github.com/fixture-py/fixture>`__
=========================================================================

Supports only SQLAlchemy

Install
-------

Using pip

.. code:: sh

    pip install fixturegen

Or using easy\_install

.. code:: sh

    easy_install fixturegen

Usage
-----

Basic

.. code:: sh

    $ fixturegen-sqlalchemy mysql://user:password@localhost/your_db user
    from fixture import DataSet

    class UserData(DataSet):
        class user_0:
            id = 1
            name = u'first'
        class user_1:
            id = 2
            name = u'second'
        class user_2:
            id = 3
            name = u'third'

Limiting

.. code:: sh

    $ fixturegen-sqlalchemy mysql://user:password@localhost/your_db user --limit=2 
    from fixture import DataSet

    class UserData(DataSet):
        class user_0:
            id = 1
            name = u'first'
        class user_1:
            id = 2
            name = u'second'

Ordering

.. code:: sh

    $ fixturegen-sqlalchemy mysql://user:password@localhost/your_db user --order-by='id DESC'
    from fixture import DataSet

    class UserData(DataSet):
        class user_0:
            id = 3
            name = u'third'
        class user_1:
            id = 2
            name = u'second'
        class user_2:
            id = 1
            name = u'first'

Filtering

.. code:: sh

    $ fixturegen-sqlalchemy mysql://user:password@localhost/your_db user --where='id > 1'
    from fixture import DataSet

    class UserData(DataSet):
        class user_0:
            id = 2
            name = u'second'

Hide import statement

.. code:: sh

    $ fixturegen-sqlalchemy mysql://user:password@localhost/your_db user --limit=1 --without-import
    class UserData(DataSet):
        class user_0:
            id = 1
            name = u'first'

Custom fixture class name:

.. code:: sh

    $ fixturegen-sqlalchemy mysql://user:password@localhost/your_db user --fixture-class-name DummyData --limit=1
    class Dummy(DataSet):
        class user_0:
            id = 1
            name = u'first'

Help

.. code:: sh

    $ fixturegen-sqlalchemy --help
