import sys
import random
from bisect import bisect

VALID_CHOICES = set(['rock', 'paper', 'scissors', 'lizard', 'spock'])
WINNER_LOOKUPS = {
    'rock': {
        'win' : ['scissors', 'lizard'],
        'lose' : ['paper', 'spock']
    },
    'paper' : {
        'win' : ['rock', 'spock'],
        'lose': ['scissors', 'lizard']
    },
    'scissors' : {
        'win': ['paper', 'lizard'],
        'lose': ['spock', 'rock']
    },
    'lizard' : {
        'win': ['spock', 'paper'],
        'lose': ['scissors', 'rock']
    },
    'spock' : {
        'win' : ['rock', 'scissors'],
        'lose' : ['lizard', 'paper']
    }
}
PLAYER_THROW_HISTORY = {
    'rock': 0, 'paper': 0, 'scissors': 0, 'lizard': 0, 'spock': 0
}
SCORE = {
    'win' : 0,
    'lose': 0,
    'tie': 0
}

def update_game(user_choice, result):
    """
    Update game state

    @param string user_choice    user move
    @param string result         end result of the game
    """
    PLAYER_THROW_HISTORY[user_choice] += 1
    SCORE[result] += 1

def random_choice():
    """
    Picks a move at random
    """
    return random.sample(VALID_CHOICES, 1)[0]

def weighted_choice():
    """
    Picks a move based on past turns (weighted choice) 
    """
    throws = PLAYER_THROW_HISTORY.keys()
    total = 0
    picks = []

    for throw in PLAYER_THROW_HISTORY:
        total += PLAYER_THROW_HISTORY[throw]
        picks.append(total)

    r = random.random() * picks[-1]
    i = bisect(picks, r)

    return random.sample(WINNER_LOOKUPS[k[i]]['lose'], 1)[0]

def calculate_winner(user_choice, random_choice):
    """
    Calculates the winner

    @param string user_choice    user move
    @param string result         end result of the game
    """
    if random_choice in WINNER_LOOKUPS[user_choice]['win']:
        update_game(user_choice, 'win')
        return 'You win!'
    elif random_choice in WINNER_LOOKUPS[user_choice]['lose']:
        update_game(user_choice, 'lose')
        return 'The computer wins!'
    else:
        update_game(user_choice, 'tie')
        return 'Draw!'

def main():
    turns = 0
    while True:
        try:
            if turns > 5:
                cpu_input = weighted_choice()
            else:
                cpu_input = random_choice()

            cmd_input = raw_input('Rock, Paper, Scissors, Lizard, Spock! What do you choose? ').lower()
            if cmd_input in VALID_CHOICES:
                print "You chose...", cmd_input
                print "The computer chose...", cpu_input 
                print calculate_winner(cmd_input, cpu_input)
            else:
                print "Please choose a valid move."
            turns += 1
        except KeyboardInterrupt:
            print '\n'
            print 'Wins: ', SCORE['win'], 'Losses: ', SCORE['lose'], 'Ties: ', SCORE['tie']
            break

if __name__  == '__main__':
    main()
