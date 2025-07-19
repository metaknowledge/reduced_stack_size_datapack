# Reduced Stack Size Datapack

A datapack/tool for Minecraft to reduce the stack size of items. 

## Instructions

Since we can't edit an item definition I decided to have a python script change recipes and loot tables so that every drop has max_stack_size component added to it.
Copy the recipes and loot_tables folder from the current Minecraft jar version into the folder `presets/`. This is where the script will draw definitions from.
Take a look at the config.json to see how to define items. Then run `python generator.py` to make the files. Copy the whole folder into your datapacks/ folder and run the /reload command.
I haven't tested it for every item, so there's bound to be some edge cases.
