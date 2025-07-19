import os
import json


data_minecraft_dir = './data/minecraft/'
loot_table_dir = data_minecraft_dir + 'loot_table/'
recipe_dir = data_minecraft_dir + 'recipe/'

presets_dir = './presets/'
presets_loot_table_dir = presets_dir + 'loot_table/'
presets_recipe_dir = presets_dir + 'recipe/'

config = './config.json'

with open(config, 'r') as file:
    config = json.load(file)

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def get_file(path: str):
    with open(path, "r") as file:
        js = json.load(file)
    return js

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')

def change_recipe(name: str):
    js = get_file(presets_recipe_dir + name + ".json")
    js['result'].update(config[name])
    # print(json.dumps(js, indent=2))
    with safe_open_w(recipe_dir + name + ".json") as output:
        output.writelines(json.dumps(js, indent=2))

def change_loot_table(name: str):
    js = get_file(presets_loot_table_dir + name + ".json")
    for pool in js['pools']:

        for entries in pool['entries']:
            for key in config[name].keys(): 
                if (key == entries['name']):
                    entries['functions'].insert(0, config[name][key])
                    # print(json.dumps(entries['functions'], indent=2))
    # print(json.dumps(js, indent=2))
    with safe_open_w(loot_table_dir + name + ".json") as output:
        output.writelines(json.dumps(js, indent=2))

def main():
    for name in config:
        default_recipe = find(name + ".json", presets_recipe_dir)  
        if (default_recipe is not None):
            change_recipe(name)
        if os.path.isfile(presets_loot_table_dir + name + ".json"):
            change_loot_table(name)


main()
