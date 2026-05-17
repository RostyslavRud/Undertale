from pygame import *
import random
import math

init()
window_size = 1200, 700
window = display.set_mode(window_size)
SCREEN_W, SCREEN_H = window_size
T = 60
PLAYER_SIZE = 40

maze_map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,0,1,1,1,1,0,0,1,1,1,1,1,0,0,1,0,0,1,0,0,0,1],
    [1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,1],
    [1,0,0,1,0,0,1,1,1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,1,0,0,1,1,1,1,1,0,0,1,0,0,0,1],
    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,4,0,1],
    [1,0,0,0,0,0,1,0,0,1,1,1,0,0,1,0,0,0,0,1,0,0,0,1],
    [1,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1],
    [1,0,0,0,1,1,1,1,0,0,1,1,0,0,1,1,0,0,0,1,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,1,0,0,0,1],
    [1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1,0,1,0,5,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1],
    [1,0,0,1,1,1,0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1],
    [1,2,0,0,0,1,1,1,0,0,1,1,1,1,0,0,0,0,0,3,0,0,0,1],
    [1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]
# 0 - підлога
# 1 - стіна
# 2 - ключ/монстр
# 3 - двері
# 4 - вихід
# 5 - босс
# 6 - секретний ключ
# 7 - секретний босс
kills_total = 0

# ════════════════════════════════════════════
# ЗАВАНТАЖЕННЯ ТЕКСТУР
# масштабуємо під потрібний розмір одразу при старті
# ════════════════════════════════════════════
def load_texture(path, size):
    """Завантажує зображення і масштабує до потрібного розміру"""
    try:
        img = image.load(path).convert()
        img.set_colorkey((0, 0, 0))  # чорний фон прозорий
        return transform.scale(img, size)
    except:
        return None

# текстури для битви (розмір спрайта ворога/боса)
TEX_SLIME      = load_texture("slime.png",      (120, 120))  # Слиз у битві
TEX_SHADOW     = load_texture("shadow.png",     (120, 120))  # Тінь у битві
TEX_SAVER      = load_texture("saver.png",      (160, 140))  # Хранитель пацифіст
TEX_SAVER_EVIL = load_texture("saver_evil.png", (160, 140))  # Хранитель геноцид
TEX_KEY        = load_texture("key.jpg",        (T-20, T-20))  # Ключ у лабіринті

# ════════════════════════════════════════════
# КЛАС SOUL — серце гравця під час битви
# ════════════════════════════════════════════
class soul:
    def __init__(self):
        self.x = SCREEN_W // 2
        self.y = SCREEN_H // 2 + 60
        self.size = 16
        self.speed = 5
        self.hp = 100
        self.max_hp = 100
        self.invincible = 0

    def move(self, arena_rect):
        pressed = key.get_pressed()
        if pressed[K_a]: self.x -= self.speed
        if pressed[K_d]: self.x += self.speed
        if pressed[K_w]: self.y -= self.speed
        if pressed[K_s]: self.y += self.speed
        self.x = max(arena_rect.left+self.size, min(arena_rect.right-self.size, self.x))
        self.y = max(arena_rect.top+self.size, min(arena_rect.bottom-self.size, self.y))

    def draw(self, surf):
        if self.invincible % 6 < 3:
            cx, cy, s = self.x, self.y, self.size
            draw.circle(surf,(220,30,30),(cx-s//3,cy-s//4),s//2)
            draw.circle(surf,(220,30,30),(cx+s//3,cy-s//4),s//2)
            draw.polygon(surf,(220,30,30),[(cx-s//1.3,cy),(cx+s//1.3,cy),(cx,cy+s//1.1)])

    def take_damage(self, dmg):
        if self.invincible <= 0:
            self.hp -= dmg
            self.invincible = 50

    def update(self):
        if self.invincible > 0:
            self.invincible -= 1

    def get_rect(self):
        return Rect(self.x-self.size, self.y-self.size, self.size*2, self.size*2)


# ════════════════════════════════════════════
# КЛАС BUTTON — кнопки вибору дії у битві
# ════════════════════════════════════════════
class button:
    def __init__(self, is_boss=False):
        self.selected = 0
        self.font = font.SysFont(None, 42)
        self.is_boss = is_boss

    def get_labels(self):
        if self.is_boss:
            return ["FIGHT","ACT","MERCY"]
        return ["FIGHT","ACT"] if kills_total > 0 else ["FIGHT","ACT","MERCY"]

    def get_colors(self):
        if self.is_boss:
            return [(200,50,50),(50,180,80),(80,80,220)]
        return [(200,50,50),(50,180,80)] if kills_total > 0 else [(200,50,50),(50,180,80),(80,80,220)]

    def handle(self, e):
        if e.type == KEYDOWN:
            count = len(self.get_labels())
            if e.key == K_LEFT:  self.selected = (self.selected-1) % count
            if e.key == K_RIGHT: self.selected = (self.selected+1) % count

    def draw(self, surf):
        labels, colors = self.get_labels(), self.get_colors()
        self.selected = min(self.selected, len(labels)-1)
        btn_w, gap = 180, 20
        total_w = len(labels)*btn_w+(len(labels)-1)*gap
        start_x = SCREEN_W//2-total_w//2
        y = SCREEN_H-90
        for i,(label,col) in enumerate(zip(labels,colors)):
            bx = start_x+i*(btn_w+gap)
            border = (255,255,255) if i==self.selected else (100,100,100)
            draw.rect(surf,(30,30,30),Rect(bx,y,btn_w,50))
            draw.rect(surf,border,Rect(bx,y,btn_w,50),3)
            txt = self.font.render(label,True,col if i==self.selected else (130,130,130))
            surf.blit(txt,(bx+btn_w//2-txt.get_width()//2,y+12))

    def get_selected(self):
        labels = self.get_labels()
        self.selected = min(self.selected, len(labels)-1)
        return labels[self.selected]


# ── атаки звичайних ворогів ──────────────────
def attack_rain(en, arena):
    for _ in range(6):
        x = random.randint(arena.left+20, arena.right-20)
        en.bullets.append([float(x),float(arena.top),0.0,random.uniform(1.2,2.0),8,(255,80,80)])

def attack_spiral(en, arena):
    corners = [(arena.left+20,arena.top+20),(arena.right-20,arena.top+20),
               (arena.left+20,arena.bottom-20),(arena.right-20,arena.bottom-20)]
    cx,cy = arena.centerx,arena.centery
    for sx,sy in corners:
        dist = math.hypot(cx-sx,cy-sy)
        en.bullets.append([float(sx),float(sy),(cx-sx)/dist*1.5,(cy-sy)/dist*1.5,8,(255,160,0)])

def attack_sides(en, arena):
    for _ in range(3):
        y = random.randint(arena.top+20,arena.bottom-20)
        en.bullets.append([float(arena.left),float(y),random.uniform(1.5,2.2),0.0,7,(100,100,255)])

def attack_cross(en, arena):
    corners = [(arena.left+20,arena.top+20),(arena.right-20,arena.top+20),
               (arena.left+20,arena.bottom-20),(arena.right-20,arena.bottom-20)]
    cx,cy = arena.centerx,arena.centery
    for sx,sy in corners:
        dist = math.hypot(cx-sx,cy-sy)
        en.bullets.append([float(sx),float(sy),(cx-sx)/dist*1.8,(cy-sy)/dist*1.8,7,(200,50,200)])


# ── атаки боса пацифіст ──────────────────────
def boss_attack_walls(en, arena):
    gap_x = random.randint(arena.left+40, arena.right-80)
    gap_w = 70
    for x in range(arena.left, arena.right, 22):
        if gap_x <= x <= gap_x+gap_w: continue
        en.bullets.append([float(x),float(arena.top),0.0,2.0,12,(255,50,50)])
        en.bullets.append([float(x),float(arena.bottom),0.0,-2.0,12,(255,50,50)])

def boss_attack_laser(en, arena):
    y = random.choice([arena.top+30,arena.top+70,arena.centery-20,
                       arena.centery+20,arena.bottom-70,arena.bottom-30])
    for i,x in enumerate(range(arena.left,arena.right,22)):
        en.bullets.append([float(x),float(arena.top+5),0.0,0.8,18,(255,50,0),i*2])
def boss_attack_spiral_fast(en, arena):
    cx,cy = arena.centerx,arena.centery
    for i in range(8):
        angle = i*math.pi/4
        sx = cx + math.cos(angle)*(arena.width//4)
        sy = cy + math.sin(angle)*(arena.height//4)
        dx = -math.sin(angle)*2.2
        dy =  math.cos(angle)*2.2
        en.bullets.append([float(sx),float(sy),dx,dy,10,(100,200,255)])

def boss_attack_chase(en, arena):
    cx,cy = arena.centerx,arena.centery
    for sx,sy,dx,dy in [(arena.left,cy,2.5,0),(arena.right,cy,-2.5,0),
                         (cx,arena.top,0,2.5),(cx,arena.bottom,0,-2.5)]:
        for offset in [-30,0,30]:
            ox = offset if dx==0 else 0
            oy = offset if dy==0 else 0
            en.bullets.append([float(sx+ox),float(sy+oy),dx,dy,12,(150,100,255)])

def boss_attack_rain_heavy(en, arena):
    for _ in range(14):
        x = random.randint(arena.left+10,arena.right-10)
        en.bullets.append([float(x),float(arena.top),0.0,random.uniform(1.8,3.2),10,(255,100,50)])

def boss_attack_bounce(en, arena):
    for i in range(5):
        x = arena.left+i*(arena.width//5)
        en.bullets.append([float(x),float(arena.top),1.5,2.0,8,(50,255,150)])
        en.bullets.append([float(arena.right-i*(arena.width//5)),float(arena.top),-1.5,2.0,8,(50,255,150)])


# ── атаки боса геноцид ───────────────────────
def boss_evil_walls(en, arena):
    gap_x = random.randint(arena.left+40, arena.right-80)
    gap_w = 55
    for x in range(arena.left, arena.right, 22):
        if gap_x <= x <= gap_x+gap_w: continue
        en.bullets.append([float(x),float(arena.top),0.0,2.5,15,(200,0,0)])
        en.bullets.append([float(x),float(arena.bottom),0.0,-2.5,15,(200,0,0)])

def boss_evil_laser(en, arena):
    """Два ряди куль зверху і знизу — спавняться всередині арени"""
    for i,x in enumerate(range(arena.left, arena.right, 22)):
        en.bullets.append([float(x),float(arena.top+5),0.0,3.0,18,(255,50,0),i*2])
        en.bullets.append([float(x),float(arena.bottom-5),0.0,-3.0,18,(255,50,0),i*2])

def boss_evil_spiral(en, arena):
    """8 куль від країв летять до центру арени"""
    cx,cy = arena.centerx,arena.centery
    for i in range(8):
        angle = i*math.pi/4
        sx = cx + math.cos(angle)*(arena.width//2-10)
        sy = cy + math.sin(angle)*(arena.height//2-10)
        dist = math.hypot(cx-sx,cy-sy)
        dx = (cx-sx)/dist*2.5
        dy = (cy-sy)/dist*2.5
        en.bullets.append([float(sx),float(sy),dx,dy,14,(255,50,200)])

def boss_evil_cross(en, arena):
    cx,cy = arena.centerx,arena.centery
    for i in range(8):
        angle = i*math.pi/4
        sx = cx + math.cos(angle)*(arena.width//3)
        sy = cy + math.sin(angle)*(arena.height//3)
        dx = -math.cos(angle)*2.2
        dy = -math.sin(angle)*2.2
        en.bullets.append([float(sx),float(sy),dx,dy,14,(255,0,100)])

def boss_evil_cage(en, arena):
    """12 куль з центру розлітаються назовні"""
    cx,cy = arena.centerx,arena.centery
    for i in range(12):
        angle = i*math.pi/6
        dx = math.cos(angle)*2.0
        dy = math.sin(angle)*2.0
        en.bullets.append([float(cx),float(cy),dx,dy,13,(255,120,0)])


# ════════════════════════════════════════════
# КЛАС ENEMY — звичайний ворог
# у лабіринті — кольоровий квадрат
# у битві — текстура
# ════════════════════════════════════════════
class enemy:
    def __init__(self, col, row, name, hp, color, attacks, key_pos, spawn_after, texture=None):
        self.col = col
        self.row = row
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.color = color
        self.attacks = attacks
        self.key_pos = key_pos
        self.spawn_after = spawn_after
        self.texture = texture       # текстура для відображення у битві
        self.alive = True
        self.spared = False
        self.act_count = 0
        self.attack_phase = "player_turn"
        self.bullets = []
        self.current_attack = 0
        self.phase_timer = 0

    def world_rect(self):
        """Хітбокс на карті — квадрат"""
        return Rect(self.col*T+5,self.row*T+5,T-10,T-10)

    def draw_world(self, surf, ox, oy):
        """У лабіринті — завжди квадрат з '!'"""
        if not self.alive: return
        r = self.world_rect()
        draw.rect(surf,self.color,Rect(r.x+ox,r.y+oy,r.w,r.h),border_radius=6)
        f = font.SysFont(None,22)
        txt = f.render("!",True,(255,255,255))
        surf.blit(txt,(r.x+ox+r.w//2-txt.get_width()//2,r.y+oy+r.h//2-txt.get_height()//2))

    def draw_battle(self, surf):
        """У битві — текстура якщо є, інакше квадрат"""
        ex,ey = SCREEN_W//2, 170
        if self.texture:
            # центруємо текстуру
            tw, th = self.texture.get_size()
            surf.blit(self.texture, (ex - tw//2, ey - th//2))
        else:
            draw.rect(surf,self.color,Rect(ex-50,ey-50,100,100),border_radius=10)

        # ім'я і HP бар завжди
        f = font.SysFont(None,36)
        txt = f.render(self.name,True,(255,255,255))
        # ім'я над спрайтом
        surf.blit(txt,(ex-txt.get_width()//2, ey-75))
        bar_w = 200
        hp_r = max(0,self.hp/self.max_hp)
        bar_y = ey + 70
        draw.rect(surf,(60,60,60),Rect(ex-bar_w//2,bar_y,bar_w,12))
        draw.rect(surf,(220,50,50),Rect(ex-bar_w//2,bar_y,int(bar_w*hp_r),12))
        f2 = font.SysFont(None,24)
        t2 = f2.render(f"HP {self.hp}/{self.max_hp}",True,(200,200,200))
        surf.blit(t2,(ex-t2.get_width()//2,bar_y+14))

    def can_spare(self): return self.act_count >= 2

    def start_attack(self, arena):
        self.bullets.clear()
        self.attacks[self.current_attack % len(self.attacks)](self,arena)
        self.current_attack += 1
        self.phase_timer = 180
        self.attack_phase = "enemy_turn"

    def update_attack(self, arena, soul_obj):
        for b in self.bullets[:]:
            if len(b)>6 and b[6]>0:
                b[6] -= 1; continue
            b[0]+=b[2]; b[1]+=b[3]
            br = Rect(b[0]-5,b[1]-5,10,10)
            if soul_obj.invincible<=0 and br.colliderect(soul_obj.get_rect()):
                soul_obj.take_damage(b[4])
                self.bullets.remove(b)
            elif not arena.colliderect(br):
                self.bullets.remove(b)
        self.phase_timer -= 1
        if self.phase_timer <= 0:
            self.bullets.clear()
            self.attack_phase = "player_turn"

    def draw_bullets(self, surf):
        for b in self.bullets:
            if len(b)>6 and b[6]>0: continue
            draw.circle(surf,b[5],(int(b[0]),int(b[1])),6)

    def get_spawn_pos(self):
        c,r = self.spawn_after
        return float(c*T+(T-PLAYER_SIZE)//2), float(r*T+(T-PLAYER_SIZE)//2)


# ════════════════════════════════════════════
# КЛАС BOSS_GOOD_ENDING — бос лабіринту
# пацифіст: золотий з текстурою saver.png
# геноцид: червоний, переродження
# ════════════════════════════════════════════
class boss_good_ending:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.name = "Хранитель"
        self.hp = 300
        self.max_hp = 300
        self.color = (200,160,50)
        self.evil_form = False
        self.alive = True
        self.spared = False
        self.act_count = 0
        self.attack_phase = "player_turn"
        self.bullets = []
        self.current_attack = 0
        self.phase_timer = 0
        self.reborn_flash = 0
        self._set_normal_attacks()

    def _set_normal_attacks(self):
        self.attacks = [boss_attack_walls,boss_attack_laser,boss_attack_spiral_fast,
                        boss_attack_chase,boss_attack_rain_heavy,boss_attack_bounce]

    def _set_evil_attacks(self):
        self.attacks = [boss_evil_walls,boss_evil_laser,boss_evil_spiral,
                        boss_evil_cross,boss_evil_cage]

    def reborn(self):
        """Переродження у геноцидну форму"""
        self.evil_form = True
        self.hp = 400
        self.max_hp = 400
        self.name = "Хранитель ГНІВУ"
        self.color = (180,0,0)
        self.current_attack = 0
        self.bullets.clear()
        self.reborn_flash = 60
        self._set_evil_attacks()

    def world_rect(self):
        return Rect(self.col*T+2,self.row*T+2,T-4,T-4)

    def trigger_rect(self):
        """Зона тригера — весь коридор"""
        return Rect((self.col-1)*T, self.row*T, T*3, T)

    def draw_world(self, surf, ox, oy):
        """У лабіринті — квадрат (не текстура)"""
        if not self.alive: return
        r = self.world_rect()
        c = self.color
        if self.reborn_flash > 0:
            t = self.reborn_flash/60
            c = (min(255,int(255*t+self.color[0]*(1-t))),
                 min(255,int(255*t+self.color[1]*(1-t))),
                 min(255,int(255*t+self.color[2]*(1-t))))
        draw.rect(surf,c,Rect(r.x+ox,r.y+oy,r.w,r.h),border_radius=8)
        border_col = (255,50,50) if self.evil_form else (255,220,100)
        draw.rect(surf,border_col,Rect(r.x+ox,r.y+oy,r.w,r.h),3,border_radius=8)
        f = font.SysFont(None,15)
        label = "ГНІВ" if self.evil_form else "БOСС"
        txt = f.render(label,True,(255,255,255))
        surf.blit(txt,(r.x+ox+r.w//2-txt.get_width()//2,r.y+oy+r.h//2-txt.get_height()//2))

    def draw_battle(self, surf):
        """У битві — saver.png для пацифіста, saver_evil.png для геноциду"""
        ex,ey = SCREEN_W//2, 160

        if not self.evil_form:
            # ── пацифістська форма — saver.png ──
            if TEX_SAVER:
                tw, th = TEX_SAVER.get_size()
                if self.reborn_flash > 0:
                    # мигання при переродженні — поступово зникає
                    s = Surface((tw,th))
                    s.blit(TEX_SAVER,(0,0))
                    s.set_alpha(int(255*(1-self.reborn_flash/60)))
                    surf.blit(s,(ex-tw//2, ey-th//2))
                else:
                    surf.blit(TEX_SAVER,(ex-tw//2, ey-th//2))
            else:
                draw.rect(surf,self.color,Rect(ex-70,ey-60,140,120),border_radius=12)
                draw.rect(surf,(255,220,100),Rect(ex-70,ey-60,140,120),3,border_radius=12)
        else:
            # ── геноцидна форма — saver_evil.png ──
            if TEX_SAVER_EVIL:
                tw, th = TEX_SAVER_EVIL.get_size()
                if self.reborn_flash > 0:
                    # поступово проявляється після переродження
                    s = Surface((tw,th))
                    s.blit(TEX_SAVER_EVIL,(0,0))
                    s.set_alpha(int(255*(self.reborn_flash/60)))
                    surf.blit(s,(ex-tw//2, ey-th//2))
                else:
                    surf.blit(TEX_SAVER_EVIL,(ex-tw//2, ey-th//2))
            else:
                # запасний варіант якщо текстура не завантажилась
                draw.rect(surf,self.color,Rect(ex-70,ey-60,140,120),border_radius=12)
                draw.rect(surf,(255,50,50),Rect(ex-70,ey-60,140,120),3,border_radius=12)

        # ім'я
        f = font.SysFont(None,28)
        name_col = (255,50,50) if self.evil_form else (255,220,100)
        txt = f.render(self.name,True,name_col)
        surf.blit(txt,(ex-txt.get_width()//2, ey-85))

        # HP бар
        bar_w = 400
        hp_r = max(0,self.hp/self.max_hp)
        bar_y = ey + 80
        draw.rect(surf,(60,60,60),Rect(ex-bar_w//2,bar_y,bar_w,16))
        bar_col = (220,0,0) if self.evil_form else (220,180,0)
        draw.rect(surf,bar_col,Rect(ex-bar_w//2,bar_y,int(bar_w*hp_r),16))
        f2 = font.SysFont(None,24)
        t2 = f2.render(f"HP {self.hp}/{self.max_hp}",True,(255,100,100) if self.evil_form else (255,220,100))
        surf.blit(t2,(ex-t2.get_width()//2,bar_y+18))

        if self.evil_form:
            f3 = font.SysFont(None,22)
            warn = f3.render("ПЕРЕРОДЖЕННЯ",True,(255,80,80))
            surf.blit(warn,(ex-warn.get_width()//2,ey-110))

    def can_spare(self):
        return self.act_count >= 6 and not self.evil_form

    def start_attack(self, arena):
        self.bullets.clear()
        self.attacks[self.current_attack % len(self.attacks)](self,arena)
        self.current_attack += 1
        self.phase_timer = 150 if self.evil_form else 200
        self.attack_phase = "enemy_turn"

    def update_attack(self, arena, soul_obj):
        if self.reborn_flash > 0:
            self.reborn_flash -= 1
        for b in self.bullets[:]:
            if len(b)>6 and b[6]>0:
                b[6] -= 1; continue
            b[0]+=b[2]; b[1]+=b[3]
            br = Rect(b[0]-5,b[1]-5,10,10)
            if soul_obj.invincible<=0 and br.colliderect(soul_obj.get_rect()):
                soul_obj.take_damage(b[4])
                self.bullets.remove(b)
            elif not arena.colliderect(br):
                self.bullets.remove(b)
        self.phase_timer -= 1
        if self.phase_timer <= 0:
            self.bullets.clear()
            self.attack_phase = "player_turn"

    def draw_bullets(self, surf):
        for b in self.bullets:
            if len(b)>6 and b[6]>0: continue
            r = 8 if self.evil_form else 7
            draw.circle(surf,b[5],(int(b[0]),int(b[1])),r)




# ════════════════════════════════════════════
# КЛАС FIGHT — логіка вікна битви
# ════════════════════════════════════════════
class fight:
    def __init__(self, enemy_obj, is_boss=False):
        self.enemy = enemy_obj
        self.soul = soul()
        self.buttons = button(is_boss=is_boss)
        self.is_boss = is_boss
        self.state = "buttons"
        self.result = None
        self.message = ""
        self.message_timer = 0
        self.font = font.SysFont(None,30)
        self.big_font = font.SysFont(None,60)
        if is_boss:
            self.arena = Rect(SCREEN_W//2-220,SCREEN_H//2-60,440,200)
        else:
            self.arena = Rect(SCREEN_W//2-160,SCREEN_H//2-20,320,160)
        self.soul.x = self.arena.centerx
        self.soul.y = self.arena.centery
        self.waiting_confirm = False
        self.reborn_timer = 0

    def handle_event(self, e):
        if e.type != KEYDOWN: return
        if self.state == "result":
            if e.key == K_RETURN: self.waiting_confirm = False
            return
        if self.state == "reborn_pause":
            return
        if self.state == "buttons":
            self.buttons.handle(e)
            if e.key == K_RETURN:
                action = self.buttons.get_selected()

                if action == "FIGHT":
                    if (self.is_boss and kills_total > 0
                            and isinstance(self.enemy,boss_good_ending)
                            and not self.enemy.evil_form):
                        self.enemy.hp = 0
                        self.message = ""
                        self.message_timer = 0
                        self.state = "reborn_pause"
                        self.reborn_timer = 120
                    else:
                        dmg = random.randint(20,40) if self.is_boss else random.randint(15,30)
                        self.enemy.hp -= dmg
                        self.message = f"Завдано {dmg} шкоди!"
                        self.message_timer = 60
                        if self.enemy.hp <= 0:
                            self.result = "win_kill"
                            self.state = "result"
                            self.waiting_confirm = True
                        else:
                            self.state = "enemy_attack"
                            self.enemy.start_attack(self.arena)

                elif action == "ACT":
                    if self.is_boss and isinstance(self.enemy,boss_good_ending) and self.enemy.evil_form:
                        self.message = "Він більше не слухає тебе..."
                    else:
                        self.enemy.act_count += 1
                        needed = 6 if self.is_boss else 2
                        msgs_boss = ["Ти намагаєшся порозумітися...",
                                     "Хранитель здивований...",
                                     "Він починає вагатися...",
                                     "Хранитель слухає тебе...",
                                     "Майже переконав його...",
                                     "Ще одне зусилля..."]
                        if self.enemy.act_count < needed:
                            self.message = msgs_boss[min(self.enemy.act_count-1,5)] if self.is_boss else "Ти говориш з ворогом..."
                        else:
                            self.message = "Хранитель готовий відступити!" if self.is_boss else "Ворог готовий здатись!"
                    self.message_timer = 80
                    self.state = "enemy_attack"
                    self.enemy.start_attack(self.arena)

                elif action == "MERCY":
                    if self.is_boss and isinstance(self.enemy,boss_good_ending) and self.enemy.evil_form:
                        self.message = "Він не прийме милосердя!"
                        self.message_timer = 80
                        self.state = "enemy_attack"
                        self.enemy.start_attack(self.arena)
                    elif self.enemy.can_spare():
                        self.result = "win_spare"
                        self.state = "result"
                        self.waiting_confirm = True
                    else:
                        needed = 6 if self.is_boss else 2
                        left = needed - self.enemy.act_count
                        self.message = f"Ще {left} раз(и) ACT!"
                        self.message_timer = 80
                        self.state = "enemy_attack"
                        self.enemy.start_attack(self.arena)

    def update(self):
        self.soul.update()
        if self.message_timer > 0: self.message_timer -= 1

        if self.state == "enemy_attack":
            self.soul.move(self.arena)
            self.enemy.update_attack(self.arena,self.soul)
            if self.enemy.attack_phase == "player_turn":
                self.state = "buttons"
            if self.soul.hp <= 0:
                self.result = "lose"
                self.state = "result"
                self.waiting_confirm = True

        elif self.state == "reborn_pause":
            self.reborn_timer -= 1
            if self.reborn_timer <= 0:
                self.enemy.reborn()
                self.state = "enemy_attack"
                self.enemy.start_attack(self.arena)

    def draw(self, surf):
        if self.is_boss and isinstance(self.enemy,boss_good_ending) and self.enemy.evil_form:
            surf.fill((20,5,5))
        else:
            surf.fill((10,10,10))

        self.enemy.draw_battle(surf)

        if self.message_timer > 0:
            col = (255,80,80) if (self.is_boss and isinstance(self.enemy,boss_good_ending) and self.enemy.evil_form) else (255,255,255)
            txt = self.font.render(self.message,True,col)
            surf.blit(txt,(SCREEN_W//2-txt.get_width()//2,SCREEN_H//2-140))

        draw.rect(surf,(255,255,255),self.arena,3)
        self.enemy.draw_bullets(surf)

        if self.state in ("enemy_attack","reborn_pause"):
            self.soul.draw(surf)

        bar_w = 300
        hp_r = max(0,self.soul.hp/self.soul.max_hp)
        bx,by = SCREEN_W//2-bar_w//2,SCREEN_H-130
        f2 = font.SysFont(None,26)
        surf.blit(f2.render("HP",True,(255,255,0)),(bx-40,by+4))
        draw.rect(surf,(60,60,60),Rect(bx,by,bar_w,18))
        draw.rect(surf,(80,220,80),Rect(bx,by,int(bar_w*hp_r),18))
        surf.blit(f2.render(f"{self.soul.hp}/{self.soul.max_hp}",True,(255,255,255)),(bx+bar_w+10,by+2))

        if self.state == "buttons":
            self.buttons.draw(surf)
        elif self.state == "result":
            if self.result == "win_kill":    msg = self.big_font.render("ПЕРЕМОЖЕНО!",True,(220,50,50))
            elif self.result == "win_spare": msg = self.big_font.render("ПОМИЛУВАНО!",True,(80,220,80))
            else:                            msg = self.big_font.render("ТИ ЗАГИНУВ",True,(200,200,200))
            surf.blit(msg,(SCREEN_W//2-msg.get_width()//2,SCREEN_H//2-20))
            hint = self.font.render("Натисни Enter щоб продовжити",True,(150,150,150))
            surf.blit(hint,(SCREEN_W//2-hint.get_width()//2,SCREEN_H//2+50))

    def is_done(self):
        return self.state == "result" and not self.waiting_confirm


class Keys:
    def __init__(self):
        self.count = 0
    def add_key(self): self.count += 1
    def has_all(self): return self.count >= 2
class secret_key:
    def __init__(self):
        self.count = 0
    def add_key(self) : self.count += 1
    def has_all(self): return self.count >= 1


# ════════════════════════════════════════════
# КЛАС LABIRINT — ігровий світ
# ════════════════════════════════════════════
class labirint:
    def __init__(self):
        self.keys_pos = []
        self.door_pos = None
        self.exit_pos = None
        self.enemies = []
        self.walls = []
        self.boss = None
        self._parse_map()
        self._place_enemies()

    def _parse_map(self):
        for ri,row in enumerate(maze_map):
            for ci,cell in enumerate(row):
                if cell==1:   self.walls.append(Rect(ci*T,ri*T,T,T))
                elif cell==2: self.keys_pos.append([ci,ri])
                elif cell==3: self.door_pos=[ci,ri]
                elif cell==4: self.exit_pos=[ci,ri]
                elif cell==5: self.boss=boss_good_ending(ci,ri)

    def _place_enemies(self):
        """Вороги отримують текстури для битви"""
        self.enemies.append(enemy(
            col=17,row=11,name="Слиз",hp=60,color=(80,180,80),
            attacks=[attack_rain,attack_sides],
            key_pos=(17,12),spawn_after=(16,12),
            texture=TEX_SLIME   # текстура slime.png у битві
        ))
        self.enemies.append(enemy(
            col=2,row=17,name="Тінь",hp=80,color=(120,80,200),
            attacks=[attack_spiral,attack_cross],
            key_pos=(1,17),spawn_after=(3,16),
            texture=TEX_SHADOW  # текстура shadow.png у битві
        ))

    def is_solid(self, col, row, door_open):
        if row<0 or row>=len(maze_map) or col<0 or col>=len(maze_map[0]): return True
        if maze_map[row][col]==1: return True
        if maze_map[row][col]==3 and not door_open: return True
        return False

    def collides_at(self, x, y, door_open):
        for cx,cy in [(x+1,y+1),(x+PLAYER_SIZE-1,y+1),
                      (x+1,y+PLAYER_SIZE-1),(x+PLAYER_SIZE-1,y+PLAYER_SIZE-1)]:
            if self.is_solid(int(cx//T),int(cy//T),door_open): return True
        return False

    def check_enemy_contact(self, px, py):
        pr = Rect(px,py,PLAYER_SIZE,PLAYER_SIZE)
        for en in self.enemies:
            if en.alive and pr.colliderect(en.world_rect()):
                return en, False
        if self.boss and self.boss.alive and pr.colliderect(self.boss.trigger_rect()):
            return self.boss, True
        return None, False

    def check_key_pickup(self, px, py, keys_obj):
        pr = Rect(px,py,PLAYER_SIZE,PLAYER_SIZE)
        for kp in self.keys_pos[:]:
            guarded = any(en.alive and en.key_pos==(kp[0],kp[1]) for en in self.enemies)
            if guarded: continue
            kr = Rect(kp[0]*T+10,kp[1]*T+10,T-20,T-20)
            if pr.colliderect(kr):
                self.keys_pos.remove(kp)
                maze_map[kp[1]][kp[0]] = 0
                keys_obj.add_key()

    def check_exit(self, px, py, door_open):
        if not door_open: return False
        if self.boss and self.boss.alive: return False
        if not self.exit_pos: return False
        pr = Rect(px,py,PLAYER_SIZE,PLAYER_SIZE)
        er = Rect(self.exit_pos[0]*T,self.exit_pos[1]*T,T,T)
        return pr.colliderect(er)

    def draw(self, surf, ox, oy, door_open):
        for ri,row in enumerate(maze_map):
            for ci,cell in enumerate(row):
                if cell==1:   color=(20,20,20)
                elif cell==4: color=(0,120,0) if (self.boss and not self.boss.alive) else (30,60,30)
                else:         color=(50,50,50)
                draw.rect(surf,color,Rect(ci*T+ox,ri*T+oy,T,T))

        # ключі — текстура key.jpg якщо є, інакше жовтий квадрат
        for kp in self.keys_pos:
            guarded = any(en.alive and en.key_pos==(kp[0],kp[1]) for en in self.enemies)
            if not guarded:
                kx = kp[0]*T+10+ox
                ky = kp[1]*T+10+oy
                if TEX_KEY:
                    surf.blit(TEX_KEY,(kx, ky))
                else:
                    draw.rect(surf,(255,215,0),Rect(kx,ky,T-20,T-20))

        dp = self.door_pos
        draw.rect(surf,(50,50,50) if door_open else (139,69,19),
                  Rect(dp[0]*T+ox,dp[1]*T+oy,T,T))
        for en in self.enemies:
            en.draw_world(surf,ox,oy)
        if self.boss:
            self.boss.draw_world(surf,ox,oy)


# ── Ініціалізація ─────────────────────────────
lab = labirint()
keys_obj = Keys()
door_open = False
player_x = float(T+(T-PLAYER_SIZE)//2)
player_y = float(T+(T-PLAYER_SIZE)//2)
clock = time.Clock()
game_state = "exploration"
current_fight = None
current_enemy = None
current_is_boss = False
hud_font = font.SysFont(None,36)
big_font = font.SysFont(None,80)
small_font = font.SysFont(None,40)

# ── Головний цикл ─────────────────────────────
while True:
    events = event.get()
    for e in events:
        if e.type == QUIT:
            quit()

    if game_state == "win":
        is_pacifist = kills_total == 0
        window.fill((10,10,30) if is_pacifist else (20,5,5))
        for i in range(60):
            random.seed(i*7)
            col = (255,255,200) if is_pacifist else (255,80,80)
            draw.circle(window,col,
                        (random.randint(0,SCREEN_W),random.randint(0,SCREEN_H)),
                        random.randint(1,3))
        if is_pacifist:
            window.blit(big_font.render("ВИ ПЕРЕМОГЛИ!",True,(255,220,50)),
                        (SCREEN_W//2-big_font.size("ВИ ПЕРЕМОГЛИ!")[0]//2,SCREEN_H//2-120))
            window.blit(small_font.render("Ти пройшов лабіринт з добрим серцем.",True,(200,200,255)),
                        (SCREEN_W//2-small_font.size("Ти пройшов лабіринт з добрим серцем.")[0]//2,SCREEN_H//2-30))
            window.blit(small_font.render("Ніхто не постраждав.",True,(150,255,150)),
                        (SCREEN_W//2-small_font.size("Ніхто не постраждав.")[0]//2,SCREEN_H//2+20))
        else:
            window.blit(big_font.render("ТИ ВИЙШОВ...",True,(200,50,50)),
                        (SCREEN_W//2-big_font.size("ТИ ВИЙШОВ...")[0]//2,SCREEN_H//2-120))
            window.blit(small_font.render("Лабіринт запам'ятав твої вчинки.",True,(200,100,100)),
                        (SCREEN_W//2-small_font.size("Лабіринт запам'ятав твої вчинки.")[0]//2,SCREEN_H//2-30))
            window.blit(small_font.render(f"Вбивств: {kills_total}",True,(255,80,80)),
                        (SCREEN_W//2-small_font.size(f"Вбивств: {kills_total}")[0]//2,SCREEN_H//2+20))
        window.blit(small_font.render("Натисни Esc щоб вийти",True,(150,150,150)),
                    (SCREEN_W//2-small_font.size("Натисни Esc щоб вийти")[0]//2,SCREEN_H//2+100))
        for e in events:
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                quit()

    elif game_state == "exploration":
        pressed = key.get_pressed()
        dx,dy = 0,0
        if pressed[K_w]: dy -= 3
        if pressed[K_s]: dy += 3
        if pressed[K_d]: dx += 3
        if pressed[K_a]: dx -= 3

        step_x = 1 if dx>0 else -1
        for _ in range(abs(dx)):
            if not lab.collides_at(player_x+step_x,player_y,door_open):
                player_x += step_x
        step_y = 1 if dy>0 else -1
        for _ in range(abs(dy)):
            if not lab.collides_at(player_x,player_y+step_y,door_open):
                player_y += step_y

        lab.check_key_pickup(int(player_x),int(player_y),keys_obj)
        if keys_obj.has_all():
            door_open = True

        if lab.check_exit(int(player_x),int(player_y),door_open):
            game_state = "win"

        touched,is_boss = lab.check_enemy_contact(int(player_x),int(player_y))
        if touched:
            current_enemy = touched
            current_is_boss = is_boss
            current_fight = fight(touched,is_boss=is_boss)
            game_state = "battle"

        px,py = int(player_x),int(player_y)
        ox = SCREEN_W//2-px-PLAYER_SIZE//2
        oy = SCREEN_H//2-py-PLAYER_SIZE//2

        window.fill((80,80,80))
        lab.draw(window,ox,oy,door_open)
        draw.rect(window,(200,200,200),
                  Rect(SCREEN_W//2-PLAYER_SIZE//2,SCREEN_H//2-PLAYER_SIZE//2,PLAYER_SIZE,PLAYER_SIZE))
        window.blit(hud_font.render(f"Ключі: {keys_obj.count}/2",True,(255,255,255)),(20,20))
        window.blit(hud_font.render(f"Вбивств: {kills_total}",True,(255,100,100)),(20,55))
        if door_open:
            window.blit(hud_font.render("Двері відчинені!",True,(0,255,0)),(20,90))

    elif game_state == "battle":
        for e in events:
            current_fight.handle_event(e)
        current_fight.update()
        current_fight.draw(window)

        if current_fight.is_done():
            res = current_fight.result
            en = current_enemy
            if res == "win_kill":
                en.alive = False
                kills_total += 1
                if current_is_boss:
                    player_x = float(lab.boss.col*T+(T-PLAYER_SIZE)//2)
                    player_y = float((lab.boss.row-1)*T+(T-PLAYER_SIZE)//2)
                else:
                    player_x,player_y = en.get_spawn_pos()
            elif res == "win_spare":
                en.alive = False
                en.spared = True
                if current_is_boss:
                    player_x = float(lab.boss.col*T+(T-PLAYER_SIZE)//2)
                    player_y = float((lab.boss.row-1)*T+(T-PLAYER_SIZE)//2)
                else:
                    player_x,player_y = en.get_spawn_pos()
            else:
                player_x = float(T+(T-PLAYER_SIZE)//2)
                player_y = float(T+(T-PLAYER_SIZE)//2)

            game_state = "exploration"
            current_fight = None
            current_enemy = None
            current_is_boss = False

    display.update()
    clock.tick(60)