import math
from command import *
import time
import random
import timeit

id = "taqueria"
passwd = "diana"

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
	

	if ay > 0 and ax > 0:
		return 1, math.pi * 2 - math.atan(ay/ax)
	elif ay > 0 and ax < 0:
		return 1, math.atan(ay/ax) + math.pi
	elif ay < 0 and ax > 0:
		return 1, - math.atan(ay/ax)
	else:
		return 1, - math.atan(ay/ax) + math.pi
	'''
	return 1, math.atan2(ay,ax)


def check_mine_existance(current, mines):
	for m in mines:
		if m.x == current[0] and m.y == current[1]:
			return True
	return False

def delete_mine_wormhole(x, y, r):
	tmp = []
	for m in stored_mine.keys():
		if (m[0] < x + r and m[0] > x - r and m[1] < y + r and m[1] > y - r):
			tmp.append(m)
	for t in tmp:
		stored_mine.pop(t, None)

def closest_mine(x, y):
	i = 0
	minimum = 10000.0**2
	for m in stored_mine.keys():
		if stored_mine[m] == id:
			i = i + 1
			continue
		curr = (m[0]-x)**2 + (m[1]-y)**2
		if curr < minimum:
			minimum =  curr
			minimum_x = m[0]
			minimum_y = m[1]
	if (i == len(stored_mine.keys())):
		return 0, 0
	return minimum_x, minimum_y
#a, theta = calculate_acceleration(0.99, 5000, 5000, 10, -10, 7000, 7000)

s = STATUS()
scanner = STATUS()
c = CONFIGURATIONS()
tt = 0

current = (0, 0)
prev_current = (0, 0)
stored_mine = dict()

# while(True):
# 	if scanner.receive_scan(s.x-s.dy*c.scan_radius, s.y+s.dx*c.scan_radius):
# 		#print(c.scan_radius)
# 		print((s.x, s.y), (scanner.x, scanner.y))

stored_mine[(0,0)] = id

print(c.width, c.height)

ACCELERATE(3, 1)

while(True):
	#print(current)
	s.receive_info()
	if scanner.receive_scan(s.x-s.dy*c.scan_radius, s.y+s.dx*c.scan_radius):
		#print(c.scan_radius)
		print((s.x, s.y), (scanner.x, scanner.y))
		#print(scanner.mines)
	if scanner.mines:
		print("scanner {}".format(scanner.mines))
	#print("current {}, mines {}, stored {}".format(current, s.mines, stored_mine))
	#print("")
	tt = tt + 1
	#print(tt)
	if (tt > 1000):
		print("overtime", tt)
		ACCELERATE(random.random()*2*math.pi, 1)
		tt = 0

	if s.wormholes:
		w = s.wormholes[0]
		a, theta = calculate_acceleration(c.friction, s.x, s.y, s.dx, s.dy, w.x, w.y)
		ACCELERATE(theta + math.pi, a)
		#print(stored_mine)
		delete_mine_wormhole(w.x, w.y, w.r)
		#print(stored_mine)
		#print("wormhole detected {}".format(s.wormholes))

	if s.mines or scanner.mines:
		# update mine
		for m in s.mines:
			stored_mine[(m.x,m.y)] = m.owner
		for m in scanner.mines:
			stored_mine[(m.x,m.y)] = m.owner
		
		if stored_mine:
			current = closest_mine(s.x, s.y)
			if (stored_mine[current] == id):
				current = (0, 0)
				a, theta = calculate_acceleration(c.friction, s.x, s.y, s.dx, s.dy, current[0], current[1])

		# if I own it
		if (stored_mine[current] != id):
			t = 0
			current = closest_mine(s.x, s.y)
			print('new mine', current)
			BRAKE()
			time.sleep(2.5)
			BRAKE()
			time.sleep(2.5)

			if s.wormholes:
				w = s.wormholes[0]
				a, theta = calculate_acceleration(c.friction, s.x, s.y, s.dx, s.dy, w.x, w.y)
				ACCELERATE(theta + math.pi, a)
				delete_mine_wormhole(w.x, w.y, w.r)
				#print(stored_mine)
				#print("wormhole detected {}".format(s.wormholes))
				#print(stored_mine)
				current = (0, 0)
			
			while (stored_mine[current] != id):
				if (t % 30 == 29):
					BRAKE()
					time.sleep(4)
				if (t > 300):
					print("overtime", t)
					ACCELERATE(random.random()*2*math.pi, 1)
					break					
				s.receive_info()
				for m in s.mines:
					stored_mine[(m.x,m.y)] = m.owner
				for m in scanner.mines:
					stored_mine[(m.x,m.y)] = m.owner
				
				scanner.receive_scan(s.x-s.dy*c.scan_radius*5, s.y+s.dx*c.scan_radius*5)
				print((s.x, s.y), (scanner.x, scanner.y))
				if scanner.mines:
					print("scanner {}".format(scanner.mines))
					for m in scanner.mines:
						stored_mine[(m.x,m.y)] = m.owner	
								
				a, theta = calculate_acceleration(c.friction, s.x, s.y, s.dx, s.dy, current[0], current[1])
				# print('theta', theta,  t)
				if (abs(s.x-current[0]) > c.width * 0.8 or (s.y-current[1]) >  c.height * 0.8):
					ACCELERATE(theta+math.pi, 1)
				else:
					ACCELERATE(theta, 1)
				time.sleep(0.01)
				t = t + 1
			
			ACCELERATE(random.random()*2*math.pi, 1)
			print('Captured mine')

	time.sleep(0.01)

print(a, theta)
