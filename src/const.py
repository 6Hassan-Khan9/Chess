from enum import Enum

class Dims(Enum):
    COL = 0
    ROW = 1

# Screen dimensions
WIDTH = 600
HEIGHT = 600

# Board dimensions
ROWS = 8
COLS = 8
SQSIZE = WIDTH // COLS