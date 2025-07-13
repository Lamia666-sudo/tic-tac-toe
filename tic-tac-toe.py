import tkinter as tk
from collections import deque

# Initialize the main application window
class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe")
        self.geometry("300x350")
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player_symbol = 'O'  # Default player symbol
        self.computer_symbol = 'X'  # Default computer symbol
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()

    def create_widgets(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self, text=' ', font=('Arial', 24), width=5, height=2,
                                   command=lambda row=i, col=j: self.player_move(row, col),
                                   bg='lightgray', activebackground='lightblue')
                button.grid(row=i, column=j, sticky="nsew")
                self.buttons[i][j] = button
        
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)
        
        self.symbol_choice()

    def symbol_choice(self):
        choice_frame = tk.Frame(self)
        choice_frame.grid(row=3, column=0, columnspan=3, sticky="ew")

        tk.Label(choice_frame, text="Choose your symbol:").pack(side=tk.LEFT)

        x_button = tk.Button(choice_frame, text='X', command=lambda: self.set_symbol('X'))
        x_button.pack(side=tk.LEFT)

        o_button = tk.Button(choice_frame, text='O', command=lambda: self.set_symbol('O'))
        o_button.pack(side=tk.LEFT)

        self.grid_rowconfigure(3, weight=0)

    def set_symbol(self, symbol):
        self.player_symbol = symbol
        self.computer_symbol = 'O' if symbol == 'X' else 'X'
        self.reset_board()

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ' '
                self.buttons[i][j]['text'] = ' '
                self.buttons[i][j]['bg'] = 'lightgray'

    def player_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.player_symbol
            self.buttons[row][col]['text'] = self.player_symbol
            self.buttons[row][col]['bg'] = 'lightgreen'
            
            # Check for win/tie
            if self.evaluate(self.board, self.player_symbol) == 10:
                self.show_result("You win!")
                return
            elif self.evaluate(self.board, self.player_symbol) == 0:
                self.show_result("It's a tie!")
                return
            
            # Computer's turn
            move = self.best_move(self.board, self.computer_symbol)
            if move != (-1, -1):
                self.board[move[0]][move[1]] = self.computer_symbol
                self.buttons[move[0]][move[1]]['text'] = self.computer_symbol
                self.buttons[move[0]][move[1]]['bg'] = 'salmon'
                
                # Check for win/tie after computer move
                if self.evaluate(self.board, self.computer_symbol) == 10:
                    self.show_result("Computer wins!")
                elif self.evaluate(self.board, self.computer_symbol) == 0:
                    self.show_result("It's a tie!")

    def show_result(self, message):
        result_window = tk.Toplevel(self)
        result_window.title("Game Over")
        tk.Label(result_window, text=message, font=('Arial', 16)).pack(pady=20)
        tk.Button(result_window, text="OK", command=self.quit_game).pack(pady=10)

    def quit_game(self):
        self.destroy()

    def evaluate(self, board, symbol):
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != ' ':
                return 10 if board[i][0] == symbol else -10
            if board[0][i] == board[1][i] == board[2][i] != ' ':
                return 10 if board[0][i] == symbol else -10
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return 10 if board[0][0] == symbol else -10
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return 10 if board[0][2] == symbol else -10
        if all(cell != ' ' for row in board for cell in row):
            return 0
        return None

    def best_move(self, board, computer_symbol):
        player_symbol = 'O' if computer_symbol == 'X' else 'X'

        # Check if the computer can win in the next move
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = computer_symbol
                    if self.evaluate(board, computer_symbol) == 10:
                        return (i, j)
                    board[i][j] = ' '  # Undo the move

        # Check if the player can win in the next move, and block them
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = player_symbol
                    if self.evaluate(board, player_symbol) == -10:
                        board[i][j] = ' '  # Undo the move
                        return (i, j)  # Block player's winning move
                    board[i][j] = ' '  # Undo the move

        # If no immediate win/block, choose a random empty space
        empty_spaces = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
        if empty_spaces:
            return empty_spaces[0]  # Return the first available move

        return (-1, -1)

# Run the application
if __name__ == "__main__":
    app = TicTacToe()
    app.mainloop()
