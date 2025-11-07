import matplotlib.pyplot as plt  # noqa: F401
import matplotlib.patches as patches  # noqa: F401
from matplotlib.animation import FuncAnimation  # noqa: F401
import numpy as np  # noqa: F401

class WarehouseVisualizer:
    """
    Creates beautiful, animated visualization of robot movement
    - Shows grid with obstacles
    - Highlights start (green), exit (red), path (blue)
    - Animates robot movement step-by-step
    """
    def __init__(self, warehouse, path, start, goal):
        """
        Initialize visualizer
        Parameters:
        - warehouse: WarehouseGrid object
        - path: List of (x, y) coordinates
        - start: Starting position tuple
        - goal: Goal position tuple
        """
        self.warehouse = warehouse
        self.path = path
        self.start = start
        self.goal = goal
        self.size = warehouse.size
    
    def _draw_grid(self, ax):
        """Draw the warehouse grid with obstacles"""
        for i in range(self.size):
            for j in range(self.size):
                if self.warehouse.grid[i][j] == 1:
                    # Obstacle
                    rect = patches.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                            linewidth=1, edgecolor='black',
                                            facecolor='#424242', zorder=1)
                    ax.add_patch(rect)
                else:
                    # Empty space
                    rect = patches.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                            linewidth=0.5, edgecolor='lightgray',
                                            facecolor='white', zorder=0)
                    ax.add_patch(rect)
    
    def _draw_markers(self, ax):
        """Draw start and goal markers"""
        # Start marker (green)
        start_marker = plt.Circle((self.start[1], self.start[0]), 0.35,
                                 color='#4CAF50', zorder=3, linewidth=2,
                                 edgecolor='white', label='Start')
        ax.add_patch(start_marker)
        
        # Goal marker (red)
        goal_marker = plt.Circle((self.goal[1], self.goal[0]), 0.35,
                                color='#F44336', zorder=3, linewidth=2,
                                edgecolor='white', label='Exit')
        ax.add_patch(goal_marker)
    
    def create_static_visualization(self):
        """
        single frame showing complete path
        Useful for quick visualization
        """
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Draw grid
        self._draw_grid(ax)
        
        # Draw complete path
        if self.path:
            path_array = np.array(self.path)
            ax.plot(path_array[:, 1], path_array[:, 0], 'b-', 
                   linewidth=4, alpha=0.6, label='Robot Path', zorder=2)
        
        # Draw start and goal
        self._draw_markers(ax)
        
        # Styling
        ax.set_title('🤖 Smart Warehouse Robot - Complete Path', 
                    fontsize=18, fontweight='bold', pad=20)
        ax.legend(loc='upper right', fontsize=12, framealpha=0.9)
        ax.set_xlim(-0.5, self.size - 0.5)
        ax.set_ylim(-0.5, self.size - 0.5)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        
        # Add grid lines
        ax.set_xticks(np.arange(-0.5, self.size, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, self.size, 1), minor=True)
        ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
        ax.tick_params(which='minor', size=0)
        
        plt.tight_layout()
        plt.show()
    
    def create_animation(self, interval=200, save_path=None):
        
        if not self.path:
            print("No path to animate!")
            return
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Draw static elements
        self._draw_grid(ax)
        self._draw_markers(ax)
        
        # Initialize robot (blue circle)
        robot = plt.Circle((self.start[1], self.start[0]), 0.3, 
                          color='#2196F3', zorder=5, linewidth=3, 
                          edgecolor='white', label='Robot')
        ax.add_patch(robot)
        
        # Initialize path line
        path_line, = ax.plot([], [], 'b-', linewidth=4, alpha=0.6, 
                            label='Path Traveled', zorder=2)
        
        # Status text
        status_text = ax.text(0.02, 0.98, '', transform=ax.transAxes,
                             fontsize=14, verticalalignment='top',
                             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9),
                             zorder=10)
        
        # Styling
        ax.set_title('🤖 Smart Warehouse Robot - Live Navigation', 
                    fontsize=18, fontweight='bold', pad=20)
        ax.legend(loc='upper right', fontsize=12, framealpha=0.9)
        ax.set_xlim(-0.5, self.size - 0.5)
        ax.set_ylim(-0.5, self.size - 0.5)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        
        # Grid lines
        ax.set_xticks(np.arange(-0.5, self.size, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, self.size, 1), minor=True)
        ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
        ax.tick_params(which='minor', size=0)
        
        def init():
            """Initialize animation"""
            robot.center = (self.start[1], self.start[0])
            path_line.set_data([], [])
            status_text.set_text('Step 0 of {}'.format(len(self.path)))
            return robot, path_line, status_text
        
        def animate(frame):
            """Update animation for each frame"""
            if frame < len(self.path):
                # Update robot position
                y, x = self.path[frame]
                robot.center = (x, y)
                
                # Update path line
                path_so_far = np.array(self.path[:frame + 1])
                path_line.set_data(path_so_far[:, 1], path_so_far[:, 0])
                
                # Update status text
                status_text.set_text(
                    f'Step {frame + 1} of {len(self.path)}\n'
                    f'Position: ({y}, {x})'
                )
                
                # Change robot color when reaching goal
                if frame == len(self.path) - 1:
                    robot.set_color('#4CAF50')  # Green when complete
                    status_text.set_text(
                        f'✓ Reached Exit!\n'
                        f'Total Steps: {len(self.path)}'
                    )
            
            return robot, path_line, status_text
        
        # Create animation
        anim = FuncAnimation(fig, animate, init_func=init,
                           frames=len(self.path), interval=interval,
                           blit=True, repeat=True, repeat_delay=1000)
        
        # Save if path provided
        if save_path:
            try:
                anim.save(save_path, writer='pillow', fps=1000//interval)
                print(f"Animation saved to {save_path}")
            except Exception as e:
                print(f"Could not save animation: {e}")
        
        plt.tight_layout()
        plt.show()
        
        return anim


if __name__ == "__main__":
    # Example usage - this code runs only when file is executed directly
    
    
    print("WarehouseVisualizer class loaded successfully!")
    print("To use: from warehouse_visualizer import WarehouseVisualizer")
    
    