import random

from Projects.Wheel_of_Python.lib.global_vars import LETTERS
from Projects.Wheel_of_Python.lib.global_vars import VOWELS
from Projects.Wheel_of_Python.lib.global_vars import VOWEL_COST


class WOFPlayer:

    def __init__(self, name):
        self.name = name
        self.prizeMoney = 0
        self.prizes = []


    def addMoney(self, amount):
        self.prizeMoney += amount


    def goBankrupt(self):
        self.prizeMoney = 0


    def addPrize(self, prize):
        self.prizes.append(prize)


    def __str__(self):
        return "{name} (${money})".format(name= self.name, money= self.prizeMoney)



class WOFHumanPlayer(WOFPlayer):

    def getMove(self, guessed=""):

        while True:
            player_input = input("Guess a letter, phrase or type 'exit' or 'pass': ").upper()

            # phrase or keyword will be processed later
            if len(player_input) > 1:
                return player_input

            # if player guesses a single character
            if len(player_input) == 1:

                # the user entered an invalid letter (such as @, #, or $)
                if player_input not in LETTERS:
                    print('Guesses should be letters. Try again.')
                    continue

                # this letter has already been guessed
                elif player_input in guessed:
                    print('{} has already been guessed. Try again.'.format(player_input))
                    continue

                # if guessing a vowel make sure player has enough money to buy vowel
                if player_input in VOWELS and self.prizeMoney < VOWEL_COST:
                    print('Need ${} to guess a vowel. Try again.'.format(VOWEL_COST))
                    continue

                else:
                    return player_input


class WOFComputerPlayer(WOFPlayer):

    SORTED_FREQUENCIES = 'ZQXJKVBPYGFWMUCLDRHSNIOATE'

    def __init__(self, name, difficulty):
        WOFPlayer.__init__(self, name)
        self.difficulty = difficulty


    def smartCoinFlip(self):
        smart_move = False

        if random.randrange(1, 10) > self.difficulty:
            smart_move = True

        return smart_move


    def getPossibleLetters(self, guessed):
        letters = [letter for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        possible_letters = []

        # add letters to possible_letters that aren't in guessed
        for letter in letters:
            if letter not in guessed:
                possible_letters.append(letter)

        # if not enough money to buy vowels
        if self.prizeMoney < 250:
            for vowel in VOWELS:

                # remove them from possible moves
                if vowel in possible_letters:
                    possible_letters.remove(vowel)

        return possible_letters


    def getMove(self, guessed):   # 'guessed' list should be all caps
        possible_letters = self.getPossibleLetters(guessed)

        # if only vowels left and money < 250, pass turn
        if len(possible_letters) == 0:
            return 'PASS'

        # use smartCoinFlip to decide good move or bad move
        make_good_move = self.smartCoinFlip()

        # if good move, return highest index in SORTED_FREQUENCIES that matches possible_moves
        if make_good_move is True:
            for most_used_char in WOFComputerPlayer.SORTED_FREQUENCIES[::-1]:
                if most_used_char in possible_letters:
                    return most_used_char

        # else make bad move, return random character from possible characters using random.choice()
        else:
            return random.choice(possible_letters)
