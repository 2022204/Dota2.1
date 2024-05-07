import database_updated_file as a
from flask import session, render_template, request
from flask import flash

# Establishing connection to the database
uri = "postgresql://dbms_owner:mWs2AfUrNK7T@ep-muddy-meadow-a5wol2jq.us-east-2.aws.neon.tech/dbms?sslmode=require"
conn = a.establish_connection(uri)

def sell():
    if conn:
        # Retrieve the user ID from the session
        userid = session["user"]

        # Select Warrior Ids from users inventory
        warrior_ids = a.select_data(conn, f"SELECT warrior_id FROM Heros_owned WHERE user_id = {userid}")

        # Select all items associated with the warriors
        owned_items = []
        for warrior_id in warrior_ids:
            items = a.select_data(conn, f"SELECT items_id FROM Warriors WHERE Warrior_id = {warrior_id}")
            owned_items.extend(items)

        # Fetch details of owned items
        items = []
        for item_id in owned_items:
            item = a.select_data(conn, f"SELECT * FROM items WHERE item_id = {item_id}")
            items.append(item)

        if request.method == "GET":
            return render_template("sell.html", items=items)
        else:
            item_id = int(request.form.get("item_id"))

            # Fetch the price of the item being sold
            price = a.select_data(conn, f"SELECT price FROM items WHERE item_id = {item_id}")

            # Update user_money From users where user_id = user_id
            update_query = "UPDATE users SET user_money = user_money + %s WHERE user_id = %s"
            update_values = (price, userid)
            a.update_data(conn, update_query, update_values)

            # Delete from warriors_owned where item_id = item_id
            delete_query = "DELETE FROM warriors_owned WHERE item_id = %s"
            delete_values = (item_id,)
            a.delete_data(conn, delete_query, delete_values)

            # Fetch updated list of items after deletion
            new_items = [item for item in items if item.get('itemid') != item_id]

            # Assuming you have a Flask flash message functionality
            flash("Item sold successfully.")

            return render_template("sell.html", items=new_items)

    else:
        # Handle if connection is not established
        return "Failed to establish connection to the database."

# Other Flask routes, etc.
