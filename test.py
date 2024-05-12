from dotenv import load_dotenv
import database_updated_file as db
import os
from helper import hashed_password, get_challenges, get_history, get_heroes, get_items_by_ids, get_items, get_list, get_tradeOffers, get_users, difference_of_lists
load_dotenv('.env.local')

conn = db.establish_connection(os.getenv('uri'))
user_id = 1


# my_challenges = get_challenges(db.select_data(conn, 
#         """
# SELECT u1.username, h1.name, c.hero_id, c.gold, c.challenger_id, c.challenge_id FROM challenges as c
# JOIN users as u1 ON u1.user_id = c.challenger_id 
# JOIN heroes as h1 ON h1.hero_id = c.hero_id
# WHERE c.defender_id = %s""",(user_id, )))

# print(my_challenges)


# items = db.select_data(conn, 
#         f"""SELECT I.name, c.item_id FROM challenge_items as c 
#         JOIN challenges as ch ON ch.challenge_id = c.challenge_id
#         JOIN items as I on I.item_id = c.item_id
#         WHERE c.challenge_id = %s""",
#         (int(my_challenges[0]["challenge_id"]), ))

# print(items)
user_id = 3
my_items = db.select_data(conn,
        f"""SELECT 
    u1.username, 
    h1.name AS hero_name, 
    c.hero_id, 
    c.gold, 
    c.challenger_id, 
    c.challenge_id,
    I.name AS item_name, 
    ci.item_id 
FROM 
    challenges AS c
JOIN 
    users AS u1 ON u1.user_id = c.challenger_id 
JOIN 
    heroes AS h1 ON h1.hero_id = c.hero_id
JOIN 
    challenge_items AS ci ON c.challenge_id = ci.challenge_id
JOIN 
    items AS I ON ci.item_id = I.item_id
WHERE 
    c.defender_id = %s""",
    (user_id, ))

# print(get_challenges(my_items))

def merge_items_by_challenge(challenges):
    # Create a dictionary to store items grouped by challenge_id
    items_by_challenge = {}
    
    # Group items by challenge_id
    for challenge in challenges:
        challenge_id = challenge['challenge_id']
        if challenge_id not in items_by_challenge:
            items_by_challenge[challenge_id] = {
                'challenger_username': challenge['challenger_username'],
                'hero_name': challenge['hero_name'],
                'hero_id': challenge['hero_id'],
                'gold': challenge['gold'],
                'challenger_id': challenge['challenger_id'],
                'challenge_id': challenge_id,
                'item_1_id': challenge['item_id'],
                'item_1_name': challenge['item_name'],
                'item_2_id': None,
                'item_2_name': 'None',
                'item_3_id': None,
                'item_3_name': 'None'
            }
        else:
            if items_by_challenge[challenge_id]['item_2_id'] is None:
                items_by_challenge[challenge_id]['item_2_id'] = challenge['item_id']
                items_by_challenge[challenge_id]['item_2_name'] = challenge['item_name']
            elif items_by_challenge[challenge_id]['item_3_id'] is None:
                items_by_challenge[challenge_id]['item_3_id'] = challenge['item_id']
                items_by_challenge[challenge_id]['item_3_name'] = challenge['item_name']
    
    merged_challenges = list(items_by_challenge.values())
    
    return merged_challenges

merged_challenges = merge_items_by_challenge(get_challenges(my_items))
print(merged_challenges)
