
duels = [
        {'username':'hasan','opponent': 'Murtaza', 'time': '12:00', 'result': 'Won', 'exchange':100},
        {'username':'hasan','opponent': 'Farza', 'time': '12:30', 'result': 'Lost', 'exchange':-230},
        {'username':'hasan','opponent': 'Maryam', 'time': '13:00', 'result': 'Won', 'exchange': 102},
        {'username':'farza','opponent': 'Hasan', 'time': '12:30', 'result': 'Won', 'exchange': 230},
    ]
username = "farza"

my_duels = [duel for duel in duels if duel.get('username') == username]

print(my_duels)