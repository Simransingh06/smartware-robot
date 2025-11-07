import heapq

class AStarPathfinder:
    """
    Implements A* algorithm for finding optimal path
    
    A* = Dijkstra + Heuristic
    - Uses Manhattan distance as heuristic (city-block distance)
    - Guarantees shortest path if heuristic is admissible
    - More efficient than Dijkstra for grid-based pathfinding
    """
    
    def __init__(self, grid):
        """
        Initialize pathfinder with warehouse grid
        
        Parameters:
        - grid: WarehouseGrid object
        """
        self.grid = grid
        self.size = grid.size
    
    def heuristic(self, pos1, pos2):
        """
        Manhattan distance heuristic (L1 distance)
        Estimates remaining cost to reach goal
        
        Formula: |x1 - x2| + |y1 - y2|
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def get_neighbors(self, pos):
        """
        Get valid neighboring cells (up, down, left, right)
        Diagonal movement disabled for realistic warehouse robot movement
        """
        x, y = pos
        neighbors = []
        
        # Four directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if self.grid.is_valid_position(new_x, new_y):
                neighbors.append((new_x, new_y))
        
        return neighbors
    
    def find_path(self, start, goal):
        """
        A* Algorithm Implementation
        
        Returns: List of (x, y) coordinates from start to goal
                 Empty list if no path exists
        
        Algorithm steps:
        1. Start with initial position in priority queue
        2. Pop position with lowest f_score (g_score + heuristic)
        3. Explore neighbors, update costs
        4. Continue until goal is reached
        5. Reconstruct path by backtracking
        """
        
        # Priority queue: (f_score, counter, position)
        # counter prevents comparison errors when f_scores are equal
        counter = 0
        frontier = [(0, counter, start)]
        
        # Track where we came from for path reconstruction
        came_from = {}
        
        # Cost from start to current position
        g_score = {start: 0}
        
        # Estimated total cost (g_score + heuristic)
        f_score = {start: self.heuristic(start, goal)}
        
        # Set of positions in frontier (for fast lookup)
        in_frontier = {start}
        
        while frontier:
            # Get position with lowest f_score
            _, _, current = heapq.heappop(frontier)
            in_frontier.discard(current)
            
            # Goal reached! Reconstruct path
            if current == goal:
                return self._reconstruct_path(came_from, current)
            
            # Explore neighbors
            for neighbor in self.get_neighbors(current):
                # Calculate tentative g_score
                tentative_g = g_score[current] + 1  # Cost = 1 per move
                
                # If this path to neighbor is better than previous
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    # Update path information
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, goal)
                    
                    # Add to frontier if not already there
                    if neighbor not in in_frontier:
                        counter += 1
                        heapq.heappush(frontier, (f_score[neighbor], counter, neighbor))
                        in_frontier.add(neighbor)
        
        # No path found
        return []
    
    def _reconstruct_path(self, came_from, current):
        """
        Backtrack from goal to start using came_from dictionary
        Returns path as list of coordinates
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path