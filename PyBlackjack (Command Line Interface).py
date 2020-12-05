import random
import os

class Dealer():
    
    def __init__(self):

        # give the dealer his first two cards

        dealerFirstCard = random.randrange(1, 12)
        dealerSecondCard = random.randrange(1, 12)
        
        self.dealerCards = [dealerFirstCard, dealerSecondCard]

    def displayFirstCard(self):
        print('The dealer has a', self.dealerCards[0], 'showing and a hidden card.')
        print('His total is hidden as well.')

    def displayHiddenCard(self):
        print("The dealer's hidden card was a " + str(self.dealerCards[1]) + ".")

    def displayCards(self):
        print("Dealer's Cards:", self.dealerCards)

    def drawCard(self):

        cardDrawn = random.randrange(1, 12)

        print('The Dealer draws a', cardDrawn)

        self.dealerCards.append(cardDrawn)

    def getCardTotal(self):

        cardTotal = sum(self.dealerCards)

        return cardTotal

    def displayCardTotal(self):

        print('Dealer Total:', self.getCardTotal())

    def makeDecision(self):
        # if the dealer's total is 16 or lower then it will hit
        # if greater then he will stay

        dealerChoice = None

        while dealerChoice != 'stay':
        
            if self.getCardTotal() <= 16:
                print('Dealer chooses to hit.')
                dealerChoice = 'hit'
                self.drawCard()
                self.displayCardTotal()
            else:
                if not self.getCardTotal() >= 21:
                    print('Dealer stays')
                    
                dealerChoice = 'stay'
                break

            


class Player():
    
    def __init__(self):

        # give the dealer his first two cards

        playerFirstCard = random.randrange(1, 12)
        playerSecondCard = random.randrange(1, 12)
        
        self.playerCards = [playerFirstCard, playerSecondCard]

    def displayFirstCards(self):
        print('You get a ' + str(self.playerCards[0]) + ' and a ' + str(self.playerCards[1]) + '.')
        self.displayCardTotal()
        
    def drawCard(self):

        cardDrawn = random.randrange(1, 12)

        print('You draw a', cardDrawn)

        self.playerCards.append(cardDrawn)

    def getCardTotal(self):

        cardTotal = sum(self.playerCards)

        return cardTotal

    def promptDecision(self):

        print('Would you like to "hit" or "stay"?')
        userChoice = input(':')

        return userChoice

    def displayCardTotal(self):

        print('Your total is:', self.getCardTotal())


class Game():

    # Game states: 'Game Started', 'Player Turn', 'Dealer Turn', 'Game Over'

    def __init__(self):

        self.player = Player()
        self.dealer = Dealer()
        self.gameState = None
        self.totalGameTurns = 0
        self.gameWinner = None

        # dealerHidden is set to True once the dealer has shown his initial
        # hidden card to the player
        self.dealerHidden = False
        
    def startGame(self):
        self.gameState = 'Game Started'

        # game loop
        while self.gameState != 'Game Over':
            if self.gameState == 'Game Started':
                print('-------------------')
                
                self.player.displayFirstCards()
                self.dealer.displayFirstCard()
                self.gameState = 'Player Turn'
                self.totalGameTurns += 1
                
            elif self.gameState == 'Player Turn':
                print('-------------------')

                endGame = self.checkScore()

                if endGame:
                    
                    self.gameState = 'Game Over'
                    
                else:
                
                    playerChoice = None

                    while playerChoice != 'stay':

                        # if the player's score is more than 21, the player will automatically stay

                        if self.player.getCardTotal() > 21:
                            playerChoice = 'stay'
                            
                        else:

                            playerChoice = self.player.promptDecision()
                        
                        if playerChoice == 'hit':
                            self.player.drawCard()
                            self.player.displayCardTotal()
                            
                            
                        elif playerChoice == 'stay':
                            break

                    self.gameState = 'Dealer Turn'
                    self.totalGameTurns += 1

            elif self.gameState == 'Dealer Turn':
                print('-------------------')

                endGame = self.checkScore()

                if endGame:

                    self.gameState = 'Game Over'

                else:
                
                    if self.dealerHidden == False:
                        self.dealer.displayHiddenCard()
                        self.dealerHidden = True
                        self.dealer.displayCardTotal()
                    
                    self.dealer.makeDecision()

                    self.gameState = 'Player Turn'
                    self.totalGameTurns += 1

            elif self.gameState == 'Game Over':
                print('-------------------')
                break

        return self.gameWinner

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

                print('Player Score:', playerTotal)
                print('Dealer Score:', dealerTotal)
                print('Dealer Wins')

                self.gameWinner = 'Dealer'

                return True
                
            elif playerTotal == 21:

                print('Player Score:', playerTotal)
                print('Dealer Score:', dealerTotal)
                print('Player Wins')

                self.gameWinner = 'Player'

                return True
                
            elif dealerTotal > 21:

                print('Player Score:', playerTotal)
                print('Dealer Score:', dealerTotal)
                print('Player Wins')

                self.gameWinner = 'Player'
                
                return True

            elif dealerTotal == 21:

                print('Player Score:', playerTotal)
                print('Dealer Score:', dealerTotal)
                print('Dealer Wins')

                self.gameWinner = 'Dealer'

                return True
            
        elif self.totalGameTurns > 2:

            if not playerTotal > 21 and not dealerTotal > 21:
                if playerTotal > dealerTotal:

                    print('Player Score:', playerTotal)
                    print('Dealer Score:', dealerTotal)
                    print('Player Wins')

                    self.gameWinner = 'Player'

                    return True
                
                elif playerTotal < dealerTotal:

                    print('Player Score:', playerTotal)
                    print('Dealer Score:', dealerTotal)
                    print('Dealer Wins')

                    self.gameWinner = 'Dealer'

                    return True

                elif playerTotal == dealerTotal:
                    # dealer wins all draws
                    print('Player Score:', playerTotal)
                    print('Dealer Score:', dealerTotal)
                    print('DRAW')
                    print('Dealer Wins')

                    self.gameWinner = 'Dealer'

                    return True
                
            elif playerTotal > 21 or dealerTotal > 21:
                if dealerTotal > 21:
                    print('Player Score:', playerTotal)
                    print('Dealer Score:', dealerTotal)
                    print('Player Wins')

                    self.gameWinner = 'Player'

                    return True
                
                elif playerScore > 21:
                    print('Player Score:', playerTotal)
                    print('Dealer Score:', dealerTotal)
                    print('Dealer Wins')

                    self.gameWinner = 'Dealer'

                    return True

        else:
            return False
            


def main():

    playerCoins = 1000
    
    userChoice = None

    while userChoice != 'no':

        os.system('cls')

        print('Player Coins:', playerCoins)
        print('--------------------------')

        userWager = None

        while userWager == None or userWager > playerCoins: 
            print('How much do you wager?')
            userWager = int(input(':'))

            if userWager > playerCoins:
                print('You do not have that many coins.')
            elif userWager <= playerCoins:
                break
        
        game = Game()
        
        gameWinner = game.startGame()

        if gameWinner == 'Player':
            playerCoins = playerCoins + (2 * userWager)
        else:
            playerCoins -= userWager


        # if the player still has coin, let him keep playing.
        # if he does not then its game over

        if playerCoins > 0 :
            print('\nPlay Again?')
            userChoice = input(':')
            
            if userChoice == 'no':
                break
        else:
            print('You are out of money.')
            print('Game Over.')
            break

    exitGame = input()


if __name__ == '__main__':
    main()
                
            


    
            


        
