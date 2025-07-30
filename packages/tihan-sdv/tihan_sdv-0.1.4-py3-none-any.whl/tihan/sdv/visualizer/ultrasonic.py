import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc, Circle, Wedge, Annulus
from matplotlib.animation import FuncAnimation
import numpy as np
from PIL import Image
from pathlib import Path
from typing import Union
from matplotlib.axes import Axes
import matplotlib.image as mpimg
import math


class UltrasonicVisualizer:
    def __init__(self, **kwargs):
        self.distances = {f'distance_{i+1}': kwargs.get(f'distance_{i+1}', 0) for i in range(len(kwargs))}
        # Create the figure and axis
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        plt.title('Sensor Visualization')

        # Set fixed axis limits and aspect ratio to prevent shrinking of the plot
        self.ax.set_xlim(0, 2)
        self.ax.set_ylim(0, 2)
        self.ax.set_aspect('equal')

        self.initial_x = 0.32 +0.5
        self.initial_y = 0.25 + 0.5

        self.rectangle_width = 0.26
        self.rectangle_height = 0.64


        # ---------------------------- Image Background -------------------------------------
        self.image_path = 'tihan/sdv/visualizer/Resources/Images/maini_cart.png'
        self.image = self.load_img(self.image_path)
        self.image_extent = [0.8, 1.1, 0.75, 1.4]# Define the extent for positioning the image
        # Display the image as the background
        self.ax.imshow(self.image, extent=self.image_extent, zorder=1)  # Lower zorder to keep it below

        
        # ----------------------------ultrasonic sensors--------------------------------
        # Define the positions for the 8 ultrasonic sensors
        self.sensor_positions = {
            'S1': (self.initial_x, self.initial_y),
            'S2': (self.initial_x + self.rectangle_width, self.initial_y),
            'S3': (self.initial_x,  self.initial_y + self.rectangle_height),
            'S4': (self.initial_x + self.rectangle_width, self.initial_y + self.rectangle_height),
            'S5': (self.initial_x + self.rectangle_width / 2, self.initial_y),
            'S6': (self.initial_x + self.rectangle_width / 2, self.initial_y + self.rectangle_height),

            'S7': (self.initial_x,  self.initial_y + self.rectangle_height / 4),
            'S8': (self.initial_x,  self.initial_y + self.rectangle_height * (2/4)),
            'S9': (self.initial_x,  self.initial_y + self.rectangle_height * (3/4)),

            'S13': (self.initial_x + self.rectangle_width, self.initial_y + self.rectangle_height * (1/4)),
            'S14': (self.initial_x + self.rectangle_width, self.initial_y + self.rectangle_height * (2/4)),
            'S15': (self.initial_x + self.rectangle_width, self.initial_y + self.rectangle_height * (3/4)),

        }
        # Plot the ultrasonic sensors (small circles)
        self.sensor_radius = 0.015
        self.sensors = []

        for pos in self.sensor_positions.values():
            sensor = Circle(pos, self.sensor_radius, color='#0047AB',zorder=2)  # Sensor color is blue
            self.ax.add_patch(sensor)  # Add the sensor to the plot
            self.sensors.append(sensor)

        # -------------------------Animation-------------------------------------
        # Maximum wave radius and number of frames in the animation
        self.num_frames = 30  # Number of frames for the animation

        # Create the animation
        self.ani = FuncAnimation(self.fig, self.update, frames=self.num_frames, interval=30, repeat=True)
        plt.show(block=False)
        

        #---------------------------------load the resource image------------------ 

    def load_img(self,path_to_image:Union[Path,str]):
        return mpimg.imread(path_to_image) 
        
    # Function to draw a single track layer
    def draw_track(self,ax, center_x, center_y, width, num_track, spacing, zorder):
        # Define a list of colors (can be expanded)
        colors = ['blue','red','orange','green']

        for i in range(num_track):
            radius = 0.1 + i * spacing
            color = colors[i]  # Assign different colors to different tracks

            # Draw top semicircle
            arc_top = Arc((center_x, center_y + radius), 2 * radius, 2 * radius, angle=0, 
                        theta1=0, theta2=180, color=color, lw=2, zorder=zorder)
            ax.add_patch(arc_top)

            # Draw bottom semicircle
            arc_bottom = Arc((center_x, center_y - radius), 2 * radius, 2 * radius, angle=0, 
                            theta1=180, theta2=360, color=color, lw=2, zorder=zorder)
            ax.add_patch(arc_bottom)

            # Draw straight lines connecting semicircles
            ax.plot([center_x - radius, center_x - radius], [center_y - radius, center_y + radius], 
                    color=color, lw=2, zorder=zorder)
            ax.plot([center_x + radius, center_x + radius], [center_y - radius, center_y + radius], 
                    color=color, lw=2, zorder=zorder)
            
    def set_distances(self, new_distances):
        """Update distances and refresh the visualization."""
        self.distances.update(new_distances)
        self.ax.clear()
        self.update(1) # Call update function to redraw the plot
        plt.draw() # Draw the plot

    def obs_color(self,distance):
         if 0 <= distance <= 30:
             return 'red'
         
         elif 30 <= distance <=60:
             return 'orange'                                                                   
         
         else:
             return 'green'


    def draw_obstacle(self, ax,x,y,num_arcs, frame, obstacle_distance):
        """Draws concentric arcs with varying thickness (thin to thick)"""
        alpha = 0.02 + (frame / num_arcs) * 0.4  # Gradual transparency
        linewidth = 0.01 + (frame / num_arcs) * 0.3  # Start thin and gradually thicken  
        obstacle = Circle((x,y), self.sensor_radius, color=self.obs_color(obstacle_distance),zorder=2,alpha=alpha,linewidth=linewidth)  # obstacle color is Red
        ax.add_patch(obstacle)  # Add the sensor to the plot

    def calculate_angle(self, sensor_pos):
        """Calculate the angle from sensor to the edge of the rectangle to direct the wave."""
    
        sensor_angle_map = {
            (0.82,0.75): 145,  # S1
            (1.08,0.75): 215,  # S2
            (0.82,1.39): 35,   # S3
            (1.08,1.39): 325,  # S4
            (0.95,0.75): 180,  # S5
            (0.95,1.39): 0,    # S6
            (0.82, 0.91):115,  # S7
            (0.82, 1.07):90,   # S8
            (0.82, 1.23):65,   # S9
            (1.08, 0.91):245,  # S10
            (1.08, 1.07):270,  # S11
            (1.08, 1.23):295,  # S12
        }

        return sensor_angle_map.get(sensor_pos, 0) 


    # Function to update the plot for each frame of the animation
    def update(self, frame):
        self.ax.set_xlim(0, 2)
        self.ax.set_ylim(0, 2)
        self.ax.set_aspect('equal')

        # Redraw the image in the background
        self.ax.imshow(self.image, extent=self.image_extent, zorder=1)
        self.fig.set_size_inches(8, 8)
        # Draw the track
        self.draw_track(ax = self.ax, center_x=0.95, center_y=1.075, width=0.2,num_track=4,spacing=0.11,zorder=0)

        
        # Draw the ultrasonic sensors
        for pos in self.sensor_positions.values():
            sensor = Circle(pos, self.sensor_radius, color='#0047AB', zorder=2)
            self.ax.add_patch(sensor)


        for i, (sensor, pos) in enumerate(self.sensor_positions.items()):
            pos = (round(pos[0], 2), round(pos[1], 2))
            distance_key = f'distance_{i+1}'
            distance = self.distances.get(distance_key, 0)
            wave_radius = distance * 0.003
            angle = np.radians(self.calculate_angle(pos))  # Convert to radians

            # Shift angle dynamically based on sensor position
            shift_angle = np.pi / 2  # 90 degrees shift for better alignment

            # Calculate label position relative to wave radius
            self.label_x = pos[0] + (wave_radius + 0.05) * np.cos(angle + shift_angle)
            self.label_y = pos[1] + (wave_radius + 0.05) * np.sin(angle + shift_angle)

            
            x = self.label_x
            y = self.label_y
            self.draw_obstacle(self.ax,x,y, num_arcs=30, frame=frame, obstacle_distance=distance)
            self.ax.text(x+0.03, y+0.03, f'{distance} cm', ha='center', color='black', fontsize=10)
        self.ax.axis('off')

