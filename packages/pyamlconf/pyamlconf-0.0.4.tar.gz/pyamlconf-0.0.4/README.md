# PyamlConf

A simple YAML-based configuration loader for Python

## Mustache 
bala bala..... see demo

## Install

```commandline
pip install pyamlconf
```

## Demo

create yaml file on local path: tests/config.yaml

```yaml
db:
  url: mysql://{{.host}}:3306
  host: 127.0.0.1
  name: dbtest
  pwd: 123456
  pool:
    size: 100
    maxidle: 10
  desc: "db.url = {{ db.url }}; db.name = {{ .name }}; db.pool = {{.pool}} "
```

create tests/test.py, like:

```python
from pyamlconf.config import PyamlConfig

config = PyamlConfig('tests/config.yaml')

print(config.get('db.url'))
print(config.get('db.desc'))
```

run test

```commandline
python tests/test.py
```

output:

```text
mysql://127.0.0.1:3306
db.url = mysql://127.0.0.1:3306; db.name = dbtest; db.pool = {'size': 100, 'maxidle': 10}
```

### update config

update with local config, use for development

create yaml file on local path: tests/config.local.yaml
```yaml
db:
  host: 127.0.0.1
  pwd: 123456
```

modify python tests/test.py, like
```python
from pyamlconf.config import PyamlConfig

config = PyamlConfig('tests/config.yaml')

print(config.get('db.url'))
print(config.get('db.desc'))

config.update(PyamlConfig('tests/config.local.yaml'))

print(config.get('db.url'))
print(config.get('db.desc'))
```

run test

```commandline
python tests/test.py
```

output:

```text
mysql://10.0.22.1:3306
db.url = mysql://10.0.22.1:3306; db.name = dbtest; db.pool = {'size': 100, 'maxidle': 10}
mysql://127.0.0.1:3306
db.url = mysql://127.0.0.1:3306; db.name = dbtest; db.pool = {'size': 100, 'maxidle': 10}
```
