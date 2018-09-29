import clientpy3

id = "taqueria"
passwd = "diana"

class Mine:
    def __init__(self, owner, x, y):
        self.owner = owner
        self.x = x
        self.y = y

class Player:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Wormhole:
    def __init__(self, x, y, r, out_x, out_y):
        self.x = x
        self.y = y
        self.r = r
        self.out_x = out_x
        self.out_y = out_y

class STATUS:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.num_mines = 0
        self.num_players = 0
        self.num_bombs = 0
        self.num_wormholes = 0
        self.mines = []
        self.players = []
        self.bombs = []
        self.wormholes = []
    
    def parse_info(self, info):
        info = info.split()
        self.x, self.y, self.dx, self.dy = info[1:5]
        idx_mine = info.index("MINES")
        idx_players = info.index("PLAYERS")
        idx_bombs = info.index("BOMBS")
        idx_wormholes = info.index("WORMHOLES")
        
        #print(idx_mine, idx_players, idx_bombs, idx_wormholes, len(info))

        # MINES
        self.num_mines = info[idx_mine+1]
        for i in range(idx_mine+2, idx_players, 3):
            self.mines.append(Mine(
                owner = info[i],
                x = info[i+1],
                y = info[i+2]
            ))
        
        # PLAYERS
        self.num_players = info[idx_players+1]
        for i in range(idx_players+2, idx_bombs, 4):
            self.players.append(Player(
                x = info[i],
                y = info[i+1],
                dx = info[i+2],
                dy = info[i+3]
            ))

        # BOMBS
        self.num_bombs = info[idx_bombs+1]
        for i in range(idx_bombs+2, idx_wormholes, 2):
            self.bombs.append(Bomb(
                x = info[i],
                y = info[i+1]
            ))

        # Wormhole
        self.num_wormholes = info[idx_wormholes+1]
        for i in range(idx_wormholes+2, len(info), 5):
            self.wormholes.append(Bomb(
                x = info[i],
                y = info[i+1],
                r = info[i+2],
                out_x = info[i+3],
                out_y = info[i+4]
            ))

    def receive_info(self):
        info = clientpy3.run(id, passwd, "STATUS")
        #print(info)
        self.parse_info(info)
    
    def receive_scan(self, x, y):
        info = clientpy3.run(id, passwd, "SCAN {} {}".format(x, y))
        #print(info)
        self.parse_info(info)
        
class CONFIGUREATIONS:      
    def __init__(self, to_parse):
        self.to_parse = to_parse
        self.run()
        
    def run(self):
        parsed = self.to_parse.split(" ")    
        self.width = float(parsed[2])
        self.height = float(parsed[4])
        self.capture_radius = float(parsed[6])
        self.vision_radius = float(parsed[8])
        self.friction = float(parsed[10])
        self.brake_friction = float(parsed[12])
        self.bomb_placer_radius = float(parsed[14])
        self.bomb_effect_radius = float(parsed[16])
        self.bomb_delay = float(parsed[18])
        self.bomb_power = float(parsed[20])
        self.scan_radius = float(parsed[22])
        self.scan_delay = float(parsed[24].replace('\n',''))

def ACCELERATE(radians, accel):
    clientpy3.run(id, passwd, "ACCELERATE {} {}".format(radians, accel))

def BRAKE():
    clientpy3.run(id, passwd, "BRAKE")

def BOMB(x, y):
    clientpy3.run(id, passwd, "BOMB {} {}".format(x, y))

def BOMB(x, y, t):
    clientpy3.run(id, passwd, "BOMB {} {} {}".format(x, y, t))