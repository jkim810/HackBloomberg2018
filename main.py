import math
from command import *
import time

def calculate_acceleration(friction, curr_x, curr_y, curr_dx, curr_dy, dest_x, dest_y):
	travel_x = dest_x - curr_x;
	travel_y = dest_y - curr_y;

	'''
	# calculate magnitude / distance
	r = math.sqrt(pow(travel_x, 2) + pow(travel_y,2))
	
	# calculate angle
	cosine = math.acos(travel_x/r)
	sine = math.asin(travel_y/r)

	# plot theta according to cosine and sine values

	'''
#	ax = travel_x/friction - curr_dx
#	ay = travel_y/friction - curr_dy

	# a = math.sqrt(pow(ax, 2) + pow(ay,2))

# ADDED CODE
	v_x = curr_dx
	v_y = curr_dy
	V = math.sqrt(v_x**2 + v_y**2)
	D_x = dest_x - curr_x
	D_y = dest_y - curr_y
	D = math.sqrt(D_x**2 + D_y**2)
	d_x = D_x / D
	d_y = D_y / D
	ax = V*d_x - V*v_x
	ay = V*d_y - V*v_y

	return 1, math.atan(ax/ay)


a, theta = calculate_acceleration(0.99, 5000, 5000, 10, -10, 7000, 7000)

s = STATUS()

while(True):
	print('iterating')
	s.receive_info()
	time.sleep(0.1)
	if int(s.num_mines) > 0:
		print('spotted mine')
		a, theta = calculate_acceleration(s.x, s.y, s.dx, s,dy, s.mine[0].x, s.mine[0].y)
		ACCELERATE(1,theta)




print(a, theta)
