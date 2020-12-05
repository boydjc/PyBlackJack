import random

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
import sys
import time

class Dealer():
    
    def __init__(self):
        
        self.dealerCards = []

        self.hiddenCardGraphic = None

    def addCard(self, card):

        # this is where we will process the ace card
        # the ace card can represent either 1 or 11 depending on what would make a
        # better hand. In this case we will let the ace represent 11 if the dealer's
        # total is 10 or less. Any other case the ace will stay equal to 1

        if card[1][1] == 1:
            # check the dealer's score
            dealerScore = self.getCardTotal()
            if dealerScore <= 10:
                self.dealerCards.append(11)
            else:
                self.dealerCards.append(1)

        else:
            # only keep the card's numerical value
            self.dealerCards.append(card[1][1])

    def emptyHand(self):
        self.dealerCards = []
        self.hiddenCardGraphic = None

    def setHiddenCardGraphic(self, cardGraphic):
        self.hiddenCardGraphic = cardGraphic

    def getHiddenCardGraphic(self):
        return self.hiddenCardGraphic

    def getDealerCards(self):
        return self.dealerCards

    def getCardTotal(self):
        
        cardTotal = sum(self.dealerCards)
        
        return cardTotal
            


class Player():
    
    def __init__(self):
        
        self.playerCards = []

    def addCard(self, card):
        # this is where we will process the ace card
        # the ace card can represent either 1 or 11 depending on what would make a
        # better hand. In this case we will let the ace represent 11 if the player's
        # total is 10 or less. Any other case the ace will stay equal to 1

        if card[1][1] == 1:
            # check the dealer's score
            playerScore = self.getCardTotal()
            if playerScore <= 10:
                self.playerCards.append(11)
            else:
                self.playerCards.append(1)

        else:
            # only keep the card's numerical value
            self.playerCards.append(card[1][1])

    def emptyHand(self):
        self.playerCards = []

    def getPlayerCards(self):
        return self.playerCards
    
    def getCardTotal(self):

        cardTotal = sum(self.playerCards)

        return cardTotal


# our game will act as our controller
# the game instance will be given an instance of the gui to control
# and update
class Game():

    def __init__(self, gameGui):

        self.player = Player()
        self.dealer = Dealer()
        self.gameState = None
        self.totalGameTurns = 0
        self.gameWinner = None

        self.gameGui = gameGui
        self.gameGui.show()

        # dealerHidden is set to True once the dealer has shown his initial
        # hidden card to the player
        self.dealerHidden = False

        # connect the signals from the gameGui to functions that affect the game state
        self.gameGui.betButtonSig.connect(self.buttonListener)
        self.gameGui.hitButtonSig.connect(self.buttonListener)
        self.gameGui.stayButtonSig.connect(self.buttonListener)

        self.betAmount = 0

    def run(self):
        self.gameState = 'Place Bet'

        # reset the deck and make sure the the deck has every card in it
        self.gameGui.resetDeck()

        # set the status label to 'Place Bet'

        self.gameGui.statusLabel.setText('Place Bet')      

        
    def startGame(self):
        self.gameState = 'Game Started'

        # game loop
        if self.gameState == 'Game Started':

            # get dealers first card
            
            # get a card
            dealerFirstCard = self.drawCard()

            # set this card as the dealer's first card graphic
            self.gameGui.dealerCardOneLabel.setPixmap(dealerFirstCard[1][0])

            # pass this card to the Dealer object to keep track of what cards the dealer has
            self.dealer.addCard(dealerFirstCard)


            # get dealer second card

            # get a card
            dealerSecondCard = self.drawCard()

            # we will pass the card back to the second card graphic to keep the card hidden
            self.gameGui.dealerCardTwoLabel.setPixmap(self.gameGui.getCardInfo('Card Back')[0])

            # and pass the real card graphic to the dealer object's setHiddenCardGraphic function
            # this graphic will be retrieved later when the dealer reveals the card
            self.dealer.setHiddenCardGraphic(dealerSecondCard[1][0])
            
            # pass this card to the Dealer object to keep track of what cards the dealer has
            self.dealer.addCard(dealerSecondCard)


            # get player first card         
            playerFirstCard = self.drawCard()

            # set this card as the player's first card graphic
            self.gameGui.playerCardOneLabel.setPixmap(playerFirstCard[1][0])

            # pass this card to the Player object to keep track of what cards the player has
            self.player.addCard(playerFirstCard)


            # get player second card
            playerSecondCard = self.drawCard()

            # set this card as the player's first card graphic
            self.gameGui.playerCardTwoLabel.setPixmap(playerSecondCard[1][0])

            # pass this card to the Player object to keep track of what cards the player has
            self.player.addCard(playerSecondCard)

            # update the player's score

            self.updatePlayerScore()

            # set the status label

            self.gameGui.statusLabel.setText("Player's Turn")
                    
            self.gameState = 'Player Turn'
            self.totalGameTurns += 1

    def dealerTurn(self):

        # set the status label

        self.gameGui.statusLabel.setText("Dealer's Turn")
        
        if self.dealerHidden == False:

            # if the dealer's hidden card has not been revealed, reveal the card
            self.dealerHidden = True
            self.gameGui.dealerCardTwoLabel.setPixmap(self.dealer.getHiddenCardGraphic())

            # reveal the score by updating
            self.updateDealerScore()


        # the dealer will hit if his score is above 16

        dealerDecision = None

        while dealerDecision != 'Stay':

            # get the dealer total

            dealerTotal = self.dealer.getCardTotal()

            if dealerTotal <= 17:
                dealerChoice = 'Hit'
                
                # dealer hits and get another card
                dealerNextCard = self.drawCard()

                # use the length of the dealer card list to determine which
                # dealer graphic slot to fill with the drawn card graphic

                dealerCardsLength = len(self.dealer.getDealerCards()) + 1

                if dealerCardsLength == 3:
                    self.gameGui.dealerCardThreeLabel.setPixmap(dealerNextCard[1][0])
                elif dealerCardsLength == 4:
                    self.gameGui.dealerCardFourLabel.setPixmap(dealerNextCard[1][0])
                elif dealerCardsLength == 5:
                    self.gameGui.dealerCardFiveLabel.setPixmap(dealerNextCard[1][0])
                elif dealerCardsLength == 6:
                    self.gameGui.dealerCardSixLabel.setPixmap(dealerNextCard[1][0])

                # pass this card to the dealer object to keep track of what cards the dealer has
                self.dealer.addCard(dealerNextCard)

                # update the dealer's score

                self.updateDealerScore()


            else:
                dealerChoice = 'Stay'
                self.gameGui.statusLabel.setText("Player's Turn")
                    
                break;
                

        # check the score to see if the game is over
        self.gameState = 'Player Turn'
        self.checkScore()
        self.totalGameTurns += 1
        

    # checkScore returns True if a condition is met that ends the game
    # these conditions are as follows:
    # Player hits 21 or goes over
    # Dealer hits 21 or goes over
    # total number of turns is greater than 3
    def checkScore(self):

        playerTotal = self.player.getCardTotal()
        dealerTotal = self.dealer.getCardTotal()

        if self.totalGameTurns <= 2:
            
            if playerTotal > 21:
                self.gameGui.statusLabel.setText('Dealer Wins')
                self.gameGui.setCoinAmount(int(self.gameGui.getCoinAmount()[7:]) - int(self.betAmount))
                self.gameState = 'Place Bet'
              
            elif playerTotal == 21:
                self.gameGui.statusLabel.setText('Player Wins')
                self.gameGui.setCoinAmount(int(self.gameGui.getCoinAmount()[7:]) + (int(self.betAmount) * 2))
                self.gameState = 'Place Bet'
                
            elif dealerTotal > 21:
                self.gameGui.statusLabel.setText('Player Wins')
                self.gameGui.setCoinAmount(int(self.gameGui.getCoinAmount()[7:]) + (int(self.betAmount) * 2))
                self.gameState = 'Place Bet'
                

            elif dealerTotal == 21:
                # if the dealer draws 21 right from the start,
                # his 2nd card will still be hidden

                if self.dealerHidden == False:
                    self.dealerHidden = True
                    self.gameGui.dealerCardTwoLabel.setPixmap(self.dealer.getHiddenCardGraphic())

                    # reveal the score by updating
                    self.updateDealerScore()
                    
                self.gameGui.statusLabel.setText('Dealer Wins')
                self.gameGui.setCoinAmount(int(self.gameGui.getCoinAmount()[7:]) - int(self.betAmount))
                self.gameState = 'Place Bet'

            
        elif self.totalGameTurns > 2:

            if not playerTotal > 21 and not dealerTotal > 21:
                if playerTotal > dealerTotal:
                    self.gameGui.statusLabel.setText('Player Wins')
                    self.gameGui.setCoinAmount(int(self.gameGui.getCoinAmount()[7:]) + (int(self.betAmount) * 2))
                    self.gameState = 'Place Bet'
                
                elif playerTotal < dealerTotal:
                    self.gameGui.statusLabel.setText('Dealer Wins')
                    self.gameGui.setCoinAmount(int(self.gameGui.getCoinAmount()[7:]) - int(self.betAmount))
                    self.gameState = 'Place Bet'


                elif playerTotal == dealerTotal:
                    # dealer wins all draws
                    self.gameGui.statusLabel.setText('Dealer Wins')
                    self.gameGui.setCoinAmount(int(self.gameGui.getCoinAmount()[7:]) - int(self.betAmount))
                    self.gameState = 'Place Bet'

                
            elif playerTotal > 21 or dealerTotal > 21:
                if dealerTotal > 21:
                    self.gameGui.statusLabel.setText('Player Wins')
                    self.gameGui.setCoinAmount(int(self.gameGui.getCoinAmount()[7:]) + (int(self.betAmount) * 2))
                    self.gameState = 'Place Bet'

                
                elif playerTotal > 21:
                    self.gameGui.statusLabel.setText('Dealer Wins')
                    self.gameGui.setCoinAmount(int(self.gameGui.getCoinAmount()[7:]) - int(self.betAmount))
                    self.gameState = 'Place Bet'






    # grabs a card for either the dealer or player
    def drawCard(self):

        # get a copy of the deck

        deckCopy = self.gameGui.getDeck()
        
        # get all of the dict keys and store them in a list
        keyList = list(deckCopy.keys())

        cardFound = False
        cardNum = 0

        while not cardFound:
            # roll a random number between 1 and 53(the number of cards in the deck)
            cardNum = random.randrange(3, 55)

            # check to make sure that card is in the deck
            if deckCopy[keyList[cardNum]][2]:
                # take the card out of the deck by setting it's boolean to false
                deckCopy[keyList[cardNum]][2] = False
                # pass the deck back to the gui to update
                self.gameGui.setDeck(deckCopy)
                break

        # return the key and contents of the card in the dictionary as a list      
        return [keyList[cardNum], deckCopy[keyList[cardNum]]]

    def updatePlayerScore(self):
        """ Passes the player's score to the gui to update the label """

        self.gameGui.setPlayerScoreLabel(self.player.getCardTotal())

    def updateDealerScore(self):
        """ Passes the dealer's score to the gui to update the label """

        self.gameGui.setDealerScoreLabel(self.dealer.getCardTotal())
        

    # listens for a button to be pressed on the GUI
    def buttonListener(self, buttonMsg):
        if buttonMsg == 'Hit':
            # only do something if its the player's turn
            if self.gameState == 'Player Turn':

                # player hits and get another card
                playerNextCard = self.drawCard()

                # use the length of the player card list to determine which
                # player graphic slot to fill with the drawn card graphic

                playerCardsLength = len(self.player.getPlayerCards()) + 1

                if playerCardsLength == 3:
                    self.gameGui.playerCardThreeLabel.setPixmap(playerNextCard[1][0])
                elif playerCardsLength == 4:
                    self.gameGui.playerCardFourLabel.setPixmap(playerNextCard[1][0])
                elif playerCardsLength == 5:
                    self.gameGui.playerCardFiveLabel.setPixmap(playerNextCard[1][0])
                elif playerCardsLength == 6:
                    self.gameGui.playerCardSixLabel.setPixmap(playerNextCard[1][0])

                # pass this card to the Player object to keep track of what cards the player has
                self.player.addCard(playerNextCard)

                # update the player's score

                self.updatePlayerScore()

                # check the score to see if the game is over
                self.checkScore()
                    

        elif buttonMsg == 'Stay':
            if self.gameState == 'Player Turn':
                # player stays and now its dealer's turn
                self.gameState = 'Dealer Turn'
                self.dealerTurn()
                self.totalGameTurns += 1
                
        elif buttonMsg == 'Bet':
            # only do something if the game is waiting for a bet to be placed
            if self.gameState == 'Place Bet':
                # make all of the card positions for both the player and the dealer equal to a blank card
                self.gameGui.clearBoard()

                # empty the player and dealer's hands
                self.dealer.emptyHand()
                self.player.emptyHand()

                # set the dealer and player score to 0
                self.gameGui.setDealerScoreLabel('0')
                self.gameGui.setPlayerScoreLabel('0')

                # dealer's card has not been revealed
                self.dealerHidden = False

                # game turns reset to 0
                self.totalGameTurns = 0
                
                
                # try to cast the bet amount to int
                try:
                    self.betAmount = int(self.gameGui.wagerInputBox.text())
                except:
                    self.betAmount = 0
                    
                if not self.betAmount <= 0 and not self.betAmount > int(self.gameGui.getCoinAmount()[7:]):
                    self.startGame()
        
        

# class for the BlackJack GUI

class PyBlackjackGui(QMainWindow):
    """PyBlackjack GUI"""


    # signal that will be emited when the player clicks hit or stay
    betButtonSig = pyqtSignal(str)
    hitButtonSig = pyqtSignal(str)
    stayButtonSig = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Py Blackjack')
        self.setFixedSize(850, 600)

        # Create a dictionary with the card name, it's picture value  as a QPixmap,
        # it's numerical value, and a boolean true or false if they are currently in the deck

        self.deckDict = {
                'Card Blank' : [QPixmap('cards/cardDeckBlank.png'), 0, True],
                'Deck Stack' : [QPixmap('cards/cardDeckStack.png'), 0, True],
                'Card Back' : [QPixmap('cards/cardDeckBack.png'), 0, True],
                # clubs
                'Ace Clubs' : [QPixmap('cards/clubs/aceClubs.png'), 1, True],
                'Two Clubs' : [QPixmap('cards/clubs/twoClubs.png'), 2, True],
                'Three Clubs' : [QPixmap('cards/clubs/threeClubs.png'), 3, True],
                'Four Clubs' : [QPixmap('cards/clubs/fourClubs.png'), 4, True],
                'Five Clubs' : [QPixmap('cards/clubs/fiveClubs.png'), 5, True],
                'Six Clubs' : [QPixmap('cards/clubs/sixClubs.png'), 6, True],
                'Seven Clubs' : [QPixmap('cards/clubs/sevenClubs.png'), 7, True],
                'Eight Clubs' : [QPixmap('cards/clubs/eightClubs.png'), 8, True],
                'Nine Clubs' : [QPixmap('cards/clubs/nineClubs.png'), 9, True],
                'Ten Clubs' : [QPixmap('cards/clubs/tenClubs.png'), 10, True],
                'Jack Clubs' : [QPixmap('cards/clubs/jackClubs.png'), 10, True],
                'Queen Clubs' : [QPixmap('cards/clubs/queenClubs.png'), 10, True],
                'King Clubs' : [QPixmap('cards/clubs/kingClubs.png'), 10, True],

                # diamonds
                'Ace Diamonds' : [QPixmap('cards/diamonds/aceDiamonds.png'), 1, True],
                'Two Diamonds' : [QPixmap('cards/diamonds/twoDiamonds.png'), 2, True],
                'Three Diamonds' : [QPixmap('cards/diamonds/threeDiamonds.png'), 3, True],
                'Four Diamonds' : [QPixmap('cards/diamonds/fourDiamonds.png'), 4, True],
                'Five Diamonds' : [QPixmap('cards/diamonds/fiveDiamonds.png'), 5, True],
                'Six Diamonds' : [QPixmap('cards/diamonds/sixDiamonds.png'), 6, True],
                'Seven Diamonds' : [QPixmap('cards/diamonds/sevenDiamonds.png'), 7, True],
                'Eight Diamonds' : [QPixmap('cards/diamonds/eightDiamonds.png'), 8, True],
                'Nine Diamonds' : [QPixmap('cards/diamonds/nineDiamonds.png'), 9, True],
                'Ten Diamonds' : [QPixmap('cards/diamonds/tenDiamonds.png'), 10, True],
                'Jack Diamonds' : [QPixmap('cards/diamonds/jackDiamonds.png'), 10, True],
                'Queen Diamonds' : [QPixmap('cards/diamonds/queenDiamonds.png'), 10, True],
                'King Diamonds' : [QPixmap('cards/diamonds/kingDiamonds.png'), 10, True],

                # hearts
                'Ace Hearts' : [QPixmap('cards/hearts/aceHearts.png'), 1, True],
                'Two Hearts' : [QPixmap('cards/hearts/twoHearts.png'), 2, True],
                'Three Hearts' : [QPixmap('cards/hearts/threeHearts.png'), 3, True],
                'Four Hearts' : [QPixmap('cards/hearts/fourHearts.png'), 4, True],
                'Five Hearts' : [QPixmap('cards/hearts/fiveHearts.png'), 5, True],
                'Six Hearts' : [QPixmap('cards/hearts/sixHearts.png'), 6, True],
                'Seven Hearts' : [QPixmap('cards/hearts/sevenHearts.png'), 7, True],
                'Eight Hearts' : [QPixmap('cards/hearts/eightHearts.png'), 8, True],
                'Nine Hearts' : [QPixmap('cards/hearts/nineHearts.png'), 9, True],
                'Ten Hearts' : [QPixmap('cards/hearts/tenHearts.png'), 10, True],
                'Jack Hearts' : [QPixmap('cards/hearts/jackHearts.png'), 10, True],
                'Queen Hearts' : [QPixmap('cards/hearts/queenHearts.png'), 10, True],
                'King Hearts' : [QPixmap('cards/hearts/kingHearts.png'), 10, True],

                # spades
                'Ace Spades' : [QPixmap('cards/spades/aceSpades.png'), 1, True],
                'Two Spades' : [QPixmap('cards/spades/twoSpades.png'), 2, True],
                'Three Spades' : [QPixmap('cards/spades/threeSpades.png'), 3, True],
                'Four Spades' : [QPixmap('cards/spades/fourSpades.png'), 4, True],
                'Five Spades' : [QPixmap('cards/spades/fiveSpades.png'), 5, True],
                'Six Spades' : [QPixmap('cards/spades/sixSpades.png'), 6, True],
                'Seven Spades' : [QPixmap('cards/spades/sevenSpades.png'), 7, True],
                'Eight Spades' : [QPixmap('cards/spades/eightSpades.png'), 8, True],
                'Nine Spades' : [QPixmap('cards/spades/nineSpades.png'), 9, True],
                'Ten Spades' : [QPixmap('cards/spades/tenSpades.png'), 10, True],
                'Jack Spades' : [QPixmap('cards/spades/jackSpades.png'), 10, True],
                'Queen Spades' : [QPixmap('cards/spades/queenSpades.png'), 10, True],
                'King Spades' : [QPixmap('cards/spades/kingSpades.png'), 10, True]
            }
        

        

        # set up the central widget that will hold everything
        # the central widget will have a boxlayout to stack
        # four vertical rows on top of one another
        self.generalLayout = QVBoxLayout()
        self.generalLayout.setContentsMargins(0, 0, 0, 0)
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.generalLayout)



        # start creating each bar that will make up the game screen
        self._createWagerBar()
        self._createDealerScoreBar()
        self._createDealerCardRow()
        self._createPlayerScoreBar()
        self._createPlayerCardRow()
        self._createHitStayButtonRow()
        

        # connect the buttons to their functions

        self.wagerBetButton.clicked.connect(self.emitBetButtonSig)
        self.hitButton.clicked.connect(self.emitHitButtonSig)
        self.stayButton.clicked.connect(self.emitStayButtonSig)

        # connect button signals to the button pressed listener function
        
    def _createWagerBar(self):
        # the wager bar used a horizontal box layout
        self.wagerBarLayout = QHBoxLayout()

        self.wagerBarLayout.setContentsMargins(11, 0, 11, 0)

        # Py BlackJack logo in top left corner
        self.pyBlackJackLabel = QLabel('Py BlackJack')
        self.pyBlackJackLabel.setFixedSize(180, 90)
        self.pyBlackJackLabel.setStyleSheet("font-size: 25px;"
                                            "font-weight: bold;"
                                            "font-style: italic;"
                                            "border-top: none;"
                                            "border-bottom: none;"
                                            "border-right: 1px solid black;"
                                            "border-left: none;")

        # this label will display who's turn it is and additional messages
        self.statusLabel = QLabel("Player Wins!")
        self.statusLabel.setStyleSheet("font-size: 30px;"
                                       "border-right: 1px solid black;"
                                       "border-top: none;"
                                       "border-bottom: none;")
        self.statusLabel.setFixedSize(270, 90)

        # this label will show how many coins the player has
        self.coinLabel = QLabel('Coins: 1000')
        self.coinLabel.setStyleSheet("font-size: 18px;"
                                     "border: none;")

        # this is where the player will type how much they
        # are willing to wager
        self.wagerInputBox = QLineEdit()
        self.wagerInputBox.setFixedSize(100, 20)
        self.wagerInputBox.setStyleSheet("border: 1px solid black;")

        self.wagerBetButton = QPushButton('Bet')
        self.wagerBetButton.setFixedSize(50, 50)
        self.wagerBetButton.setStyleSheet("border-style: solid;"
                                          "border-color: black;"
                                          "border-width: 2px;"
                                          "border-radius: 25px;"
                                          "font-size: 17px;")

        # adding each component to the master widget by adding
        # it to the wagerBarLayout assigned to the wagerWidget
        self.wagerBarLayout.addWidget(self.pyBlackJackLabel)
        self.wagerBarLayout.addSpacing(80)
        self.wagerBarLayout.addWidget(self.statusLabel)
        self.wagerBarLayout.addSpacing(90)
        self.wagerBarLayout.addWidget(self.coinLabel)
        self.wagerBarLayout.addWidget(self.wagerInputBox)
        self.wagerBarLayout.addWidget(self.wagerBetButton)

        # adding the layout to a QFrame so that we can add a border
        # around the entire layout
        self.wagerBarFrame = QFrame()
        self.wagerBarFrame.setLayout(self.wagerBarLayout)
        self.wagerBarFrame.setFixedSize(850, 90)
        self.wagerBarFrame.setContentsMargins(0, 0, 0, 0)
        self.wagerBarFrame.setStyleSheet("border: 1px solid black;"
                                         "border-left: none;"
                                         "border-right: none;")

        # wagerBarLayout must be added to the general Layout
        # before components can be added to the wagerBarLayout
        self.generalLayout.addWidget(self.wagerBarFrame)


    def _createDealerScoreBar(self):

        self.dealerScoreLayout = QHBoxLayout()
        self.dealerScoreLayout.setContentsMargins(11, 0, 11, 0)

        # Dealer Label
        self.dealerLabel = QLabel("Dealer")
        self.dealerLabel.setFixedSize(75, 45)

        self.dealerLabel.setStyleSheet("font-size: 20px;")

        self.dealerScoreLabel = QLabel("Total: 0")
        self.dealerScoreLabel.setFixedSize(90, 45)

        self.dealerScoreLabel.setStyleSheet("font-size: 20px;")

        self.dealerScoreLayout.addWidget(self.dealerLabel)
        self.dealerScoreLayout.addSpacing(100)
        self.dealerScoreLayout.addWidget(self.dealerScoreLabel)
        self.dealerScoreLayout.addStretch()

        self.dealerScoreFrame = QFrame()
        self.dealerScoreFrame.setLayout(self.dealerScoreLayout)
        self.dealerScoreFrame.setFixedSize(850, 45)
        self.dealerScoreFrame.setStyleSheet("border-bottom: 1px solid black;")
        self.dealerScoreFrame.setContentsMargins(11, 0, 11, 0)
        
        
        self.generalLayout.addWidget(self.dealerScoreFrame)

    def _createDealerCardRow(self):

        self.dealerCardRowLayout = QHBoxLayout()

        # the dealer will have a "slot" for 6 cards
        # each game shouldn't need any more cards than that

        self.dealerCardBackLabel = QLabel()
        self.dealerCardBackLabel.setStyleSheet("border: none;")
        self.dealerCardBackLabel.setFixedSize(85, 115)
        self.dealerCardBackLabel.setPixmap(self.deckDict['Deck Stack'][0])

        self.dealerCardOneLabel = QLabel()
        self.dealerCardOneLabel.setStyleSheet("border: none;")
        self.dealerCardOneLabel.setFixedSize(74, 115)
        self.dealerCardOneLabel.setPixmap(self.deckDict['Card Blank'][0])

        self.dealerCardTwoLabel = QLabel()
        self.dealerCardTwoLabel.setStyleSheet("border: none;")
        self.dealerCardTwoLabel.setFixedSize(74, 115)
        self.dealerCardTwoLabel.setPixmap(self.deckDict['Card Blank'][0])

        self.dealerCardThreeLabel = QLabel()
        self.dealerCardThreeLabel.setStyleSheet("border: none;")
        self.dealerCardThreeLabel.setFixedSize(74, 115)

        self.dealerCardFourLabel = QLabel()
        self.dealerCardFourLabel.setStyleSheet("border: none;")
        self.dealerCardFourLabel.setFixedSize(74, 115)

        self.dealerCardFiveLabel = QLabel()
        self.dealerCardFiveLabel.setStyleSheet("border: none;")
        self.dealerCardFiveLabel.setFixedSize(74, 115)

        self.dealerCardSixLabel = QLabel()
        self.dealerCardSixLabel.setStyleSheet("border: none;")
        self.dealerCardSixLabel.setFixedSize(74, 115)
        
        self.dealerCardRowLayout.addWidget(self.dealerCardOneLabel)
        self.dealerCardRowLayout.addSpacing(-112)
        self.dealerCardRowLayout.addWidget(self.dealerCardTwoLabel)
        self.dealerCardRowLayout.addSpacing(-112)
        self.dealerCardRowLayout.addWidget(self.dealerCardThreeLabel)
        self.dealerCardRowLayout.addSpacing(-112)
        self.dealerCardRowLayout.addWidget(self.dealerCardFourLabel)
        self.dealerCardRowLayout.addSpacing(-112)
        self.dealerCardRowLayout.addWidget(self.dealerCardFiveLabel)
        self.dealerCardRowLayout.addSpacing(-112)
        self.dealerCardRowLayout.addWidget(self.dealerCardSixLabel)
        self.dealerCardRowLayout.addSpacing(380)
        self.dealerCardRowLayout.addWidget(self.dealerCardBackLabel)

        self.dealerCardRowFrame = QFrame()
        self.dealerCardRowFrame.setLayout(self.dealerCardRowLayout)
        self.dealerCardRowFrame.setFixedSize(850, 150)
        self.dealerCardRowFrame.setStyleSheet("border-bottom: 1px solid black;")

        self.generalLayout.addWidget(self.dealerCardRowFrame)

    def _createPlayerScoreBar(self):

        self.playerScoreLayout = QHBoxLayout()
        self.playerScoreLayout.setContentsMargins(11, 0, 11, 0)

        # Dealer Label
        self.playerLabel = QLabel("You")
        self.playerLabel.setFixedSize(75, 45)

        self.playerLabel.setStyleSheet("font-size: 20px;")

        self.playerScoreLabel = QLabel("Total: 0")
        self.playerScoreLabel.setFixedSize(90, 45)

        self.playerScoreLabel.setStyleSheet("font-size: 20px;")

        self.playerScoreLayout.addWidget(self.playerLabel)
        self.playerScoreLayout.addSpacing(100)
        self.playerScoreLayout.addWidget(self.playerScoreLabel)
        self.playerScoreLayout.addStretch()

        self.playerScoreFrame = QFrame()
        self.playerScoreFrame.setLayout(self.playerScoreLayout)
        self.playerScoreFrame.setFixedSize(850, 45)
        self.playerScoreFrame.setStyleSheet("border-top: 1px solid black;")
        self.playerScoreFrame.setContentsMargins(11, 0, 11, 0)
        
        
        self.generalLayout.addWidget(self.playerScoreFrame)

    def _createPlayerCardRow(self):

        # the player will have a "slot" for 6 cards
        # each game shouldn't need any more cards than that

        self.playerCardRowLayout = QHBoxLayout()

        self.playerCardBackLabel = QLabel()
        self.playerCardBackLabel.setStyleSheet("border: none;")
        self.playerCardBackLabel.setFixedSize(74, 115)

        self.playerCardOneLabel = QLabel()
        self.playerCardOneLabel.setStyleSheet("border: none;")
        self.playerCardOneLabel.setFixedSize(74, 115)

        self.playerCardTwoLabel = QLabel()
        self.playerCardTwoLabel.setStyleSheet("border: none;")
        self.playerCardTwoLabel.setFixedSize(74, 115)

        self.playerCardThreeLabel = QLabel()
        self.playerCardThreeLabel.setStyleSheet("border: none;")
        self.playerCardThreeLabel.setFixedSize(74, 115)

        self.playerCardFourLabel = QLabel()
        self.playerCardFourLabel.setStyleSheet("border: none;")
        self.playerCardFourLabel.setFixedSize(74, 115)

        self.playerCardFiveLabel = QLabel()
        self.playerCardFiveLabel.setStyleSheet("border: none;")
        self.playerCardFiveLabel.setFixedSize(74, 115)

        self.playerCardSixLabel = QLabel()
        self.playerCardSixLabel.setStyleSheet("border: none;")
        self.playerCardSixLabel.setFixedSize(74, 115)

        self.playerCardRowLayout.addWidget(self.playerCardOneLabel)
        self.playerCardRowLayout.addSpacing(-112)
        self.playerCardRowLayout.addWidget(self.playerCardTwoLabel)
        self.playerCardRowLayout.addSpacing(-112)
        self.playerCardRowLayout.addWidget(self.playerCardThreeLabel)
        self.playerCardRowLayout.addSpacing(-112)
        self.playerCardRowLayout.addWidget(self.playerCardFourLabel)
        self.playerCardRowLayout.addSpacing(-112)
        self.playerCardRowLayout.addWidget(self.playerCardFiveLabel)
        self.playerCardRowLayout.addSpacing(-112)
        self.playerCardRowLayout.addWidget(self.playerCardSixLabel)
        self.playerCardRowLayout.addSpacing(380)

        # the back card for the player will actually be invisible
        # it is only there for a place holder so that the cards are nicely aligned
        self.playerCardRowLayout.addWidget(self.playerCardBackLabel)

        self.playerCardRowFrame = QFrame()
        self.playerCardRowFrame.setLayout(self.playerCardRowLayout)
        self.playerCardRowFrame.setFixedSize(850, 150)
        self.playerCardRowFrame.setStyleSheet("border-bottom: 1px solid black;")

        self.generalLayout.addWidget(self.playerCardRowFrame)

    def _createHitStayButtonRow(self):

        self.hitStayRowLayout = QHBoxLayout()

        self.hitButton = QPushButton('Hit')
        self.hitButton.setFixedSize(70, 70)

        # set the button as a toggle button so that we can
        # check if it is clicked or not
        
        self.hitButton.setCheckable(True)
        self.hitButton.setStyleSheet("border-style: solid;"
                                          "border-color: black;"
                                          "border-width: 2px;"
                                          "border-radius: 35px;"
                                          "font-size: 19px;")


        self.stayButton = QPushButton('Stay')
        self.stayButton.setFixedSize(70, 70)
        self.stayButton.setStyleSheet("border-style: solid;"
                                          "border-color: black;"
                                          "border-width: 2px;"
                                          "border-radius: 35px;"
                                          "font-size: 19px;")

        self.hitStayRowLayout.addSpacing(325)
        self.hitStayRowLayout.addWidget(self.hitButton)
        self.hitStayRowLayout.addSpacing(40)
        self.hitStayRowLayout.addWidget(self.stayButton)
        self.hitStayRowLayout.addStretch()

        self.hitStayRowFrame = QFrame()
        self.hitStayRowFrame.setLayout(self.hitStayRowLayout)
        self.hitStayRowFrame.setFixedSize(850, 100)
        self.hitStayRowFrame.setStyleSheet("border-top: 1px solid black;"
                                           "border-bottom: 1px solid black;")

        self.generalLayout.addWidget(self.hitStayRowFrame)


    def getDeck(self):
        """ Returns the entire deck """
        return self.deckDict

    def setDeck(self, deck):
        """ sets the deck equal to one that is passed in.
            The game instance will copy the current state of
            the deck and pick a card. Once it has the card it will set that card's value
            to FALSE and then pass the new version of the deck to this function. """

        self.deckDict = deck

    def getCardInfo(self, cardName):
        """ Gets the information for a specific card in the deck dictionary.
            Takes the card name as a parameter. """

        return self.deckDict[cardName]

    def emitHitButtonSig(self):
        self.hitButtonSig.emit('Hit')

    def emitStayButtonSig(self):
        self.stayButtonSig.emit('Stay')

    def emitBetButtonSig(self):
        self.betButtonSig.emit('Bet')

    def setDealerScoreLabel(self, score):
        """ Sets the dealer score label to what is passed to paramter """
        self.dealerScoreLabel.setText('Total: ' + str(score))

    def setPlayerScoreLabel(self, score):
        """ Sets the player score label to what is passed to parameter """
        self.playerScoreLabel.setText('Total: ' + str(score))

    def resetDeck(self):
        # sets all the deck card values in the dictionary back to true
        # to simulate placing all of the cards back in the deck

        for key in self.deckDict:
            self.deckDict[key][2] = True

    def setCoinAmount(self, coinAmount):
        self.coinLabel.setText('Coins: ' + str(coinAmount))

    def getCoinAmount(self):
        return self.coinLabel.text()

    def clearBoard(self):

        # sets all of the dealer and player card slots to invisible "blank" cards

        cardBlankPic = self.getCardInfo('Card Blank')[0] 

        # dealer cards
        self.dealerCardOneLabel.setPixmap(cardBlankPic)
        self.dealerCardTwoLabel.setPixmap(cardBlankPic)
        self.dealerCardThreeLabel.setPixmap(cardBlankPic)
        self.dealerCardFourLabel.setPixmap(cardBlankPic)
        self.dealerCardFiveLabel.setPixmap(cardBlankPic)
        self.dealerCardSixLabel.setPixmap(cardBlankPic)

        # player cards

        self.playerCardOneLabel.setPixmap(cardBlankPic)
        self.playerCardTwoLabel.setPixmap(cardBlankPic)
        self.playerCardThreeLabel.setPixmap(cardBlankPic)
        self.playerCardFourLabel.setPixmap(cardBlankPic)
        self.playerCardFiveLabel.setPixmap(cardBlankPic)
        self.playerCardSixLabel.setPixmap(cardBlankPic)
        

        


if __name__ == '__main__':

    pyBlackJack = QApplication([])
    gameGui = PyBlackjackGui()

    game = Game(gameGui)
    game.run()
    sys.exit(pyBlackJack.exec())
                
            


    
            


        
