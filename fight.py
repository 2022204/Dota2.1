def and_the_winner_is(me, opponent):
    me_healthpoints = me["health"] + (me["health"] * (1 - 1 / me["armor"]))
    opponent_healthpoints = opponent["health"] + (
        opponent["health"] * (1 - 1 / opponent["armor"])
    )

    me_dps = me["damage"] * (me["attackspeed"] / 100)
    opponent_dps = opponent["damage"] * (opponent["attackspeed"] / 100)

    while me_healthpoints > 0 and opponent_healthpoints > 0:
        opponent_healthpoints -= me_dps
        me_healthpoints -= opponent_dps

    if me_healthpoints > 0:
        return me, opponent
    else:
        return opponent, me
