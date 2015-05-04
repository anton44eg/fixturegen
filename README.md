# Fixture Generator for [Fixture](https://github.com/fixture-py/fixture)

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
$ fixturegen mysql://user:password@localhost/your_db user
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
```

Limiting

```sh
$ fixturegen mysql://user:password@localhost/your_db user --limit=2 
from fixture import DataSet

class UserData(DataSet):
    class user_0:
        id = 1
        name = u'first'
    class user_1:
        id = 2
        name = u'second'
```

Ordering

```sh
$ fixturegen mysql://user:password@localhost/your_db user --order-by='id DESC'
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
```

Filtering

```sh
$ fixturegen mysql://user:password@localhost/your_db user --where='id > 1'
from fixture import DataSet

class UserData(DataSet):
    class user_0:
        id = 2
        name = u'second'
```
