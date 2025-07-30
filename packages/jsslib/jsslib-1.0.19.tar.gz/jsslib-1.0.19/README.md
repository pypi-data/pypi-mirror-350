# jsslib

JSON Structure Search library

Example
```
from jsslib import JSS

jss = JSS()

jss.LoadTable('./lang/table/table.lst')

print(jss.RunSql("SELECT TOP 10 id, Zi FROM zi WHERE PinYin = 'ding1' and id > 2;"))
```

Output
```
[{'Zi': '丁', 'id': 4}, {'Zi': '灯', 'id': 2077}, {'Zi': '钉', 'id': 3123}, {'Zi': '仃', 'id': 3426}, {'Zi': '叮', 'id': 3725}, {'Zi': '町', 'id': 5646}, {'Zi': '盯', 'id': 5756}, {'Zi': '酊', 'id': 7027}, {'Zi': '玎', 'id': 7917}]
```
