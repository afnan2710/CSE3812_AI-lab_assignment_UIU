# Python program for A* Search Algorithm
import math
import heapq


# Function for reading the source and destination coordinates.
# It is called from inside the main() function.

def read_src_dest_from_file(input_file):
    try:
        # Reading the content of the input file
        with open(input_file, 'r') as infile:
            lines = infile.readlines()
            src = eval(lines[0].strip())
            dest = eval(lines[1].strip())
        print(f"\nSource: {src}, Destination: {dest}")
        return src, dest

    except FileNotFoundError:
        print(f"\nThe file {input_file} does not exist.")
        return None, None

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        return None, None


# Define the Cell class

class Cell:
    def __init__(self):
        # Parent cell's row index
        self.parent_i = 0
        # Parent cell's column index
        self.parent_j = 0
        # Total cost of the cell (g + h)
        self.f = float('inf')
        # Cost from start to this cell
        self.g = float('inf')
        # Heuristic cost from this cell to destination
        self.h = 0


# Define the size of the grid
ROW = 9
COL = 10

# Check if a cell is valid (within the grid)


def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# Check if a cell is unblocked


def is_unblocked(grid, row, col):
    return grid[row][col] == 1

# Check if a cell is the destination


def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]


# Calculate the heuristic value of a cell 

def calculate_h_value(row, col, dest):
    """Calculates the heuristic value of a cell (Euclidean distance to destination) and returns it"""
    distance = math.sqrt((row - dest[0])**2 + (col - dest[1])**2)
    return distance


# Trace the path from source to destination

def trace_path(cell_details, dest):
    """Traces the path from destination to source using parent cells"""
    row = dest[0]
    col = dest[1]
    path = []

    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col

    path.append((row, col))
    path.reverse()  # Reverse the path to get it from source to destination
    return path


# Implement the A* search algorithm

def a_star_search(grid, src, dest):
    # Check if the source and destination are valid
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        print("\nSource or destination is invalid")
        return []

    # Check if the source and destination are unblocked
    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("\nSource or the destination is blocked")
        return []

    # Check if we are already at the destination
    if is_destination(src[0], src[1], dest):
        print("\nWe are already at the destination")
        return [src]

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    # Initialize the start cell details
    i = src[0]
    j = src[1]
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Initialize the flag for whether destination is found
    found_dest = False

    # Main loop of A* search algorithm
    while open_list:
        # Get the cell with the minimum f value
        current = heapq.heappop(open_list)
        i, j = current[1], current[2]
        closed_list[i][j] = True
        print(f"Checking cell: ({i}, {j})")

        # Check all 8 possible movements from the current cell
        for new_i, new_j in [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1), (i + 1, j - 1),
                             (i + 1, j), (i + 1, j + 1)]:
            if is_valid(new_i, new_j):
                if is_destination(new_i, new_j, dest):
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    found_dest = True
                    print("\nDestination found!")
                    return trace_path(cell_details, dest)

                elif not closed_list[new_i][new_j] and is_unblocked(grid, new_i, new_j):
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new

                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

    # If the destination is not found after visiting all cells
    if not found_dest:
        print("Failed to find the destination cell")


# Driver Code

def main():
    # Define the grid (1 for unblocked, 0 for blocked)
    grid = [
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 0, 0, 1]
    ]

    # Paths to read from an input file
    input_file = ("C:/Users/Afnan Shahriar/OneDrive/Desktop/python_practice/AStar_assignment_011213001/"
                  "Sample IO/io2/in.txt")

    # Read from input file and store variables
    src, dest = read_src_dest_from_file(input_file)

    # Run the A* search algorithm
    if src and dest:
        path = a_star_search(grid, src, dest)
        if path:
            questioned_path = " -> ".join([f"({r}, {c})" for r, c in path])
            print(f"\nBest Path is: "+questioned_path)
        else:
            print("\nNo path found")


if __name__ == "__main__":
    main()
