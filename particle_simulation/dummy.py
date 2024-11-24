import random

def generate_particle_colors(particle_types, iterations):
    """
    Generates unique colors for each particle type with equal iterations.

    Args:
        particle_types (list): List of particle types (e.g., ['type1', 'type2']).
        iterations (int): Total number of colors to generate (must be divisible by number of types).

    Returns:
        dict: A dictionary where each particle type has a set of unique colors.
    """
    # Ensure iterations are divisible by the number of particle types so that each type for sure gets a color
    num_types = len(particle_types)
    assert iterations % num_types == 0, f"Iterations ({iterations}) must be divisible by {num_types}."

    colors_per_type = iterations // num_types

    # Define base colorways for each particle type
    base_colorways = {
        "type1": "red",
        "type2": "green",
        "type3": "blue",
        "type4": "yellow"
    }

    # Initialize a dictionary to store unique colors for each particle type
    particle_colors = {ptype: set() for ptype in particle_types}
    
    for ptype in particle_types:
        colorway = base_colorways.get(ptype, "other")
        for _ in range(colors_per_type):
            while True:
                # Generate a random color
                r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                color = (r, g, b)
                
                # Assign the color based on its colorway
                if colorway == "red" and r > g and r > b:
                    particle_colors[ptype].add(color)
                    break
                elif colorway == "green" and g > r and g > b:
                    particle_colors[ptype].add(color)
                    break
                elif colorway == "blue" and b > r and b > g:
                    particle_colors[ptype].add(color)
                    break
                elif colorway == "yellow" and r > 200 and g > 200 and b < 100:
                    particle_colors[ptype].add(color)
                    break

    return particle_colors


# Example Usage
particle_types = ["type1", "type2", "type3", "type4"]
iterations = 16  # Total iterations (must be divisible by 4)

colors = generate_particle_colors(particle_types, iterations)
for ptype, color_set in colors.items():
    print(f"{ptype}: {color_set}")
