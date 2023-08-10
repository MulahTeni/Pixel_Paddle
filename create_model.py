import pickle

with open("veri.pkl", "rb") as f:
    data = pickle.load(f)

game_states = [item[0] for item in data]
player_actions = [item[1] for item in data]

print(player_actions)
