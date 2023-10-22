import random

from player import Player
from game import Game
from flask import Flask, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = '123'
g = Game()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/<player_type>')
def start_game(player_type):
    if player_type == Player.Min.value:
        g.set_user(Player.Min)
        i, j = random.choice([(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)])
        g.matrix[i][j] = g.bot.value
    elif player_type == Player.Max.value:
        g.set_user(Player.Max)
    return render_template('game.html', matrix=g.matrix)


@app.route('/end')
def end():
    return render_template('game.html', matrix=g.matrix, end=True)


@app.route('/play/<int:i>/<int:j>')
def play(i, j):
    if g.terminal():
        return redirect(url_for('end'))
    try:
        g.play_user(i, j)
        if g.terminal():
            if g.evaluate() == 0:
                flash('you tied', 'info')
            else:
                flash('you won', 'info')
            return redirect(url_for('end'))
        g.minimax()
        if g.terminal():
            if g.evaluate() == 0:
                flash('you tied', 'info')
            else:
                flash('you lost', 'info')
            return redirect(url_for('end'))
        return render_template('game.html', matrix=g.matrix)
    except Exception as e:
        flash(f'{e}', 'danger')
        return render_template('game.html', matrix=g.matrix)


if __name__ == '__main__':
    app.run(debug=True)
