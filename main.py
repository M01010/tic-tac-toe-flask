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


@app.route('/stats')
def game_stats():
    return render_template('stats.html', games=g.games, wins=g.wins, losses=g.losses, ties=g.ties)


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
            g.games += 1
            if g.evaluate() == 0:
                flash('you tied', 'info')
                g.ties += 1
            else:
                flash('you won', 'info')
                g.wins += 1
            return redirect(url_for('end'))
        g.minimax()
        if g.terminal():
            g.games += 1
            if g.evaluate() == 0:
                flash('you tied', 'info')
                g.ties += 1
            else:
                flash('you lost', 'info')
                g.losses += 1
            return redirect(url_for('end'))
        return render_template('game.html', matrix=g.matrix)
    except Exception as e:
        flash(f'{e}', 'danger')
        return render_template('game.html', matrix=g.matrix)


if __name__ == '__main__':
    app.run(debug=True)
