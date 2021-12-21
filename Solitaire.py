import random

# Creates a card w/ suit and number, described in Deck class
class Card:
	def __init__(self, suit, number):
		self.suit = suit
		self.number = number

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

# Simulation Variables
sim_runs = 10000
num_won = 0
total_rem = 0
largest_rem = 0

file = open("output.csv", "w")

# Solitaire runs here
for x in range(sim_runs):
	deck = Deck()
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

	file.write(str(len(hand)))
	file.write("\n")

	# Running post-simulation statistics
	if(len(hand) > largest_rem):
		largest_rem = len(hand)
	total_rem = total_rem + len(hand)
	if(len(hand) == 0): 
		num_won = num_won + 1

print("Games Run:", sim_runs)
print("Games Won:", num_won)
print("Win %:", num_won/sim_runs)
print("Avg Remaining:", total_rem/sim_runs)
print("Most Remaining:", largest_rem)

file.close()