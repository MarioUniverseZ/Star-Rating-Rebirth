import numpy as np
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from scipy.interpolate import interp1d

class ColorMap():
    def __init__(self, difficulty_value):
        # Define the difficulty domain and corresponding colors
        domain = [0.1, 1.25, 2, 2.5, 3.3, 4.2, 4.9, 5.8, 6.7, 7.7, 9]
        colors = ['#4290FB', '#4FC0FF', '#4FFFD5', '#7CFF4F', '#F6F05C', '#FF8068', 
                '#FF4E6F', '#C645B8', '#6563DE', '#18158E', '#000000']

        # Convert hex to RGB (normalized 0-1)
        rgb_colors = [to_rgb(c) for c in colors]

        # Create a custom colormap
        self.cmap = LinearSegmentedColormap.from_list("difficulty", rgb_colors, N=256)

        # Interpolation function to map difficulty to 0-1 for colormap
        self.norm = interp1d(domain, np.linspace(0, 1, len(domain)), kind="linear", fill_value="extrapolate")
        self.difficulty_value = difficulty_value

    # Function to get color for a difficulty value
    def get_difficulty_color(self, value):
        color = self.cmap(self.norm(value))
        rgb_color = [int(255 * c) for c in color[:3]]
        return rgb_color
    
if __name__ == "__main__":
    # Example usage
    color_map = ColorMap(1.5)
    color = color_map.get_difficulty_color(1.5)
    print(color)