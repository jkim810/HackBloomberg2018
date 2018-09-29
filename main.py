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
	ax = travel_x/friction - curr_dx
	ay = travel_y/friction - curr_dy

	# a = math.sqrt(pow(ax, 2) + pow(ay,2))

	return 1, math.atan(ax/ay)


a, theta = calculate_acceleration(0.99, 5000, 5000, 10, -10, 7000, 7000)

s = STATUS()

ACCELERATE(1,1)

while(True):

	print('iterating')
	tmp = s.receive_info();
	time.sleep(0.1)
	if int(s.num_mines) > 0:
		print('spotted mine')
		a, theta = calculate_acceleration(tmp.x, tmp.y, tmp.dx, tmp,dy, s.mine[0].x, s.mine[0].y)
		ACCELERATE(1,theta)


print(a, theta)
