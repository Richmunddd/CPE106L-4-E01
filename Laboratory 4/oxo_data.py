# oxo_data.py

def saveGame(game, filename='saved_game.txt'):
    with open(filename, 'w') as f:
        f.write(''.join(game))

def restoreGame(filename='saved_game.txt'):
    with open(filename, 'r') as f:
        data = f.read().strip()
        return list(data)
