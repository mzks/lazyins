# lazyins
A stupid database insert helper

This tool makes MySQL/SQLite table with the values, then insert the values.

# Install
```
python -m pip install lazyins
```

# Usage
Set environment variables to connect your mysql database.
```
export LAZYINS_HOST="localhost"
export LAZYINS_PORT=3306
export LAZYINS_USER="root"
export LAZYINS_PASSWD="password"
````
You don't need this setting for SQLite database.

Then make cursor.
```
from lazyins import Cursor
cur = Cursor()  # default : mysql
# cur = Cursor(db='sqlite', db_name='your_db.db', table_name='your_table')  # sqlite option
```

This `Cursor()` function also recieves `db`, `host`, `port`, `user`, `passwd`, `db_name`, and `table_name` as arguments.


## Case 1
If you have two list to insert database.
```
names = ['value1', 'value2', 'value3']
values = [1, 2, 3.3]
```
You can make table and insert with `cur.register(values, names)`.
The column types will be assumed.


## Case 2
You have a list of tuple like that.
```
data = [('value1', 1), ('value2', 2), ('value3', 3.3)]
```
This simple `cur.register(data)` works.


## Case 3
If you want to let it assume almost all values, but you want set explicit types for some values.
For example, you need to set `tinyint` instead of `int` (assumed) for `value2`,
```
explicit_types = [('values', 'tinyint')]
cur.register(values, names, explicit_types=explicit_types)
```

## Detail options
For string, default length is 40.
If you need more, `cur.default_char_length = 100`.


