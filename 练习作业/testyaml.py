import yaml

path = r'yamlTest.yaml'
yaml_file = (open(path, 'r')).read()
print(yaml_file)
yaml_str = yaml.load(yaml_file, yaml.FullLoader)
print(yaml_str)
