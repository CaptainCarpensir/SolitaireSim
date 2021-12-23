import random
import copy
import time

# Creates a card w/ suit and number, described in Deck class
class Card:
	def __init__(self, suit, number):
		self.suit = suit
		self.number = number

	def get_suit(self):
		suits = ("Clubs","Diamonds","Hearts","Spades")
		return suits[self.suit]

	def get_number(self):
		numbers = ("Ace","2","3","4","5","6","7","8","9","10","Jack","Queen","King")
		return numbers[self.number]

	def print_card(self):
		suits = ("Clubs","Diamonds","Hearts","Spades")
		numbers = ("Ace","2","3","4","5","6","7","8","9","10","Jack","Queen","King")
		print(numbers[self.number], suits[self.suit])

class Deck:
	def __init__(self):
		self.size = 52 # Total deck size
		self.suits = 4 # Number of suits: 0/1/2/3 = clubs/diamonds/hearts/spades
		self.faces = 13; # Number/face on the card
		self.cards = []
		for x in range(self.faces):
			for y in range(self.suits):
				self.cards.append(Card(y, x))
		self.randomize()

	def randomize(self):
		random.shuffle(self.cards)

def run_sim(deck):
	hand = []
	phase_one_finished = False
	phase_two_finished = False

	# Phase one runs until there are no more cards able to be pulled from the deck
	while(phase_one_finished == False):

		# Get 4 cards in hand at all time
		while(len(hand) < 4):
			# Game lost if you run out of cards to draw
			if(len(deck.cards) == 0): 
				phase_one_finished = True
				break;
			else:
				hand.append(deck.cards.pop())
		
		if(phase_one_finished == True): break

		# At least 4 cards are in hand, continue to check and remove cards
		if(hand[len(hand) - 1].number == hand[len(hand) - 4].number):
			# Remove the last four cards in the hand
			for y in range(4):
				hand.pop()
			continue

		if(hand[len(hand) - 1].suit == hand[len(hand) - 4].suit):
			# Remove second and third to last cards in hand
			for y in range(2):
				hand.pop(len(hand) - 2)
			continue

		# Drawing a card
		if(len(deck.cards) != 0):
			hand.append(deck.cards.pop())
		else:
			phase_one_finished = True

	# Phase two starts
	# Runs until unable to do anything
	while(phase_two_finished == False):
		curr_len = len(hand)

		if(len(hand) < 4):
			phase_two_finished = True
			break;

		for y in range(len(hand)):
			# Face/number matches
			if(hand[len(hand) - 1].number == hand[len(hand) - 4].number):
				# Remove the last four cards in the hand
				for y in range(4):
					hand.pop()
				break

			# Suit matches
			if(hand[len(hand) - 1].suit == hand[len(hand) - 4].suit):
				# Remove second and third to last cards in hand
				for y in range(2):
					hand.pop(len(hand) - 2)
				break

			# Cycle the hand
			temp_card = hand.pop(0)
			hand.append(temp_card)

			if(y == len(hand) - 1):
				phase_two_finished = True

	return len(hand)

# Simulation Variables
sim_runs = 10000
num_won = 0
total_rem = 0
largest_rem = 0
histogram_rem = {}
max_deck = Deck()
time_start = time.process_time_ns()

# Create dictionary with num remaining as key val to be represented in histogram 
for x in range(27):
	histogram_rem[x*2] = 0

file = open("output9.csv", "w")

# Solitaire runs here
for x in range(sim_runs):
	deck = Deck()
	temp_deck = copy.deepcopy(deck)

	# Showing progress on simulation
	if(((x+1)%(sim_runs/100)) == 0):
		print("% Progress:",round((x/sim_runs)*100))
		print("Time Elapsed:",(time.process_time_ns()-time_start)/1000000000)
		print()

	# Call function to run the simulation
	num_rem = run_sim(deck)

	# Running post-simulation information
	if(num_rem > largest_rem):
		largest_rem = num_rem
		max_deck = copy.deepcopy(temp_deck)
	total_rem = total_rem + num_rem
	if(num_rem == 0): 
		num_won = num_won + 1
	histogram_rem[num_rem] += 1

# Writing data to csv file in form rem,freq
for x in range(27):
	file.write(str(x*2))
	file.write(",")
	file.write(str(histogram_rem[x*2]))
	file.write("\n")

for x in max_deck.cards:
	file.write(str(x.get_number()))
	file.write(",")
	file.write(str(x.get_suit()))
	file.write("\n")

# Printing sim statistics
print("Games Run:", sim_runs)
print("Games Won:", num_won)
print("Win %:", num_won/sim_runs)
print("Avg Remaining:", total_rem/sim_runs)
print("Most Remaining:", largest_rem)

file.close()