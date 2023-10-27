import random

from player import Player
from game import Game
from flask import Flask, render_template, flash, session

app = Flask(__name__)
app.secret_key = '123'
g = Game()


def init_stats():
    if 'stats' not in session:
        session['stats'] = {
            'games': 0,
            'wins': 0,
            'losses': 0,
            'ties': 0
        }


def update_stats():
    init_stats()
    session['stats']['games'] += 1
    val = g.evaluate()
    if val == 0:
        flash('you tied', 'info')
        session['stats']['ties'] += 1
    elif val > 10 and g.user == Player.Max or val < 10 and g.user == Player.Min:
        flash('you won', 'info')
        session['stats']['wins'] += 1
    else:
        flash('you lost', 'info')
        session['stats']['losses'] += 1


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/<player_type>/<two>')
def start_game(player_type, two):
    if two == 'True':
        g.set_user(player_type)
        return render_template('game.html', matrix=g.matrix, p=Player.Max.value)
    if player_type == Player.Min.value:
        g.set_user(Player.Min)
        i, j = random.choice([(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)])
        g.matrix[i][j] = g.bot.value
    elif player_type == Player.Max.value:
        g.set_user(Player.Max)
    return render_template('game.html', matrix=g.matrix)


@app.route('/stats')
def game_stats():
    if 'stats' not in session:
        init_stats()
    return render_template('stats.html', stats=session.get('stats'))


@app.route('/play/<int:i>/<int:j>')
def play(i, j):
    if g.terminal():
        return render_template('game.html', matrix=g.matrix, end=True)
    try:
        g.play_user(i, j)
        if g.terminal():
            update_stats()
            return render_template('game.html', matrix=g.matrix, end=True)
        g.minimax()
        if g.terminal():
            update_stats()
            return render_template('game.html', matrix=g.matrix, end=True)
        return render_template('game.html', matrix=g.matrix)
    except Exception as e:
        flash(f'{e}', 'danger')
        return render_template('game.html', matrix=g.matrix)


@app.route('/play2/<player_type>/<int:i>/<int:j>')
def play2(player_type, i, j):
    if g.terminal():
        return render_template('game.html', matrix=g.matrix, end=True)
    try:
        g.play_user(i, j, player_type)
        if g.terminal():
            if g.evaluate() == 0:
                flash('you tied', 'info')
            else:
                flash(f'{player_type} won!', 'info')
            return render_template('game.html', matrix=g.matrix, end=True)
        if player_type == Player.Max.value:
            return render_template('game.html', matrix=g.matrix, p=Player.Min.value)
        else:
            return render_template('game.html', matrix=g.matrix, p=Player.Max.value)
    except Exception as e:
        flash(f'{e}', 'danger')
        return render_template('game.html', matrix=g.matrix, p=player_type)


if __name__ == '__main__':
    app.run(debug=True)
