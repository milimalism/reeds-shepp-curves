import matplotlib.pyplot as plt
import numpy as np

# Example path segment: straight followed by left curve
path = [
    {'t': np.pi / 2, 'steering': 'LEFT', 'gear': 'FORWARD'},  # Curve left with angle π/2 radians
    {'t': 10, 'steering': 'STRAIGHT', 'gear': 'FORWARD'}  # Move straight for 10 units
]

# Function to calculate points for straight motion
def calculate_straight_points(start_position, start_angle, distance, step_size=1):
    points = []
    for d in np.arange(0, distance, step_size):
        new_x = start_position[0] + d * np.cos(start_angle)
        new_y = start_position[1] + d * np.sin(start_angle)
        points.append((new_x, new_y))
    return points

# Function to calculate points for a curved motion
def calculate_curve_points(start_position, start_angle, radius, angle, direction, step_size=1):
    points = []
    theta_step = step_size / radius  # Step in radians
    for theta in np.arange(0, angle, theta_step):
        if direction == 'LEFT':
            new_x = start_position[0] + radius * (np.sin(start_angle + theta) - np.sin(start_angle))
            new_y = start_position[1] - radius * (np.cos(start_angle + theta) - np.cos(start_angle))
        elif direction == 'RIGHT':
            new_x = start_position[0] + radius * (np.sin(start_angle - theta) - np.sin(start_angle))
            new_y = start_position[1] + radius * (np.cos(start_angle - theta) - np.cos(start_angle))
        points.append((new_x, new_y))
    return points

# Starting point and orientation
start_position = (10, 20)
start_angle = 0  # Facing right initially
radius = 5  # Radius for the left curve

# Collect all points from the path
all_points = []

# Process each segment of the path
for segment in path:
    if segment['steering'] == 'STRAIGHT':
        straight_points = calculate_straight_points(start_position, start_angle, segment['t'])
        all_points.extend(straight_points)
        start_position = straight_points[-1]  # Update starting point
    elif segment['steering'] == 'LEFT':
        curve_points = calculate_curve_points(start_position, start_angle, radius, segment['t'], 'LEFT')
        all_points.extend(curve_points)
        start_position = curve_points[-1]  # Update starting point
        start_angle += segment['t']  # Update the angle after turning

# Convert points to x, y arrays for plotting
x_points, y_points = zip(*all_points)

# Plot the path points
plt.figure(figsize=(6, 6))
plt.plot(x_points, y_points, marker='o')
plt.title("Path Segmentation into Points")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.axis('equal')
plt.show()
