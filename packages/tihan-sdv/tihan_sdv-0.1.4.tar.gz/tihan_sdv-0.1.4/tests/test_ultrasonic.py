import pytest
import matplotlib
import numpy as np
import random
matplotlib.use('Agg')  # Use non-GUI backend for testing

from tihan.sdv.visualizer.ultrasonic import UltrasonicVisualizer

def test_ultrasonic_visualizer_update(tmp_path):
    # Provide mock distances for sensors
    distances = {f'distance_{i+1}': i*10 for i in range(12)}
    visualizer = UltrasonicVisualizer(**distances)

    # # Update distances and redraw
    # new_distances = {f'distance_{i+1}': 100 - i*5 for i in range(12)}
    # visualizer.set_distances(new_distances)

    new_data = {
        f'distance_{i+1}': random.randint(10, 100) 
        for i in range(12)
    }
    visualizer.set_distances(new_data)

    # Save the figure to ensure it renders
    output_file = tmp_path / "output.png"
    visualizer.fig.savefig(output_file)
    assert output_file.exists()
