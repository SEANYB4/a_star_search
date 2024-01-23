import heapq


class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0 # Cost from start to node
        self.h = 0 # Heuristic cost from node to end
        self.f = 0 # Total cost


    def __eq__(self, other):
        return self.position == other.position
    

    def __lt__(self, other):
        return self.f < other.f
    


def a_star_search(start, end, grid):

    # Create start and end node
    start_node = Node(start)
    end_node = Node(end)

    # Initialize both open and closed list
    open_list = []
    closed_list = set()
    g_costs = {}


    # Heapify the open_list and add the start node
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)


    # Adding a stop condition
    
    outer_iterations = 0
    max_iterations = len(grid) * len(grid[0])


    # Loop until you find the end

    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
            # If we've exceeded the max number of iterations, return a failure.
            return None
        
        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node.position)


        # DEBUG
        print(current_node.position)
        


        # Found the goal
        if current_node.position == end_node.position:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path
        

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (len(grid[len(grid)-1])-1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if grid[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(node_position, current_node)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Check if child is on the closed list
            if child.position in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
            child.f = child.g + child.h

            # Check if child is already in the open list and has a higher g value
           
            if child.position in g_costs and g_costs[child.position] <= child.g:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)
            g_costs[child.position] = child.g

    return None



def main():
    # Create a 2D grid (0 = walkable, 1 = obstacle)
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0]
    ]

    start = (0, 0) # Starting position
    end= (4, 4) # Ending position

    print("Starting search from {} to {} on the following grid:".format(start, end))
    for row in grid:
        print(row)

    path = a_star_search(start, end, grid)
    if path:
        print("Path found:", path)
    else:
        print("No path found")


if __name__ == '__main__':
    main()

        