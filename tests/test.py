from lazyins import Cursor


table_name = 'test_table2_'

names = ['i1', 'i2', 'f1', 'st1']
values  = [1, 2, 3.4, 'hello!']
types = ['int', 'int', 'float', 'varchar(10)']
explicit_types = [('i2', 'bool')]

cur1 = Cursor(host='localhost', port=3306, user='root', passwd='password')
cur1.table_name = table_name + '1'
cur1.register(values, names, explicit_types=explicit_types)

cur2 = Cursor()
cur2.table_name = table_name + '2'
cur2.setup(names, values, explicit_types=explicit_types)
cur2.register(values)

cur3 = Cursor()
cur3.table_name = table_name + '3'
cur3.setup(names, types=types)
cur3.register(values)

cur4 = Cursor()
cur4.table_name = table_name + '4'
data = list(zip(names, values))
cur4.register(data, explicit_types=explicit_types)


from datetime import datetime
now = datetime.now()
cur5 = Cursor()
cur5.table_name = table_name + '5'
cur5.register([1, now], ['num', 'log_date'])
