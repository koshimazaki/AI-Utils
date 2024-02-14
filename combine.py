import os
import json

def combine_json_files(directory='.'):
    combined_config = {"deforum_settings": []}

    # Create a list to hold filenames
    file_list = []

    # Loop through all files in the directory to find matching pattern
    for filename in os.listdir(directory):
        if filename.startswith("deforum_creature_") and filename.endswith("_config.json"):
            file_list.append(filename)

    # Sort files by their numeric part in the filename
    file_list.sort(key=lambda f: int(f.split('_')[2]))

    # Process each file in sorted order
    for filename in file_list:
        with open(os.path.join(directory, filename), 'r') as file:
            creature_config = json.load(file)
            combined_config["deforum_settings"].append(creature_config)

    # Save the combined configuration to a file
    with open('combined_deforum_config.json', 'w') as file:
        json.dump(combined_config, file, indent=4)

# Run the function in the current directory
combine_json_files()
