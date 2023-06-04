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

        # Colocamos los peones en las casillas correspondientes.
        for col in range(self.SIZE):
            self.canvas.create_image(
                (col * self.SQUARE_SIZE)
                + (self.PADDING // 2)
                + (self.SQUARE_SIZE // 2),
                self.BOARD_SIZE - (self.PADDING // 2) - (self.SQUARE_SIZE // 2) - self.SQUARE_SIZE,
                image=self.white_pawn,
                tags=("piece",),
            )
            self.canvas.create_image(
                (col * self.SQUARE_SIZE)
                + (self.PADDING // 2)
                + (self.SQUARE_SIZE // 2),
                (self.PADDING // 2) + (self.SQUARE_SIZE // 2) + self.SQUARE_SIZE,
                image=self.black_pawn,
                tags=("piece",),
            )

        # Colocamos las torres en las casillas correspondientes.
        self.canvas.create_image(
            self.PADDING,
            self.BOARD_SIZE - self.PADDING,
            image=self.white_rook,
            tags=("piece",),
        )
        self.canvas.create_image(
            self.BOARD_SIZE - self.PADDING,
            self.BOARD_SIZE - self.PADDING,
            image=self.white_rook,
            tags=("piece",),
        )
        self.canvas.create_image(
            self.PADDING,
            self.PADDING,
            image=self.black_rook,
            tags=("piece",),
        )
        self.canvas.create_image(
            self.BOARD_SIZE - self.PADDING,
            self.PADDING,
            image=self.black_rook,
            tags=("piece",),
        )

        # Colocamos los alfínes en las casillas correspondientes.
        self.canvas.create_image(
            self.PADDING + 2 * self.SQUARE_SIZE,
            self.BOARD_SIZE - self.PADDING,
            image=self.white_bishop,
            tags=("piece",),
        )
        self.canvas.create_image(
            self.BOARD_SIZE - self.PADDING - 2 * self.SQUARE_SIZE,
            self.BOARD_SIZE - self.PADDING,
            image=self.white_bishop,
            tags=("piece",),
        )
        self.canvas.create_image(
            self.PADDING + 2 * self.SQUARE_SIZE,
            self.PADDING,
            image=self.black_bishop,
            tags=("piece",),
        )
        self.canvas.create_image(
            self.BOARD_SIZE - self.PADDING - 2 * self.SQUARE_SIZE,
            self.PADDING,
            image=self.black_bishop,
            tags=("piece",),
        )

        # Colocamos los caballos en las casillas correspondientes.
        self.canvas.create_image(
            self.PADDING + self.SQUARE_SIZE,
            self.BOARD_SIZE - self.PADDING,
            image=self.white_knight,
            tags=("piece",),
        )
        self.canvas.create_image(
            self.BOARD_SIZE - self.PADDING - self.SQUARE_SIZE,
            self.BOARD_SIZE - self.PADDING,
            image=self.white_knight,
            tags=("piece",),
        )
        self.canvas.create_image(
            self.PADDING + self.SQUARE_SIZE,
            self.PADDING,
            image=self.black_knight,
            tags=("piece",),
        )
        self.canvas.create_image(
            self.BOARD_SIZE - self.PADDING - self.SQUARE_SIZE,
            self.PADDING,
            image=self.black_knight,
            tags=("piece",),
        )

        # Colocamos las reinas en las casillas correspondientes.
        self.canvas.create_image(
            self.PADDING + 3 * self.SQUARE_SIZE,
            self.BOARD_SIZE - self.PADDING,
            image=self.white_queen,
            tags=("piece",),
        )
        self.canvas.create_image(
            self.PADDING + 3 * self.SQUARE_SIZE,
            self.PADDING,
            image=self.black_queen,
            tags=("piece",),
        )

        # Colocamos los reyes en las casillas correspondientes.
        self.canvas.create_image(
            self.PADDING + 4 * self.SQUARE_SIZE,
            self.BOARD_SIZE - self.PADDING,
            image=self.white_king,
            tags=("piece",),
        )
        self.canvas.create_image(
            self.PADDING + 4 * self.SQUARE_SIZE,
            self.PADDING,
            image=self.black_king,
            tags=("piece",),
        )

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


if __name__ == '__main__':
    # Run the app.
    app = Board()
    app.window.mainloop()
