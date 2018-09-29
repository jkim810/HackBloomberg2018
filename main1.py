import math
from command import *
import time
import random
import timeit
import js

id = "taqueria"
passwd = "diana"

def calculate_acceleration(friction, curr_x, curr_y, curr_dx, curr_dy, dest_x, dest_y):
	ax = dest_x - curr_x;
	ay = dest_y - curr_y;
	if ax **2 + ay **2 < 640000:
		return 0.3, math.atan2(ay,ax)
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
			continue
		curr = (m[0]-x)**2 + (m[1]-y)**2
		if curr < minimum:
			minimum =  curr
			minimum_x = m[0]
			minimum_y = m[1]
	return minimum_x, minimum_y
#a, theta = calculate_acceleration(0.99, 5000, 5000, 10, -10, 7000, 7000)

def update():
	print("updated")
	tmp = js.log()
	for d in tmp[0]:
		stored_mine[(float(d["px"]), float(d["py"]))] = d["owner"]
	for j in tmp[1]:
		delete_mine_wormhole(float(j["px"]), float(j["py"]), float(j["radius"])+140)

s = STATUS()
scanner = STATUS()
c = CONFIGURATIONS()
tt = 0
s.receive_info()

stored_mine = dict()

update()

# x_avg = 0
# y_avg = 0

# for ss in stored_mine.keys():
# 	x_avg = x_avg + ss[0]
# 	y_avg = y_avg + ss[1]

# x_avg = x_avg / len(stored_mine.keys())
# y_avg = y_avg / len(stored_mine.keys())

# a, theta = calculate_acceleration(c.friction, s.x, s.y, s.dx, s.dy, x_avg, y_avg)
ACCELERATE(3, 1)

while(True):
	try:
		s.receive_info()
		
		tt = tt + 1
		if (tt > 1000):
			print("overtime", tt)
			ACCELERATE(random.random()*2*math.pi, 1)
			tt = 0

		if s.wormholes:
			w = s.wormholes[0]
			a, theta = calculate_acceleration(c.friction, s.x, s.y, s.dx, s.dy, w.x, w.y)
			ACCELERATE(theta + math.pi, a)
			delete_mine_wormhole(w.x, w.y, w.r)
		
		if stored_mine:
			for m in s.mines:
				stored_mine[(m.x,m.y)] = m.owner

			if stored_mine:
				current = closest_mine(s.x, s.y)
				a, theta = calculate_acceleration(c.friction, s.x, s.y, s.dx, s.dy, current[0], current[1])
				
			# if I own it
			if (stored_mine[current] != id):
				t = 0
				update()
				current = closest_mine(s.x, s.y)
				print('new mine', current)
				BRAKE()
				BRAKE()
				time.sleep(3)

				if s.wormholes:
					w = s.wormholes[0]
					a, theta = calculate_acceleration(c.friction, s.x, s.y, s.dx, s.dy, w.x, w.y)
					ACCELERATE(theta + math.pi, a)
					delete_mine_wormhole(w.x, w.y, w.r)
					#print(stored_mine)
					#print("wormhole detected {}".format(s.wormholes))
					#print(stored_mine)
					#current = (0, 0)
				
				while (stored_mine[current] != id):
					if (t > 60 and t % 40 == 39):
						BRAKE()
						update()
					if (t > 100):
						print("overtime", t)
						ACCELERATE(random.random()*2*math.pi, 1)
						break					
					s.receive_info()
					for m in s.mines:
						stored_mine[(m.x,m.y)] = m.owner
								
					a, theta = calculate_acceleration(c.friction, s.x, s.y, s.dx, s.dy, current[0], current[1])
					# print('theta', theta,  t)
					if (abs(s.x-current[0]) > c.width * 0.8 or abs(s.y-current[1]) >  c.height * 0.8):
					 	ACCELERATE(theta+math.pi, 1)
					else:
						ACCELERATE(theta, 1)
					for m in s.mines:
						stored_mine[(m.x,m.y)] = m.owner
					time.sleep(0.01)
					t = t + 1
				print('Captured mine')

		time.sleep(0.01)
	except:
		continue

print(a, theta)
