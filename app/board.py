import tkinter as tk
from itertools import cycle



class Board:
    """
    Representación gráfica del tablero de ajedrez.
    """

    TITLE = 'Tablero de ajedrez'

    MARGIN = 30

    SIZE = 8
    SQUARE_SIZE = 80
    BOARD_SIZE = 8 * SQUARE_SIZE + (MARGIN * 2)

    WHITE_COLOR = '#F6FFDE'
    BLACK_COLOR = '#769656'
    BORDER_COLOR = '#C9DBB2'
    FOCUSED_COLOR = '#F6F668'

    def __init__(self):
        """
        Inicializa la ventana, las variables de instancia y el lienzo,
        pintamos el tablero sobre el lienzo y ubicamos las fichas en el tablero.
        Por último, establecemos los eventos del ratón.
        """
        self._init_window()
        self._init_vars()
        self._init_canvas()
        self._paint_board()
        self._place_pieces()
        self._init_mouse_events()


# ------------------------------------------------------------------------------
# ------------------------- MÉTODOS DE INICIALIZACIÓN
# ------------------------------------------------------------------------------


    def _init_window(self):
        """
        Inicializa la ventana de la interfaz gráfica.
        """
        self.window = tk.Tk()
        self.window.title(self.TITLE)
        self.window.resizable(False, False)


    def _init_vars(self):
        """
        Inicializa las variables de instancia.
        """
        # Jugadores existentes.
        self.players = cycle(['white', 'black'])

        # Próximo jugador. Cada vez que se llama devuelve el siguiente elemento de la lista.
        self.next_player = next(self.players)

        # Jugador actual. Inician las blancas.
        self.current_player = 'white'

        # Matriz numérica que representa el tablero.
        # Cada elemento de la matriz corresponde a (puntaje_ficha, color_ficha)
        self.matrix = [[(0, 0)] * self.SIZE for _ in range(self.SIZE)]

        # Celdas que están enfocadas en un momento dado.
        # Permite enfocar los posibles movimientos de una ficha seleccionada.
        self.focus_squares = []
        self.focus_borders = []
        self.focus_moves = []

        # Variables utilizadas con los eventos del ratón.
        self.selected_piece = None
        self.origin_x = None
        self.origin_y = None
        self.last_x = None
        self.last_y = None

        # Lista de objetos que representan las fichas del tablero.
        self.images = []

        # Rutas a las imágenes de las fichas de ajedrez.
        self.image_paths = {
            'black_bishop': './app/images/black_bishop.png',
            'black_king': './app/images/black_king.png',
            'black_knight': './app/images/black_knight.png',
            'black_pawn': './app/images/black_pawn.png',
            'black_queen': './app/images/black_queen.png',
            'black_rook': './app/images/black_rook.png',

            'white_bishop': './app/images/white_bishop.png',
            'white_king': './app/images/white_king.png',
            'white_knight': './app/images/white_knight.png',
            'white_pawn': './app/images/white_pawn.png',
            'white_queen': './app/images/white_queen.png',
            'white_rook': './app/images/white_rook.png',
        }

        # Ubicación de cada ficha en el tablero de ajedrez.
        self.piece_mapping = {
            (0, 0): 'black_rook',
            (0, 1): 'black_knight',
            (0, 2): 'black_bishop',
            (0, 3): 'black_queen',
            (0, 4): 'black_king',
            (0, 5): 'black_bishop',
            (0, 6): 'black_knight',
            (0, 7): 'black_rook',

            (1, 0): 'black_pawn',
            (1, 1): 'black_pawn',
            (1, 2): 'black_pawn',
            (1, 3): 'black_pawn',
            (1, 4): 'black_pawn',
            (1, 5): 'black_pawn',
            (1, 6): 'black_pawn',
            (1, 7): 'black_pawn',

            (7, 0): 'white_rook',
            (7, 1): 'white_knight',
            (7, 2): 'white_bishop',
            (7, 3): 'white_queen',
            (7, 4): 'white_king',
            (7, 5): 'white_bishop',
            (7, 6): 'white_knight',
            (7, 7): 'white_rook',

            (6, 0): 'white_pawn',
            (6, 1): 'white_pawn',
            (6, 2): 'white_pawn',
            (6, 3): 'white_pawn',
            (6, 4): 'white_pawn',
            (6, 5): 'white_pawn',
            (6, 6): 'white_pawn',
            (6, 7): 'white_pawn',
        }

        # Puntaje de cada ficha de ajedrez.
        self.piece_score = {
            'bishop': 3,
            'king': 10,
            'knight': 3,
            'pawn': 1,
            'queen': 9,
            'rook': 5,
        }


    def _init_canvas(self):
        """
        Inicializa el lienzo con un tamaño específico definido por BOARD_SIZE.
        """
        self.canvas = tk.Canvas(self.window, width=self.BOARD_SIZE, height=self.BOARD_SIZE)
        self.canvas.pack()


    def _init_mouse_events(self):
        """
        Establece los eventos del ratón dentro del lienzo.
        """
        self.canvas.bind("<Button-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._dragging)
        self.canvas.bind("<ButtonRelease-1>", self._release)


# ------------------------------------------------------------------------------
# -------------------- MÉTODOS PARA DIBUJAR SOBRE EL CANVAS
# ------------------------------------------------------------------------------


    def _paint_board(self):
        """
        Dibuja las casillas del tablero de ajedrez.
        """
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                # Obtenemos el nombre de la casilla.
                square_name = self._get_cell_name(row, col)

                # Pintamos la casilla de blanco o negro según corresponda.
                if (row + col) % 2 == 0:
                    self._paint_square(row, col, self.WHITE_COLOR, square_name)
                else:
                    self._paint_square(row, col, self.BLACK_COLOR, square_name)

        # Pintamos el borde del tablero.
        self._paint_border()


    def _paint_square(self, row:int, col:int, color:str, square_name:str):
        """
        Pinta un cuadrado en el tablero de juego según su posición dentro de la matriz.
        Devuelve el identificador del rectángulo creado, el cual nos permite
        manipularlo posteriormente.
        """
        # Obtenemos las coordenadas de la esquina superior izquierda e inferior derecha.
        x1, y1, x2, y2 = self._get_coords(row, col)

        # Creamos la casilla del color indicado.
        square = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')

        # Agregamos las etiquetas necesarias.
        self.canvas.addtag_withtag('square', square)
        self.canvas.addtag_withtag(square_name, square)


    def _paint_border(self):
        """
        Pinta el borde exterior del tablero de juego.
        """
        x1 = self.MARGIN
        y1 = self.MARGIN
        x2 = self.BOARD_SIZE - self.MARGIN
        y2 = self.BOARD_SIZE - self.MARGIN

        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill='', outline=self.BORDER_COLOR, width=2,
            state='disabled', tags='border'
        )


# ------------------------------------------------------------------------------
# ----------------- MÉTODOS PARA UBICAR LAS FICHAS EN EL CANVAS
# ------------------------------------------------------------------------------


    def _place_pieces(self):
        """
        Ubicamos las fichas de ajedrez en el tablero.
        """
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                # Obtenemos las coordenadas en pixeles.
                x, y = self._get_center_coords(row, col)

                # Obtenemos las coordenadas dentro de la matriz.
                i, j = self._get_pos(x, y)

                # Obtenemos el nombre de la pieza
                piece_name = self.piece_mapping.get((i, j))

                if piece_name:
                    # Obtenemos la ruta de la imagen.
                    image_path = self.image_paths.get(piece_name)

                    if image_path:
                         # Si la ruta existe, creamos la imagen en el lienzo.
                        image = tk.PhotoImage(file=image_path)
                        resized_image = image.subsample(image.width() // 60, image.height() // 60)
                        self.images.append(resized_image)

                        # Definimos etiquetas para el tipo de jugador y ficha.
                        name_parts = piece_name.split('_')
                        player = name_parts[0]      # e.g. white
                        piece_type = name_parts[1]  # e.g. king

                        self.canvas.create_image(
                            x, y, image=resized_image, tags=('piece', player, piece_type))

                        # Actualizamos la matriz colocando en la posición dada la ficha.
                        self.matrix[i][j] = (self.piece_score[piece_type], player)


# ------------------------------------------------------------------------------
# ------------------- MÉTODOS PARA LOS EVENTOS DEL RATÓN
# ------------------------------------------------------------------------------


    def _start_drag(self, event):
        """
        Inicia el arrastre de una pieza del tablero cuando se hace clic en ella.
        """
        # Desenfocamos las celdas del movimiento anterior.
        self._unfocus_square()

        # Obtenemos las coordenadas de origen donde comienza el arrastre.
        self.origin_x = self.canvas.canvasx(event.x)
        self.origin_y = self.canvas.canvasy(event.y)

        # Obtenemos la ficha más cercana a las coordenadas de origen.
        chess_piece = self.canvas.find_closest(self.origin_x, self.origin_y)[0]

        # Obtenemos las etiquetas del elemento.
        tags = self.canvas.gettags(chess_piece)

        # Si se seleccionó una ficha, actualizamos las variables del tablero.
        if 'piece' in tags and self.current_player in tags:
            self.selected_piece = chess_piece
            self.last_x = self.origin_x
            self.last_y = self.origin_y

            # Elevamos la ficha seleccionada.
            self.canvas.lift(self.selected_piece)

            # Enfocamos la celda de inicio.
            self._focus_square(self.origin_x, self.origin_y)

            # Señalamos los posibles movimientos.
            self._focus_moves()


    def _dragging(self, event):
        """
        Realiza el arrastre de la pieza seleccionada.
        Se ejecuta indefinidamente mientras el usuario mueve la ficha.
        """
        # A medida que nos movemos vamos descoloreando las celdas anteriores.
        # De modo que solo se acentúe el borde de la celda sobre la que está el cursor.
        self._unfocus_border()

        # Obtenemos la coordenada (x, y) donde está el ratón con la ficha.
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        if self._is_within_board(x, y) and self.selected_piece:
            # Obtenemos la nueva posición del cursor.
            dx = x - self.last_x
            dy = y - self.last_y

            # Situamos la ficha seleccionada en la nueva posición mientras está siendo arrastrada.
            self.canvas.move(self.selected_piece, dx, dy)

            # Acentuamos el borde de la celda actual.
            self._focus_border(x, y)

            self.last_x = x
            self.last_y = y


    def _release(self, event):
        """
        Libera la pieza y la coloca en la última casilla tocada.
        """
        # Obtenemos la coordenada cuando el usuario suelta la ficha.
        dest_x = self.canvas.canvasx(event.x)
        dest_y = self.canvas.canvasy(event.y)

        # Obtenemos la fila y columna de la última celda.
        row, col = self._get_pos(dest_x, dest_y)

        # Obtenemos los movimientos permitidos de la ficha con relación
        # a la posición inicial.
        moves = self._get_moves(self.origin_x, self.origin_y)

        # Si la ficha seleccionada se mueve a una celda dentro del tablero, vacía y que está dentro de los movimientos permitidos.
        if self._is_within_board(dest_x, dest_y) and self._is_empty(row, col) and (row, col) in moves and self.selected_piece:
            # Obtenemos las coordenadas del centro de la última celda por la que pasó.
            centered_x, centered_y = self._get_center_coords(row, col)

            # Mueve la ficha seleccionada al centro de la celda dada.
            self.canvas.coords(self.selected_piece, centered_x, centered_y)

            # Actualizamos la matrix que representa el tablero de juego.
            origin_row, origin_col = self._get_pos(self.origin_x, self.origin_y)
            row, col = self._get_pos(centered_x, centered_y)

            self.matrix[origin_row][origin_col] = (0, 0)
            self.matrix[row][col] = (self._get_selected_piece_score(), self._get_selected_piece_owner())

            # Enfocamos la celda final del movimiento.
            self._focus_square(dest_x, dest_y)

            # Imprimimos datos de la jugada.
            self._print_data(row, col)

            # Actualizamos las variables del tablero.
            self.selected_piece = None
            self.last_x = None
            self.last_y = None

            # Determinamos si la ficha seleccionada comió alguna del enemigo.
            has_eaten = self._eat(row, col)

            if has_eaten:
                piece_removed = has_eaten[0]
                score = has_eaten[1]  # !!! hacer algo con el puntaje.

                # Miramos en las etiquetas si la ficha eliminada es un rey.
                tags = self.canvas.gettags(piece_removed)

                # Si es un rey, el juego termina.
                if 'king' in tags:
                    if self.current_player == 'white':
                        message = 'Han ganado las blancas'
                    elif self.current_player == 'black':
                        message = 'Han ganado las negras'

                    text = tk.Label(
                        self.canvas,
                        text=message,
                        font=('Arial', 30, 'bold'),
                        bg=self.WHITE_COLOR)
                    text.place(relx=0.5, rely=0.5, anchor='center')

                    # Deshabilitamos todos los eventos del ratón.
                    self.canvas.unbind('<Button-1>')
                    self.canvas.unbind('<B1-Motion>')
                    self.canvas.unbind('<ButtonRelease-1>')

                # Si no es un rey, eliminamos la ficha comida del tablero.
                self.canvas.delete(piece_removed)

            # Actualizamos al jugador que le toca mover.
            self._set_turn(dest_x, dest_y)

        else:
            # Si se suelta la ficha fuera del tablero o a una posición inválida,
            # vuelve a su posición original.
            row, col = self._get_pos(self.origin_x, self.origin_y)
            centered_x, centered_y = self._get_center_coords(row, col)

            if self.selected_piece:
                self.canvas.coords(self.selected_piece, centered_x, centered_y)

        # Desenfocamos las celdas porque ya ha terminado el movimiento.
        self._unfocus_border()
        self._unfocus_moves()


# ------------------------------------------------------------------------------
# --------------- MÉTODOS PARA COLOREAR CELDAS SELECCIONADAS
# ------------------------------------------------------------------------------


    def _focus_square(self, x:int, y:int):
        """
        Enfoca la celda inicial que el usuario acaba de seleccionar.
        """
        # Obtenemos la fila y columna del tablero en la posición dada.
        row, col = self._get_pos(x, y)

        # Obtenemos las coordenadas de la celda.
        x1, y1, x2, y2 = self._get_coords(row, col)

        # Obtenemos los elementos dentro de la celda.
        items = self.canvas.find_enclosed(x1, y1, x2, y2)

        for item in items:
            # Para cada elemento obtenemos sus etiquetas.
            tags = self.canvas.gettags(item)

            # Si el elemento es una casilla, cambiamos su color y lo añadimos a
            # la lista de celdas enfocadas del tablero.
            if 'square' in tags:
                color = self.WHITE_COLOR if (row + col) % 2 == 0 else self.BLACK_COLOR
                self.canvas.itemconfig(item, fill=self.FOCUSED_COLOR)
                self.focus_squares.append((item, color))


    def _unfocus_square(self):
        """
        Desenfoca la celda por la cual ha pasado la ficha seleccionada por el usuario.
        """
        for item in self.focus_squares:
            square, color = item[0], item[1]
            self.canvas.itemconfig(square, fill=color)


    def _focus_border(self, x:int, y:int):
        """
        Enfoca el borde de la celda sobre la cual está pasando la ficha seleccionada.
        """
        # Obtenemos la fila y columna del tablero en la posición dada.
        row, col = self._get_pos(x, y)

        # Obtenemos las coordenadas de la celda.
        x1, y1, x2, y2 = self._get_coords(row, col)

        # Creamos el borde resaltado.
        item = self.canvas.create_rectangle(x1, y1, x2, y2, fill='', outline='#6D5D6E', width='2')
        self.focus_borders.append(item)

        # Obtenemos el elemento actualmente seleccionado y lo elevamos.
        current = self.canvas.find_withtag('current')[0]
        tags = self.canvas.gettags(current)
        if 'piece' in tags: self.canvas.lift(current)


    def _unfocus_border(self):
        """
        Desenfoca el borde de la celda por la cual ha pasado la ficha seleccionada.
        """
        for item in self.focus_borders:
            self.canvas.delete(item)


    def _focus_moves(self):
        """
        Enfoca los movimientos que puede hacer la ficha seleccionada.
        """
        # Obtenemos los movimientos posibles.
        moves = self._get_moves(self.origin_x, self.origin_y)

        for move in moves:
            # Obtenemos las coordenadas de la celda.
            i, j = move
            x1, y1, x2, y2 = self._get_coords(i, j)
            x1, y1, x2, y2 = (x1 + 41), (y1 + 41), (x2 - 41), (y2 - 41)

            # Creamos el borde resaltado.
            item = self.canvas.create_oval(x1, y1, x2, y2, fill='#b4c5a0', outline='')
            self.focus_moves.append(item)

        # Obtenemos el elemento actualmente seleccionado y lo elevamos.
        current = self.canvas.find_withtag('current')[0]
        tags = self.canvas.gettags(current)
        if 'piece' in tags: self.canvas.lift(current)


    def _unfocus_moves(self):
        """
        Desenfoca los movimientos que puede hacer la ficha seleccionada.
        """
        for item in self.focus_moves:
            self.canvas.delete(item)


# ------------------------------------------------------------------------------
# ---------- MÉTODOS PARA OBTENER POSIBLES MOVIMIENTOS DE UNA FICHA
# ------------------------------------------------------------------------------

    def _set_turn(self, dest_x:float, dest_y:float):
        """
        Establece a cuál jugador le toca jugar después de que se mueve una ficha.
        """
        # Obtenemos la ficha actualmente seleccionada.
        item = self.canvas.find_withtag('current')[0]
        tags = self.canvas.gettags(item)

        # Obtenemos las celdas de inicio y final del movimiento.
        origin_row, origin_col = self._get_pos(self.origin_x, self.origin_y)
        dest_row, dest_col = self._get_pos(dest_x, dest_y)

        # Si la ficha se movió de una celda a otra, cambia de turno.
        if 'piece' in tags and (origin_row != dest_row or origin_col != dest_col):
            self.next_player = next(self.players)
            self.current_player = self.next_player


    def _get_moves(self, origin_x:int, origin_y:int):
        """
        Devuelve los posibles movimientos que puede hacer una ficha dada su
        posición original dentro del tablero de juego.
        """
        row, col = self._get_pos(origin_x, origin_y)
        piece_type = self._get_selected_piece_type()
        player = self._get_selected_piece_owner()

        if piece_type:
            if piece_type == 'rook':
                return self._get_rook_moves(row, col)
            elif piece_type == 'knight':
                return self._get_knight_moves(row, col)
            elif piece_type == 'bishop':
                return self._get_bishop_moves(row, col)
            elif piece_type == 'queen':
                return self._get_queen_moves(row, col)
            elif piece_type == 'king':
                return self._get_king_moves(row, col)
            elif piece_type == 'pawn':
                return self._get_pawn_moves(row, col, player)
        return []


    def _get_bishop_moves(self, row:int, col:int):
        """
        Devuelve los movimientos posibles del alfíl.
        """
        moves = [(row, col)]
        player = self._get_selected_piece_owner()

        # Definimos las cuatro direcciones diagonales del alfíl.
        directions = [(-1, 1), (1, 1), (1, -1), (-1, -1)]

        for direction in directions:
            # Para cada dirección calculamos la siguiente celda.
            i, j = row + direction[0], col + direction[1]

            # Evaluamos que la celda esté dentro de los límites del tablero.
            while 0 <= i <= 7 and 0 <= j <= 7:
                if self.matrix[i][j][0] != 0:
                    if self.matrix[i][j][1] != player:
                        moves.append((i, j))
                    break

                # Añadimos la celda al listado de movimientos posibles.
                moves.append((i, j))

                # Calculamos la siguiente casilla.
                i, j = i + direction[0], j + direction[1]

        return moves


    def _get_rook_moves(self, row:int, col:int):
        """
        Devuelve los movimientos posibles de la torre.
        """
        moves = [(row, col)]
        player = self._get_selected_piece_owner()

        deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        for delta_row, delta_col in deltas:
            new_row = row + delta_row
            new_col = col + delta_col
            while 0 <= new_row <= 7 and 0 <= new_col <= 7:
                if self.matrix[new_row][new_col][0] != 0:
                    if self.matrix[new_row][new_col][1] != player:
                        moves.append((new_row, new_col))
                    break

                moves.append((new_row, new_col))
                new_row += delta_row
                new_col += delta_col

        return moves


    def _get_knight_moves(self, row:int, col:int):
        """
        Devuelve los movimientos posibles del caballo.
        """
        moves = [(row, col)]
        player = self._get_selected_piece_owner()

        deltas = [(-2, 1), (-1, 2), (1, 2), (2, 1),
                (2, -1), (1, -2), (-1, -2), (-2, -1)]

        for delta_row, delta_col in deltas:
            new_row = row + delta_row
            new_col = col + delta_col
            if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                if self.matrix[new_row][new_col][1] != player:
                    moves.append((new_row, new_col))

        return moves


    def _get_queen_moves(self, row:int, col:int):
        """
        Devuelve los movimientos posibles de la reina.
        """
        moves_set_1 = self._get_rook_moves(row, col)
        moves_set_2 = self._get_bishop_moves(row, col)
        moves = list(set(moves_set_1) | set(moves_set_2))
        return moves


    def _get_king_moves(self, row:int, col:int):
        """
        Devuelve los movimientos posibles del rey.
        """
        moves = [(row, col)]
        player = self._get_selected_piece_owner()

        deltas = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 1),
                (1, -1), (1, 0), (1, 1)]

        for delta_row, delta_col in deltas:
            new_row = row + delta_row
            new_col = col + delta_col
            if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                if self.matrix[new_row][new_col][1] != player:
                    moves.append((new_row, new_col))

        return moves


    def _get_pawn_moves(self, row:int, col:int, color:str):
        
        """
        Devuelve los movimientos posibles del peón.
        """

        # Se crean dos listas las cuales contienen las posiciones iniciales de los peones
        # para asi aplicar la logica de que cuando un peon esta en su posicion inicial este puede moverse hacia delante 
        # hasta dos casillas, pero cuando sale de la posicion inicial, estos solo pueden moverse una casilla hacia adelante.

        DEFAULT_PAWN_WHITE_POSITION = [(6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7)];
        DEFAULT_PAWN_BLACK_POSITION = [(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7)];

        moves = [(row, col)]
        player = self._get_selected_piece_owner()
        
        # Las blancas se mueven hacia arriba, las negras hacia abajo.
        direction = -1 if color == 'white' else 1

        #

        if (direction == -1):

            # Verificamos si la celda de al frente está dentro de los límites y vacía.
            new_row = row + direction
            if 0 <= new_row <= 7 and self.matrix[new_row][col][0] == 0:
                # Si la posicion inicial del peon blanco se encuentra en la lista de posiciones iniciales
                # Se permite que el peon pueda moverse dos casillas hacia adelante
                if (row,col) in DEFAULT_PAWN_WHITE_POSITION:
                    
                    moves.append((new_row, col))
                    moves.append((new_row-1, col))
                    
                else:
                    # De lo contrario se le permite solo moverse una casilla hacia adelante 
                    moves.append((new_row, col))
                
                
        else:
            # Verificamos si la celda de al frente está dentro de los límites y vacía.
            new_row = row + direction
            # Si la posicion inicial del peon blanco se encuentra en la lista de posiciones iniciales.
            # Se permite que el peon pueda moverse dos casillas hacia adelante.
            if 0 <= new_row <= 7 and self.matrix[new_row][col][0] == 0:
                
                if (row,col) in DEFAULT_PAWN_BLACK_POSITION:

                    moves.append((new_row, col))
                    moves.append((new_row+1, col))
                    
                    
                else:
                    # De lo contrario se le permite solo moverse una casilla hacia adelante.
                    moves.append((new_row, col))

        # Los peones pueden comer diagonal.
        capture_moves = [(new_row, col - 1), (new_row, col + 1)]
        for new_row, new_col in capture_moves:
            # Si la celda diagonal está dentro de los límites y está ocupada por una ficha enemiga.
            if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                if self.matrix[new_row][new_col][0] != 0 and self.matrix[new_row][new_col][1] != player:
                    moves.append((new_row, new_col))

        return moves


# ------------------------------------------------------------------------------
# ------------- MÉTODOS PARA CALCULAR POSICIONES DENTRO DEL TABLERO
# ------------------------------------------------------------------------------


    def _get_coords(self, row:int, col:int):
        """
        Devuelve las coordenadas en pixeles de la esquina superior izquierda (x1, y1) y
        la esquina inferior derecha (x2, y2) de una celda del tablero a partir de su
        posición dentro de la matriz.
        """
        x1, y1 = (col * self.SQUARE_SIZE + self.MARGIN, row * self.SQUARE_SIZE + self.MARGIN)
        x2, y2 = (x1 + self.SQUARE_SIZE, y1 + self.SQUARE_SIZE)

        return (x1, y1, x2, y2)


    def _get_center_coords(self, row:int, col:int):
        """
        Devuelve las coordenadas en pixeles (x, y) del centro de una celda del tablero.
        Esto es útil para ubicar las fichas del ajedrez correctamente.
        """
        centered_x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 + self.MARGIN
        centered_y = row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 + self.MARGIN

        return (centered_x, centered_y)


    def _get_pos(self, x:float, y:float):
        """
        Devuelve la posición (i, j) dentro de la matriz a partir de la
        coordenada de la esquina superior izquierda de una celda del tablero.
        """
        row = int((y - self.MARGIN) // self.SQUARE_SIZE)
        col = int((x - self.MARGIN) // self.SQUARE_SIZE)

        return (row, col)


# ------------------------------------------------------------------------------
# -------------------------- OTROS MÉTODOS AUXILIARES
# ------------------------------------------------------------------------------


    def _get_cell_name(self, row, col):
        """
        Devuelve el nombre de la celda basado en el número de fila y columna.
        """
        # La letra a corresponde al 97 en código ASCII.
        # A ese valor le sumamos el número de columna y lo convertimos a letra.
        col_letter = chr(ord('a') + col)

        # La fila de la parte superior es la #8.
        row_num = self.SIZE - row

        cell_name = f'{col_letter}{row_num}'

        return cell_name


    def _is_within_board(self, x:float, y:float):
        """
        Verifica si las coordenadas x e y están dentro de los límites del tablero.
        """
        space = 15

        left = self.MARGIN + space
        right = self.MARGIN + self.BOARD_SIZE - self.SQUARE_SIZE - space
        top = self.MARGIN + space
        bottom = self.MARGIN + self.BOARD_SIZE - self.SQUARE_SIZE - space

        if x >= left and x < right and y >= top and y < bottom:
            return True
        else:
            return False


    def _is_empty(self, row:int, col:int):
        """
        Verifica si una celda del tablero está vacía o no.
        """
        # Inicializamos un contador y obtenemos las coordenadas de la celda.
        piece_count = 0
        x1, y1, x2, y2 = self._get_coords(row, col)

        # Obtenemos el elemento actualmente seleccionado.
        player = self._get_selected_piece_owner()

        # Obtenemos todos los elementos dentro de la celda definida por la coordenada.
        items = self.canvas.find_enclosed(x1, y1, x2, y2)

        # Contamos el número de fichas que hay en esa celda.
        for item in items:
            tags = self.canvas.gettags(item)

            # Solo cuenta fichas del mismo color para permitir que una ficha pueda comerse al enemigo.
            if ('piece' in tags and 'current' not in tags and
               ('black' in tags and player == 'black' or 'white' in tags and player == 'white')):
                piece_count += 1

        if piece_count > 0:
            return False
        return True


    def _print_matrix(self):
        """
        Imprime la matriz de 8x8 que representa al tablero de juego.
        """
        print()
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                # Imprimimos solo el puntaje de cada ficha.
                if self.matrix[row][col][1] == 'white':
                    color = 'w'
                elif self.matrix[row][col][1] == 'black':
                    color = 'b'

                if self.matrix[row][col][0] == 0:
                    print('    ', end='')
                else:
                    print(f'{self.matrix[row][col][0]:3d}', end='')
                    print(f'{color}', end='')
            print()
        print()


    def _get_piece_type(self, row:int, col:int):
        """
        Devuelve el tipo de ficha de una casilla dada.
        """
        # Obtenemos las coordenadas de la casilla.
        x1, y1, x2, y2 = self._get_coords(row, col)

        # Obtenemos todos los elementos dentro de la celda definida por la coordenada.
        items = self.canvas.find_enclosed(x1, y1, x2, y2)

        # Buscamos el elemento con la etiqueta 'piece'.
        for item in items:
            tags = self.canvas.gettags(item)

            if 'piece' in tags:
                if 'rook' in tags: return 'rook'
                elif 'knight' in tags: return 'knight'
                elif 'bishop' in tags: return 'bishop'
                elif 'queen' in tags: return 'queen'
                elif 'king' in tags: return 'king'
                elif 'pawn' in tags: return 'pawn'


    def _get_selected_piece_type(self):
        """
        Devuelve el tipo de ficha de una casilla dada.
        """
        if self.selected_piece:
            item = self.selected_piece
            tags = self.canvas.gettags(item)

            if 'rook' in tags: return 'rook'
            elif 'knight' in tags: return 'knight'
            elif 'bishop' in tags: return 'bishop'
            elif 'queen' in tags: return 'queen'
            elif 'king' in tags: return 'king'
            elif 'pawn' in tags: return 'pawn'


    def _get_piece_owner(self, row:int, col:int):
        """
        Devuelve el dueño (jugador blanco o negro) de la ficha.
        """
        # Obtenemos las coordenadas de la casilla.
        x1, y1, x2, y2 = self._get_coords(row, col)

        # Obtenemos todos los elementos dentro de la celda definida por la coordenada.
        items = self.canvas.find_enclosed(x1, y1, x2, y2)

        # Buscamos el elemento con la etiqueta 'piece'.
        for item in items:
            tags = self.canvas.gettags(item)

            if 'piece' in tags:
                if 'white' in tags: return 'white'
                elif 'black' in tags: return 'black'


    def _get_selected_piece_owner(self):
        """
        Devuelve el tipo de la ficha seleccionada.
        """
        if self.selected_piece:
            item = self.selected_piece
            tags = self.canvas.gettags(item)

            if 'white' in tags: return 'white'
            elif 'black' in tags: return 'black'


    def _get_score(self, row:int, col:int):
        """
        Devuelve el puntaje de la ficha de una celda dada.
        """
        # Obtenemos las coordenadas de la casilla.
        x1, y1, x2, y2 = self._get_coords(row, col)

        # Obtenemos todos los elementos dentro de la celda definida por la coordenada.
        items = self.canvas.find_enclosed(x1, y1, x2, y2)

        # Buscamos el elemento con la etiqueta 'piece'.
        for item in items:
            tags = self.canvas.gettags(item)

            if 'piece' in tags:
                if 'rook' in tags: return self.piece_score['rook']
                elif 'knight' in tags: return self.piece_score['knight']
                elif 'bishop' in tags: return self.piece_score['bishop']
                elif 'queen' in tags: return self.piece_score['queen']
                elif 'king' in tags: return self.piece_score['king']
                elif 'pawn' in tags: return self.piece_score['pawn']


    def _get_selected_piece_score(self):
        """
        Devuelve el puntaje de la ficha seleccionada.
        """
        if self.selected_piece:
            item = self.selected_piece
            tags = self.canvas.gettags(item)

            if 'rook' in tags: return self.piece_score['rook']
            elif 'knight' in tags: return self.piece_score['knight']
            elif 'bishop' in tags: return self.piece_score['bishop']
            elif 'queen' in tags: return self.piece_score['queen']
            elif 'king' in tags: return self.piece_score['king']
            elif 'pawn' in tags: return self.piece_score['pawn']


    def _get_piece_score(self, item):
        """
        Devuelve el puntaje de un elemento del canvas siempre y cuando
        tenga la etiqueta 'piece'.
        """
        tags = self.canvas.gettags(item)

        if 'piece' in tags:
            if 'rook' in tags: return self.piece_score['rook']
            elif 'knight' in tags: return self.piece_score['knight']
            elif 'bishop' in tags: return self.piece_score['bishop']
            elif 'queen' in tags: return self.piece_score['queen']
            elif 'king' in tags: return self.piece_score['king']
            elif 'pawn' in tags: return self.piece_score['pawn']

        return 0


    def _eat(self, row:int, col:int):
        """
        Devuelve el ID de la ficha comida y su puntaje. En otro caso, None.
        """
        # Obtenemos las coordenadas de la casilla.
        x1, y1, x2, y2 = self._get_coords(row, col)

        # Obtenemos todos los elementos dentro de la celda definida por la coordenada.
        items = self.canvas.find_enclosed(x1, y1, x2, y2)

        # Buscamos el elemento con la etiqueta 'piece'.
        for item in items:
            tags = self.canvas.gettags(item)

            # Si hay una ficha que no es la seleccionada.
            if 'piece' in tags and 'current' not in tags:
                return (item, self._get_piece_score(item))


    def _print_data(self, row:int, col:int):
        """
        Imprime datos de la jugada realizada.
        """
        # Obtenemos la posición inicial.
        origin_row, origin_col = self._get_pos(self.origin_x, self.origin_y)

        if origin_row != row or origin_col != col:
            # Obtenemos la ficha que realizó el movimiento.
            piece = self._get_selected_piece_type()

            # Obtenemos el jugador que realizó el movimiento.
            player = self._get_selected_piece_owner()

            # Obtiene el puntaje de la ficha que comió (si es que lo hizo).
            has_eaten = self._eat(row, col)

            print('_________________________________________________')
            print(f'\n  {player} | {piece} ({origin_row},{origin_col}) => ({row},{col}).', end=' ')

            if has_eaten:
                if has_eaten[1] == 1:
                    print('Se comió un peón.', end=' ')
                elif has_eaten[1] == 3:
                    tags = self.canvas.gettags(has_eaten[0])
                    if 'bishop' in tags:
                        print('Se comió un alfíl.', end=' ')
                    elif 'knight' in tags:
                        print('Se comió un caballo.', end=' ')
                elif has_eaten[1] == 5:
                    print('Se comió una torre.', end=' ')
                elif has_eaten[1] == 9:
                    print('Se comió la reina.', end=' ')
                elif has_eaten[1] == 10:
                    print('Se comió al rey.', end=' ')

            self._print_matrix()


    def run(self):
        """
        Ejecuta la interfaz gráfica.
        """
        self.window.mainloop()


# ------------------------------------------------------------------------------
# ------------------------ EJECUCIÓN DE LA APLICACIÓN
# ------------------------------------------------------------------------------


if __name__ == '__main__':
    # Run the app.
    app = Board()
    app.run()