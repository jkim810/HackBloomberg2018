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
	ax = V*d_x/friction - V*v_x
	ay = V*d_y/friction - V*v_y

	return 1, math.atan(ax/ay)

def check_mine_existance(current, mines):
	for m in mines:
		if m.x == current[0] and m.y == current[1]:
			return True
	return False

def closest_mine(mines, x, y):
	minimum = 10000.0**2;
	for m in mines.keys():
		curr = (m[0]-x)**2 + (m[1]-y)**2
		if curr < minimum:
			minimum =  curr
			minimum_x = m[0]
			minimum_y = m[1]

	return minimum_x, minimum_y
#a, theta = calculate_acceleration(0.99, 5000, 5000, 10, -10, 7000, 7000)

s = STATUS()
c = CONFIGURATIONS()
current = (0, 0)
stored_mine = dict();

print(c.width, c.height)

ACCELERATE(3, 1)

while(True):

	print('iterating')
	s.receive_info();
	time.sleep(0.1)

	if s.mines:
		for m in s.mines:
			stored_mine[(m.x,m.y)] = m.owner
		
		# update when it is too far
		if (current[0]-s.x > 300 and current[1]-s.y > 300):
			current = closest_mine(stored_mine, s.x, s.y)
			print('spotted mine', current)
		
		else:
			BRAKE()
			time.sleep(1)

	if stored_mine:
		a, theta = calculate_acceleration(c.friction, s.x, s.y, s.dx, s.dy, current[0], current[1])
		ACCELERATE(theta, a) 

print(a, theta)
