import json

with open("levels\\lvl1.json", 'r') as f:
    data = json.load(f)
    level_length = data['level_length']
    obstacle_liste = data['obstacles']
    for obstacle in obstacle_liste:
        if 'used' in obstacle:
            del obstacle['used']
        if 'turned' in obstacle:
            del obstacle['turned']

with open("normal.json", 'w') as f:
    data = {"level_length": level_length, "obstacles": obstacle_liste}
    json.dump(data, f, indent=4)