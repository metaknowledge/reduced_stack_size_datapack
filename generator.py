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

def change_recipe(name: str):
    with open(presets_recipe_dir + name + ".json", "r") as file:
        js = json.load(file)
    js['result'].update(config[name])
    # print(json.dumps(js, indent=2))
    with open(recipe_dir + name + ".json", "w") as output:
        output.writelines(json.dumps(js, indent=2))

def change_loot_table(name: str):
    with open(presets_loot_table_dir + name + ".json", "r") as preset:
        js = json.load(preset)
    for pool in js['pools']:

        for entries in pool['entries']:
            for key in config[name].keys(): 
                if (key == entries['name']):
                    entries['functions'].insert(0, config[name][key])
                    # print(json.dumps(entries['functions'], indent=2))
    # print(json.dumps(js, indent=2))
    with open(loot_table_dir + name + ".json", "w") as output:
        output.writelines(json.dumps(js, indent=2))

def main():
    for name in config:
        default_recipe = find(name + ".json", presets_recipe_dir)  
        if (default_recipe is not None):
            change_recipe(name)
        if os.path.isfile(presets_loot_table_dir + name + ".json"):
            change_loot_table(name)


main()
