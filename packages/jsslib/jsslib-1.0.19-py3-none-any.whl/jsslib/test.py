from jsslib import JSS

jss=JSS()
jss.CreateTable("./anydoc/config.json", "./anydoc/json", "./anydoc/table")
jss.LoadTable("./anydoc/table")
Ret=jss.RunSql('SELECT TOP 10 id, title FROM anydoc WHERE fulltext LIKE "实验室"')
print(Ret)
