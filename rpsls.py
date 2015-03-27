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

class Game():
    def __init__(self):
        self.score = { 'win' : 0, 'lose': 0, 'tie': 0 }
        self.player_throw_history = { 'rock': 0, 'paper': 0, 'scissors': 0, 'lizard': 0, 'spock': 0 }

    def update_game(self, user_choice, result):
        """
        Update game state

        @param string user_choice    user move
        @param string result         end result of the game
        """
        self.player_throw_history[user_choice] += 1
        self.score[result] += 1

    def calculate_winner(self, user_choice, random_choice):
        """
        Calculates the winner

        @param string user_choice    user move
        @param string result         end result of the game
        """
        if random_choice in WINNER_LOOKUPS[user_choice]['win']:
            self.update_game(user_choice, 'win')
            return 'You win!'
        elif random_choice in WINNER_LOOKUPS[user_choice]['lose']:
            self.update_game(user_choice, 'lose')
            return 'The computer wins!'
        else:
            self.update_game(user_choice, 'tie')
            return 'Draw!'

    def run(self, cpu_input):
        cmd_input = raw_input('Rock, Paper, Scissors, Lizard, Spock! What do you choose? ').lower()
        if cmd_input in VALID_CHOICES:
            print "You chose...", cmd_input
            print "The computer chose...", cpu_input
            print self.calculate_winner(cmd_input, cpu_input)
        else:
            print "Please choose a valid move."

class RandomGameBot():
    def choice(self):
        """
        Picks a move at random
        """
        return random.sample(VALID_CHOICES, 1)[0]

class WeightedGameBot():
    def choice(self, player_throw_history):
        """
        Picks a move based on past turns (weighted choice)
        """
        throws = player_throw_history.keys()
        total = 0
        picks = []

        for throw in player_throw_history:
            total += player_throw_history[throw]
            picks.append(total)

            r = random.random() * picks[-1]
            i = bisect(picks, r)

        return random.sample(WINNER_LOOKUPS[throws[i]]['lose'], 1)[0]

def main():
    turns = 0
    random_bot = RandomGameBot()
    weighted_bot = WeightedGameBot()
    game = Game()

    while True:
        try:
            if turns > 5:
                cpu_input = weighted_bot.choice(game.player_throw_history)
            else:
                cpu_input = random_bot.choice()
            game.run(cpu_input)
            turns += 1
        except KeyboardInterrupt:
            print '\n'
            score = game.score
            print 'Wins: ', score['win'], 'Losses: ', score['lose'], 'Ties: ', score['tie']
            break

if __name__  == '__main__':
    main()
