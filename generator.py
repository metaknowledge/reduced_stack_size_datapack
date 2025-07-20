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

def check_and_change_recipe(file: str):
    js = get_file(presets_recipe_dir + file)
    result = js.get('result')

    if type(result) is dict and config.get(result.get('id')) is not None:
        result.update(config.get(result.get('id')))
        with safe_open_w(recipe_dir + file) as output:
            output.writelines(json.dumps(js, indent=2)) 

def loot_table_helper(js, entry, dirpath, file):
    if config.get(entry.get('name')) is not None:
        if entry.get('functions') is None:
            entry['functions'] = []
        new_function = config.get(entry.get('name'))
        new_function['function'] = 'minecraft:set_components'
        entry['functions'].insert(0, new_function)
        with safe_open_w(loot_table_dir + dirpath + '/' + file) as output:
            output.writelines(json.dumps(js, indent=2))


        

def check_and_change_loot_table(dirpath: str, file: str):
    js = get_file(presets_loot_table_dir + dirpath + '/' + file)
    if js.get('pools') is not None:

        for pool in js.get('pools'):
            for entry in pool.get('entries'):
                if type(entry) is dict:
                    match entry.get('type'):
                        case "minecraft:alternatives":
                            for child in entry.get('children'):
                                loot_table_helper(js, child, dirpath, file)
                                
                                print("wrote", file)
                        case "minecraft:item":
                            loot_table_helper(js, entry, dirpath, file)

                    


def main():
    for dirpath, dirname, filenames in os.walk(presets_recipe_dir):
        for file in filenames:
            check_and_change_recipe(file)

    for dirpath, dirname, filenames in os.walk(presets_loot_table_dir):
        for file in filenames:
            check_and_change_loot_table(dirpath[21:], file)

main()
