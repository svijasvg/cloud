
### easy way to list attributes of an object

```
str = '\n'.join(str(vars(field)).split(",")[1:])
print(str)
```
