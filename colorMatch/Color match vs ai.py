import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QLabel, QGridLayout, QVBoxLayout,
    QHBoxLayout, QComboBox
)
from PyQt6.QtCore import QTimer


# Card class
class Card:
    def __init__(self, color):
        self.color = color
        self.revealed = False
        self.matched = False

    def reveal(self):
        self.revealed = True

    def hide(self):
        self.revealed = False

    def markMatched(self):
        self.matched = True


# Ai class
class AIPlayer:
    def __init__(self, difficulty="easy"):
        self.memory = {}
        self.difficulty = difficulty

    def rememberCard(self, index, color):
        self.memory[index] = color

    def findKnownCards(self):
        seen = {}

        for index, color in self.memory.items():
            if color in seen:
                return seen[color], index
            else:
                seen[color] = index
        
        return None, None
    
    def chooseCard(self, cards):
        if self.difficulty == "easy":
            return self.selectRandomCards(cards)
        elif self.difficulty == "medium":
            index1, index2 = self.findKnownCards()

            if index1 is not None and random.random() < 0.5:
                return index1, index2
            
            return self.selectRandomCards(cards)
        elif self.difficulty == "hard":
            index1, index2 = self.findKnownCards()

            if index1 is not None:
                return index1, index2
            
            return self.selectRandomCards(cards)

    def selectRandomCards(self, cards):
        available = []

        for i, card in enumerate(cards):
            if not card.matched and not card.revealed:
                available.append(i)

        return random.sample(available, 2)

    def makeMove(self, game):
        index1, index2 = self.chooseCard(game.cards)

        game.revealCard(index1)
        game.revealCard(index2)

        game.selectedCards = [index1, index2]

        QTimer.singleShot(1000, lambda: game.checkMatch("AI"))


# Game Manager Class
class GameManager:
    def __init__(self, window):
        self.window = window

        self.playerScore = 0
        self.aiScore = 0

        self.currentTurn = "Player"

        self.selectedCards = []

        self.ai = AIPlayer()

        self.initializeGame()

    def initializeGame(self):
        self.cards = []

        colors = [
            "red", "blue", "green", "yellow",
            "orange", "purple", "pink", "cyan",
            "brown", "gray", "lime", "navy",
            "gold", "teal", "magenta", "olive",
            "red", "blue", "green", "yellow",
            "orange", "purple", "pink", "cyan",
            "brown", "gray", "lime", "navy",
            "gold", "teal", "magenta", "olive"
        ]

        colors = colors * 2

        random.shuffle(colors)

        for color in colors:
            self.cards.append(Card(color))

    def handleCardSelection(self, index):
        if self.currentTurn != "Player":
            return

        card = self.cards[index]

        if card.revealed or card.matched:
            return

        self.revealCard(index)

        self.selectedCards.append(index)

        if len(self.selectedCards) == 2:
            QTimer.singleShot(1000, lambda: self.checkMatch("Player"))

    def revealCard(self, index):
        card = self.cards[index]

        card.reveal()

        self.ai.rememberCard(index, card.color)

        self.window.buttons[index].setStyleSheet(
            f"background-color: {card.color};"
        )

    def hideCards(self, index1, index2):
        self.cards[index1].hide()
        self.cards[index2].hide()

        self.window.buttons[index1].setStyleSheet(
            "background-color: white;"
        )

        self.window.buttons[index2].setStyleSheet(
            "background-color: white;"
        )

    def checkMatch(self, turn):
        index1 = self.selectedCards[0]
        index2 = self.selectedCards[1]

        card1 = self.cards[index1]
        card2 = self.cards[index2]

        if card1.color == card2.color:
            card1.markMatched()
            card2.markMatched()

            self.ai.memory.pop(index1, None)
            self.ai.memory.pop(index2, None)

            self.window.buttons[index1].setStyleSheet(
                f"background-color: {card1.color};"
            )

            self.window.buttons[index2].setStyleSheet(
                f"background-color: {card2.color};"
            )

            if turn == "Player":
                self.playerScore += 1
            else:
                self.aiScore += 1

            self.window.updateScores()

            if turn == "AI" and (self.playerScore + self.aiScore) < 32:    
                QTimer.singleShot(1000, lambda: self.ai.makeMove(self))

        else:
            self.hideCards(index1, index2)
            self.switchTurn()

        self.selectedCards = []
        self.checkWinner()

    def switchTurn(self):
        if self.currentTurn == "Player":
            self.currentTurn = "AI"
            self.window.updateTurnDisplay()

            QTimer.singleShot(1000, lambda: self.ai.makeMove(self))

        else:
            self.currentTurn = "Player"
            self.window.updateTurnDisplay()

    def restartGame(self):
        self.playerScore = 0
        self.aiScore = 0

        self.currentTurn = "Player"

        self.selectedCards = []

        self.initializeGame()

        self.window.resetBoard()

        self.window.updateScores()

        self.window.updateTurnDisplay()

    def checkWinner(self):
        total = self.playerScore + self.aiScore

        if total == 32:
            if self.playerScore > self.aiScore:
                self.window.turnLabel.setText("Player Wins!")
            elif self.aiScore > self.playerScore:
                self.window.turnLabel.setText("AI Wins!")
            else:
                self.window.turnLabel.setText("Draw Game!")


# Main Window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Color Match Game")
        self.game = GameManager(self)
        self.setupUI()

    def setupUI(self):
        mainLayout = QVBoxLayout()
        topLayout = QHBoxLayout()

        self.playerLabel = QLabel("Player: 0")
        self.aiLabel = QLabel("AI: 0")
        self.turnLabel = QLabel("Player Turn")
        self.difficultyLabel = QLabel("AI Current Difficulty:")

        self.difficultyBox = QComboBox()
        self.difficultyBox.addItems(["easy", "medium", "hard"])
        self.difficultyBox.setCurrentText(self.game.ai.difficulty)
        self.difficultyBox.currentTextChanged.connect(self.difficultyChanged)

        topLayout.addWidget(self.playerLabel)
        topLayout.addWidget(self.aiLabel)
        topLayout.addWidget(self.turnLabel)
        topLayout.addWidget(self.difficultyLabel)
        topLayout.addWidget(self.difficultyBox)

        mainLayout.addLayout(topLayout)

        self.gridLayout = QGridLayout()
        self.buttons = []
        self.createBoardUI()

        mainLayout.addLayout(self.gridLayout)

        restartButton = QPushButton("Restart")

        restartButton.clicked.connect(
            self.restartClicked
        )

        mainLayout.addWidget(restartButton)

        self.setLayout(mainLayout)

    def createBoardUI(self):
        for i in range(64):
            button = QPushButton()

            button.setFixedSize(60, 60)

            button.setStyleSheet(
                "background-color: white;"
            )

            button.clicked.connect(
                lambda checked, index=i:
                self.game.handleCardSelection(index)
            )

            self.buttons.append(button)

            row = i // 8
            col = i % 8

            self.gridLayout.addWidget(button, row, col)

    def updateScores(self):
        self.playerLabel.setText(
            f"Player: {self.game.playerScore}"
        )

        self.aiLabel.setText(
            f"AI: {self.game.aiScore}"
        )

    def updateTurnDisplay(self):
        self.turnLabel.setText(
            f"{self.game.currentTurn} Turn"
        )

    def restartClicked(self):
        self.game.restartGame()

    def difficultyChanged(self, newDifficulty):
        self.game.ai.difficulty = newDifficulty
        print(f"AI difficulty changed to: {newDifficulty}")

    def resetBoard(self):
        for button in self.buttons:
            button.setStyleSheet(
                "background-color: white;"
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
