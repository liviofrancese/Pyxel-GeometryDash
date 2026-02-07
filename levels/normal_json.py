import json

with open("levels\\lvl2.json", 'r') as f:
    data = json.load(f)
    level_length = data['level_length']
    obstacle_liste = data['obstacles']
    for obstacle in obstacle_liste:
        obstacle['y'] += 140
        if 'used' not in obstacle:
            obstacle['used'] = False
        if 'turned' not in obstacle:
            obstacle['turned'] = False

with open("normal.json", 'w') as f:
    data = {"level_length": level_length, "obstacles": obstacle_liste}
    json.dump(data, f, indent=4)