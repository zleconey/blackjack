import random

possibleValues = ["a", "2", "3", "4", "5", "6", "7", "8", "9","10","j","q","k"]
possibleSuites = ["spades","clubs","diamonds","hearts"]
valueDict = {"a":11,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"j":10,"q":10,"k":10}

class Card:
    def __init__(self,value,suite):
        self.value = value
        self.suite = suite
        self.trueVal = valueDict[self.value]
        self.isAce = True if self.value == "a" else False
        self.faceUp = False
        self.trueCardName = f"{self.value} of {self.suite}"
        self.cardName = "face down card"

    def callHand(self):
        print(self.cardName)

class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.hand = None
        self.inactiveHands = []

    def callHand(self):
        tempList = []
        for card in self.hand.cards:
            tempList.append(card.cardName)
        return tempList
    def draw(self,drawnDeck):
        drawnCard = drawnDeck.pop()
        drawnCard.faceUp = True
        drawnCard.cardName = drawnCard.trueCardName
        print(f"{self.name} drew a {drawnCard.cardName}")
        self.hand.cards.append(drawnCard)
    def drawFaceDown(self,drawnDeck):
        drawnCard = drawnDeck.pop()
        print(f"{self.name} drew a {drawnCard.cardName}")
        self.hand.cards.append(drawnCard)
    def payWin(self,mult):
        winnings = self.hand.bet * mult
        print(f"{self.name} receives {winnings}")
        self.balance += winnings
        self.hand = None
    def payLoss(self):
        print(f"{self.name} losses {self.hand.bet}")
        self.hand = None
    def placeBet(self,amount):
        self.balance -= amount
        print(f"{self.name} bet {amount}")
        return amount

class Dealer(Player):
    def __init__(self):
        super().__init__("dealer", 0)
        self.hand = Hand(0)

class Table:
    def __init__(self,shoe):
        self.shoe = shoe
        self.discard = []
    def deal(self):
        drawnCard = self.shoe.pop()
        drawnCard.faceUp = True
        drawnCard.cardName = drawnCard.trueCardName
        return drawnCard

    def callAllHands(self):
        for player in playerList:
            print(f"{player.name} has {player.callHand()}")
        print(f"{dealer.name} has {dealer.callHand()}")
class Hand:
    def __init__(self,bet):
        self.cards = []
        self.bet = bet
def getShoe():
    newShoe = deck + deck2 + deck3 +deck4
    random.shuffle(newShoe)
    return newShoe
def getPlayers():
    numberOfPlayers = int(input("how many players: "))
    playerList = []

    for i in range(numberOfPlayers):
        playerName = input("Enter player name: ")
        playerBalance = int(input("Enter player balance: "))
        playerList.append(Player(playerName, playerBalance))
    return playerList
def startGame():
    shoe = getShoe()
    table = Table(shoe)
    dealer = Dealer()

    return table,dealer
def firstDeal():
    for player in playerList:
        player.draw(table.shoe)

    dealer.drawFaceDown(table.shoe)

    for player in playerList:
        player.draw(table.shoe)

    dealer.draw(table.shoe)

    table.callAllHands()
def getDeck():
    deck = []
    for values in possibleValues:
        for suites in possibleSuites:
            deck.append(Card(values,suites))
    return deck

def checkBust(player):
    totalValue = 0
    i = 0
    for cards in player.hand.cards:
        totalValue += cards.trueVal
    while totalValue >21 and i < len(player.hand.cards):
        if player.hand.cards[i].isAce == True:
            totalValue -= 10
            i += 1
        elif player.hand.cards[i].isAce == False:
            i += 1
    if totalValue > 21:
        print("total value is: ",totalValue)
        return True
    else:
        print("total value is: ",totalValue)
        return False

##############################################################
##############################################################
def checkBj(player):
    handValue = 0
    for cards in player.hand.cards:
        handValue += cards.trueVal
    if handValue == 21:
        return True
    else:
        return False
def canSplit(player):
    if player.hand.cards[0] == player.hand.cards[1]:
        return True
    else:
        return False
deck = getDeck()
deck2 = getDeck()
deck3 = getDeck()
deck4 = getDeck()
table,dealer = startGame()
"""playerList = getPlayers()   #creates list of player objs"""
player1 = Player("Zack",500)
player2 = Player("Nick",1000)
playerList = [player1,player2]

"""for player in playerList:
     print(f"{player.name} has {player.balance}")
     bet = int(input(f"{player.name} Enter a bet: "))
     player.placeBet(bet)
     player.hand = Hand(bet)"""

playerList[0].hand = Hand(10)
playerList[1].hand = Hand(20)

firstDeal()
#all players have 2 face up cards
#dealer has one face up card and one face down card

if checkBj(dealer) == True:
    print("dealer has blackjack!")
    for player in playerList:
        if checkBj(player) == True:
            print(f"{player.name} has blackjack.")
            print(f"{player.name} pushes")
            player.payWin(1)
        else:
            print(f"{player.name} losses")
            player.payLoss()
    #round end func here<<<<<<<<<
else:
    pass
playerMoveDict = {"hit":1,"h":1,"stand":2,"s":2,"double":3,"d":3,"split":4,"sp":4}

for player in playerList:
    isPlayerTurn = True
    if checkBj(player) == True:
        print(f"{player.name} has blackjack.")
        player.payWin(2.5)
        isPlayerTurn = False            #>>>>>>>>>>>will this end loop or do i need break<<<<<<<<<<<<<<
    else:
        pass
    while isPlayerTurn == True:
        if canSplit(player) == True:
            playerChoice = input(f"{player.name} your turn. will you hit, stand, double, or split?: ").lower()
            playerChoice = playerMoveDict[playerChoice]           #>>>>>>>>>>>>>must make this happen only once<<<<<<<<<<<
        else:
            playerChoice = input(f"{player.name} your turn. will you hit, stand, or double: ").lower()
            playerChoice = playerMoveDict[playerChoice]

        if playerChoice == 1:
            player.draw(table.shoe)
            if checkBust(player) == True:
                player.payLoss()
                isPlayerTurn = False
            else:
                pass

        elif playerChoice == 2:     #>>>>>>>checkBj first, set isplayerturn = False if True<<<<<<<<<<<
            print(f"{player.name} stands")
            isPlayerTurn = False
        elif playerChoice == 3:
            player.hand.bet *= 2
            print(f"{player.name} doubles bet to {player.hand.bet}")
            player.draw(table.shoe)
            if checkBust(player) == True:
                player.payLoss()
                isPlayerTurn = False
            else:
                pass
            isPlayerTurn = False
        else:
            pass
                #run player.split   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    print(f"{player.name} turn over")

dealerHandTotal = 0  #make dealer flip face down card
for card in dealer.hand.cards:
    dealerHandTotal += card.trueVal
while dealer.hand.handtotal() < 17:
    print(f"{dealer.name} has {dealerHandTotal}. {dealer.name} hits")
    dealer.draw(table.shoe)
    dealer.hand.handtotal()

if checkBust(dealer) == True:
    print("dealer has busts")
else:
    print(f"{dealer.name} has {dealerHandTotal}")




#>>>>>>>>>>>>>>>>>>>>> instead of having an attribute for hand value ([a of spades, 3 of diamonds, 7 of hearts]),
#>>>>>>>>>>>>>>>>>>>>> make a method that creates that list
#>>>>>>>>>>>>>>>>>>>>> this way it will update that list whenever called
#>>>>>>>>>>>>>>>>>>>>> as an attribute, list will be made when initialized, and not updated when new cards added

