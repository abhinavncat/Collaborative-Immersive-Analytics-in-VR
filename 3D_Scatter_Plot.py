import viz
import vizfx
import vizconnect
import vizact
import vizshape
import vizinfo
import random
from sklearn.datasets import load_iris
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Load the Vizconnect configuration (reusing Head Anatomy config)
vizconnect.go('vizconnect_config.py')

# Load the background environment scene
viz.add('art/VisualizationRoom.OSGB')

# Create a container group for scatter plot and box
container_group = viz.addGroup()
container_group.setPosition([0, 1.7, 0])  # Adjusted to align with podium top

# Create a visible 3D box frame to contain the scatter plot
box_size = 1.0
box = vizshape.addBox(size=[box_size, box_size, box_size], alpha=0.1)
box.color(viz.WHITE)
box.setParent(container_group)

# Add X, Y, Z axes along the bottom edges of the cube
axis_len = 1.0
axis_thickness = 0.005

x_axis = vizshape.addCylinder(height=axis_len, radius=axis_thickness, axis=vizshape.AXIS_X)
x_axis.color(viz.RED)
x_axis.setPosition([0, -0.5, -0.5])
x_axis.setParent(container_group)

y_axis = vizshape.addCylinder(height=axis_len, radius=axis_thickness, axis=vizshape.AXIS_Y)
y_axis.color(viz.GREEN)
y_axis.setPosition([-0.5, 0, -0.5])
y_axis.setParent(container_group)

z_axis = vizshape.addCylinder(height=axis_len, radius=axis_thickness, axis=vizshape.AXIS_Z)
z_axis.color(viz.BLUE)
z_axis.setPosition([-0.5, -0.5, 0])
z_axis.setParent(container_group)

# Load and normalize the Iris dataset
iris = load_iris()
data = iris.data[:, [0, 2, 3]]  # Use sepal length, petal length, petal width
labels = iris.target
species = iris.target_names

# Normalize data to fit in -0.5 to +0.5 cube
scaler = MinMaxScaler(feature_range=(-0.5, 0.5))
data_scaled = scaler.fit_transform(data)

# Define color map for species
color_map = {
    0: viz.RED,       # Setosa
    1: viz.GREEN,     # Versicolor
    2: viz.BLUE       # Virginica
}

POINT_RADIUS = 0.02

scatter_points = []

# Create data point spheres inside the box
for i in range(len(data_scaled)):
    x, y, z = data_scaled[i]
    label = labels[i]
    color = color_map[label]
    point = vizshape.addSphere(radius=POINT_RADIUS)
    point.setPosition([x, y, z])
    point.color(color)
    point.setParent(container_group)
    scatter_points.append(point)

# Floating legend panel with color-coded text using font color setting
legend_panel = vizinfo.InfoPanel(title='Legend', align=viz.ALIGN_RIGHT_TOP, icon=False)
legend_panel.setText('')
legend_panel.addLabelItem('Setosa', viz.addText3D('', color=viz.RED))
legend_panel.addLabelItem('Versicolor', viz.addText3D('', color=viz.GREEN))
legend_panel.addLabelItem('Virginica', viz.addText3D('', color=viz.BLUE))
legend_panel.setPosition([0.8, 0.9])

# Interaction: Highlight a point when selected
def on_select():
    info = viz.pick()
    if info.valid and info.object in scatter_points:
        for pt in scatter_points:
            pt.color(pt.getColor())  # reset to original color
        info.object.color(viz.YELLOW)  # Highlight selected point

# Map selection to left mouse click or wand trigger
vizact.onmousedown(viz.MOUSEBUTTON_LEFT, on_select)

# If using the Wand Proxy, map the trigger action to the same function
import tools

class PointSelector(tools.Tool):
    def __init__(self, *args, **kwargs):
        super(PointSelector, self).__init__(*args, **kwargs)

    def select(self, e=None):
        on_select()

selector = PointSelector()

def show():
    for proxyWrapper in vizconnect.getToolsWithMode('Proxy'):
        proxyWrapper.getRaw().setCallback(selector, selector.select, 1)

def hide():
    for proxyWrapper in vizconnect.getToolsWithMode('Proxy'):
        proxyWrapper.getRaw().clear()

show()
