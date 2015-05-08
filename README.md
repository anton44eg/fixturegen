# Fixture Generator for [Fixture](https://github.com/fixture-py/fixture)
[![Coverage Status](https://coveralls.io/repos/anton44eg/fixturegen/badge.svg)](https://coveralls.io/r/anton44eg/fixturegen)

Supports only SQLAlchemy

## Install

Using pip

```sh
pip install fixturegen
```

Or using easy_install

```sh
easy_install fixturegen
```

## Usage

Basic

```sh
$ fixturegen-sqlalchemy mysql://user:password@localhost/your_db user
from fixture import DataSet

class UserData(DataSet):
    class user_1:
        id = 1
        name = u'first'
    class user_2:
        id = 2
        name = u'second'
    class user_3:
        id = 3
        name = u'third'
```

Limiting

```sh
$ fixturegen-sqlalchemy mysql://user:password@localhost/your_db user --limit=2 
from fixture import DataSet

class UserData(DataSet):
    class user_1:
        id = 1
        name = u'first'
    class user_2:
        id = 2
        name = u'second'
```

Ordering

```sh
$ fixturegen-sqlalchemy mysql://user:password@localhost/your_db user --order-by='id DESC'
from fixture import DataSet

class UserData(DataSet):
    class user_3:
        id = 3
        name = u'third'
    class user_2:
        id = 2
        name = u'second'
    class user_1:
        id = 1
        name = u'first'
```

Filtering

```sh
$ fixturegen-sqlalchemy mysql://user:password@localhost/your_db user --where='id > 1'
from fixture import DataSet

class UserData(DataSet):
    class user_2:
        id = 2
        name = u'second'
```

Hide import statement

```sh
$ fixturegen-sqlalchemy mysql://user:password@localhost/your_db user --limit=1 --without-import
class UserData(DataSet):
    class user_1:
        id = 1
        name = u'first'
```

Custom fixture class name:

```sh
$ fixturegen-sqlalchemy mysql://user:password@localhost/your_db user --fixture-class-name DummyData --limit=1
class Dummy(DataSet):
    class user_1:
        id = 1
        name = u'first'
```

Custom row class naming:
```sh
$ fixturegen-sqlalchemy mysql://user:password@localhost/your_db user --naming-row-columns=id,name --limit=1
class Dummy(DataSet):
    class user_1_first:
        id = 1
        name = u'first'
```

Help

```sh
$ fixturegen-sqlalchemy --help
```