import reeds_shepp as rs
import utils as u
import math
obs = []

def avoid_obstacles(path, start_point, end_point, obstacle_grid, grid_resolution):
    modified_path = []
    current_position = start_point
    current_angle = 0  # Initial vehicle orientation (assumed facing right)

    for element in path:
        # Discretize the path element into small points
        segment_points = discretize_path_element(element, current_position, current_angle, grid_resolution)
        
        # Check if any point in the segment collides with an obstacle
        collision_detected = False
        for point in segment_points:
            if is_collision(point, obs):
                collision_detected = True
                # delete path from paths
                break
        
        if collision_detected:
            # Adjust the path around the obstacle
            # adjusted_element = replan_around_obstacle(element, current_position, current_angle, obstacle_grid, grid_resolution)
            # modified_path.append(adjusted_element)
            abort path
        else:
            # Append the original element if no collision
            modified_path.append(element)
        
        # Update the current position and angle after following the segment
        current_position, current_angle = update_position_and_angle(element, current_position, current_angle)
    
    return modified_path


def discretize_path_element(element, start_position, start_angle, grid_resolution):
    points = []
    delta = 0.5  # Small step for discretization

    if element.steering == rs.Steering.LEFT or element.steering == rs.Steering.RIGHT:
        # For curved segments (steering LEFT or RIGHT)
        radius = u.turning_radius
        arc_length = element.t  # t is the angle in radians for curves
        angle_step = delta / radius  # Small angle step for discretization

        for theta in range(0, arc_length, angle_step):
            point = calculate_curved_point(start_position, start_angle, theta, radius, element.steering)
            points.append(point)
    
    elif element.steering == rs.Steering.STRAIGHT:
        # For straight segments (steering STRAIGHT)
        distance = element.t  # t is the forward distance
        for d in range(0, distance, delta):
            point = calculate_straight_point(start_position, start_angle, d)
            points.append(point)
    
    return points

def calculate_curved_point(start_position, start_angle, theta, radius, steering):
    if steering == rs.Steering.LEFT:
        new_x = start_position.x + radius * (math.sin(start_angle + theta) - math.sin(start_angle))
        new_y = start_position.y - radius * (math.cos(start_angle + theta) - math.cos(start_angle))
    elif steering == rs.Steering.RIGHT:
        new_x = start_position.x + radius * (math.sin(start_angle - theta) - math.sin(start_angle))
        new_y = start_position.y + radius * (math.cos(start_angle - theta) - math.cos(start_angle))

    #floor both points 
    return (new_x, new_y)

def calculate_straight_point(start_position, start_angle, distance):
    new_x = start_position.x + distance * math.cos(start_angle)
    new_y = start_position.y + distance * math.sin(start_angle)
    return (new_x, new_y)

def is_collision(point):
    return point in obs
