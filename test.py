# Define data structures
my_heros = [
    {"username": "hasan", "heroname": "slardar", "warriorid": 1},
    {"username": "hasan", "heroname": "sniper", "warriorid": 2},
    {"username": "farza", "heroname": "slark", "warriorid": 3}
]

my_warriors = [
    {"warriorid": 1, "itemid": 1}, {"warriorid": 1, "itemid": 2},
    {"warriorid": 2, "itemid": 1}, {"warriorid": 2, "itemid": 3},
    {"warriorid": 3, "itemid": 2}, {"warriorid": 3, "itemid": 3}
]

my_items = [
    {"itemid": 1, "health": 200, "attack": 0, "damage": 0, "armor": 3},
    {"itemid": 2, "health": 0, "attack": 110, "damage": 230, "armor": 3},
    {"itemid": 3, "health": 55, "attack": 55, "damage": 55, "armor": 5}
]

userid = "farza"

details = []
for hero in [h for h in my_heros if h["username"] == userid]:
    hero_details = {"heroname": hero["heroname"], "items": []}
    for warrior in [w for w in my_warriors if w["warriorid"] == hero["warriorid"]]:
        item = next(item for item in my_items if item["itemid"] == warrior["itemid"])
        hero_details["items"].append({"itemid": warrior["itemid"], "details": item})
    details.append(hero_details)

print(details)

for i in details:
    print(f'\n\nHERONAME: {i["heroname"]}\n\n')
    for j in range(len(i["items"])):
        item = i["items"][j]  # Retrieve the item dictionary
        print(f'Item {item["itemid"]}: Health: {item["details"]["health"]}   Attack: {item["details"]["attack"]} '
              f'Damage: {item["details"]["damage"]}   Armor: {item["details"]["armor"]}')
