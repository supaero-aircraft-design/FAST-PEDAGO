import plotly

# Base colors for the graph
COLORS = plotly.colors.qualitative.Plotly

# Horizontal tail

# Height of the horizontal tail root compared to the center line of the
# fuselage. 0.0 means on the center line, 1.0 means at a height same as
# the radius of the fuselage
HT_HEIGHT = 0.3
# Height of the horizontal tail tip compared to the center line of the
# fuselage. 0.0 means on the center line, 1.0 means at a height same as
# the radius of the fuselage
HT_DIHEDRAL = 0.42


# Engine

# Height of the middle of the engine 0.0 means on the center line
# 1.0 means the middle of the engine is just on the lower line of the aircraft
ENGINE_HEIGHT = 0.5
# Height of the wing root compared to the center line of the fuselage. 0.0
# means on the center line, 1.0 means at a height same as the radius of the
# fuselage below
WING_ROOT_HEIGHT = 0.2

# Nacelle position compared to the leading edge. 0 means that the back of the
# nacelle is aligned with the beginning of the root, 1 means that the
# beginning of the nacelle is aligned with the kink_x.
NACELLE_POSITION = 0.7


# Elevator

# Percentage of the tail root concerned by the elevator.
HORIZONTAL_TAIL_ROOT = 0.3
# Percentage of the tail tip, at 90 percent of the horizontal tail width,
# covered by the elevator.
HORIZONTAL_TAIL_TIP = 0.3
# Percentage of the width of the horizontal tail concerned by the elevator.
HORIZONTAL_WIDTH_ELEVATOR = 0.85
