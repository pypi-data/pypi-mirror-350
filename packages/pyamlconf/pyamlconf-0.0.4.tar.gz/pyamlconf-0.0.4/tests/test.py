from pyamlconf.config import PyamlConfig

config = PyamlConfig('tests/config.yaml')

print(config.get('db.url'))
print(config.get('db.desc'))

config.update(PyamlConfig('tests/config.local.yaml'))

print(config.get('db.url'))
print(config.get('db.desc'))