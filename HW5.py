# Problem 2: Probability of Loss (Weight 1). Modify your model so that you can also
# estimate the probability that you lose money in this game. Print your estimate using
# 1,000 games. Hint: You can estimate this probability by calculating the proportion of
# times that you lose money in 1,000 games.

import numpy as np
import scr.FigureSupport as FigSupport


class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250


class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = []  # create an empty list where rewards will be stored
        self.nGames = n_games

        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)

    def n_neg_reward(self):

        n_neg = sum(1 for i in self._gameRewards if i < 0)
        return float(n_neg)/self.nGames


# run trail of 1000 games to calculate expected reward
games = SetOfGames(prob_head=0.5, n_games=1000)
# print the average reward
print('Expected reward when the probability of head is 0.5:', games.get_ave_reward())

FigSupport.graph_histogram(observations=games._gameRewards,
                           title='Rewards over 1,000 games',
                           x_label='Reward ($)',
                           y_label='Count')
print('The minimum reward in a trial of 1,000 games with a fair coin is',
      min(games._gameRewards))
print('The maximum reward in a trial of 1,000 games with a fair coin is',
      max(games._gameRewards))
print('The probability of losing money is', games.n_neg_reward())
