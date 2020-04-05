import json
import os
import pathlib
import sys
import time

# file_path = pathlib.Path.cwd().parent
# filename = os.path.join(file_path, 'lib')
# sys.path.append(filename)

## another way to import another directory?
# import os
# import sys
sys.path.insert(0, os.getcwd())

import random
import player
from global_vars import LETTERS
from global_vars import VOWELS
from global_vars import VOWEL_COST


# TODO label code sections
# TODO create failsafe for only vowels are left but no one has money to buy vowels?

def game():
    # ---- GAME LOGIC CODE ---- #

    # Game intro and variable initialization
    print('=' * 15)
    print('WHEEL OF PYTHON')
    print('=' * 15)
    print('')

    guessed = []

    # create players
    player_list = create_players()

    # choose phrase
    category, phrase = choose_phrase()

    player_index = 0

    while True:
        # loads current player
        player = player_list[player_index]

        # displays category and the letters that have been guessed so far
        show_board(category, phrase, guessed)

        print('{player} spins...'.format(player=player.name))
        time.sleep(3)  # pause for dramatic effect!

        # spin wheel to determine if player can make a move
        with open('wheel.json', 'r') as file:
            wheel = json.loads(file.read())
            wheel_prize = random.choice(wheel)

        print('{result}!'.format(result=wheel_prize['text']))
        time.sleep(1.5)  # pause again for more dramatic effect!


        #----- Handle different wheel outputs -----#
        if wheel_prize['type'] == 'bankrupt':
            # player loses their money and move onto next player
            player.goBankrupt()

        if wheel_prize['type'] == 'loseturn':
            # do nothing, move onto next player
            pass

        if wheel_prize['type'] == 'cash':
            move = player.getMove(guessed)

            # quit the game
            if move == 'EXIT':
                print('Until next time!')
                break

            # will just move onto next player
            if move == 'PASS':
                print('{player} passes'.format(player=player.name))

            #----- player guesses letter -----#
            if len(move) == 1:
                guessed.append(move)

                print('{player} guesses "{letter}"'.format(player=player.name, letter=move))

                if move in VOWELS:
                    player.prizeMoney -= VOWEL_COST

                # check if letter is in phrase and if so how many
                count = phrase.count(move)
                if count > 0:
                    if count == 1:
                        print("There is one {}".format(move))
                    else:
                        print("There are {} {}'s".format(count, move))

                    # add prize and money to player if they guess right
                    player.addMoney(count * wheel_prize['value'])
                    if wheel_prize['prize']:
                        player.addPrize(wheel_prize['prize'])

                    # all of the letters have been guessed
                    if obscure_phrase(phrase, guessed) == phrase:

                        # TODO debug msg?
                        print("A winner is you!")
                        win_game(player, phrase)
                        break

                    # player gets another turn if they guess atleast one letter
                    continue

                # else state letter is incorrect
                elif count == 0:
                    print("There is no {}".format(move))

            # they guess the whole phrase
            else:
                # if they guessed correctly
                if move == phrase:
                    # give them the money and the prizes
                    player.addMoney(wheel_prize['value'])
                    if wheel_prize['prize']:
                        player.addPrize(wheel_prize['prize'])

                    win_game(player, phrase)
                    break

                else:
                    print('{} was not the phrase'.format(move))

        # Move on to the next player (or go back to player[0] if we reached the end)
        player_index = (player_index + 1) % len(player_list)    # TODO test this code later


def get_number_of_players():    # TODO place inside create players?


    def get_number_between(prompt, min, max):
        '''
        Repeatedly asks the user for a number between min & max (inclusive)

        :param prompt:
        :param min:
        :param max:

        :return:
        '''

        while True:
            try:
                user_input = int (input(prompt))
            except ValueError:
                print("Please enter a number.")
                continue

            if user_input < min:
                print("number must be higher than", min)
            elif user_input > max:
                print("number must be lower than", max)
            else:
                return user_input


    # determine number of human players
    number_of_human_players = get_number_between("How many human players?", 0, 10)  # TODO better handle max and min number of each player type

    # determine number of computer players
    number_of_computer_players = get_number_between("How many computer players?", 0, 10)  # TODO better handle max and min number of each player type

    # select computer difficulty
    if number_of_computer_players > 0:
        computer_difficulty = get_number_between("How difficult should the computers be? (1-10)", 1, 10)
    else:
        computer_difficulty = -1

    # TODO debug msg
    print("humans:", number_of_human_players, "computers:", number_of_computer_players, "computer difficulty:", computer_difficulty)

    return number_of_human_players, number_of_computer_players, computer_difficulty


def create_players():

    number_of_humans, number_of_computers, computer_difficulty = get_number_of_players()
    player_list = []

    for x in range(number_of_humans):   # TODO turn into list comprehensions?
        player_name = input("enter name of player {number}: ".format(number= x+1))
        player_list.append(player.WOFHumanPlayer(player_name))

    for x in range(number_of_computers):
        computer_name = "computer {number}".format(number= x+1)
        player_list.append(player.WOFComputerPlayer(computer_name, computer_difficulty))

    if len(player_list) == 0:
        print('We need players to play!')
        raise Exception('Not enough players')

    return player_list


def choose_phrase(): # TODO break apart function into create_showboard()?
    with open('phrases.json', 'r') as file:

        # read file and load json as a dict
        phrases_json = json.loads(file.read())

        ## .choice() selects a an element of a list by a random index up to list length
        # retrieve phrases dict as list of keys
        # so .choice() can select an element by list index
        category = random.choice(list(phrases_json.keys()))
        phrase = random.choice(phrases_json[category])

        return category, phrase.upper()


def show_board(category, phrase, guessed):

    obscured_phrase = obscure_phrase(phrase, guessed)

    # display board
    print('')
    print('-'*15)
    print("""
Category: {}
Phrase:   {}
Guessed:  {}""".format(category, obscured_phrase, ', '.join(sorted(guessed))))
    print('')

    # return obscured_phrase


def obscure_phrase(phrase, guessed):
    obscured_phrase = phrase

    for char in obscured_phrase:
        if char in LETTERS and char not in guessed:
            obscured_phrase = obscured_phrase.replace(char, '_')

    return obscured_phrase


def win_game(winner, phrase):
    # In your head, you should hear this as being announced by a game show host
    print('{} wins! The phrase was {}'.format(winner.name, phrase))
    print('{} won ${}'.format(winner.name, winner.prizeMoney))
    if len(winner.prizes) > 0:
        print('{} also won:'.format(winner.name))
        for prize in winner.prizes:
            print('    - {}'.format(prize))









#############################  TESTING  ###################################
# print(get_number_from_player("pick a number ", 0, 10))
# get_number_of_players()
# create_players()
# print(choose_phrase())
# create_showboard('The Sixties', 'LYNDON JOHNSON RE-ELECTED AS PRESIDENT', ['E', 'N', 'Z', 'L', 'D'])

# take_turn()

game()
