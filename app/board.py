import tkinter as tk




class Board:
    """
    Representación del tablero de ajedrez.
    """

    TITLE = 'Tablero de ajedrez'

    PADDING = 60
    
    SIZE = 8
    SQUARE_SIZE = 60
    BOARD_SIZE = 8 * SQUARE_SIZE + PADDING

    WHITE_COLOR = '#F6FFDE'
    BLACK_COLOR = '#C9DBB2'
    BORDER_COLOR = '#C9DBB2'


    def __init__(self):
        """
        Inicializamos la ventana, el lienzo y pintamos las casillas del tablero.
        """
        # Inicializamos la ventana.
        self.window = tk.Tk()
        self.window.title(self.TITLE)
        self.window.resizable(False, False)

        # Incializamos el lienzo.
        self._init_canvas()

        # Dibujamos y pintamos las casillas de tablero.
        self._paint()

        # Colocamos las fichas de ajedrez en el tablero.
        self._place_pieces()


    def _init_canvas(self):
        """
        Inicializamos el lienzo con un tamaño específico definido por BOARD_SIZE.
        """
        self.canvas = tk.Canvas(self.window, width=self.BOARD_SIZE, height=self.BOARD_SIZE)
        self.canvas.pack()


    def _paint(self):
        """
        Dibujamos y pintamos las casillas del tablero.
        """
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                # Calculamos las coordenadas de la esquina superior izquierda de la casilla.
                x1, y1 = ((col * self.SQUARE_SIZE) + (self.PADDING // 2), (row * self.SQUARE_SIZE) + (self.PADDING // 2))

                # Calculamos las coordenadas de la esquina inferior derecha de la casilla.
                x2, y2 = (x1 + self.SQUARE_SIZE, y1 + self.SQUARE_SIZE)

                # Pintamos las casillas de blanco o negro según corresponda.
                if (row + col) % 2 == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.WHITE_COLOR, outline=self.WHITE_COLOR)
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.BLACK_COLOR, outline=self.WHITE_COLOR)
        
        # Dibujamos el borde del tablero.
        self.canvas.create_rectangle(self.PADDING // 2, self.PADDING // 2, self.BOARD_SIZE - (self.PADDING // 2), self.BOARD_SIZE - (self.PADDING // 2), outline=self.BORDER_COLOR)


    def _place_pieces(self):
        """
        Ubicamos las fichas de ajedrez en el tablero.
        """
        # Cargamos las imágenes de las fichas.
        self.black_bishop = tk.PhotoImage(file='./app/images/black_bishop.png')
        self.black_king = tk.PhotoImage(file='./app/images/black_king.png')
        self.black_knight = tk.PhotoImage(file='./app/images/black_knight.png')
        self.black_pawn = tk.PhotoImage(file='./app/images/black_pawn.png')
        self.black_queen = tk.PhotoImage(file='./app/images/black_queen.png')
        self.black_rook = tk.PhotoImage(file='./app/images/black_rook.png')
        self.white_bishop = tk.PhotoImage(file='./app/images/white_bishop.png')
        self.white_king = tk.PhotoImage(file='./app/images/white_king.png')
        self.white_knight = tk.PhotoImage(file='./app/images/white_knight.png')
        self.white_pawn = tk.PhotoImage(file='./app/images/white_pawn.png')
        self.white_queen = tk.PhotoImage(file='./app/images/white_queen.png')
        self.white_rook = tk.PhotoImage(file='./app/images/white_rook.png')

        # Colocamos los peones en las casillas correspondientes.
        for col in range(self.SIZE):
            self.canvas.create_image((col * self.SQUARE_SIZE) + (self.PADDING // 2) + (self.SQUARE_SIZE // 2), self.BOARD_SIZE - (self.PADDING // 2) - (self.SQUARE_SIZE // 2) - self.SQUARE_SIZE, image=self.white_pawn)
            self.canvas.create_image((col * self.SQUARE_SIZE) + (self.PADDING // 2) + (self.SQUARE_SIZE // 2), (self.PADDING // 2) + (self.SQUARE_SIZE // 2) + self.SQUARE_SIZE, image=self.black_pawn)

        # Colocamos las torres en las casillas correspondientes.
        self.canvas.create_image(self.PADDING, self.BOARD_SIZE - self.PADDING, image=self.white_rook)
        self.canvas.create_image(self.BOARD_SIZE - self.PADDING, self.BOARD_SIZE - self.PADDING, image=self.white_rook)
        self.canvas.create_image(self.PADDING, self.PADDING, image=self.black_rook)
        self.canvas.create_image(self.BOARD_SIZE - self.PADDING, self.PADDING, image=self.black_rook)

        # Colocamos los alfínes en las casillas correspondientes.
        self.canvas.create_image(self.PADDING + 2 * self.SQUARE_SIZE, self.BOARD_SIZE - self.PADDING, image=self.white_bishop)
        self.canvas.create_image(self.BOARD_SIZE - self.PADDING - 2 * self.SQUARE_SIZE, self.BOARD_SIZE - self.PADDING, image=self.white_bishop)
        self.canvas.create_image(self.PADDING + 2 * self.SQUARE_SIZE, self.PADDING, image=self.black_bishop)
        self.canvas.create_image(self.BOARD_SIZE - self.PADDING - 2 * self.SQUARE_SIZE, self.PADDING, image=self.black_bishop)

        # Colocamos los caballos en las casillas correspondientes.
        self.canvas.create_image(self.PADDING + self.SQUARE_SIZE, self.BOARD_SIZE - self.PADDING, image=self.white_knight)
        self.canvas.create_image(self.BOARD_SIZE - self.PADDING - self.SQUARE_SIZE, self.BOARD_SIZE - self.PADDING, image=self.white_knight)
        self.canvas.create_image(self.PADDING + self.SQUARE_SIZE, self.PADDING, image=self.black_knight)
        self.canvas.create_image(self.BOARD_SIZE - self.PADDING - self.SQUARE_SIZE, self.PADDING, image=self.black_knight)

        # Colocamos las reinas en las casillas correspondientes.
        self.canvas.create_image(self.PADDING + 3 * self.SQUARE_SIZE, self.BOARD_SIZE - self.PADDING, image=self.white_queen)
        self.canvas.create_image(self.PADDING + 3 * self.SQUARE_SIZE, self.PADDING, image=self.black_queen)

        # Colocamos los reyes en las casillas correspondientes.
        self.canvas.create_image(self.PADDING + 4 * self.SQUARE_SIZE, self.BOARD_SIZE - self.PADDING, image=self.white_king)
        self.canvas.create_image(self.PADDING + 4 * self.SQUARE_SIZE, self.PADDING, image=self.black_king)




if __name__ == '__main__':
    # Run the app.
    app = Board()
    app.window.mainloop()