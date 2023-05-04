import json
import asyncio

# Mods the commends.json file for new commends
async def mod_json(id, name, discrim):
    with open("commends.json", 'r') as f:
        txt = f.read()
    data = json.loads(txt)
    if len(data) == 0:
        data = {}
    if str(id) not in data:
        data[str(id)] = {
            "name": str(name) + "#" + str(discrim),
            "commendations": 1
            }
    else:
        data[str(id)]["commendations"] += 1
        
    with open("commends.json", 'w') as f:
        json.dump(data, f, indent = 4)

# Retrieves commends when i!scoreboard is used
def get_commends():
    with open("commends.json", 'r') as f:
        txt = f.read()
    data = json.loads(txt)
    data = sorted(data.items(), key=lambda kv: kv[1]['commendations'], reverse=True)
    message = ""
    for key in data:
        message += f"{key[1]['name']}: {key[1]['commendations']}\n"

    return message
