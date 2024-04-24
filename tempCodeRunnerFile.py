
# List of itemids for which details are needed
requested_itemids = [1, 3]  # Modify this list as needed

# Create a dictionary to store details of specified items
item_details = {item['itemid']: item for item in my_items if item['itemid'] in requested_itemids}

# Example usage: Print details of all requested items
for itemid in requested_itemids:
    print(f"Details for itemid {itemid}:", item_details[itemid])