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

        # Inicializamos el lienzo.
        self._init_canvas()

        # Dibujamos y pintamos las casillas del tablero.
        self._paint()

        # Creamos el tablero y lo inicializamos con celdas vacías.
        self.matrix = [[0] * self.SIZE for _ in range(self.SIZE)]

        # Colocamos las fichas de ajedrez en el tablero.
        self._place_pieces()

        # Inicializamos las variables para el movimiento de las piezas.
        self.selected_piece = None
        self.last_x = None
        self.last_y = None

        # Configuramos los eventos del ratón.
        self.canvas.bind("<Button-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._drag)
        self.canvas.bind("<ButtonRelease-1>", self._release)


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
                x1, y1 = (
                    (col * self.SQUARE_SIZE) + (self.PADDING // 2),
                    (row * self.SQUARE_SIZE) + (self.PADDING // 2),
                )

                # Calculamos las coordenadas de la esquina inferior derecha de la casilla.
                x2, y2 = (x1 + self.SQUARE_SIZE, y1 + self.SQUARE_SIZE)

                # Pintamos las casillas de blanco o negro según corresponda.
                if (row + col) % 2 == 0:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=self.WHITE_COLOR, outline=self.WHITE_COLOR
                    )
                else:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=self.BLACK_COLOR, outline=self.WHITE_COLOR
                    )

        # Dibujamos el borde del tablero.
        self.canvas.create_rectangle(
            self.PADDING // 2,
            self.PADDING // 2,
            self.BOARD_SIZE - (self.PADDING // 2),
            self.BOARD_SIZE - (self.PADDING // 2),
            outline=self.BORDER_COLOR,
        )


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

        for row in range(self.SIZE):
            for col in range(self.SIZE):
                # Coordenadas en pixeles.
                x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 + self.PADDING // 2
                y = row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 + self.PADDING // 2

                # Coordenadas dentro de la matriz.
                i = (y - (self.PADDING // 2)) // self.SQUARE_SIZE
                j = (x - (self.PADDING // 2)) // self.SQUARE_SIZE

                # Ubicamos las fichas negras.
                if (i, j) in [(0, 0), (0, 7)]:
                    self.canvas.create_image(x, y, image=self.black_rook, tags=("piece"))
                    self.matrix[i][j] = 1
                elif (i, j) in [(0, 1), (0, 6)]:
                    self.canvas.create_image(x, y, image=self.black_knight, tags=("piece"))
                    self.matrix[i][j] = 1
                elif (i, j) in [(0, 2), (0, 5)]:
                    self.canvas.create_image(x, y, image=self.black_bishop, tags=("piece"))
                    self.matrix[i][j] = 1
                elif (i, j) == (0, 3):
                    self.canvas.create_image(x, y, image=self.black_queen, tags=("piece"))
                    self.matrix[i][j] = 1
                elif (i, j) == (0, 4):
                    self.canvas.create_image(x, y, image=self.black_king, tags=("piece"))
                    self.matrix[i][j] = 1
                elif (i, j) in [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)]:
                    self.canvas.create_image(x, y, image=self.black_pawn, tags=("piece"))
                    self.matrix[i][j] = 1

                # Ubicamos las fichas blancas.
                if (i, j) in [(7, 0), (7, 7)]:
                    self.canvas.create_image(x, y, image=self.white_rook, tags=("piece"))
                    self.matrix[i][j] = 1
                elif (i, j) in [(7, 1), (7, 6)]:
                    self.canvas.create_image(x, y, image=self.white_knight, tags=("piece"))
                    self.matrix[i][j] = 1
                elif (i, j) in [(7, 2), (7, 5)]:
                    self.canvas.create_image(x, y, image=self.white_bishop, tags=("piece"))
                    self.matrix[i][j] = 1
                elif (i, j) == (7, 3):
                    self.canvas.create_image(x, y, image=self.white_queen, tags=("piece"))
                    self.matrix[i][j] = 1
                elif (i, j) == (7, 4):
                    self.canvas.create_image(x, y, image=self.white_king, tags=("piece"))
                    self.matrix[i][j] = 1
                elif (i, j) in [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7)]:
                    self.canvas.create_image(x, y, image=self.white_pawn, tags=("piece"))
                    self.matrix[i][j] = 1


    def _print_matrix(self):
        """
        Método auxiliar que imprime la matriz que representa al tablero.
        """
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                print(self.matrix[row][col], end='  ')
            print()
        print()


    def _start_drag(self, event):
        """
        Inicia el arrastre de una pieza cuando se hace clic en ella.
        """
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        item = self.canvas.find_closest(x, y)[0]
        tags = self.canvas.gettags(item)
        if "piece" in tags:
            self.selected_piece = item
            self.last_x = x
            self.last_y = y

            # Actualizamos la matrix que representa el tablero de juego.
            i = int((self.last_y - self.PADDING // 2) // self.SQUARE_SIZE)
            j = int((self.last_x - self.PADDING // 2) // self.SQUARE_SIZE)
            self.matrix[i][j] = 0


    def _drag(self, event):
        """
        Realiza el arrastre de la pieza seleccionada.
        """
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        dx = x - self.last_x
        dy = y - self.last_y
        self.canvas.move(self.selected_piece, dx, dy)
        self.last_x = x
        self.last_y = y


    def _release(self, event):
        """
        Libera la pieza y la coloca en la última casilla tocada.
        """
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        col = int((x - self.PADDING / 2) // self.SQUARE_SIZE)
        row = int((y - self.PADDING / 2) // self.SQUARE_SIZE)
        x_center = (col * self.SQUARE_SIZE) + self.PADDING / 2 + self.SQUARE_SIZE / 2
        y_center = (row * self.SQUARE_SIZE) + self.PADDING / 2 + self.SQUARE_SIZE / 2
        self.canvas.coords(self.selected_piece, x_center, y_center)
        self.selected_piece = None
        self.last_x = None
        self.last_y = None

        # Actualizamos la matrix que representa el tablero de juego.
        i = int((y_center - self.PADDING // 2) // self.SQUARE_SIZE)
        j = int((x_center - self.PADDING // 2) // self.SQUARE_SIZE)
        self.matrix[i][j] = 1

        self._print_matrix()


if __name__ == '__main__':
    # Run the app.
    app = Board()
    app.window.mainloop()