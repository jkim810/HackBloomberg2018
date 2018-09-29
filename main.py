import math
from command import *

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

id = 'taqueria'
ps = 'diana'


run(id, ps, 'ACCELERATE 1 1')

while(True):
	tmp = s.receive_info();
	if s.mines:
		target = tmp.mines[0]
		a, theta = calculate_acceleration(tmp.x, tmp.y, tmp.dx, tmp,dy, target.x, target.y)
		run(id, ps, 'ACCELERATE ' + theta + ' 1')

print(a, theta)
