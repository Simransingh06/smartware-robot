from warehouse import WarehouseGrid
from pathfinder import AStarPathfinder
from visualizer import WarehouseVisualizer

def get_user_input(warehouse):
    """
    Get and validate user input for start and exit coordinates
    
    Parameters:
    - warehouse: WarehouseGrid object
    
    Returns:
    - start: Tuple (x, y)
    - goal: Tuple (x, y)
    """
    print("\n" + "="*70)
    print("  📍 COORDINATE INPUT")
    print("="*70)
    print(f"Grid size: {warehouse.size}x{warehouse.size}")
    print(f"Valid coordinates: 0 to {warehouse.size - 1}")
    print("Example: Enter '0 0' for top-left corner")
    print("="*70 + "\n")
    
    def get_coordinates(prompt):
        """Helper function to get and validate single coordinate pair"""
        while True:
            try:
                user_input = input(prompt)
                x, y = map(int, user_input.strip().split())
                
                # Validate bounds
                if not (0 <= x < warehouse.size and 0 <= y < warehouse.size):
                    print(f"❌ Error: Coordinates must be between 0 and {warehouse.size - 1}")
                    continue
                
                # Check if position is obstacle
                if warehouse.grid[x, y] == 1:
                    print(f"⚠️  Warning: Position ({x}, {y}) has an obstacle!")
                    clear = input("   Clear this position? (y/n): ").lower()
                    if clear == 'y':
                        warehouse.clear_position(x, y)
                        print(f"✓ Position ({x}, {y}) cleared!")
                        return (x, y)
                    else:
                        print("   Please choose another position.")
                        continue
                
                return (x, y)
                
            except ValueError:
                print("❌ Error: Please enter two numbers separated by space (e.g., '0 0')")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    # Get start position
    start = get_coordinates("🟢 Enter START coordinates (x y): ")
    print(f"✓ Start position set: {start}\n")
    
    # Get goal position
    while True:
        goal = get_coordinates("🔴 Enter EXIT coordinates (x y): ")
        if goal == start:
            print("❌ Error: Exit cannot be same as start position!\n")
            continue
        print(f"✓ Exit position set: {goal}\n")
        break
    
    return start, goal

def print_header():
    """Print fancy header"""
    print("\n" + "="*70)
    print("  🤖 SMART WAREHOUSE ROBOT SIMULATION")
    print("  Optimal Pathfinding with A* Algorithm")
    print("="*70)

def print_results(path, start, goal):
    """Print path results in a nice format"""
    print("\n" + "="*70)
    print("  📊 NAVIGATION RESULTS")
    print("="*70)
    
    if not path:
        print("❌ NO PATH FOUND!")
        print("   The robot cannot reach the exit due to obstacles.")
        print("   Try different coordinates or reduce obstacle density.")
    else:
        path_length = len(path) - 1  # Subtract 1 because start doesn't count
        print(f"✅ PATH FOUND!")
        print(f"   Start: {start}")
        print(f"   Exit:  {goal}")
        print(f"   Path length: {path_length} steps")
        
        # Calculate efficiency
        manhattan_distance = abs(goal[0]-start[0]) + abs(goal[1]-start[1])
        efficiency = (manhattan_distance / max(1, path_length)) * 100
        print(f"   Manhattan distance: {manhattan_distance} steps")
        print(f"   Efficiency: {efficiency:.1f}%")
        print("\n   🎉 ITEM DELIVERED SUCCESSFULLY!")
        
        # Show first few and last few steps
        if len(path) <= 10:
            print(f"\n   Complete path: {' → '.join([str(p) for p in path])}")
        else:
            first_steps = ' → '.join([str(p) for p in path[:3]])
            last_steps = ' → '.join([str(p) for p in path[-3:]])
            print(f"\n   Path: {first_steps} → ... → {last_steps}")
    
    print("="*70 + "\n")

def main():
    """
    Main program execution
    1. Create warehouse with obstacles
    2. Get user input for start/exit
    3. Find optimal path using A*
    4. Visualize and animate results
    """
    
    # Print header
    print_header()
    
    # Configuration
    grid_size = 10
    obstacle_density = 0.10  # 10% of cells are obstacles
    
    print(f"\n⚙️  Configuration:")
    print(f"   Grid size: {grid_size}x{grid_size}")
    print(f"   Obstacle density: {obstacle_density*100:.0f}%")
    print(f"   Algorithm: A* (optimal pathfinding)")
    
    # Create warehouse
    print("\n🏭 Generating warehouse layout...")
    warehouse = WarehouseGrid(size=grid_size, obstacle_density=obstacle_density)
    
    # Display grid info
    info = warehouse.get_grid_info()
    print(f"✓ Warehouse created!")
    print(f"   Free cells: {info['free_cells']}")
    print(f"   Obstacles: {info['obstacles']}")
    
    # Get user input
    start, goal = get_user_input(warehouse)
    
    # Find path using A*
    print("🔍 Computing optimal path using A* algorithm...")
    pathfinder = AStarPathfinder(warehouse)
    path = pathfinder.find_path(start, goal)
    
    if path:
        print(f"✓ Path computed! ({len(path)} steps)")
    else:
        if not path:
            print("❌ No valid path found between Start and Exit!")
            print("🤖 Trying nearby alternate exits...")

    # Try neighboring cells around goal (3x3 area)
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                new_goal = (goal[0] + dx, goal[1] + dy)
            # Skip out-of-bound positions
                if not (0 <= new_goal[0] < warehouse.size and 0 <= new_goal[1] < warehouse.size):
                    continue
            # Skip if obstacle
                if warehouse.grid[new_goal[0], new_goal[1]] == 1:
                    continue
            # Try finding path to this new goal
                alt_path = pathfinder.find_path(start, new_goal)
                if alt_path:
                    print(f"✅ Alternate path found to nearby cell {new_goal}")
                    goal = new_goal
                    path = alt_path
                    break

    # Still no luck after trying all nearby exits
    if not path:
        print("⚠️ Even alternate exits are blocked! Try regenerating the warehouse.")
    
    # Print results
    print_results(path, start, goal)
    
    # Visualize
    if path:
        print("📊 Generating visualizations...\n")
        
        visualizer = WarehouseVisualizer(warehouse, path, start, goal)
        
        # Static visualization
        print("1️⃣  Static Path Visualization:")
        visualizer.create_static_visualization()
        
        # Animated visualization
        print("\n2️⃣  Animated Robot Movement:")
        visualizer.create_animation()
        
        print("\n✨ Visualization complete!")
    
    print("\n" + "="*70)
    print("  Thank you for using Smart Warehouse Robot Simulator!")
    print("="*70 + "\n")
    


if __name__ == "__main__":
    main()