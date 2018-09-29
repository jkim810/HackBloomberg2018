import math
from command import *
import time

id = "a"
passwd = "a"

def calculate_acceleration(friction, curr_x, curr_y, curr_dx, curr_dy, dest_x, dest_y):
	ax = dest_x - curr_x;
	ay = dest_y - curr_y;
	
	'''
	# calculate magnitude / distance
	r = math.sqrt(pow(travel_x, 2) + pow(travel_y,2))
	
	# calculate angle
	cosine = math.acos(travel_x/r)
	sine = math.asin(travel_y/r)

	# plot theta according to cosine and sine values

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

	'''

	if ay > 0 and ax > 0:
		return 1, math.pi * 2 - math.atan(ay/ax)
	elif ay > 0 and ax < 0:
		return 1, math.atan(ay/ax) + math.pi
	elif ay < 0 and ax > 0:
		return 1, math.atan(ay/ax)
	else:
		return 1, - math.atan(ay/ax) + math.pi



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
prev_current = (0, 0)
stored_mine = dict()

print(c.width, c.height)

ACCELERATE(3, 1)

while(True):
	s.receive_info()
	print("current {}, mines {}, stored {}".format(current, s.mines, stored_mine))
	print("")

	if s.mines:
		# update mine
		for m in s.mines:
			stored_mine[(m.x,m.y)] = m.owner
		
		if stored_mine:
			current = closest_mine(stored_mine, s.x, s.y)
			if (stored_mine[current] == id):
				current = (0, 0)
				a, theta = calculate_acceleration(c.friction, s.x, s.y, s.dx, s.dy, current[0], current[1])

		# if I own it
		if (current in stored_mine and stored_mine[current] != id):
			current = closest_mine(stored_mine, s.x, s.y)
			print('new mine', current)
			
			BRAKE()
			time.sleep(1)
			BRAKE()
			time.sleep(1)
			BRAKE()
			time.sleep(1)

			while (stored_mine[current] != id):
				s.receive_info()
				for m in s.mines:
					stored_mine[(m.x,m.y)] = m.owner
				a, theta = calculate_acceleration(c.friction, s.x, s.y, s.dx, s.dy, current[0], current[1])
				print('theta', theta)
				ACCELERATE(theta, a)
				time.sleep(0.01)


	time.sleep(0.01)

print(a, theta)
