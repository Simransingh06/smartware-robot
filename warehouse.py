import numpy as np

class WarehouseGrid:
    """
    Creates and manages the warehouse grid environment
    - Generates random obstacles (shelves, boxes, etc.)
    - Validates positions for start/exit points
    - Provides grid state management
    """
    
    def __init__(self, size=10, obstacle_density=0.20):
        """
        Initialize warehouse grid
        
        Parameters:
        - size: Grid dimensions (size x size)
        - obstacle_density: Percentage of cells that are obstacles (0.0 to 1.0)
        """
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)  #grid with zeros generation
        self.obstacle_density = obstacle_density
        self._generate_obstacles()
        self.grid[0, 0] = 0
        self.grid[self.size - 1, self.size - 1] = 0

    
    def _generate_obstacles(self):
        """
        Randomly place obstacles in the warehouse
        Creates clusters to simulate realistic warehouse layout (shelving units)
        """
        num_obstacles = int(self.size * self.size * self.obstacle_density)
        placed = 0
        
        while placed < num_obstacles:
            x = np.random.randint(0, self.size)
            y = np.random.randint(0, self.size)
            
            if self.grid[x, y] == 0:  
                self.grid[x, y] = 1
                placed += 1           #obstacle generation
                
                # Add neighboring obstacles to create clusters (realistic shelving)
                if placed < num_obstacles and np.random.random() > 0.5:
                    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                    for nx, ny in neighbors:
                        if (0 <= nx < self.size and 0 <= ny < self.size and 
                            self.grid[nx, ny] == 0 and placed < num_obstacles):
                            if np.random.random() > 0.5:
                                self.grid[nx, ny] = 1
                                placed += 1
    
    def is_valid_position(self, x, y):
        """robot doesnt move outside of grid"""
        return (0 <= x < self.size and 0 <= y < self.size and self.grid[x, y] == 0)
    
    def clear_position(self, x, y):
        """Ensure a specific position is free (for start/exit)"""
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[x, y] = 0
    
    def get_grid_info(self):
        """Return grid statistics"""
        total_cells = self.size * self.size
        obstacle_count = np.sum(self.grid == 1)
        free_count = total_cells - obstacle_count
        
        return {
            'size': self.size,
            'total_cells': total_cells,
            'obstacles': obstacle_count,
            'free_cells': free_count,
            'obstacle_percentage': (obstacle_count / total_cells) * 100
        }