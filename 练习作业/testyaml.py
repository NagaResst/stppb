import yaml

path = r'yamlTest.yaml'
yaml_file = (open(path, 'r', encoding='UTF-8')).read()
print(yaml_file)
yaml_str = yaml.load(yaml_file, yaml.FullLoader)
print(yaml_str)
to_str = yaml.dump(yaml_str)
print(to_str)