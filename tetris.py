
import pygame, sys, random
pygame.init()

# -------------------------
# BASIC SETTINGS
# -------------------------
# Our Tetris playground is a grid! Let's set it up.
COLS, ROWS = 10, 20     # 10 blocks wide, 20 blocks tall
CELL = 30               # each block is 30 pixels
GRID_W, GRID_H = COLS * CELL, ROWS * CELL
SIDE = 180              # a sidebar to show score and next piece
W, H = GRID_W + SIDE, GRID_H

screen = pygame.display.set_mode((W, H))
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# Colors to paint with!
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
LIGHT_GRAY = (90, 90, 90)

# Tetromino shapes (the puzzle pieces!)
# Each shape has 4 rotations. Each rotation is a list of (x, y) squares.
SHAPES = {
    'I': [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(1, 0), (1, 1), (1, 2), (1, 3)],
    ],
    'O': [
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
    ],
    'T': [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    'S': [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
        [(1, 1), (2, 1), (0, 2), (1, 2)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
    ],
    'Z': [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 2), (2, 2)],
        [(1, 0), (0, 1), (1, 1), (0, 2)],
    ],
    'J': [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    'L': [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
}

COLORS = {
    'I': (0, 240, 240),
    'O': (240, 240, 0),
    'T': (160, 0, 240),
    'S': (0, 240, 0),
    'Z': (240, 0, 0),
    'J': (0, 0, 240),
    'L': (240, 160, 0),
}

# Game state
grid = None          # This will be a ROWS x COLS list of colors or None
current = None       # The piece that is falling right now
next_shape = None    # The next piece (we show it in the sidebar!)
fall_timer_ms = 0    # Time counter for automatic falling
fall_delay_ms = 700  # How fast pieces fall (smaller = faster)
score = 0
lines_cleared_total = 0
game_over = False
game_started = False


class Piece:
    def __init__(self, name: str, rotations: int, xs: int, ys : int):
        self.name = name
        self.rotation = rotations
        self.x = xs     # start near middle
        self.y = ys    # start just above the top (slides in)
        self.color = COLORS[name]
    @property
    def cells(self):
        variant = SHAPES[self.name][self.rotation % 4]
        return [(self.x + cx, self.y + cy) for (cx, cy) in variant]
    
    # @property
    def x(self):
        return self.x
    
    # @property
    def y(self):
        return self.y
    
    # @property
    def rotation(self):
        return self.rotation

    # @property
    def change_x(self, new_x):
        self.x = new_x

    # @property
    def change_y(self, new_y):
        self.y = new_y
    
    # @property
    def change_rotation(self,new_r):
        self.rotation = new_r





# -------------------------
# HELPER FUNCTIONS
# -------------------------

def make_piece(name,rot=0,x=2,y=-2):
    piece = Piece(name,rot,x,y)
    return piece

def make_empty_grid():
    """Create a blank grid (all None)."""
    # TODO: Return a list with ROWS rows and COLS columns, all values None
    # HINT: Use a list comprehension like [[None for _ in range(COLS)] for _ in range(ROWS)]
    COLS = []
    ROWS = []


def can_place(cell):
    """Check if given cells can be placed on the grid (not out of bounds or colliding)."""
    # TODO: For each (x, y):
    # 1) If y < 0, allow it (spawning above grid is okay), just continue
    # 2) If x is outside 0..COLS-1 or y >= ROWS -> return False
    # 3) If the grid cell is not None -> return False
    # If all cells are okay, return True

    cellx = cell.x
    celly = cell.y
    if celly < 0:
        if cellx > COLS-1 or celly >= ROWS:
            return False
        if grid is not None:
               return False                

            
        




def spawn_piece():
    """Create a new current piece. If it can't be placed, game over!"""
    global current, next_shape, game_over, game_started
    # TODO:
    if next_shape is None:
        next_shape = random.choice(list(SHAPES.keys()))
    current = make_piece(next_shape)
    next_shape = random.choice(list(SHAPES.keys()))
    game_started = True
    if can_place(current) is False: game_over = True
    # - Choose the shape name: if next_shape exists, use it; otherwise pick random from SHAPES keys
    # - Create the Piece and assign to current
    # - Choose a new next_shape randomly
    # - Set game_started = True
    # - If can_place(current.cells) is False -> set game_over = True
    


def end_game():
    """End the game."""
    global game_over
    game_over = True


def lock_current_and_clear():
    """Stick the current piece into the grid and clear any full lines."""
    global grid, score, lines_cleared_total
    # TODO:
    # 1) For each (x, y) in current.cells: if 0 <= y < ROWS, set grid[y][x] = current.color
    # 2) Make a new list of rows that are NOT completely full
    #    HINT: a row is full if every cell is not None -> all(cell is not None for cell in row)
    # 3) Count how many rows you removed (cleared)
    # 4) Add that many empty rows to the TOP
    # 5) Update score using simple rule: [0, 100, 300, 500, 800][cleared]
    # 6) Increase lines_cleared_total by cleared
    if current:
        x = current.x
        y = current.y
        if 0 <= y < ROWS:
            grid[y][x] = current.color
            


def try_move(dx: int, dy: int):
    """Try to move the current piece by (dx, dy). Return True if success."""
    # TODO:
    # - Save old x,y
    # - Change x,y by dx,dy
    # - If can_place fails, restore old x,y and return False
    # - Otherwise return True
    oldx = current.x
    oldy = current.y
    current.change_x(oldx + dx)
    current.change_y(oldy + dy)
    if can_place(current) is False:
        current.change_x(oldx)
        current.change_y(oldy)
        return False
    return True


def try_rotate():
    """Try to rotate the current piece. Use tiny wall-kicks (nudge left/right) if needed."""
    # TODO:
    # - Save old rotation
    # - Rotate +1 (mod 4)
    # - If can_place ok -> return True
    # - Else try nudges: -1, +1, -2, +2 on x. If any works -> return True
    # - If none work -> restore rotation and return False
    oldro = current.rotation
    current.change_rotation(+1)
    if can_place(current): return True
    current.change_rotation(+2)
    if can_place(current): return True
    current.change_rotation(-1)
    if can_place(current): return True
    current.change_rotation(-2)
    if can_place(current): return True
    current.change_rotation(oldro)
    return False


def hard_drop():
    """Drop the piece all the way down!"""
    # TODO: while try_move(0, 1) succeeds, keep going
    while try_move(0, 1) == True:
        try_move(0,1)


def reset_game():
    """Start a brand new game!"""
    global grid, current, next_shape, fall_timer_ms, fall_delay_ms
    global score, lines_cleared_total, game_over, game_started
    # TODO: Set everything back to the beginning values
    # HINTS:
    # - grid should be a new empty grid from make_empty_grid()
    # - current and next_shape are None at the start
    # - fall_timer_ms = 0, fall_delay_ms = 700
    # - score = 0, lines_cleared_total = 0
    # - game_over = False, game_started = False
    # - finally, call spawn_piece()
    make_empty_grid()
    current = None
    next_shape = None
    fall_delay_ms = 700
    fall_timer_ms = 0
    score = 0
    lines_cleared_total = 0
    game_over = False
    game_started = False
    spawn_piece()



def update_fall(dt_ms: int):
    """Make the piece fall over time. Tiny difficulty: speed up every 5 cleared lines!"""
    global fall_timer_ms, fall_delay_ms
    if game_over or not game_started:
        return
    # TODO:
    # 1) Compute speedups = lines_cleared_total // 5
    # 2) Set fall_delay_ms = max(180, 700 - speedups * 60)
    # 3) Add dt_ms to fall_timer_ms
    # 4) If fall_timer_ms >= fall_delay_ms:
    #    - reset timer to 0
    #    - if try_move(0, 1) fails -> lock_current_and_clear(); if game not over -> spawn_piece()
    speed_ups = lines_cleared_total // 5
    fall_delay_ms = max(180,700 - speed_ups * 60)
    fall_timer_ms += dt_ms
    if fall_timer_ms >= fall_delay_ms:
        fall_timer_ms = 0
        if try_move(0,1) is False:
            lock_current_and_clear()
            if game_over is False:
                spawn_piece()

def handle_key(key):
    """Handle keyboard presses!"""
    # Controls:
    # LEFT/RIGHT: move piece
    # DOWN: soft drop (move down 1)
    # UP: rotate
    # SPACE: hard drop (fall all the way)
    # R: restart when game over
    global game_over
    # TODO:
    # - If game_over and key == pygame.K_r: call reset_game() and return
    # - If key is LEFT/RIGHT/DOWN -> try_move appropriately
    # - If key is UP -> try_rotate()
    # - If key is SPACE -> hard_drop(); then lock_current_and_clear(); if not over -> spawn_piece()
    if game_over and key == pygame.K_r:
        reset_game()
        return
    if key == pygame.K_LEFT: try_move(-1,0)
    elif key == pygame.K_RIGHT: try_move(1,0)
    elif key == pygame.K_UP: try_rotate()
    elif key == pygame.K_DOWN: try_move(0,1)
    elif key == pygame.K_SPACE: hard_drop()


def draw_grid_background():
    """Draw the playfield background and grid lines."""
    # TODO:
    # - Draw a LIGHT_GRAY rectangle for the playfield (0,0,GRID_W,GRID_H)
    # - Draw thin grid lines using pygame.draw.line with GRAY color
    pygame.draw.rect(
        screen,
        LIGHT_GRAY,
        (0,0,GRID_W,GRID_H),
    )
    # pygame.draw.line()



def draw_locked_blocks():
    """Draw all the blocks that are already locked in the grid."""
    # TODO: For each grid cell that is not None, draw a small rectangle of that color


def draw_piece(piece):
    """Draw the current falling piece."""
    # TODO: For each (x, y) in piece.cells, draw a rectangle of piece.color (skip y < 0)
    pass


def draw_sidebar():
    """Draw the side panel with score, lines, speed, and next piece preview."""
    # TODO:
    # - Draw a dark rectangle for the sidebar (start at x = GRID_W)
    # - Show title "Tetris", score, lines, and speed number
    # - Show "Next:" and draw a small preview of the next piece (rotation 0)
    # - If game_over, show "Game Over" and "Press R to Restart"
    # pygame.draw.re
    #     screen,
    #     BLACK,
    #     (GRID_W,0)
    #         )
    # game_font = pygame.font.SysFont("Arial", 24)
    # text = game_font.render("Moikka!", True, (255, 0, 0))
    #display.blit(text, (100, 50))
    text = font.render("TETRIS", True,(255, 255, 255))
    screen.blit(text,(GRID_W,0))

def draw_all():
    """Draw everything and flip the screen!"""
    # TODO: Fill screen BLACK, draw grid, locked blocks, current piece, sidebar, then pygame.display.flip()
    screen.fill(BLACK)
    draw_grid_background()
    draw_locked_blocks()
    draw_piece(current)
    draw_sidebar()
    pygame.display.flip()


# -------------------------
# MAIN GAME LOOP
# -------------------------
reset_game()
while True:
    dt = clock.tick(60)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if ev.type == pygame.KEYDOWN:
            handle_key(ev.key)

    # Make the piece fall and draw the world!
    update_fall(dt)
    draw_all()
