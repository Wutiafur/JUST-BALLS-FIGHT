import sys
import math
import random
import pygame

# ================= 极简风格配置 (Minimalist Config) ================= #

# 1. 配色方案：深色背景 + 柔和扁平色块
THEME = {
    "bg": (40, 44, 52),             # 游戏主背景（深蓝灰）
    "grid": (45, 50, 60),           # 背景网格线
    "ui_panel_bg": (33, 37, 43),    # 右侧UI面板背景
    "card_bg": (50, 55, 65),        # 实体卡片背景
    "text_main": (220, 223, 228),   # 主文字色
    "text_sub": (150, 155, 165),    # 副文字色
    "accent": (97, 175, 239),       # 强调色（亮蓝）
    "hp_bar_bg": (30, 30, 35),      # 血条底色
    "hp_bar_fill": (224, 108, 117), # 血条填充（柔和红）
    "shield_fill": (152, 195, 121), # 护盾填充（柔和绿）
    "fire_bar": (178, 102, 255),    # 烈火条
    "cold_bar": (86, 182, 255),     # 寒冰条
    "border": (255, 255, 255),      # 实体描边
}

# 2. 实体色板 (莫兰迪/扁平风格)
COLOR_PALETTE = [
    (152, 195, 121), # Green
    (224, 108, 117), # Red
    (97, 175, 239),  # Blue
    (229, 192, 123), # Yellow
    (198, 120, 221), # Purple
    (86, 182, 194),  # Cyan
    (209, 154, 102), # Orange
    (171, 178, 191), # Grey
]

# ================= 游戏参数 (Game Constants) ================= #

UI_HEIGHT = 0   # 底部高度设为0，我们将UI整合到右侧侧边栏
COUNTER_WIDTH = 220 # 加宽右侧侧边栏以容纳更多信息

BUFF_DURATION = 4.0
ITEM_INTERVAL_MIN = 5.0
ITEM_INTERVAL_MAX = 8.0
ITEM_MAX_COUNT = 3
BULLET_SPEED = 420.0
HEX_BURST_COUNT = 6
HEX_BURST_DELAY = 2.0
AURA_COLOR = (229, 192, 123) # 金色光环
AURA_TEETH = 12
AURA_OUTER_OFFSET = 8
AURA_INNER_OFFSET = 3
AURA_WIDTH = 2
SPIKE_DURATION = 2.0
SPEED_SCALE = 1.25
SPIKE_BAND = 12
SPIKE_TOOTH_W = 12
SPIKE_TOOTH_H = 10
FLASH_DURATION = 0.3
SWEEP_SPEED = 480
MAX_HP = 5
ENTITY_RADIUS = 20
AOE_DURATION = 5.0
MIN_SPEED = 80.0
BALL_MIN_SPEED = 120.0
TRAIL_EFFECT_DURATION = 2.0
TRAIL_SEG_LIFE = 1.0
TRAIL_EMIT_INTERVAL = 0.08
RIPPLE_DURATION = 2.0
RIPPLE_SCALE = 3.0
FREEZE_RIPPLE_TOTAL = 6.0
FREEZE_RIPPLE_INTERVAL = 2.0
FREEZE_STUN_TIME = 1.0
BURN_DURATION = 9.0
BURN_TICK_INTERVAL = 3.0
FROST_STUN_DURATION = 5.0
FIRE_STACK_MAX = 6
COLD_STACK_MAX = 5
ELEMENT_IMMUNE_DURATION = 4.0
ELEMENT_EXPLOSION_DURATION = 0.4
ELEMENT_EXPLOSION_SCALE = 2.0
ELEMENT_EXPLOSION_DAMAGE = 2
SHIELD_MAX = 5
CURSE_MARK_DURATION = 0.6
HURT_SPEED_DURATION = 1.0
HURT_SLOW_DURATION = 3.0
HURT_SLOW_MULT = 0.7
DRONE_CD = 8.0
DRONE_SPEED = 520.0
DRONE_RADIUS = 8
DRONE_GAIN_INTERVAL = 20.0
DRONE_MAX_COUNT = 3
WALL_DURATION = 15.0

ASSASSIN_BURST = 1.0
ASSASSIN_COOLDOWN = 3.5
ASSASSIN_SPEED_MULT = 1.8
ASSASSIN_CHARGE_TRIGGER_SPEED = 520.0  # 刺客边界叠速触发值
ASSASSIN_CHARGE_TRIGGER_SPEED = 520.0
TANK_SPEED_SCALE = 0.65
TANK_MASS = 4.0
TANK_SHOCK_CD = 5.0
TANK_SHOCK_RADIUS = 180
TANK_SHOCK_FORCE = 360
TANK_EXTRA_HP = 5
MAGE_ORB_INTERVAL = 5.0
MAGE_MAX_ORBS = 2
TIME_SLOW_CD = 7.0
TIME_SLOW_DURATION = 2.0
TIME_SLOW_RADIUS = 200
TIME_SLOW_SCALE = 0.55
GRAVITY_CD = 8.0
GRAVITY_DURATION = 1.6
GRAVITY_RADIUS_SCALE = 1.5
GRAVITY_FORCE = 220
HUNTER_TURN_RATE = 0.9
HUNTER_SHOT_CD = 8.0
LIGHTNING_CD = 10.0
LIGHTNING_MAX_TARGET = 3
LIGHTNING_PUSH = 220
LIGHTNING_LIFE = 0.25
TETHER_MAX_DIST = 200
DEMON_RAGE_MAX = 88
DEMON_SHRINK_SCALE = 0.5
DEMON_SHOT_CD = 4.0
DEMON_SHOT_COUNT = 2
DEMON_HOST_HEAL = 5
DEMON_RING_COLOR = (210, 70, 70)
DEMON_ORBIT_SPEED = 2.5

PHOENIX_PERCH_INTERVAL = 20.0
PHOENIX_PERCH_REST = 3.0
PHOENIX_EGG_HP = 12
PHOENIX_EGG_DURATION = 15.0
PHOENIX_WAVE_INTERVAL = 4.0
PHOENIX_WAVE_DURATION = 1.0
PHOENIX_WAVE_SCALE = 5.0
PHOENIX_WAVE_PUSH = 240
PHOENIX_SHIELD_RATIO = 0.5

ENV_START_TIME = 60.0
POISON_SHRINK_DURATION = 30.0
POISON_DAMAGE_INTERVAL = 4.0
ELECTRIC_WALL_INTERVAL = 10.0
ELECTRIC_WALL_DURATION = 20.0
ELECTRIC_WALL_ATTRACT = 140.0
THUNDER_INTERVAL = 10.0
OVERLOAD_EXTRA_MIN = 2
OVERLOAD_EXTRA_MAX = 3

ENV_CRISIS_OPTIONS = {
    "none": {"name": "无", "desc": "无特殊环境效果。"},
    "poison": {"name": "毒圈", "desc": "60秒后边界向内缩圈，圈外每4秒掉1点，30秒后全场有毒。"},
    "electric": {"name": "电墙", "desc": "60秒后每10秒随机一面墙变黄20秒，撞击掉1血并被轻微吸引。"},
    "thunder": {"name": "雷霆", "desc": "60秒后每10秒随机打击1个实体并连锁最近目标，各造成1-3点伤害。"},
    "overload": {"name": "过载", "desc": "60秒后捡道具会额外触发随机2-3次，并对拾取者造成1点伤害。"},
    "random": {"name": "随机", "desc": "开局随机选择一种环境危机。"},
}

# 优先字体
PREFERRED_FONTS = [
    "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "SimSun",
    "Noto Sans CJK SC", "Source Han Sans SC", "Arial Unicode MS", "Arial"
]

SCENES = [
    {
        "name": "基础场景",
        "shape": "rect",
        "time_limit": 60,
        "blocks": [
            {"pos": (200, 200), "vel": (220, 150), "color": COLOR_PALETTE[0]},
            {"pos": (450, 300), "vel": (-180, -140), "color": COLOR_PALETTE[1]},
        ],
        "balls": [
            {"pos": (320, 160), "vel": (160, 140), "color": COLOR_PALETTE[2]},
            {"pos": (520, 260), "vel": (-140, -160), "color": COLOR_PALETTE[3]},
        ],
    },
    {
        "name": "高速乱斗",
        "shape": "rect",
        "time_limit": 60,
        "blocks": [
            {"pos": (150, 250), "vel": (260, 210), "color": COLOR_PALETTE[6]},
        ],
        "balls": [
            {"pos": (300, 200), "vel": (260, 220), "color": COLOR_PALETTE[2]},
            {"pos": (380, 260), "vel": (-240, 170), "color": COLOR_PALETTE[4]},
            {"pos": (460, 220), "vel": (230, -190), "color": COLOR_PALETTE[0]},
            {"pos": (540, 260), "vel": (-260, -200), "color": COLOR_PALETTE[3]},
        ],
    },
    {
        "name": "无尽模式",
        "shape": "circle",
        "time_limit": None,
        "blocks": [
            {"pos": (240, 260), "vel": (240, 200), "color": COLOR_PALETTE[4]},
            {"pos": (520, 320), "vel": (-200, 180), "color": COLOR_PALETTE[1]},
        ],
        "balls": [
            {"pos": (360, 200), "vel": (200, -180), "color": COLOR_PALETTE[5]},
            {"pos": (620, 240), "vel": (-220, 190), "color": COLOR_PALETTE[3]},
        ],
    },
]

MAPS = [
    {"name": "标准方形", "width": 720, "height": 720, "shape": "rect", "border_margin": 40},
    {"name": "宽屏方形", "width": 1080, "height": 720, "shape": "rect", "border_margin": 40},
    {"name": "大圆形", "width": 960, "height": 720, "shape": "circle", "border_margin": 50},
]

# 用于时间覆盖的默认哨兵
TIME_OVERRIDE_DEFAULT = object()
CURRENT_GAME = None

PROFESSIONS = ["assassin", "tank", "mage", "time", "gravity", "hunter", "lightning", "drone", "heavy", "vampire", "demon", "phoenix"]

PROFESSION_NAMES = {
    "assassin": "刺客", "tank": "坦克", "mage": "法师", "time": "时空",
    "gravity": "引力", "hunter": "猎手", "lightning": "闪电", "drone": "机械",
    "heavy": "巨力", "vampire": "吸血鬼", "demon": "恶魔", "phoenix": "凤凰",
}

# ================= 绘图辅助函数 ================= #

def draw_saw_ring(surface, cx, cy, base_radius):
    points = []
    outer = base_radius + AURA_OUTER_OFFSET
    inner = base_radius + AURA_INNER_OFFSET
    total_points = AURA_TEETH * 2
    for i in range(total_points):
        angle = 2 * math.pi * i / total_points
        r = outer if i % 2 == 0 else inner
        points.append((cx + math.cos(angle) * r, cy + math.sin(angle) * r))
    pygame.draw.polygon(surface, AURA_COLOR, points, width=AURA_WIDTH)

def draw_spike_edges(surface, rect, axis):
    x, y, w, h = rect
    def draw_teeth_horizontal(y_line, upward):
        dir_sign = -1 if upward else 1
        count = max(1, int(w // SPIKE_TOOTH_W))
        step = w / count
        for i in range(count):
            x0 = x + i * step
            x1 = x + (i + 1) * step
            xm = (x0 + x1) / 2
            apex = (xm, y_line + dir_sign * SPIKE_TOOTH_H)
            pygame.draw.polygon(surface, AURA_COLOR, [(x0, y_line), (x1, y_line), apex], width=1)
    def draw_teeth_vertical(x_line, leftward):
        dir_sign = -1 if leftward else 1
        count = max(1, int(h // SPIKE_TOOTH_W))
        step = h / count
        for i in range(count):
            y0 = y + i * step
            y1 = y + (i + 1) * step
            ym = (y0 + y1) / 2
            apex = (x_line + dir_sign * SPIKE_TOOTH_H, ym)
            pygame.draw.polygon(surface, AURA_COLOR, [(x_line, y0), (x_line, y1), apex], width=1)
    if axis == "tb":
        draw_teeth_horizontal(y, True)
        draw_teeth_horizontal(y + h, False)
    else:
        draw_teeth_vertical(x, True)
        draw_teeth_vertical(x + w, False)

def enforce_min_speed(vx, vy, minimum):
    speed = math.hypot(vx, vy)
    if speed >= minimum:
        return vx, vy
    if speed == 0:
        angle = random.uniform(0, 2 * math.pi)
        return math.cos(angle) * minimum, math.sin(angle) * minimum
    factor = minimum / speed
    return vx * factor, vy * factor

def draw_ui_rect(surface, rect, color, border_radius=6):
    """绘制半透明圆角矩形"""
    if len(color) == 4:
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, color, s.get_rect(), border_radius=border_radius)
        surface.blit(s, (rect.x, rect.y))
    else:
        pygame.draw.rect(surface, color, rect, border_radius=border_radius)

def draw_bar(surface, x, y, w, h, pct, color, bg_color=None):
    """绘制简约进度条"""
    if bg_color is None:
        bg_color = (0, 0, 0, 60)
    draw_ui_rect(surface, pygame.Rect(x, y, w, h), bg_color, border_radius=2)
    fill_w = max(0, int(w * pct))
    if fill_w > 0:
        draw_ui_rect(surface, pygame.Rect(x, y, fill_w, h), color, border_radius=2)

# ================= 实体类 ================= #

class EntityBase:
    """实体基类，提取公共属性"""
    def __init__(self, x, y, vx, vy, color):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        self.alive = True
        self.max_hp = MAX_HP
        self.hp = self.max_hp
        self.shield_hp = 0
        self.name = ""
        self.power = None
        self.power_timer = 0.0
        self.spike_axis = None
        self.pending_bullet = False
        self.death_effect_done = False
        self.profession = None
        self.mass = 1.0
        self.speed_base = 1.0
        self.speed_bonus = 1.0
        self.external_speed_scale = 1.0
        self.hurt_speed_timer = 0.0
        self.hurt_slow_timer = 0.0
        self.shield_charges = 0
        self.orb_angles = []
        self.mage_cd = 0.0
        self.assassin_cd = 0.0
        self.assassin_active = 0.0
        self.shock_cd = 0.0
        self.time_cd = 0.0
        self.time_active = 0.0
        self.gravity_cd = 0.0
        self.gravity_active = 0.0
        self.gravity_mode = 1
        self.lightning_cd = 0.0
        self.freeze_timer = 0.0
        self.frozen_velocity = (0.0, 0.0)
        self.fire_stacks = 0
        self.cold_stacks = 0
        self.burning = False
        self.burn_timer = 0.0
        self.burn_tick_timer = 0.0
        self.burn_source = None
        self.cold_frozen = False
        self.element_immunity = 0.0
        self.trail_emit_timer = 0.0
        self.vampire_marks = 0
        self.damage_from_tether = False
        self.demon_rage = 0
        self.demon_rage_max = DEMON_RAGE_MAX
        self.demon_target = None
        self.demon_host = None
        self.demon_possessing = False
        self.demon_shoot_cd = DEMON_SHOT_CD
        self.demon_shrunken = False
        self.demon_seeking = False
        self.demon_base_radius = None
        self.demon_base_w = None
        self.demon_base_h = None
        self.demon_orbit_angle = 0.0
        self.phoenix_perch_cd = 0.0
        self.phoenix_perching = False
        self.phoenix_rest_timer = 0.0
        self.phoenix_egg = False
        self.phoenix_egg_timer = 0.0
        self.phoenix_wave_cd = 0.0
        self.phoenix_rebirth_used = False
        self.phoenix_saved_radius = None
        self.phoenix_saved_w = None
        self.phoenix_saved_h = None
        self.phoenix_saved_max_hp = None

    def common_update_physics(self, dt, bounds_rect, w, h):
        self.x += self.vx * dt
        self.y += self.vy * dt
        hit_wall = False
        shape = bounds_rect["shape"]
        
        if shape == "rect":
            rect = bounds_rect["rect"]
            if self.x < rect.left:
                self.x = rect.left
                self.vx *= -1
                hit_wall = True
            elif self.x + w > rect.right:
                self.x = rect.right - w
                self.vx *= -1
                hit_wall = True
            if self.y < rect.top:
                self.y = rect.top
                self.vy *= -1
                hit_wall = True
            elif self.y + h > rect.bottom:
                self.y = rect.bottom - h
                self.vy *= -1
                hit_wall = True
        else:
            # Circle bounds logic (simplified center check)
            cx = self.x + w/2
            cy = self.y + h/2
            bx, by = bounds_rect["center"]
            r_bound = bounds_rect["radius"]
            dx = cx - bx
            dy = cy - by
            dist = math.hypot(dx, dy)
            # effective radius roughly
            my_r = max(w, h)/2
            if dist + my_r > r_bound:
                if dist == 0: dx, dy = 0.01, 0.01; dist=0.01
                nx, ny = dx/dist, dy/dist
                new_dist = r_bound - my_r
                cx = bx + nx * new_dist
                cy = by + ny * new_dist
                self.x = cx - w/2
                self.y = cy - h/2
                dot = self.vx * nx + self.vy * ny
                self.vx -= 2 * dot * nx
                self.vy -= 2 * dot * ny
                hit_wall = True
        
        self.vx, self.vy = enforce_min_speed(self.vx, self.vy, BALL_MIN_SPEED)
        return hit_wall

    def take_damage(self, attacker=None, redirect_chain=None):
        if not self.alive: return
        if redirect_chain is None:
            redirect_chain = set()
        if getattr(self, "demon_possessing", False) and getattr(self, "demon_host", None) and self.demon_host is not self and getattr(self.demon_host, "alive", False):
            if id(self) in redirect_chain:
                pass
            else:
                redirect_chain.add(id(self))
                return self.demon_host.take_damage(attacker=attacker, redirect_chain=redirect_chain)
        prev_hp = self.hp
        if getattr(self, "damage_from_tether", False):
            self.damage_from_tether = False
        else:
            try:
                if CURRENT_GAME: CURRENT_GAME.handle_tether_damage(self)
            except Exception:
                pass
        if self.shield_charges > 0:
            self.shield_charges -= 1
            if self.profession == "mage" and self.orb_angles:
                self.orb_angles.pop()
            return
        if self.shield_hp > 0:
            self.shield_hp -= 1
            return
        self.hurt_speed_timer = HURT_SPEED_DURATION
        self.hurt_slow_timer = HURT_SPEED_DURATION + HURT_SLOW_DURATION
        if attacker is not None and attacker is not self and CURRENT_GAME:
            CURRENT_GAME.add_damage(attacker, 1)
        self.hp -= 1
        handled = False
        if CURRENT_GAME:
            CURRENT_GAME.add_demon_rage_on_loss(self, max(0, prev_hp - self.hp))
            handled = CURRENT_GAME.handle_phoenix_after_damage(self)
        if handled:
            return
        if self.hp <= 0:
            self.alive = False

    def set_power(self, ptype, duration, axis=None):
        self.power = ptype
        self.power_timer = duration
        self.power_duration = duration
        self.spike_axis = axis

    def clear_power(self):
        self.power = None
        self.power_timer = 0
        self.spike_axis = None
        self.pending_bullet = False
        self.trail_emit_timer = 0.0

class Block(EntityBase):
    def __init__(self, x, y, w, h, vx, vy, color):
        super().__init__(x, y, vx, vy, color)
        self.w = w
        self.h = h
        self.radius = max(w, h) / 2

    def update(self, dt, bounds_rect):
        return self.common_update_physics(dt, bounds_rect, self.w, self.h)

    def draw(self, surface):
        rect = pygame.Rect(int(self.x), int(self.y), int(self.w), int(self.h))
        # 极简风格：扁平填充 + 白色细描边
        pygame.draw.rect(surface, self.color, rect, border_radius=4)
        pygame.draw.rect(surface, THEME["border"], rect, width=2, border_radius=4)

        if self.power == "aura":
            cx, cy = self.x + self.w/2, self.y + self.h/2
            draw_saw_ring(surface, cx, cy, self.radius + 2)
        elif self.power == "bullet":
            # 简化为一个小三角标记
            cx = self.x + self.w/2
            pygame.draw.circle(surface, THEME["accent"], (int(cx), int(self.y - 8)), 4)
        elif self.power == "spike":
            draw_spike_edges(surface, (self.x, self.y, self.w, self.h), self.spike_axis or "tb")

class Ball(EntityBase):
    def __init__(self, x, y, radius, vx, vy, color):
        super().__init__(x, y, vx, vy, color)
        self.radius = radius

    def update(self, dt, bounds_rect):
        # ball logic x is center for logic usually in game code provided, 
        # but inherited common uses x as top-left roughly? 
        # Actually original code: Ball x,y is center? No, draw uses (x,y) as center.
        # But update uses x +- radius. So x,y is center.
        # Let's adjust common physics or override.
        # Original code Ball x,y is center. Block x,y is top-left.
        # I will keep original logic manually to avoid breaking physics.
        
        hit_wall = False
        self.x += self.vx * dt
        self.y += self.vy * dt
        shape = bounds_rect["shape"]
        if shape == "rect":
            rect = bounds_rect["rect"]
            if self.x - self.radius < rect.left:
                self.x = rect.left + self.radius; self.vx *= -1; hit_wall = True
            elif self.x + self.radius > rect.right:
                self.x = rect.right - self.radius; self.vx *= -1; hit_wall = True
            if self.y - self.radius < rect.top:
                self.y = rect.top + self.radius; self.vy *= -1; hit_wall = True
            elif self.y + self.radius > rect.bottom:
                self.y = rect.bottom - self.radius; self.vy *= -1; hit_wall = True
        else:
            bx, by = bounds_rect["center"]
            r_bound = bounds_rect["radius"]
            dx = self.x - bx; dy = self.y - by
            dist = math.hypot(dx, dy)
            if dist + self.radius > r_bound:
                if dist == 0: dx, dy = 0.01, 0.01; dist=0.01
                nx, ny = dx/dist, dy/dist
                new_dist = r_bound - self.radius
                self.x = bx + nx * new_dist
                self.y = by + ny * new_dist
                dot = self.vx * nx + self.vy * ny
                self.vx -= 2 * dot * nx
                self.vy -= 2 * dot * ny
                hit_wall = True
        self.vx, self.vy = enforce_min_speed(self.vx, self.vy, BALL_MIN_SPEED)
        return hit_wall

    def draw(self, surface):
        # 极简风格：扁平填充 + 白色细描边
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))
        pygame.draw.circle(surface, THEME["border"], (int(self.x), int(self.y)), int(self.radius), 2)

        if self.power == "aura":
            draw_saw_ring(surface, self.x, self.y, self.radius + 4)
        elif self.power == "bullet":
            pygame.draw.circle(surface, THEME["accent"], (int(self.x), int(self.y - self.radius - 8)), 4)
        elif self.power == "spike":
            draw_spike_edges(surface, (self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2), self.spike_axis or "tb")

class Item:
    def __init__(self, x, y, radius=8):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, surface):
        # 简单的金色菱形
        points = [
            (self.x, self.y - self.radius),
            (self.x + self.radius, self.y),
            (self.x, self.y + self.radius),
            (self.x - self.radius, self.y)
        ]
        pygame.draw.polygon(surface, (255, 215, 0), points)
        pygame.draw.polygon(surface, (255, 255, 255), points, 1)

class Wall:
    def __init__(self, x, y, w, h, duration=WALL_DURATION):
        self.rect = pygame.Rect(int(x), int(y), int(w), int(h))
        self.time_left = duration

    def update(self, dt):
        self.time_left -= dt
    def alive(self): return self.time_left > 0
    def draw(self, surface):
        # 极简半透明墙
        draw_ui_rect(surface, self.rect, (200, 200, 220, 150))
        pygame.draw.rect(surface, (220, 220, 240), self.rect, 2)

class Bullet:
    def __init__(self, x, y, vx, vy, owner, color):
        self.x = x; self.y = y; self.vx = vx; self.vy = vy
        self.owner = owner; self.color = color
        self.w = 14; self.h = 6; self.alive = True

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface):
        # 简单的胶囊形状
        rect = pygame.Rect(int(self.x - self.w/2), int(self.y - self.h/2), self.w, self.h)
        pygame.draw.rect(surface, self.color, rect, border_radius=3)

class FloatingText:
    def __init__(self, text, x, y, duration=1.2, color=THEME["text_main"]):
        self.text = text
        self.x = x
        self.y = y
        self.duration = duration
        self.time_left = duration
        self.color = color

    def update(self, dt):
        self.time_left -= dt
        self.y -= 20 * dt 
    def alpha(self): return max(0, min(1, self.time_left / self.duration))

class Debris:
    def __init__(self, x, y, vx, vy, size, color, life):
        self.x = x; self.y = y; self.vx = vx; self.vy = vy
        self.size = size; self.color = color; self.life = life; self.time_left = life
    def update(self, dt):
        self.time_left -= dt; self.x += self.vx * dt; self.y += self.vy * dt
    def draw(self, surface):
        alpha = int(255 * (self.time_left / self.life))
        s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (self.size, self.size), self.size)
        surface.blit(s, (self.x-self.size, self.y-self.size))

class TriangleToken:
    def __init__(self, x, y, target, radius=8):
        self.x = x; self.y = y; self.target = target; self.radius = radius; self.alive = True
    def update(self, dt): pass
    def draw(self, surface):
        r = self.radius
        p1 = (int(self.x), int(self.y - r))
        p2 = (int(self.x - r), int(self.y + r))
        p3 = (int(self.x + r), int(self.y + r))
        pygame.draw.polygon(surface, (255, 105, 180), [p1, p2, p3])

class TrailSegment:
    def __init__(self, x, y, size, owner, duration=TRAIL_SEG_LIFE):
        self.x = x; self.y = y; self.size = size; self.owner = owner
        self.duration = duration; self.time_left = duration; self.hit_ids = set()
    def update(self, dt): self.time_left -= dt
    def alive(self): return self.time_left > 0
    def rect(self): return pygame.Rect(int(self.x), int(self.y), int(self.size), int(self.size))
    def draw(self, surface):
        alpha = int(100 * max(0, min(1, self.time_left/self.duration))) # 更淡的拖尾
        s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        s.fill((*self.owner.color, alpha))
        surface.blit(s, (self.x, self.y))

class SweepRect:
    def __init__(self, x, y, w, h, vx, owner, area_rect):
        self.x = x; self.y = y; self.w = w; self.h = h; self.vx = vx
        self.owner = owner; self.area_rect = area_rect; self.alive = True; self.hit_ids = set()
    def rect(self): return pygame.Rect(int(self.x), int(self.y), int(self.w), int(self.h))

class ExpandingCircle:
    def __init__(self, owner, cx, cy, max_radius, expand_duration=AOE_DURATION, linger=0.0):
        self.owner = owner; self.cx = cx; self.cy = cy; self.max_radius = max_radius
        self.radius = 0; self.expand_duration = expand_duration; self.linger_duration = linger
        self.total_time = expand_duration + linger; self.time_left = self.total_time
        self.hit_ids = set(); self.alive = True
    def update(self, dt):
        self.time_left -= dt
        elapsed = self.total_time - max(self.time_left, 0)
        if elapsed < self.expand_duration: self.radius = self.max_radius * (elapsed/self.expand_duration)
        else: self.radius = self.max_radius
        if self.time_left <= 0: self.alive = False

class RippleWave:
    def __init__(self, owner, cx, cy, base_radius):
        self.owner = owner; self.cx = cx; self.cy = cy
        self.base_radius = base_radius; self.max_radius = base_radius * RIPPLE_SCALE
        self.radius = base_radius; self.duration = RIPPLE_DURATION
        self.time_left = RIPPLE_DURATION; self.hit_ids = set(); self.alive = True
    def update(self, dt):
        self.time_left -= dt
        progress = 1 - max(self.time_left, 0)/self.duration
        self.radius = self.base_radius + (self.max_radius-self.base_radius)*min(1, progress)
        if self.time_left <= 0: self.alive = False

class FreezeRipple:
    def __init__(self, owner, cx, cy, base_radius):
        self.owner = owner; self.cx = cx; self.cy = cy
        self.base_radius = base_radius; self.max_radius = base_radius * RIPPLE_SCALE
        self.radius = base_radius; self.duration = RIPPLE_DURATION
        self.time_left = RIPPLE_DURATION; self.hit_ids = set(); self.alive = True
    def update(self, dt):
        self.time_left -= dt
        progress = 1 - max(self.time_left, 0)/self.duration
        self.radius = self.base_radius + (self.max_radius-self.base_radius)*min(1, progress)
        if self.time_left <= 0: self.alive = False

class PhoenixWave:
    def __init__(self, owner, cx, cy, base_radius):
        self.owner = owner; self.cx = cx; self.cy = cy
        self.base_radius = base_radius; self.max_radius = base_radius * PHOENIX_WAVE_SCALE
        self.radius = base_radius; self.duration = PHOENIX_WAVE_DURATION
        self.time_left = PHOENIX_WAVE_DURATION; self.hit_ids = set(); self.alive = True
    def update(self, dt):
        self.time_left -= dt
        progress = 1 - max(self.time_left, 0) / self.duration
        progress = max(0.0, min(1.0, progress))
        self.radius = self.base_radius + (self.max_radius - self.base_radius) * progress
        if self.time_left <= 0: self.alive = False

class ElementBurst:
    def __init__(self, owner, cx, cy, base_radius):
        self.owner = owner
        self.cx = cx
        self.cy = cy
        self.base_radius = base_radius
        self.max_radius = base_radius * ELEMENT_EXPLOSION_SCALE
        self.radius = base_radius
        self.duration = ELEMENT_EXPLOSION_DURATION
        self.time_left = self.duration
        self.hit_ids = set()
        self.alive = True

    def update(self, dt):
        self.time_left -= dt
        progress = 1 - max(self.time_left, 0) / self.duration if self.duration > 0 else 1.0
        progress = max(0.0, min(1.0, progress))
        self.radius = self.base_radius + (self.max_radius - self.base_radius) * progress
        if self.time_left <= 0:
            self.alive = False

# ------------------ 游戏主类 ------------------ #
class Game:
    def __init__(self, scenes):
        pygame.init()
        pygame.display.set_caption("Just Ball Game - Minimalist")
        self.font = self._load_font(20)
        self.font_large = self._load_font(48)
        self.font_small = self._load_font(16)

        self.scenes = scenes
        self.scene_index = 0
        self.map_index = 0
        self.selected_map_index = 0
        self.selected_entity_count = 4
        self.selected_time_limit = 60
        self.entity_count = 0

        self.state = "MENU"  # MENU / SETUP / INFO / PLAYING / TIME_UP
        self.pause_buttons = []

        # 初始设置
        self.setup_map_dimensions(MAPS[0])
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.menu_buttons = []
        self.setup_buttons = []
        self.info_tab = "prof"
        self.info_entries_prof = []
        self.info_entries_item = []
        self.info_scroll = 0

        # 游戏数据容器
        self.blocks = []; self.balls = []
        self.item = None; self.item_timer = 0.0; self.next_item_interval = ITEM_INTERVAL_MIN
        self.bullets = []; self.floating_texts = []; self.debris = []
        self.trails = []; self.lightning_beams = []; self.temp_speed_factors = {}
        self.ripples = []; self.freeze_ripples = []; self.freeze_emitters = []; self.phoenix_waves = []; self.element_bursts = []
        self.triangle_effect = None; self.triangle_tokens = []; self.curse_marks = []; self.sweepers = []; self.pending_top_sweeps = []
        self.aoes = []; self.walls = []; self.hex_burst_tasks = []
        self.aura_contacts = set(); self.flash_timer = 0.0
        self.tethers = []
        self.winner = None; self.winner_ent = None
        self.time_limit = 60
        self.time_left = self.time_limit
        self.effect_scroll = 0; self.prof_scroll = 0
        self.damage_stats = {}
        self.selected_env = "none"
        self.env_crisis = "none"
        self.env_enabled = False
        self.elapsed_time = 0.0
        self.poison_active = False
        self.poison_base_radius = 0.0
        self.poison_radius = 0.0
        self.poison_shape = "circle"
        self.poison_rect_start = None
        self.poison_rect = None
        self.poison_timer = 0.0
        self.poison_tick = POISON_DAMAGE_INTERVAL
        self.poison_center = (0.0, 0.0)
        self.electric_active = False
        self.electric_walls = []
        self.electric_spawn_cd = ELECTRIC_WALL_INTERVAL
        self.thunder_active = False
        self.thunder_cd = THUNDER_INTERVAL
        self.overload_active = False
        self.setup_row_offsets = {"map": 0.0, "count": 0.0, "time": 0.0, "env": 0.0}
        self.setup_row_active = None
        self.setup_slider_drag = None
        self.setup_row_tracks = {}
        self.setup_row_areas = {}

    def _load_font(self, size):
        for name in PREFERRED_FONTS:
            try:
                matched = pygame.font.match_font(name)
                if matched: return pygame.font.Font(matched, size)
            except: pass
        return pygame.font.SysFont("arial", size)

    def setup_map_dimensions(self, map_cfg):
        self.play_width = map_cfg["width"]
        self.play_height = map_cfg["height"]
        self.window_width = self.play_width + COUNTER_WIDTH
        self.window_height = self.play_height # 无底部UI
        self.border_margin = map_cfg.get("border_margin", 40)
        self.arena_shape = map_cfg.get("shape", "rect")
        if hasattr(self, 'screen'):
            self.screen = pygame.display.set_mode((self.window_width, self.window_height))

    def ensure_menu_window(self):
        menu_cfg = MAPS[0]
        target_w = menu_cfg["width"] + COUNTER_WIDTH
        target_h = menu_cfg["height"]
        if self.window_width != target_w or self.window_height != target_h:
            self.setup_map_dimensions(menu_cfg)

    def get_bounds(self):
        if self.arena_shape == "circle":
            cx = self.play_width / 2
            cy = self.play_height / 2
            radius = min(self.play_width, self.play_height) / 2 - self.border_margin
            return {"shape": "circle", "center": (cx, cy), "radius": radius, "rect": pygame.Rect(cx-radius, cy-radius, radius*2, radius*2)}
        else:
            return {"shape": "rect", "rect": pygame.Rect(self.border_margin, self.border_margin, self.play_width - 2*self.border_margin, self.play_height - 2*self.border_margin)}

    def load_scene(self, index, total_entities=None, time_limit_override=TIME_OVERRIDE_DEFAULT):
        cfg = self.scenes[index]
        self.scene_index = index
        self.setup_map_dimensions(MAPS[self.map_index])
        
        # 清理
        self.blocks = []; self.balls = []; self.bullets = []
        self.item = None; self.item_timer = 0.0; self.next_item_interval = random.uniform(ITEM_INTERVAL_MIN, ITEM_INTERVAL_MAX)
        self.debris = []; self.trails = []; self.floating_texts = []
        self.lightning_beams = []; self.temp_speed_factors = {}
        self.ripples = []; self.freeze_ripples = []; self.freeze_emitters = []; self.phoenix_waves = []; self.element_bursts = []
        self.triangle_effect = None; self.triangle_tokens = []; self.curse_marks = []; self.sweepers = []; self.pending_top_sweeps = []
        self.aoes = []; self.walls = []; self.hex_burst_tasks = []
        self.aura_contacts = set(); self.flash_timer = 0.0
        self.winner = None; self.winner_ent = None
        self.damage_stats = {}
        self.elapsed_time = 0.0
        self.env_crisis = getattr(self, "selected_env", "none") or "none"
        if self.env_crisis == "random":
            choices = [k for k in ENV_CRISIS_OPTIONS.keys() if k not in ("none", "random")]
            self.env_crisis = random.choice(choices) if choices else "none"
        self.env_enabled = False
        self.poison_active = False
        self.poison_base_radius = 0.0
        self.poison_radius = 0.0
        self.poison_shape = "circle"
        self.poison_rect_start = None
        self.poison_rect = None
        self.poison_timer = 0.0
        self.poison_tick = POISON_DAMAGE_INTERVAL
        self.poison_center = (0.0, 0.0)
        self.electric_active = False
        self.electric_walls = []
        self.electric_spawn_cd = ELECTRIC_WALL_INTERVAL
        self.thunder_active = False
        self.thunder_cd = THUNDER_INTERVAL
        self.overload_active = False
        self.setup_row_offsets = {"map": 0.0, "count": 0.0, "time": 0.0, "env": 0.0}
        self.setup_row_active = None
        self.setup_slider_drag = None
        self.setup_row_tracks = {}
        self.setup_row_areas = {}
        
        seeds = []
        for b in cfg.get("blocks", []): seeds.append(("block", b))
        for c in cfg.get("balls", []): seeds.append(("ball", c))
        if not seeds: seeds = [("ball", {"pos": (300,300), "vel":(200,200), "color":COLOR_PALETTE[0]})]
        
        total = total_entities or max(2, min(8, len(seeds)))
        total = max(2, min(8, total))
        for i in range(total):
            kind, data = seeds[i%len(seeds)]
            p_color = COLOR_PALETTE[i % len(COLOR_PALETTE)]
            if kind == "block":
                block = Block(data["pos"][0], data["pos"][1], ENTITY_RADIUS*2, ENTITY_RADIUS*2, data.get("vel",(200,200))[0], data.get("vel",(200,200))[1], p_color)
                block.name = f"BLOCK {i+1}"
                self.assign_profession(block)
                self.blocks.append(block)
                self._init_damage_stat(block)
            else:
                ball = Ball(data["pos"][0], data["pos"][1], ENTITY_RADIUS, data.get("vel",(200,200))[0], data.get("vel",(200,200))[1], p_color)
                ball.name = f"BALL {i+1}"
                self.assign_profession(ball)
                self.balls.append(ball)
                self._init_damage_stat(ball)
                
        if time_limit_override is TIME_OVERRIDE_DEFAULT:
            self.time_limit = cfg.get("time_limit", 60)
        else:
            self.time_limit = time_limit_override  # 可以是 None 表示无限
        self.selected_time_limit = self.time_limit
        self.time_left = self.time_limit
        self.state = "PLAYING"

    def assign_profession(self, ent):
        prof = random.choice(PROFESSIONS)
        ent.profession = prof
        ent.mass = TANK_MASS if prof == "tank" else 1.0
        ent.speed_base = TANK_SPEED_SCALE if prof == "tank" else 1.0
        ent.speed_bonus = 1.0
        ent.external_speed_scale = 1.0
        ent.max_hp = 8 if prof == "tank" else MAX_HP
        ent.hp = ent.max_hp
        ent.shield_hp = 0
        ent.hurt_speed_timer = 0.0
        ent.hurt_slow_timer = 0.0
        ent.shield_charges = 4 if prof == "tank" else 0
        ent.orb_angles = []
        ent.mage_cd = MAGE_ORB_INTERVAL
        ent.assassin_cd = ASSASSIN_COOLDOWN
        ent.assassin_active = 0.0
        ent.assassin_wall_stacks = 0
        ent.assassin_base_speed = math.hypot(ent.vx, ent.vy)
        ent.hunter_shot_cd = HUNTER_SHOT_CD
        ent.shock_cd = TANK_SHOCK_CD
        ent.time_cd = TIME_SLOW_CD
        ent.time_active = 0.0
        ent.gravity_cd = GRAVITY_CD
        ent.gravity_active = 0.0
        ent.gravity_mode = 1
        ent.lightning_cd = LIGHTNING_CD
        ent.freeze_timer = 0.0
        ent.frozen_velocity = (0.0, 0.0)
        ent.trail_emit_timer = 0.0
        ent.drone_gain_timer = DRONE_GAIN_INTERVAL
        ent.drones = []
        ent.drone_fire_cd = DRONE_CD
        ent.phoenix_perch_cd = PHOENIX_PERCH_INTERVAL
        ent.phoenix_perching = False
        ent.phoenix_rest_timer = 0.0
        ent.phoenix_egg = False
        ent.phoenix_egg_timer = 0.0
        ent.phoenix_wave_cd = PHOENIX_WAVE_INTERVAL
        ent.phoenix_rebirth_used = False
        ent.phoenix_saved_radius = getattr(ent, "radius", None)
        ent.phoenix_saved_w = getattr(ent, "w", None)
        ent.phoenix_saved_h = getattr(ent, "h", None)
        ent.phoenix_saved_max_hp = ent.max_hp
        if prof == "demon":
            ent.demon_rage = 0
            ent.demon_rage_max = DEMON_RAGE_MAX
            ent.demon_target = None
            ent.demon_host = None
            ent.demon_possessing = False
            ent.demon_shoot_cd = DEMON_SHOT_CD
            ent.demon_shrunken = False
            ent.demon_seeking = False
            ent.demon_base_radius = getattr(ent, "radius", None)
            ent.demon_base_w = getattr(ent, "w", None)
            ent.demon_base_h = getattr(ent, "h", None)
            ent.demon_orbit_angle = random.uniform(0, 2 * math.pi)
        if prof == "assassin":
            ent.assassin_wall_stacks = 0
            ent.assassin_base_speed = ent.assassin_base_speed or math.hypot(ent.vx, ent.vy)
            # 刺客模型缩小
            if isinstance(ent, Ball):
                ent.radius = max(8, int(ent.radius * 0.8))
            elif isinstance(ent, Block):
                ent.w = max(10, int(ent.w * 0.8))
                ent.h = max(10, int(ent.h * 0.8))
                ent.radius = max(ent.w, ent.h) / 2
        if prof == "drone":
            ent.drones.append(self.create_drone_unit())
        if prof == "heavy":
            ent.max_hp = 10
            ent.hp = ent.max_hp
            ent.shield_charges = 0
            ent.heavy_cd = 8.0
            ent.heavy_state = None
            ent.heavy_charge_timer = 0.0
            ent.heavy_charge_elapsed = 0.0
            ent.heavy_dash_timer = 0.0
            ent.heavy_target = None
            ent.heavy_shield_cd = 5.0

    def create_drone_unit(self):
        return {
            "phase": "orbit",
            "cd": DRONE_CD,
            "angle": random.uniform(0, 2 * math.pi),
            "pos": None,
            "dir": (0, 0),
            "hit_ids": set(),
        }

    # ------ 基础工具 ------ #
    def all_entities(self):
        return [e for e in self.blocks + self.balls if e.alive]

    def get_entity_center(self, ent):
        if isinstance(ent, Ball):
            return ent.x, ent.y
        return ent.x + ent.w / 2, ent.y + ent.h / 2

    def _init_damage_stat(self, ent):
        """为伤害统计面板注册实体（初始伤害为0）"""
        self.damage_stats[id(ent)] = {
            "ent": ent,
            "name": getattr(ent, "name", ""),
            "color": getattr(ent, "color", THEME["text_main"]),
            "damage": 0,
        }

    def add_damage(self, attacker, amount=1):
        if attacker is None:
            return
        key = id(attacker)
        if key not in self.damage_stats:
            self._init_damage_stat(attacker)
        entry = self.damage_stats[key]
        entry["damage"] += amount
        entry["name"] = getattr(attacker, "name", entry["name"])
        entry["color"] = getattr(attacker, "color", entry["color"])

    def process_assassin_hit(self, attacker, target):
        """
        刺客边界叠速：每次撞到边界叠一层速度*1.25（最多3层）；当层数>=3时首次撞到实体造成1伤害并恢复原始速度。
        """
        if not attacker or not target or not getattr(attacker, "alive", False) or not getattr(target, "alive", False):
            return
        if getattr(attacker, "profession", None) != "assassin":
            return
        if getattr(attacker, "assassin_wall_stacks", 0) < 3:
            return
        target.take_damage(attacker=attacker)
        attacker.assassin_wall_stacks = 0
        base_speed = getattr(attacker, "assassin_base_speed", 0) or math.hypot(attacker.vx, attacker.vy)
        if base_speed <= 0:
            base_speed = ASSASSIN_CHARGE_TRIGGER_SPEED / 1.25  # 合理缺省
        dir_len = math.hypot(attacker.vx, attacker.vy)
        if dir_len == 0:
            ang = random.uniform(0, 2 * math.pi)
            attacker.vx = math.cos(ang) * base_speed
            attacker.vy = math.sin(ang) * base_speed
        else:
            scale = base_speed / dir_len
            attacker.vx *= scale
            attacker.vy *= scale

    def apply_vampire_effect(self, vampire, target):
        if target is None or not getattr(target, "alive", False):
            return
        if not hasattr(target, "vampire_marks"):
            target.vampire_marks = 0
        if target.vampire_marks >= 3:
            target.take_damage(attacker=vampire)
            vampire.hp = min(vampire.max_hp, vampire.hp + 1)
            target.vampire_marks = 0
        else:
            target.vampire_marks = min(3, target.vampire_marks + 1)

    def process_vampire_collision(self, ent_a, ent_b):
        if not getattr(ent_a, "alive", False) or not getattr(ent_b, "alive", False):
            return
        if getattr(ent_a, "profession", None) == "vampire":
            self.apply_vampire_effect(ent_a, ent_b)
        if getattr(ent_b, "profession", None) == "vampire":
            self.apply_vampire_effect(ent_b, ent_a)

    def add_demon_rage_on_loss(self, ent, lost_hp):
        if not ent or getattr(ent, "profession", None) != "demon":
            return
        if lost_hp <= 0:
            return
        ent.demon_rage = min(getattr(ent, "demon_rage_max", DEMON_RAGE_MAX), getattr(ent, "demon_rage", 0) + 15 * lost_hp)
        if ent.demon_rage >= getattr(ent, "demon_rage_max", DEMON_RAGE_MAX):
            self.trigger_demon_fury(ent)

    def process_demon_collision(self, ent_a, ent_b):
        for ent in (ent_a, ent_b):
            if not getattr(ent, "alive", False):
                continue
            if getattr(ent, "profession", None) != "demon":
                continue
            if getattr(ent, "demon_possessing", False):
                continue
            ent.demon_rage = min(getattr(ent, "demon_rage_max", DEMON_RAGE_MAX), getattr(ent, "demon_rage", 0) + 1)
            if ent.demon_rage >= getattr(ent, "demon_rage_max", DEMON_RAGE_MAX):
                self.trigger_demon_fury(ent)

    def trigger_demon_fury(self, demon):
        if not demon or not getattr(demon, "alive", False):
            return
        if demon.demon_base_radius is None and hasattr(demon, "radius"):
            demon.demon_base_radius = demon.radius
        if demon.demon_base_w is None and hasattr(demon, "w"):
            demon.demon_base_w = demon.w
        if demon.demon_base_h is None and hasattr(demon, "h"):
            demon.demon_base_h = demon.h
        demon.demon_rage = 0
        demon.demon_seeking = True
        demon.demon_possessing = False
        demon.demon_host = None
        demon.demon_target = self.find_nearest(demon, self.all_entities())
        demon.demon_shoot_cd = DEMON_SHOT_CD
        if isinstance(demon, Ball):
            base_r = demon.demon_base_radius or demon.radius
            demon.radius = max(4, base_r * DEMON_SHRINK_SCALE)
        else:
            base_w = demon.demon_base_w or getattr(demon, "w", ENTITY_RADIUS * 2)
            base_h = demon.demon_base_h or getattr(demon, "h", ENTITY_RADIUS * 2)
            demon.w = max(6, base_w * DEMON_SHRINK_SCALE)
            demon.h = max(6, base_h * DEMON_SHRINK_SCALE)
            demon.radius = max(demon.w, demon.h) / 2
        demon.demon_shrunken = True
        for ent in self.all_entities():
            if ent is demon:
                continue
            ent.take_damage(attacker=demon)

    def start_demon_possession(self, demon, host):
        if not demon or not host:
            return False
        if not getattr(demon, "alive", False) or not getattr(host, "alive", False):
            return False
        demon.demon_host = host
        demon.demon_target = None
        demon.demon_seeking = False
        demon.demon_possessing = True
        demon.demon_shoot_cd = 0.0
        demon.demon_orbit_angle = random.uniform(0, 2 * math.pi)
        if hasattr(host, "hp") and hasattr(host, "max_hp"):
            host.hp = min(host.max_hp, host.hp + DEMON_HOST_HEAL)
        return True

    def end_demon_possession(self, demon):
        if not demon:
            return
        demon.demon_host = None
        demon.demon_target = None
        demon.demon_possessing = False
        demon.demon_seeking = False
        demon.demon_shoot_cd = DEMON_SHOT_CD
        if getattr(demon, "demon_shrunken", False):
            if isinstance(demon, Ball):
                if demon.demon_base_radius:
                    demon.radius = demon.demon_base_radius
            else:
                if demon.demon_base_w:
                    demon.w = demon.demon_base_w
                if demon.demon_base_h:
                    demon.h = demon.demon_base_h
                demon.radius = max(getattr(demon, "w", ENTITY_RADIUS * 2), getattr(demon, "h", ENTITY_RADIUS * 2)) / 2
            demon.demon_shrunken = False

    def fire_demon_bullets(self, demon):
        if not demon or not getattr(demon, "alive", False):
            return
        cx, cy = self.get_entity_center(demon)
        for _ in range(DEMON_SHOT_COUNT):
            ang = random.uniform(0, 2 * math.pi)
            vx = math.cos(ang) * BULLET_SPEED
            vy = math.sin(ang) * BULLET_SPEED
            b = Bullet(cx, cy, vx, vy, demon, DEMON_RING_COLOR)
            b.w = 18
            b.h = 8
            self.bullets.append(b)

    def update_demon(self, demon, entities, dt):
        if not demon or not getattr(demon, "alive", False):
            return
        if getattr(demon, "demon_possessing", False):
            host = getattr(demon, "demon_host", None)
            if not host or not getattr(host, "alive", False):
                self.end_demon_possession(demon)
                return
            hx, hy = self.get_entity_center(host)
            demon.demon_orbit_angle = (demon.demon_orbit_angle + DEMON_ORBIT_SPEED * dt) % (2 * math.pi)
            orbit_r = getattr(host, "radius", ENTITY_RADIUS) + getattr(demon, "radius", ENTITY_RADIUS) + 6
            offset_x = math.cos(demon.demon_orbit_angle) * orbit_r
            offset_y = math.sin(demon.demon_orbit_angle) * orbit_r
            if isinstance(demon, Ball):
                demon.x, demon.y = hx + offset_x, hy + offset_y
            else:
                demon.x = hx + offset_x - demon.w / 2
                demon.y = hy + offset_y - demon.h / 2
            demon.vx = 0
            demon.vy = 0
            demon.demon_shoot_cd -= dt
            if demon.demon_shoot_cd <= 0:
                self.fire_demon_bullets(demon)
                demon.demon_shoot_cd += DEMON_SHOT_CD
            return

        if not getattr(demon, "demon_seeking", False):
            return
        target = getattr(demon, "demon_target", None)
        if not target or not getattr(target, "alive", False):
            target = self.find_nearest(demon, [e for e in entities if e is not demon])
            demon.demon_target = target
            if not target:
                self.end_demon_possession(demon)
                return

        cx, cy = self.get_entity_center(demon)
        tx, ty = self.get_entity_center(target)
        dx = tx - cx; dy = ty - cy
        dist = math.hypot(dx, dy)
        if dist <= demon.radius + target.radius:
            self.start_demon_possession(demon, target)
        else:
            speed = math.hypot(demon.vx, demon.vy)
            if speed <= 0:
                speed = MIN_SPEED
            demon.vx = dx / (dist or 1) * speed
            demon.vy = dy / (dist or 1) * speed

    def start_phoenix_egg(self, ent):
        if not ent:
            return
        ent.phoenix_rebirth_used = True
        ent.phoenix_egg = True
        ent.phoenix_egg_timer = PHOENIX_EGG_DURATION
        ent.phoenix_wave_cd = 0.0
        ent.phoenix_perching = False
        ent.phoenix_rest_timer = 0.0
        if ent.phoenix_saved_radius is None and hasattr(ent, "radius"):
            ent.phoenix_saved_radius = ent.radius
        if ent.phoenix_saved_w is None and hasattr(ent, "w"):
            ent.phoenix_saved_w = ent.w
        if ent.phoenix_saved_h is None and hasattr(ent, "h"):
            ent.phoenix_saved_h = ent.h
        if ent.phoenix_saved_max_hp is None:
            ent.phoenix_saved_max_hp = ent.max_hp
        ent.max_hp = PHOENIX_EGG_HP
        ent.hp = ent.max_hp
        ent.shield_hp = 0
        ent.shield_charges = 0
        ent.vx = 0
        ent.vy = 0
        if isinstance(ent, Ball):
            ent.radius = max(4, ent.radius * 0.5)
        else:
            ent.w = max(8, ent.w * 0.5)
            ent.h = max(8, ent.h * 0.5)
            ent.radius = max(ent.w, ent.h) / 2
        ent.alive = True

    def finish_phoenix_rebirth(self, ent):
        if not ent:
            return
        remain = max(0, ent.hp)
        bonus_shield = int(round(remain * PHOENIX_SHIELD_RATIO))
        ent.phoenix_egg = False
        ent.phoenix_egg_timer = 0.0
        ent.max_hp = ent.phoenix_saved_max_hp or MAX_HP
        ent.hp = ent.max_hp
        ent.shield_hp = min(SHIELD_MAX, ent.shield_hp + bonus_shield)
        ent.vx = 0
        ent.vy = 0
        ent.phoenix_wave_cd = PHOENIX_WAVE_INTERVAL
        if isinstance(ent, Ball):
            if ent.phoenix_saved_radius:
                ent.radius = ent.phoenix_saved_radius
        else:
            if ent.phoenix_saved_w:
                ent.w = ent.phoenix_saved_w
            if ent.phoenix_saved_h:
                ent.h = ent.phoenix_saved_h
            ent.radius = max(ent.w, ent.h) / 2
        ent.phoenix_perch_cd = PHOENIX_PERCH_INTERVAL
        ent.alive = True

    def handle_phoenix_after_damage(self, ent):
        if not ent or getattr(ent, "profession", None) != "phoenix":
            return False
        if getattr(ent, "phoenix_egg", False):
            if ent.hp <= 0:
                ent.alive = False
            return True
        if ent.hp > 0:
            return False
        if getattr(ent, "phoenix_rebirth_used", False):
            return False
        self.start_phoenix_egg(ent)
        return True

    def start_phoenix_perch(self, ent):
        if not ent or getattr(ent, "phoenix_egg", False):
            return
        ent.phoenix_perching = True
        ent.phoenix_perch_cd = PHOENIX_PERCH_INTERVAL
        bounds = self.get_bounds()
        cx, cy = self.get_entity_center(ent)
        if bounds["shape"] == "rect":
            rect = bounds["rect"]
            left_gap = (cx - getattr(ent, "radius", 0)) - rect.left
            right_gap = rect.right - (cx + getattr(ent, "radius", 0))
            top_gap = (cy - getattr(ent, "radius", 0)) - rect.top
            bottom_gap = rect.bottom - (cy + getattr(ent, "radius", 0))
            gaps = [(left_gap, (-1, 0)), (right_gap, (1, 0)), (top_gap, (0, -1)), (bottom_gap, (0, 1))]
            _, direction = min(gaps, key=lambda g: g[0])
            dx, dy = direction
        else:
            bx, by = bounds["center"]
            dx = cx - bx
            dy = cy - by
            if dx == 0 and dy == 0:
                ang = random.uniform(0, 2 * math.pi)
                dx, dy = math.cos(ang), math.sin(ang)
        dist = math.hypot(dx, dy) or 1.0
        speed = max(math.hypot(ent.vx, ent.vy), MIN_SPEED)
        ent.vx = dx / dist * speed
        ent.vy = dy / dist * speed

    def spawn_phoenix_wave(self, owner):
        if not owner or not getattr(owner, "alive", False):
            return
        cx, cy = self.get_entity_center(owner)
        self.phoenix_waves.append(PhoenixWave(owner, cx, cy, getattr(owner, "radius", ENTITY_RADIUS)))

    def apply_phoenix_collision_damage(self, victim, other=None):
        if not victim or not getattr(victim, "alive", False):
            return
        if getattr(victim, "profession", None) != "phoenix":
            return
        if not getattr(victim, "phoenix_egg", False):
            return
        victim.hp -= 1
        self.handle_phoenix_after_damage(victim)

    # ------ 环境危机逻辑 ------ #
    def start_poison_circle(self):
        bounds = self.get_bounds()
        if bounds["shape"] == "rect":
            rect = bounds["rect"].copy()
            self.poison_shape = "rect"
            self.poison_rect_start = rect
            self.poison_rect = rect.copy()
            self.poison_center = rect.center
            self.poison_base_radius = 0.0
        else:
            cx, cy = bounds["center"]
            base = bounds["radius"]
            self.poison_shape = "circle"
            self.poison_center = (cx, cy)
            self.poison_base_radius = base
        self.poison_active = True
        self.poison_radius = self.poison_base_radius
        self.poison_timer = POISON_SHRINK_DURATION
        self.poison_tick = POISON_DAMAGE_INTERVAL

    def update_poison(self, dt):
        if not self.poison_active:
            return
        self.poison_timer = max(0.0, self.poison_timer - dt)
        progress = 1.0 - (self.poison_timer / POISON_SHRINK_DURATION if POISON_SHRINK_DURATION > 0 else 1.0)
        progress = max(0.0, min(1.0, progress))
        if self.poison_shape == "circle":
            self.poison_radius = max(0.0, self.poison_base_radius * (1 - progress))
        else:
            if self.poison_rect_start:
                cx, cy = self.poison_rect_start.center
                new_w = max(0.0, self.poison_rect_start.width * (1 - progress))
                new_h = max(0.0, self.poison_rect_start.height * (1 - progress))
                self.poison_rect = pygame.Rect(0, 0, new_w, new_h)
                self.poison_rect.center = (cx, cy)
        self.poison_tick -= dt
        if self.poison_tick <= 0:
            self.poison_tick += POISON_DAMAGE_INTERVAL
            for ent in self.all_entities():
                if not ent.alive:
                    continue
                cx, cy = self.get_entity_center(ent)
                if self.poison_shape == "circle":
                    dx = cx - self.poison_center[0]
                    dy = cy - self.poison_center[1]
                    dist = math.hypot(dx, dy)
                    if dist > self.poison_radius or self.poison_radius <= 0:
                        ent.take_damage()
                else:
                    rect = self.poison_rect
                    if rect is None or rect.width <= 0 or rect.height <= 0:
                        ent.take_damage()
                        continue
                    closest_x = max(rect.left, min(cx, rect.right))
                    closest_y = max(rect.top, min(cy, rect.bottom))
                    dx = cx - closest_x
                    dy = cy - closest_y
                    if dx * dx + dy * dy > getattr(ent, "radius", ENTITY_RADIUS) ** 2:
                        ent.take_damage()

    def spawn_electric_wall(self):
        side = random.choice(["left", "right", "top", "bottom"])
        self.electric_walls.append({"side": side, "time": ELECTRIC_WALL_DURATION})

    def update_electric(self, dt):
        if not self.electric_active:
            return
        self.electric_spawn_cd -= dt
        if self.electric_spawn_cd <= 0:
            self.spawn_electric_wall()
            self.electric_spawn_cd = ELECTRIC_WALL_INTERVAL
        new_walls = []
        for w in self.electric_walls:
            w["time"] -= dt
            if w["time"] > 0:
                new_walls.append(w)
        self.electric_walls = new_walls
        if not self.electric_walls:
            return
        bounds = self.get_bounds()
        if bounds["shape"] != "rect":
            return
        rect = bounds["rect"]
        for ent in self.all_entities():
            if not ent.alive:
                continue
            cx, cy = self.get_entity_center(ent)
            dists = {
                "left": (cx - rect.left, (-1, 0)),
                "right": (rect.right - cx, (1, 0)),
                "top": (cy - rect.top, (0, -1)),
                "bottom": (rect.bottom - cy, (0, 1)),
            }
            for w in self.electric_walls:
                dist, direction = dists.get(w["side"], (9999, (0, 0)))
                if dist < 140:
                    ent.vx += direction[0] * ELECTRIC_WALL_ATTRACT * dt
                    ent.vy += direction[1] * ELECTRIC_WALL_ATTRACT * dt

    def update_thunder(self, dt):
        if not self.thunder_active:
            return
        self.thunder_cd -= dt
        if self.thunder_cd > 0:
            return
        self.thunder_cd = THUNDER_INTERVAL
        alive = [e for e in self.all_entities() if e.alive]
        if not alive:
            return
        target = random.choice(alive)
        others = [e for e in alive if e is not target]
        link = self.find_nearest(target, others) if others else None
        self.apply_thunder_damage(target, link)

    def apply_thunder_damage(self, main, link=None):
        if main and main.alive:
            dmg = random.randint(1, 3)
            for _ in range(dmg):
                main.take_damage()
            cx, cy = self.get_entity_center(main)
            self.lightning_beams.append({"start": (cx, cy - 200), "end": (cx, cy), "time": LIGHTNING_LIFE})
        if link and link.alive and link is not main:
            dmg = random.randint(1, 3)
            for _ in range(dmg):
                link.take_damage()
            sx, sy = self.get_entity_center(main)
            ex, ey = self.get_entity_center(link)
            self.lightning_beams.append({"start": (sx, sy), "end": (ex, ey), "time": LIGHTNING_LIFE})

    def detect_wall_side(self, ent, bounds):
        if bounds["shape"] != "rect":
            return None
        rect = bounds["rect"]
        tol = 1.5
        if isinstance(ent, Ball):
            gaps = {
                "left": abs((ent.x - ent.radius) - rect.left),
                "right": abs((ent.x + ent.radius) - rect.right),
                "top": abs((ent.y - ent.radius) - rect.top),
                "bottom": abs((ent.y + ent.radius) - rect.bottom),
            }
        else:
            gaps = {
                "left": abs(ent.x - rect.left),
                "right": abs((ent.x + ent.w) - rect.right),
                "top": abs(ent.y - rect.top),
                "bottom": abs((ent.y + ent.h) - rect.bottom),
            }
        side, dist = min(gaps.items(), key=lambda kv: kv[1])
        if dist <= tol:
            return side
        return None

    def electric_damage_on_hit(self, ent, bounds):
        if not self.electric_walls:
            return
        side = self.detect_wall_side(ent, bounds)
        if not side:
            return
        if any(w["side"] == side for w in self.electric_walls):
            count = len(self.electric_walls)
            for _ in range(count):
                ent.take_damage()

    def update_environment(self, dt):
        self.elapsed_time += dt
        if self.env_crisis != "none" and not self.env_enabled and self.elapsed_time >= ENV_START_TIME:
            self.env_enabled = True
            if self.env_crisis == "poison":
                self.start_poison_circle()
            elif self.env_crisis == "electric":
                self.electric_active = True
                self.electric_spawn_cd = 0.0
            elif self.env_crisis == "thunder":
                self.thunder_active = True
                self.thunder_cd = 0.0
            elif self.env_crisis == "overload":
                self.overload_active = True

        if self.poison_active:
            self.update_poison(dt)
        if self.electric_active:
            self.update_electric(dt)
        if self.thunder_active:
            self.update_thunder(dt)

    def process_assassin_wall_hit(self, ent):
        if getattr(ent, "profession", None) != "assassin":
            return
        stacks = getattr(ent, "assassin_wall_stacks", 0)
        if stacks >= 3:
            return
        ent.assassin_wall_stacks = stacks + 1
        ent.vx *= 1.25
        ent.vy *= 1.25

    def find_nearest(self, src, targets):
        """返回与src最近的目标（忽略自身与未存活者），若不存在则None"""
        live_targets = [t for t in targets if t is not src and getattr(t, "alive", False)]
        if not live_targets:
            return None
        sx, sy = self.get_entity_center(src)
        return min(
            live_targets,
            key=lambda t: (self.get_entity_center(t)[0] - sx) ** 2 + (self.get_entity_center(t)[1] - sy) ** 2
        )

    def add_floating_text(self, text, ent):
        cx, cy = self.get_entity_center(ent)
        self.floating_texts.append(FloatingText(text, cx, cy))

    def spawn_debris(self, cx, cy, color, count=12):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(180, 320)
            size = random.randint(3, 6)
            life = random.uniform(0.5, 0.9)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.debris.append(Debris(cx, cy, vx, vy, size, color, life))

    def handle_deaths(self):
        for ent in self.blocks + self.balls:
            if ent.alive:
                continue
            if getattr(ent, "death_effect_done", False):
                continue
            cx, cy = self.get_entity_center(ent)
            self.spawn_debris(cx, cy, ent.color)
            ent.death_effect_done = True

    def update_debris(self, dt):
        for d in self.debris:
            d.update(dt)
        self.debris = [d for d in self.debris if d.time_left > 0]

    def draw_debris(self):
        for d in self.debris:
            d.draw(self.screen)

    def get_speed_factor(self, ent):
        factor = ent.speed_base * ent.speed_bonus * ent.external_speed_scale
        if getattr(ent, "hurt_speed_timer", 0) > 0:
            factor *= 2.0
        elif getattr(ent, "hurt_slow_timer", 0) > 0:
            factor *= HURT_SLOW_MULT
        return factor

    # ------ 道具与技能触发 ------ #
    def spawn_item(self):
        bounds = self.get_bounds()
        if bounds["shape"] == "circle":
            cx, cy = bounds["center"]
            r = bounds["radius"] - 20
            ang = random.uniform(0, 2 * math.pi)
            radius = math.sqrt(random.uniform(0, 1)) * r
            x = cx + math.cos(ang) * radius
            y = cy + math.sin(ang) * radius
        else:
            rect = bounds["rect"]
            x = random.uniform(rect.left + 20, rect.right - 20)
            y = random.uniform(rect.top + 20, rect.bottom - 20)
        self.item = Item(x, y)

    def handle_item_pickups(self):
        if not self.item:
            return
        for ent in self.all_entities():
            if isinstance(ent, Ball):
                dx = ent.x - self.item.x
                dy = ent.y - self.item.y
                reach = ent.radius + self.item.radius
            else:
                cx = ent.x + ent.w / 2
                cy = ent.y + ent.h / 2
                dx = cx - self.item.x
                dy = cy - self.item.y
                reach = max(ent.w, ent.h) / 2 + self.item.radius
            if dx * dx + dy * dy <= reach * reach:
                times = 1
                if self.env_crisis == "overload" and self.env_enabled:
                    times = random.randint(OVERLOAD_EXTRA_MIN, OVERLOAD_EXTRA_MAX)
                    ent.take_damage()
                for _ in range(times):
                    self.apply_power_up(ent)
                self.item = None
                self.item_timer = 0.0
                break

    def apply_power_up(self, ent):
        modes = ["aura", "bullet", "spike", "flash", "heal", "sweep", "aoe", "trail", "ripple", "shield", "wall", "hexshot", "freeze_ripple", "triangle", "tether"]
        weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        mode = random.choices(modes, weights=weights, k=1)[0]
        label_map = {
            "aura": "电刃环",
            "bullet": "三连弹",
            "spike": "刺轮",
            "flash": "爆裂",
            "heal": "恢复+1",
            "sweep": "扫射",
            "aoe": "范围震荡",
            "trail": "毒雾",
            "ripple": "冲击波",
            "shield": "护盾",
            "wall": "墙体",
            "hexshot": "全向连发",
            "freeze_ripple": "冰冻波",
            "triangle": "追踪三角",
            "tether": "牵引",
        }
        if mode == "aura":
            ent.set_power("aura", BUFF_DURATION)
            self.add_floating_text(label_map[mode], ent)
        elif mode == "spike":
            axis = random.choice(["tb", "lr"])
            ent.set_power("spike", SPIKE_DURATION, axis)
            self.add_floating_text(label_map[mode], ent)
        elif mode == "flash":
            for victim in self.all_entities():
                if victim is ent:
                    continue
                victim.take_damage(attacker=ent)
                cx, cy = self.get_entity_center(victim)
                self.curse_marks.append({"x": cx, "y": cy, "time": CURSE_MARK_DURATION})
            self.add_floating_text(label_map[mode], ent)
        elif mode == "heal":
            if ent.hp < ent.max_hp:
                ent.hp += 1
            self.add_floating_text(label_map[mode], ent)
        elif mode == "sweep":
            if self.start_sweep_skill(ent):
                self.add_floating_text(label_map[mode], ent)
        elif mode == "aoe":
            if self.start_aoe(ent):
                self.add_floating_text(label_map[mode], ent)
        elif mode == "trail":
            ent.set_power("trail", TRAIL_EFFECT_DURATION)
            ent.trail_emit_timer = 0.0
            self.add_floating_text(label_map[mode], ent)
        elif mode == "ripple":
            ent.set_power("ripple", BUFF_DURATION)
            self.add_floating_text(label_map[mode], ent)
        elif mode == "shield":
            if ent.shield_hp < SHIELD_MAX:
                ent.shield_hp += 1
            self.add_floating_text(label_map[mode], ent)
        elif mode == "freeze_ripple":
            if self.start_freeze_ripple(ent):
                self.add_floating_text(label_map[mode], ent)
        elif mode == "triangle":
            if self.start_triangle_effect(ent):
                self.add_floating_text(label_map[mode], ent)
        elif mode == "tether":
            if self.start_tether(ent):
                self.add_floating_text(label_map[mode], ent)
        elif mode == "wall":
            if self.spawn_wall():
                self.add_floating_text(label_map[mode], ent)
        elif mode == "hexshot":
            if self.start_hex_shot(ent):
                self.add_floating_text(label_map[mode], ent)
        else:
            launched = self.fire_bullet_spread(ent)
            if launched:
                ent.set_power("bullet", 0.0)
                self.add_floating_text(label_map[mode], ent)
            else:
                ent.clear_power()

    def fire_bullet(self, owner):
        candidates = [e for e in self.all_entities() if e is not owner]
        if not candidates:
            return False

        def center(e):
            if isinstance(e, Ball):
                return e.x, e.y
            return e.x + e.w / 2, e.y + e.h / 2

        ox, oy = center(owner)
        target = min(candidates, key=lambda e: (center(e)[0] - ox) ** 2 + (center(e)[1] - oy) ** 2)
        tx, ty = center(target)
        dx = tx - ox
        dy = ty - oy
        dist = math.hypot(dx, dy)
        if dist == 0:
            dx, dy = 1, 0
            dist = 1
        vx = dx / dist * BULLET_SPEED
        vy = dy / dist * BULLET_SPEED
        bullet_color = owner.color if hasattr(owner, "color") else (255, 215, 0)
        bullet = Bullet(ox, oy, vx, vy, owner, bullet_color)
        self.bullets.append(bullet)
        return True

    def get_target_direction(self, owner):
        candidates = [e for e in self.all_entities() if e is not owner]
        if not candidates:
            return None

        def center(e):
            if isinstance(e, Ball):
                return e.x, e.y
            return e.x + e.w / 2, e.y + e.h / 2

        ox, oy = center(owner)
        target = min(candidates, key=lambda e: (center(e)[0] - ox) ** 2 + (center(e)[1] - oy) ** 2)
        tx, ty = center(target)
        dx = tx - ox
        dy = ty - oy
        dist = math.hypot(dx, dy)
        if dist == 0:
            dx, dy = 1, 0
            dist = 1
        return dx / dist, dy / dist

    def fire_bullet_spread(self, owner):
        dir_vec = self.get_target_direction(owner)
        if not dir_vec:
            return False
        nx, ny = dir_vec
        angles = (-0.25, 0, 0.25)
        color = owner.color if hasattr(owner, "color") else (255, 215, 0)
        ox, oy = self.get_entity_center(owner)
        for ang in angles:
            cos_a = math.cos(ang)
            sin_a = math.sin(ang)
            rx = nx * cos_a - ny * sin_a
            ry = nx * sin_a + ny * cos_a
            vx = rx * BULLET_SPEED
            vy = ry * BULLET_SPEED
            self.bullets.append(Bullet(ox, oy, vx, vy, owner, color))
        return True

    def fire_hex_shot(self, owner):
        ox, oy = self.get_entity_center(owner)
        base_angle = random.uniform(0, 2 * math.pi)
        color = owner.color if hasattr(owner, "color") else (255, 215, 0)
        for i in range(HEX_BURST_COUNT):
            ang = base_angle + i * (2 * math.pi / HEX_BURST_COUNT)
            vx = math.cos(ang) * BULLET_SPEED
            vy = math.sin(ang) * BULLET_SPEED
            self.bullets.append(Bullet(ox, oy, vx, vy, owner, color))

    def start_hex_shot(self, owner):
        if not owner or not owner.alive:
            return False
        self.fire_hex_shot(owner)
        self.hex_burst_tasks.append({"owner": owner, "delay": HEX_BURST_DELAY})
        return True

    def start_sweep_skill(self, owner):
        bounds = self.get_bounds()
        area = bounds["rect"]
        h_half = area.height / 2
        bar_h = h_half
        bar_w = area.width / 2

        y_bottom = area.top + h_half
        sweeper1 = SweepRect(area.left - bar_w, y_bottom, bar_w, bar_h, SWEEP_SPEED, owner, area)
        self.sweepers.append(sweeper1)
        self.pending_top_sweeps.append(
            {
                "delay": 2.0,
                "owner": owner,
                "area": area,
                "bar_w": bar_w,
                "bar_h": bar_h,
                "y_top": area.top,
            }
        )
        return True

    def start_aoe(self, owner):
        cx, cy = self.get_entity_center(owner)
        max_r = ENTITY_RADIUS * 4
        expand_time = AOE_DURATION * 1.5
        linger = AOE_DURATION * 0.5
        aoe = ExpandingCircle(owner, cx, cy, max_r, expand_duration=expand_time, linger=linger)
        self.aoes.append(aoe)
        return True

    def start_freeze_ripple(self, owner):
        if not owner or not owner.alive:
            return False
        self.spawn_freeze_ripple(owner)
        self.freeze_emitters.append(
            {
                "owner": owner,
                "time": FREEZE_RIPPLE_TOTAL,
                "interval": FREEZE_RIPPLE_INTERVAL,
                "next_emit": FREEZE_RIPPLE_INTERVAL,
            }
        )
        return True

    def apply_freeze(self, ent, duration=FREEZE_STUN_TIME):
        if not ent or not ent.alive:
            return
        if getattr(ent, "freeze_timer", 0) <= 0:
            ent.frozen_velocity = (ent.vx, ent.vy)
        ent.freeze_timer = max(duration, getattr(ent, "freeze_timer", 0))
        ent.vx = 0
        ent.vy = 0

    def has_fire_status(self, ent):
        return getattr(ent, "burning", False) or getattr(ent, "fire_stacks", 0) > 0

    def has_cold_status(self, ent):
        return getattr(ent, "cold_frozen", False) or getattr(ent, "cold_stacks", 0) > 0

    def start_burning(self, ent, source=None):
        if not ent or not ent.alive:
            return
        ent.burning = True
        ent.burn_timer = BURN_DURATION
        ent.burn_tick_timer = BURN_TICK_INTERVAL
        ent.burn_source = source
        ent.fire_stacks = FIRE_STACK_MAX

    def apply_fire(self, ent, amount=1, source=None):
        if not ent or not ent.alive:
            return
        if getattr(ent, "element_immunity", 0) > 0:
            return
        if self.has_cold_status(ent):
            self.trigger_element_explosion(ent, source or ent)
            return
        ent.fire_stacks = min(FIRE_STACK_MAX, getattr(ent, "fire_stacks", 0) + amount)
        if ent.fire_stacks >= FIRE_STACK_MAX:
            self.start_burning(ent, source)

    def apply_cold(self, ent, amount=1, source=None):
        if not ent or not ent.alive:
            return
        if getattr(ent, "element_immunity", 0) > 0:
            return
        if self.has_fire_status(ent):
            self.trigger_element_explosion(ent, source or ent)
            return
        ent.cold_stacks = min(COLD_STACK_MAX, getattr(ent, "cold_stacks", 0) + amount)
        if ent.cold_stacks >= COLD_STACK_MAX:
            ent.cold_frozen = True
            self.apply_freeze(ent, duration=FROST_STUN_DURATION)

    def trigger_element_explosion(self, ent, source=None):
        if not ent or not ent.alive:
            return
        ent.fire_stacks = 0
        ent.cold_stacks = 0
        ent.burning = False
        ent.burn_timer = 0.0
        ent.burn_tick_timer = 0.0
        ent.burn_source = None
        ent.cold_frozen = False
        ent.freeze_timer = 0.0
        ent.element_immunity = ELEMENT_IMMUNE_DURATION
        cx, cy = self.get_entity_center(ent)
        burst_radius = getattr(ent, "radius", ENTITY_RADIUS)
        self.element_bursts.append(ElementBurst(source or ent, cx, cy, burst_radius))

    def update_elemental_state(self, ent, dt):
        if not ent or not getattr(ent, "alive", False):
            return
        if getattr(ent, "element_immunity", 0) > 0:
            ent.element_immunity = max(0.0, ent.element_immunity - dt)
        if getattr(ent, "burning", False):
            ent.burn_timer = max(0.0, ent.burn_timer - dt)
            ent.burn_tick_timer -= dt
            while ent.burn_tick_timer <= 0 and ent.burn_timer > 0:
                ent.burn_tick_timer += BURN_TICK_INTERVAL
                ent.take_damage(attacker=ent.burn_source)
            if ent.burn_timer <= 0:
                ent.burning = False
                ent.fire_stacks = 0
                ent.burn_tick_timer = 0.0
                ent.burn_source = None

    def spawn_ripple(self, owner):
        cx, cy = self.get_entity_center(owner)
        self.ripples.append(RippleWave(owner, cx, cy, owner.radius))

    def spawn_freeze_ripple(self, owner):
        cx, cy = self.get_entity_center(owner)
        self.freeze_ripples.append(FreezeRipple(owner, cx, cy, owner.radius))

    def spawn_wall(self):
        bounds = self.get_bounds()
        area = bounds["rect"]
        orientation = random.choice(["h", "v"])
        thickness = 20
        margin = 20
        if orientation == "h":
            w = max(60, area.width * 0.65)
            h = thickness
        else:
            w = thickness
            h = max(60, area.height * 0.65)
        w = min(w, area.width - margin * 2)
        h = min(h, area.height - margin * 2)
        if w <= 0 or h <= 0:
            return False
        x_min = area.left + margin
        y_min = area.top + margin
        x_max = area.right - w - margin
        y_max = area.bottom - h - margin
        if x_max < x_min or y_max < y_min:
            return False
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        self.walls.append(Wall(x, y, w, h, WALL_DURATION))
        return True

    def handle_wall_collisions(self):
        for wall in self.walls:
            rect = wall.rect
            for ball in self.balls:
                if not ball.alive:
                    continue
                cx, cy = ball.x, ball.y
                closest_x = max(rect.left, min(cx, rect.right))
                closest_y = max(rect.top, min(cy, rect.bottom))
                dx = cx - closest_x
                dy = cy - closest_y
                if dx * dx + dy * dy < ball.radius * ball.radius:
                    if abs(dx) > abs(dy):
                        if dx > 0:
                            ball.x = rect.right + ball.radius
                            ball.vx = abs(ball.vx)
                        else:
                            ball.x = rect.left - ball.radius
                            ball.vx = -abs(ball.vx)
                    else:
                        if dy > 0:
                            ball.y = rect.bottom + ball.radius
                            ball.vy = abs(ball.vy)
                        else:
                            ball.y = rect.top - ball.radius
                            ball.vy = -abs(ball.vy)
            for block in self.blocks:
                if not block.alive:
                    continue
                brect = pygame.Rect(block.x, block.y, block.w, block.h)
                if not brect.colliderect(rect):
                    continue
                overlap_x = min(brect.right - rect.left, rect.right - brect.left)
                overlap_y = min(brect.bottom - rect.top, rect.bottom - brect.top)
                if overlap_x < overlap_y:
                    if brect.centerx < rect.centerx:
                        block.x -= overlap_x
                        block.vx = -abs(block.vx)
                    else:
                        block.x += overlap_x
                        block.vx = abs(block.vx)
                else:
                    if brect.centery < rect.centery:
                        block.y -= overlap_y
                        block.vy = -abs(block.vy)
                    else:
                        block.y += overlap_y
                        block.vy = abs(block.vy)

    def update_walls(self, dt):
        for w in self.walls:
            w.update(dt)
        self.walls = [w for w in self.walls if w.alive()]

    def handle_block_collisions(self):
        n = len(self.blocks)
        for i in range(n):
            for j in range(i + 1, n):
                a = self.blocks[i]; b = self.blocks[j]
                if not a.alive or not b.alive: continue
                if (getattr(a, "profession", None) == "demon" and getattr(a, "demon_possessing", False)) or (getattr(b, "profession", None) == "demon" and getattr(b, "demon_possessing", False)):
                    continue
                acx = a.x + a.w / 2; acy = a.y + a.h / 2
                bcx = b.x + b.w / 2; bcy = b.y + b.h / 2
                dx = bcx - acx; dy = bcy - acy
                dist_sq = dx * dx + dy * dy
                min_dist = a.radius + b.radius
                if dist_sq == 0: dx, dy = 0.01, 0.01; dist_sq = dx * dx + dy * dy
                if dist_sq < min_dist * min_dist:
                    dist = math.sqrt(dist_sq)
                    nx = dx / dist; ny = dy / dist
                    overlap = (min_dist - dist)
                    total_mass = a.mass + b.mass
                    if total_mass == 0: total_mass = 1
                    a_shift = overlap * (b.mass / total_mass)
                    b_shift = overlap * (a.mass / total_mass)
                    a.x -= nx * a_shift; a.y -= ny * a_shift
                    b.x += nx * b_shift; b.y += ny * b_shift
                    vn1 = a.vx * nx + a.vy * ny
                    vn2 = b.vx * nx + b.vy * ny
                    vt1 = -a.vx * ny + a.vy * nx
                    vt2 = -b.vx * ny + b.vy * nx
                    new_vn1 = (vn1 * (a.mass - b.mass) + 2 * b.mass * vn2) / total_mass
                    new_vn2 = (vn2 * (b.mass - a.mass) + 2 * a.mass * vn1) / total_mass
                    a.vx = new_vn1 * nx - vt1 * ny
                    a.vy = new_vn1 * ny + vt1 * nx
                    b.vx = new_vn2 * nx - vt2 * ny
                    b.vy = new_vn2 * ny + vt2 * nx
                    if a.power == "ripple": self.spawn_ripple(a)
                    if b.power == "ripple": self.spawn_ripple(b)
                    self.process_assassin_hit(a, b)
                    self.process_assassin_hit(b, a)
                    self.process_vampire_collision(a, b)
                    self.process_demon_collision(a, b)
                    self.apply_phoenix_collision_damage(a, b)
                    self.apply_phoenix_collision_damage(b, a)

    def handle_ball_collisions(self):
        n = len(self.balls)
        for i in range(n):
            for j in range(i + 1, n):
                b1 = self.balls[i]; b2 = self.balls[j]
                if not b1.alive or not b2.alive: continue
                if (getattr(b1, "profession", None) == "demon" and getattr(b1, "demon_possessing", False)) or (getattr(b2, "profession", None) == "demon" and getattr(b2, "demon_possessing", False)):
                    continue
                dx = b2.x - b1.x; dy = b2.y - b1.y
                dist_sq = dx * dx + dy * dy
                min_dist = b1.radius + b2.radius
                if dist_sq == 0: dx = 0.01; dy = 0.01; dist_sq = dx * dx + dy * dy
                if dist_sq < min_dist * min_dist:
                    dist = math.sqrt(dist_sq)
                    nx = dx / dist; ny = dy / dist
                    overlap = (min_dist - dist)
                    total_mass = b1.mass + b2.mass
                    if total_mass == 0: total_mass = 1
                    b1_shift = overlap * (b2.mass / total_mass)
                    b2_shift = overlap * (b1.mass / total_mass)
                    b1.x -= nx * b1_shift; b1.y -= ny * b1_shift
                    b2.x += nx * b2_shift; b2.y += ny * b2_shift
                    vn1 = b1.vx * nx + b1.vy * ny
                    vn2 = b2.vx * nx + b2.vy * ny
                    vt1 = -b1.vx * ny + b1.vy * nx
                    vt2 = -b2.vx * ny + b2.vy * nx
                    new_vn1 = (vn1 * (b1.mass - b2.mass) + 2 * b2.mass * vn2) / total_mass
                    new_vn2 = (vn2 * (b2.mass - b1.mass) + 2 * b1.mass * vn1) / total_mass
                    b1.vx = new_vn1 * nx - vt1 * ny
                    b1.vy = new_vn1 * ny + vt1 * nx
                    b2.vx = new_vn2 * nx - vt2 * ny
                    b2.vy = new_vn2 * ny + vt2 * nx
                    if b1.power == "ripple": self.spawn_ripple(b1)
                    if b2.power == "ripple": self.spawn_ripple(b2)
                    self.process_assassin_hit(b1, b2)
                    self.process_assassin_hit(b2, b1)
                    self.process_vampire_collision(b1, b2)
                    self.process_demon_collision(b1, b2)
                    self.apply_phoenix_collision_damage(b1, b2)
                    self.apply_phoenix_collision_damage(b2, b1)

    def handle_ball_block_collisions(self):
        for ball in self.balls:
            if not ball.alive: continue
            for block in self.blocks:
                if not block.alive: continue
                if (getattr(ball, "profession", None) == "demon" and getattr(ball, "demon_possessing", False)) or (getattr(block, "profession", None) == "demon" and getattr(block, "demon_possessing", False)):
                    continue
                cx = block.x + block.w / 2; cy = block.y + block.h / 2
                dx = ball.x - cx; dy = ball.y - cy
                dist_sq = dx * dx + dy * dy
                min_dist = ball.radius + block.radius
                if dist_sq == 0: dx, dy = 0.01, 0.01; dist_sq = dx * dx + dy * dy
                if dist_sq < min_dist * min_dist:
                    dist = math.sqrt(dist_sq)
                    nx = dx / dist; ny = dy / dist
                    overlap = (min_dist - dist)
                    total_mass = ball.mass + block.mass
                    if total_mass == 0: total_mass = 1
                    ball_shift = overlap * (block.mass / total_mass)
                    block_shift = overlap * (ball.mass / total_mass)
                    ball.x += nx * ball_shift; ball.y += ny * ball_shift
                    block.x -= nx * block_shift; block.y -= ny * block_shift
                    vn1 = ball.vx * nx + ball.vy * ny
                    vn2 = block.vx * nx + block.vy * ny
                    vt1 = -ball.vx * ny + ball.vy * nx
                    vt2 = -block.vx * ny + block.vy * nx
                    new_vn1 = (vn1 * (ball.mass - block.mass) + 2 * block.mass * vn2) / total_mass
                    new_vn2 = (vn2 * (block.mass - ball.mass) + 2 * ball.mass * vn1) / total_mass
                    ball.vx = new_vn1 * nx - vt1 * ny
                    ball.vy = new_vn1 * ny + vt1 * nx
                    block.vx = new_vn2 * nx - vt2 * ny
                    block.vy = new_vn2 * ny + vt2 * nx
                    if ball.power == "ripple": self.spawn_ripple(ball)
                    if block.power == "ripple": self.spawn_ripple(block)
                    self.process_assassin_hit(ball, block)
                    self.process_assassin_hit(block, ball)
                    self.process_vampire_collision(ball, block)
                    self.process_demon_collision(ball, block)
                    self.apply_phoenix_collision_damage(ball, block)
                    self.apply_phoenix_collision_damage(block, ball)

    def apply_aura_damage(self):
        current = set()
        for ent in self.all_entities():
            if ent.power != "aura": continue
            cx, cy = self.get_entity_center(ent)
            for target in self.all_entities():
                if target is ent or target.power == "aura": continue
                tx, ty = self.get_entity_center(target)
                dx = tx - cx; dy = ty - cy
                if dx * dx + dy * dy <= (ent.radius + 8 + target.radius) ** 2:
                    key = (id(ent), id(target))
                    current.add(key)
                    if key not in self.aura_contacts:
                        target.take_damage(attacker=ent)
        self.aura_contacts = current

    def apply_spike_damage(self):
        for ent in self.all_entities():
            if ent.power != "spike": continue
            rect = pygame.Rect(ent.x - getattr(ent, "radius", 0), ent.y - getattr(ent, "radius", 0), getattr(ent, "w", ent.radius * 2 if hasattr(ent, "radius") else 0), getattr(ent, "h", ent.radius * 2 if hasattr(ent, "radius") else 0))
            for target in self.all_entities():
                if target is ent or not target.alive: continue
                tx, ty = self.get_entity_center(target)
                closest_x = max(rect.left, min(tx, rect.right))
                closest_y = max(rect.top, min(ty, rect.bottom))
                dx = tx - closest_x; dy = ty - closest_y
                if dx * dx + dy * dy <= target.radius * target.radius:
                    target.take_damage(attacker=ent)

    def update_hex_burst_tasks(self, dt):
        new_tasks = []
        for task in self.hex_burst_tasks:
            task["delay"] -= dt
            if task["delay"] <= 0:
                owner = task.get("owner")
                if owner and owner.alive:
                    self.fire_hex_shot(owner)
            else:
                new_tasks.append(task)
        self.hex_burst_tasks = new_tasks

    def update_bullets(self, dt):
        bounds = self.get_bounds()
        alive = []
        for b in self.bullets:
            b.update(dt)
            out = False
            if bounds["shape"] == "rect":
                rect = bounds["rect"]
                if b.x < rect.left - 30 or b.x > rect.right + 30 or b.y < rect.top - 30 or b.y > rect.bottom + 30:
                    out = True
            else:
                cx, cy = bounds["center"]; r = bounds["radius"] + 30
                if (b.x - cx) ** 2 + (b.y - cy) ** 2 > r * r:
                    out = True
            if out:
                continue
            hit = False
            for ent in self.all_entities():
                if ent is b.owner or not ent.alive:
                    continue
                if getattr(b.owner, "profession", None) == "demon" and getattr(b.owner, "demon_host", None) is ent:
                    continue
                tx, ty = self.get_entity_center(ent)
                if (tx - b.x) ** 2 + (ty - b.y) ** 2 <= (ent.radius + b.h) ** 2:
                    ent.take_damage(attacker=b.owner)
                    hit = True
                    break
            if not hit:
                alive.append(b)
        self.bullets = alive

    def update_powers(self, dt):
        for ent in self.blocks + self.balls:
            if ent.power == "aura":
                ent.power_timer -= dt
                if ent.power_timer <= 0: ent.clear_power()
            elif ent.power == "spike":
                ent.power_timer -= dt
                if ent.power_timer <= 0: ent.clear_power()
            elif ent.power == "trail":
                ent.power_timer -= dt
                if ent.power_timer <= 0: ent.clear_power()
            elif ent.power == "ripple":
                ent.power_timer -= dt
                if ent.power_timer <= 0: ent.clear_power()
            elif ent.power == "bullet":
                has_bullet = any(b.owner is ent for b in self.bullets)
                if not has_bullet: ent.clear_power()

        if self.flash_timer > 0:
            self.flash_timer -= dt

    def update_freeze_emitters(self, dt):
        if not self.freeze_emitters:
            return
        new_emitters = []
        for emitter in self.freeze_emitters:
            owner = emitter.get("owner")
            if not owner or not owner.alive:
                continue
            emitter["time"] -= dt
            emitter["next_emit"] -= dt
            while emitter["time"] > 0 and emitter["next_emit"] <= 0:
                self.spawn_freeze_ripple(owner)
                emitter["next_emit"] += emitter["interval"]
            if emitter["time"] > 0:
                new_emitters.append(emitter)
        self.freeze_emitters = new_emitters

    def update_freeze_ripples(self, dt):
        updated = []
        for rp in self.freeze_ripples:
            rp.update(dt)
            if not rp.alive:
                continue
            for ent in self.all_entities():
                if ent is rp.owner or not ent.alive:
                    continue
                if id(ent) in rp.hit_ids:
                    continue
                cx, cy = self.get_entity_center(ent)
                dx = cx - rp.cx; dy = cy - rp.cy
                dist = math.hypot(dx, dy)
                if dist <= rp.radius + ent.radius:
                    self.apply_cold(ent, amount=1, source=rp.owner)
                    if getattr(ent, "element_immunity", 0) <= 0:
                        self.apply_freeze(ent)
                    rp.hit_ids.add(id(ent))
            updated.append(rp)
        self.freeze_ripples = [r for r in updated if r.alive]

    def update_floating_texts(self, dt):
        for ft in self.floating_texts:
            ft.update(dt)
        self.floating_texts = [ft for ft in self.floating_texts if ft.time_left > 0]

    def update_sweepers(self, dt):
        new_sweepers = []
        for sw in self.sweepers:
            sw.x += sw.vx * dt
            rect = sw.rect()
            if sw.vx > 0 and rect.left > sw.area_rect.right:
                sw.alive = False
            elif sw.vx < 0 and rect.right < sw.area_rect.left:
                sw.alive = False
            if not sw.alive:
                continue
            for ent in self.all_entities():
                if ent is sw.owner or not ent.alive:
                    continue
                if id(ent) in sw.hit_ids:
                    continue
                cx, cy = self.get_entity_center(ent)
                if rect.collidepoint(cx, cy):
                    ent.take_damage(attacker=sw.owner)
                    sw.hit_ids.add(id(ent))
            new_sweepers.append(sw)
        self.sweepers = [s for s in new_sweepers if s.alive]

        if getattr(self, "pending_top_sweeps", None):
            remaining = []
            for task in self.pending_top_sweeps:
                task["delay"] -= dt
                if task["delay"] <= 0:
                    sw = SweepRect(task["area"].left - task["bar_w"], task["y_top"], task["bar_w"], task["bar_h"], SWEEP_SPEED, task["owner"], task["area"])
                    self.sweepers.append(sw)
                else:
                    remaining.append(task)
            self.pending_top_sweeps = remaining

    def update_aoes(self, dt):
        new_aoes = []
        for aoe in self.aoes:
            aoe.update(dt)
            if not aoe.alive:
                continue
            for ent in self.all_entities():
                if ent is aoe.owner or not ent.alive:
                    continue
                if id(ent) in aoe.hit_ids:
                    continue
                cx, cy = self.get_entity_center(ent)
                dx = cx - aoe.cx; dy = cy - aoe.cy
                dist = math.hypot(dx, dy)
                if dist <= aoe.radius + ent.radius:
                    prev_hp = ent.hp
                    ent.hp -= 2
                    if CURRENT_GAME:
                        CURRENT_GAME.add_demon_rage_on_loss(ent, max(0, prev_hp - ent.hp))
                        handled = CURRENT_GAME.handle_phoenix_after_damage(ent)
                    else:
                        handled = False
                    if ent.hp <= 0 and not handled:
                        ent.alive = False
                    else:
                        if dist == 0:
                            dx, dy = 1, 0
                            dist = 1
                        if getattr(ent, "alive", False):
                            nx = dx / dist; ny = dy / dist
                            ent.vx += nx * 200
                            ent.vy += ny * 200
                    aoe.hit_ids.add(id(ent))
            new_aoes.append(aoe)
        self.aoes = [a for a in new_aoes if a.alive]

    def update_trails(self, dt):
        for ent in self.all_entities():
            if ent.power == "trail":
                ent.trail_emit_timer -= dt
                if ent.trail_emit_timer <= 0:
                    size = ent.radius * 2
                    cx, cy = self.get_entity_center(ent)
                    seg = TrailSegment(cx - size / 2, cy - size / 2, size, ent)
                    self.trails.append(seg)
                    ent.trail_emit_timer = TRAIL_EMIT_INTERVAL

        for seg in self.trails:
            seg.update(dt)
            if not seg.alive():
                continue
            rect = seg.rect()
            for ent in self.all_entities():
                if ent is seg.owner or not ent.alive:
                    continue
                if id(ent) in seg.hit_ids:
                    continue
                cx, cy = self.get_entity_center(ent)
                r = ent.radius
                closest_x = max(rect.left, min(cx, rect.right))
                closest_y = max(rect.top, min(cy, rect.bottom))
                dx = cx - closest_x
                dy = cy - closest_y
                if dx * dx + dy * dy <= r * r:
                    ent.take_damage(attacker=seg.owner)
                    seg.hit_ids.add(id(ent))

        self.trails = [t for t in self.trails if t.alive()]

    def update_ripples(self, dt):
        new_ripples = []
        for rp in self.ripples:
            rp.update(dt)
            if not rp.alive:
                continue
            for ent in self.all_entities():
                if ent is rp.owner or not ent.alive:
                    continue
                if id(ent) in rp.hit_ids:
                    continue
                cx, cy = self.get_entity_center(ent)
                dx = cx - rp.cx; dy = cy - rp.cy
                dist = math.hypot(dx, dy)
                if dist <= rp.radius + ent.radius:
                    ent.take_damage(attacker=rp.owner)
                    rp.hit_ids.add(id(ent))
            new_ripples.append(rp)
        self.ripples = [r for r in new_ripples if r.alive]

    def update_element_bursts(self, dt):
        updated = []
        for burst in self.element_bursts:
            burst.update(dt)
            if not burst.alive:
                continue
            for ent in self.all_entities():
                if not ent.alive:
                    continue
                if id(ent) in burst.hit_ids:
                    continue
                cx, cy = self.get_entity_center(ent)
                dx = cx - burst.cx; dy = cy - burst.cy
                dist = math.hypot(dx, dy)
                if dist <= burst.radius + ent.radius:
                    for _ in range(ELEMENT_EXPLOSION_DAMAGE):
                        ent.take_damage(attacker=burst.owner)
                    burst.hit_ids.add(id(ent))
            updated.append(burst)
        self.element_bursts = [b for b in updated if b.alive]

    def update_phoenix_waves(self, dt):
        updated = []
        for wave in self.phoenix_waves:
            wave.update(dt)
            if not wave.alive or not getattr(wave.owner, "alive", False):
                continue
            for ent in self.all_entities():
                if ent is wave.owner or not ent.alive:
                    continue
                if id(ent) in wave.hit_ids:
                    continue
                cx, cy = self.get_entity_center(ent)
                dx = cx - wave.cx; dy = cy - wave.cy
                dist = math.hypot(dx, dy)
                if dist <= wave.radius + ent.radius:
                    if dist == 0:
                        dx, dy = 1, 0
                        dist = 1
                    nx = dx / dist; ny = dy / dist
                    ent.vx += nx * PHOENIX_WAVE_PUSH
                    ent.vy += ny * PHOENIX_WAVE_PUSH
                    self.apply_fire(ent, amount=2, source=wave.owner)
                    wave.hit_ids.add(id(ent))
            updated.append(wave)
        self.phoenix_waves = [w for w in updated if w.alive]

    def start_triangle_effect(self, owner):
        targets = [e for e in self.all_entities() if e is not owner]
        if not targets:
            return False
        total_tokens = random.randint(3, 9)
        random.shuffle(targets)
        chosen = targets[: total_tokens] if len(targets) >= total_tokens else targets
        tri_targets = []
        tokens = []
        for tgt in chosen:
            cnt = random.randint(1, 3)
            tri_targets.append({"target": tgt, "count": cnt})
            for _ in range(cnt):
                tx, ty = self.get_entity_center(tgt)
                offset_x = random.uniform(-tgt.radius, tgt.radius)
                offset_y = random.uniform(-tgt.radius, tgt.radius)
                tokens.append(TriangleToken(tx + offset_x, ty + offset_y, tgt))

        self.triangle_effect = {"timer": 2.0, "targets": tri_targets, "owner": owner}
        self.triangle_tokens = tokens
        return True

    def update_triangles(self, dt):
        if not self.triangle_effect:
            return
        self.triangle_effect["timer"] -= dt

        remaining_tokens = []
        for tk in self.triangle_tokens:
            if not tk.alive:
                continue
            tgt_entry = next((t for t in self.triangle_effect["targets"] if t["target"] is tk.target), None)
            if not tgt_entry or tgt_entry["count"] <= 0:
                continue
            cx, cy = self.get_entity_center(tk.target)
            dx = cx - tk.x; dy = cy - tk.y
            dist = math.hypot(dx, dy)
            if dist <= tk.target.radius + tk.radius:
                tgt_entry["count"] -= 1
                tk.alive = False
            else:
                remaining_tokens.append(tk)
        self.triangle_tokens = remaining_tokens

        if self.triangle_effect["timer"] <= 0:
            owner = self.triangle_effect.get("owner")
            for entry in self.triangle_effect["targets"]:
                if entry["count"] > 0 and entry["target"].alive:
                    entry["target"].take_damage(attacker=owner)
            self.triangle_effect = None
            self.triangle_tokens = []

    def update_lightning_beams(self, dt):
        for b in self.lightning_beams:
            b["time"] -= dt
        self.lightning_beams = [b for b in self.lightning_beams if b["time"] > 0]

    def update_curse_marks(self, dt):
        for mk in self.curse_marks:
            mk["time"] -= dt
        self.curse_marks = [mk for mk in self.curse_marks if mk["time"] > 0]

    def do_tank_shockwave(self, tank):
        cx, cy = self.get_entity_center(tank)
        for ent in self.all_entities():
            if ent is tank or not ent.alive:
                continue
            tx, ty = self.get_entity_center(ent)
            dx = tx - cx; dy = ty - cy
            dist = math.hypot(dx, dy)
            if dist <= TANK_SHOCK_RADIUS and dist > 0:
                nx = dx / dist; ny = dy / dist
                ent.vx += nx * TANK_SHOCK_FORCE
                ent.vy += ny * TANK_SHOCK_FORCE

    def update_hunter(self, hunter, entities, dt):
        nearest = None; nearest_dist = 1e9
        hx, hy = self.get_entity_center(hunter)
        for ent in entities:
            if ent is hunter or not ent.alive: continue
            tx, ty = self.get_entity_center(ent)
            d2 = (tx - hx) ** 2 + (ty - hy) ** 2
            if d2 < nearest_dist:
                nearest_dist = d2; nearest = ent
        if not nearest: return
        tx, ty = self.get_entity_center(nearest)
        dir_x = tx - hx; dir_y = ty - hy
        if dir_x == 0 and dir_y == 0: return
        desired_angle = math.atan2(dir_y, dir_x)
        speed = math.hypot(hunter.vx, hunter.vy)
        target_vx = math.cos(desired_angle) * speed
        target_vy = math.sin(desired_angle) * speed
        rate = min(1.0, HUNTER_TURN_RATE * dt)
        hunter.vx = hunter.vx * (1 - rate) + target_vx * rate
        hunter.vy = hunter.vy * (1 - rate) + target_vy * rate

    def fire_lightning(self, caster, entities):
        cx, cy = self.get_entity_center(caster)
        others = [
            (math.hypot(self.get_entity_center(e)[0] - cx, self.get_entity_center(e)[1] - cy), e)
            for e in entities if e is not caster and e.alive
        ]
        others.sort(key=lambda x: x[0])
        for dist, ent in others[:LIGHTNING_MAX_TARGET]:
            ex, ey = self.get_entity_center(ent)
            ent.take_damage(attacker=caster)
            dx = ex - cx; dy = ey - cy
            dlen = math.hypot(dx, dy) or 1
            ent.vx += dx / dlen * LIGHTNING_PUSH
            ent.vy += dy / dlen * LIGHTNING_PUSH
            self.lightning_beams.append({"start": (cx, cy), "end": (ex, ey), "time": LIGHTNING_LIFE})

    def update_professions(self, dt):
        entities = self.all_entities()
        for ent in entities:
            ent.external_speed_scale = 1.0
        for ent in entities:
            p = ent.profession
            if p == "assassin":
                ent.assassin_cd -= dt
                if ent.assassin_active > 0:
                    ent.assassin_active -= dt
                elif ent.assassin_cd <= 0:
                    ent.assassin_active = ASSASSIN_BURST
                    ent.assassin_cd = ASSASSIN_COOLDOWN
                ent.speed_bonus = ASSASSIN_SPEED_MULT if ent.assassin_active > 0 else 1.0
                ent.mass = 1.5 if ent.assassin_active > 0 else 1.0
            elif p == "tank":
                ent.speed_base = TANK_SPEED_SCALE
                ent.mass = TANK_MASS
                ent.shock_cd -= dt
                if ent.shock_cd <= 0:
                    self.do_tank_shockwave(ent)
                    ent.shock_cd = TANK_SHOCK_CD
            elif p == "mage":
                ent.mage_cd -= dt
                if ent.mage_cd <= 0:
                    if ent.shield_charges < MAGE_MAX_ORBS:
                        ent.shield_charges += 1
                        ent.orb_angles.append(random.uniform(0, 2 * math.pi))
                    ent.mage_cd = MAGE_ORB_INTERVAL
                ent.orb_angles = [(a + dt * 2.5) % (2 * math.pi) for a in ent.orb_angles][:MAGE_MAX_ORBS]
            elif p == "time":
                ent.time_cd -= dt
                if ent.time_active > 0:
                    ent.time_active -= dt
                elif ent.time_cd <= 0:
                    ent.time_active = TIME_SLOW_DURATION
                    ent.time_cd = TIME_SLOW_CD
                if ent.time_active > 0:
                    cx, cy = self.get_entity_center(ent)
                    for target in entities:
                        if target is ent or not target.alive:
                            continue
                        tx, ty = self.get_entity_center(target)
                        if (tx - cx) ** 2 + (ty - cy) ** 2 <= TIME_SLOW_RADIUS ** 2:
                            target.external_speed_scale = min(target.external_speed_scale, TIME_SLOW_SCALE)
            elif p == "gravity":
                ent.gravity_cd -= dt
                if ent.gravity_active > 0:
                    ent.gravity_active -= dt
                    cx, cy = self.get_entity_center(ent)
                    for target in entities:
                        if target is ent or not target.alive:
                            continue
                        tx, ty = self.get_entity_center(target)
                        dx = tx - cx; dy = ty - cy
                        dist = math.hypot(dx, dy) + 1e-5
                        if dist <= ent.radius * GRAVITY_RADIUS_SCALE:
                            nx = dx / dist; ny = dy / dist
                            target.vx += nx * GRAVITY_FORCE * ent.gravity_mode * dt
                            target.vy += ny * GRAVITY_FORCE * ent.gravity_mode * dt
                elif ent.gravity_cd <= 0:
                    ent.gravity_active = GRAVITY_DURATION
                    ent.gravity_cd = GRAVITY_CD
                    ent.gravity_mode = random.choice([-1, 1])
            elif p == "hunter":
                self.update_hunter(ent, entities, dt)
                ent.hunter_shot_cd -= dt
                if ent.hunter_shot_cd <= 0:
                    fired = self.fire_bullet(ent)
                    ent.hunter_shot_cd = HUNTER_SHOT_CD
            elif p == "lightning":
                ent.lightning_cd -= dt
                if ent.lightning_cd <= 0:
                    self.fire_lightning(ent, entities)
                    ent.lightning_cd = LIGHTNING_CD
                    if random.random() < 0.1 and ent.alive:
                        ent.take_damage()
            elif p == "phoenix":
                if getattr(ent, "phoenix_egg", False):
                    ent.phoenix_egg_timer -= dt
                    ent.phoenix_wave_cd -= dt
                    if ent.phoenix_wave_cd <= 0:
                        self.spawn_phoenix_wave(ent)
                        ent.phoenix_wave_cd = PHOENIX_WAVE_INTERVAL
                    if ent.phoenix_egg_timer <= 0:
                        self.finish_phoenix_rebirth(ent)
                else:
                    ent.phoenix_perch_cd -= dt
                    if ent.phoenix_perch_cd <= 0 and not ent.phoenix_perching:
                        self.start_phoenix_perch(ent)
            elif p == "demon":
                self.update_demon(ent, entities, dt)
            elif p == "drone":
                if not hasattr(ent, "drones"):
                    ent.drones = []
                if not hasattr(ent, "drone_gain_timer"):
                    ent.drone_gain_timer = DRONE_GAIN_INTERVAL
                if not ent.drones:
                    ent.drones.append(self.create_drone_unit())

        ent.drone_gain_timer -= dt
        if ent.drone_gain_timer <= 0:
            if len(ent.drones) < DRONE_MAX_COUNT:
                ent.drones.append(self.create_drone_unit())
            ent.drone_gain_timer = DRONE_GAIN_INTERVAL

        cx, cy = self.get_entity_center(ent)
        for idx, drone in enumerate(ent.drones):
            if drone["phase"] is None:
                drone["phase"] = "orbit"
            if drone["phase"] == "orbit":
                drone["cd"] -= dt
                drone["angle"] = (drone["angle"] + dt * 2.0 + idx * 0.25) % (2 * math.pi)
                offset = ent.radius + 14 + idx * 6
                px = cx + math.cos(drone["angle"]) * offset
                py = cy + math.sin(drone["angle"]) * offset
                drone["pos"] = (px, py)
                if drone["cd"] <= 0:
                    ang = random.uniform(0, 2 * math.pi)
                    drone["dir"] = (math.cos(ang), math.sin(ang))
                    drone["phase"] = "fly"
                    drone["hit_ids"] = set()
            elif drone["phase"] == "fly":
                dx, dy = drone["dir"]
                px, py = drone["pos"]
                px += dx * DRONE_SPEED * dt
                py += dy * DRONE_SPEED * dt
                drone["pos"] = (px, py)
                for target in entities:
                    if target is ent or not target.alive:
                        continue
                    if id(target) in drone["hit_ids"]:
                        continue
                    tx, ty = self.get_entity_center(target)
                    if (tx - px) ** 2 + (ty - py) ** 2 <= (target.radius + DRONE_RADIUS) ** 2:
                        target.take_damage(attacker=ent)
                        drone["hit_ids"].add(id(target))
                bounds = self.get_bounds()
                out = False
                if bounds["shape"] == "rect":
                    rect = bounds["rect"]
                    if px < rect.left - 10 or px > rect.right + 10 or py < rect.top - 10 or py > rect.bottom + 10:
                        out = True
                else:
                    bx, by = bounds["center"]; r = bounds["radius"]
                    if (px - bx) ** 2 + (py - by) ** 2 > (r + 10) ** 2:
                        out = True
                if out:
                    drone["phase"] = "return"
            elif drone["phase"] == "return":
                px, py = drone["pos"]
                dx = cx - px; dy = cy - py
                dist = math.hypot(dx, dy)
                if dist < 6:
                    drone["phase"] = "orbit"
                    drone["cd"] = DRONE_CD
                else:
                    nx = dx / dist; ny = dy / dist
                    drone["pos"] = (px + nx * DRONE_SPEED * dt, py + ny * DRONE_SPEED * dt)
            elif p == "heavy":
                ent.heavy_cd -= dt
                ent.heavy_shield_cd -= dt
                if ent.heavy_shield_cd <= 0:
                    if ent.shield_charges < 3:
                        ent.shield_charges += 1
                    ent.heavy_shield_cd = 5.0
                if ent.heavy_state is None and ent.heavy_cd <= 0:
                    ent.heavy_state = "charge"
                    ent.heavy_charge_timer = 4.0
                    ent.heavy_charge_elapsed = 0.0
                    ent.heavy_target = None
                if ent.heavy_state == "charge":
                    ent.heavy_charge_elapsed += dt
                    ent.heavy_charge_timer -= dt
                    ent.external_speed_scale = max(0.5, 1.0 - 0.5 * (ent.heavy_charge_elapsed / 4.0))
                    if ent.heavy_charge_elapsed >= 3.0:
                        others = [e for e in entities if e is not ent and e.alive]
                        target = self.find_nearest(ent, others)
                        ent.heavy_target = target
                        if target and target.alive:
                            tx, ty = self.get_entity_center(target)
                            cx, cy = self.get_entity_center(ent)
                            dx = tx - cx; dy = ty - cy
                            dist = math.hypot(dx, dy) or 1.0
                            speed = 700
                            ent.vx = dx / dist * speed
                            ent.vy = dy / dist * speed
                            ent.heavy_state = "dash"
                            ent.heavy_dash_timer = 2.0
                            ent.external_speed_scale = 1.0
                        else:
                            ent.heavy_state = None
                            ent.heavy_cd = 8.0
                            ent.external_speed_scale = 1.0
                elif ent.heavy_state == "dash":
                    ent.heavy_dash_timer -= dt
                    hit = None
                    for other in entities:
                        if other is ent or not other.alive:
                            continue
                        ox, oy = self.get_entity_center(other)
                        cx, cy = self.get_entity_center(ent)
                        if (ox - cx) ** 2 + (oy - cy) ** 2 <= (other.radius + ent.radius) ** 2:
                            hit = other
                            break
                    if hit:
                        hit.take_damage(attacker=ent)
                        ent.take_damage()
                        ent.heavy_state = None
                        ent.heavy_cd = 8.0
                        ent.external_speed_scale = 1.0
                        ent.vx *= 0.2; ent.vy *= 0.2
                    elif ent.heavy_dash_timer <= 0:
                        ent.heavy_state = None
                        ent.heavy_cd = 8.0
                        ent.external_speed_scale = 1.0

    # ------ 牵引绳逻辑 ------ #
    def start_tether(self, owner):
        alive = [e for e in self.all_entities() if e is not owner]
        if len(alive) < 2:
            self.add_floating_text("没得牵了", owner)
            return False
        pair = random.sample(alive, 2)
        self.tethers.append({"a": pair[0], "b": pair[1], "active": True})
        return True

    def update_tethers(self, dt):
        new_tethers = []
        for t in self.tethers:
            a, b = t["a"], t["b"]
            if not a.alive or not b.alive:
                continue
            ax, ay = self.get_entity_center(a); bx, by = self.get_entity_center(b)
            dx = bx - ax; dy = by - ay
            dist = math.hypot(dx, dy)
            if dist > TETHER_MAX_DIST and dist > 0:
                pull = (dist - TETHER_MAX_DIST) * 0.5
                nx, ny = dx / dist, dy / dist
                a.x += nx * pull * 0.5
                a.y += ny * pull * 0.5
                b.x -= nx * pull * 0.5
                b.y -= ny * pull * 0.5
            new_tethers.append(t)
        self.tethers = new_tethers

    def draw_tethers(self):
        for t in self.tethers:
            a, b = t["a"], t["b"]
            if not a.alive or not b.alive:
                continue
            ax, ay = self.get_entity_center(a); bx, by = self.get_entity_center(b)
            pygame.draw.line(self.screen, THEME["accent"], (int(ax), int(ay)), (int(bx), int(by)), 2)

    def handle_tether_damage(self, victim, amount=1):
        remove = None
        partner = None
        for t in self.tethers:
            if victim is t["a"] or victim is t["b"]:
                partner = t["b"] if victim is t["a"] else t["a"]
                remove = t
                break
        if remove is None or not partner or not partner.alive:
            return
        self.tethers.remove(remove)
        partner.damage_from_tether = True
        partner.take_damage()

    # ------ 绘制辅助 ------ #
    def draw_walls(self):
        for w in self.walls: w.draw(self.screen)

    def draw_trails(self):
        for t in self.trails: t.draw(self.screen)

    def draw_ripples(self):
        for rp in self.ripples:
            alpha = int(200 * (rp.time_left / rp.duration))
            surf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(surf, (120, 200, 255, alpha), (int(rp.cx), int(rp.cy)), int(rp.radius), 2)
            self.screen.blit(surf, (0, 0))

    def draw_freeze_ripples(self):
        for rp in self.freeze_ripples:
            alpha = int(180 * (rp.time_left / rp.duration))
            surf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(surf, (180, 255, 255, alpha), (int(rp.cx), int(rp.cy)), int(rp.radius), 2)
            self.screen.blit(surf, (0, 0))

    def draw_element_bursts(self):
        for b in self.element_bursts:
            alpha = int(200 * max(0, b.time_left) / b.duration) if b.duration > 0 else 120
            surf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(surf, (235, 180, 255, alpha), (int(b.cx), int(b.cy)), int(b.radius), 3)
            self.screen.blit(surf, (0, 0))

    def draw_phoenix_waves(self):
        for w in self.phoenix_waves:
            alpha = int(170 * max(0, w.time_left) / w.duration)
            surf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 170, 90, alpha), (int(w.cx), int(w.cy)), int(w.radius), 3)
            self.screen.blit(surf, (0, 0))

    def draw_environment_overlays(self, bounds):
        if self.poison_active:
            surf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            if self.poison_shape == "circle":
                pygame.draw.circle(
                    surf,
                    (120, 200, 120, 140),
                    (int(self.poison_center[0]), int(self.poison_center[1])),
                    max(0, int(self.poison_radius)),
                    3,
                )
            else:
                if self.poison_rect:
                    pygame.draw.rect(
                        surf,
                        (120, 200, 120, 140),
                        self.poison_rect,
                        3,
                    )
            self.screen.blit(surf, (0, 0))
        if self.electric_walls and bounds["shape"] == "rect":
            rect = bounds["rect"]
            count = len(self.electric_walls)
            color = (255, 210, 80)
            for w in self.electric_walls:
                if w["side"] == "left":
                    pygame.draw.line(self.screen, color, (rect.left, rect.top), (rect.left, rect.bottom), 4)
                    pos = (rect.left - 26, rect.centery)
                elif w["side"] == "right":
                    pygame.draw.line(self.screen, color, (rect.right, rect.top), (rect.right, rect.bottom), 4)
                    pos = (rect.right + 10, rect.centery)
                elif w["side"] == "top":
                    pygame.draw.line(self.screen, color, (rect.left, rect.top), (rect.right, rect.top), 4)
                    pos = (rect.centerx, rect.top - 18)
                else:
                    pygame.draw.line(self.screen, color, (rect.left, rect.bottom), (rect.right, rect.bottom), 4)
                    pos = (rect.centerx, rect.bottom + 10)
                txt = self.font_small.render(str(count), True, color)
                self.screen.blit(txt, (pos[0] - txt.get_width() // 2, pos[1] - txt.get_height() // 2))

    def draw_env_status(self):
        env_info = ENV_CRISIS_OPTIONS.get(self.env_crisis, {"name": "无"})
        name = env_info.get("name", "无")
        if self.env_crisis == "none":
            status = f"环境危机：{name}"
        else:
            remain = max(0, int(max(0.0, ENV_START_TIME - self.elapsed_time))) if not self.env_enabled else 0
            status = f"{name} 剩余{remain}s"
        surf = self.font_small.render(status, True, THEME["text_main"])
        padding = 8
        bg_rect = pygame.Rect(
            self.play_width // 2 - surf.get_width() // 2 - padding,
            self.play_height - 28,
            surf.get_width() + padding * 2,
            22,
        )
        draw_ui_rect(self.screen, bg_rect, (*THEME["card_bg"], 200), border_radius=8)
        self.screen.blit(surf, (bg_rect.x + padding, bg_rect.y + 3))

    def draw_triangles(self):
        for tk in self.triangle_tokens:
            tk.draw(self.screen)
        if not self.triangle_effect:
            return
        for entry in self.triangle_effect["targets"]:
            tgt = entry["target"]
            if not tgt.alive:
                continue
            cnt = entry["count"]
            if cnt <= 0:
                continue
            cx, cy = self.get_entity_center(tgt)
            txt = self.font.render(str(cnt), True, (255, 105, 180))
            self.screen.blit(txt, (cx - txt.get_width() / 2, cy - tgt.radius - 24))

    def draw_mage_orbs(self):
        for ent in self.all_entities():
            if ent.profession != "mage":
                continue
            cx, cy = self.get_entity_center(ent)
            for ang in ent.orb_angles:
                ox = cx + math.cos(ang) * (ent.radius + 10)
                oy = cy + math.sin(ang) * (ent.radius + 10)
                pygame.draw.circle(self.screen, (140, 200, 255), (int(ox), int(oy)), 6)
            pygame.draw.circle(self.screen, (120, 180, 255), (int(cx), int(cy)), int(ent.radius + 4), 1)

    def draw_drones(self):
        for ent in self.all_entities():
            if ent.profession != "drone":
                continue
            for drone in getattr(ent, "drones", []):
                px, py = drone.get("pos") or self.get_entity_center(ent)
                r = DRONE_RADIUS
                p1 = (int(px), int(py - r))
                p2 = (int(px - r), int(py + r))
                p3 = (int(px + r), int(py + r))
                pygame.draw.polygon(self.screen, (75, 83, 32), [p1, p2, p3])

    def draw_vampire_marks(self):
        t = pygame.time.get_ticks() / 1000.0
        for ent in self.all_entities():
            count = getattr(ent, "vampire_marks", 0)
            if count <= 0:
                continue
            cx, cy = self.get_entity_center(ent)
            base_r = getattr(ent, "radius", max(getattr(ent, "w", 0), getattr(ent, "h", 0)) / 2) + 12
            for i in range(count):
                ang = 2 * math.pi * i / count + t * 1.2
                wobble = math.sin(t * 2 + i) * 3
                px = cx + math.cos(ang) * (base_r + wobble)
                py = cy + math.sin(ang) * (base_r + wobble)
                size = 8
                pts = [
                    (px, py - size / 2),
                    (px + size / 2, py),
                    (px, py + size / 2),
                    (px - size / 2, py),
                ]
                pygame.draw.polygon(self.screen, (140, 40, 50), pts)

    def draw_demon_overlays(self):
        for ent in self.all_entities():
            if getattr(ent, "profession", None) != "demon":
                continue
            cx, cy = self.get_entity_center(ent)
            if getattr(ent, "demon_possessing", False) and getattr(ent, "demon_host", None):
                hx, hy = self.get_entity_center(ent.demon_host)
                pygame.draw.line(self.screen, DEMON_RING_COLOR, (int(cx), int(cy)), (int(hx), int(hy)), 2)
            rage = getattr(ent, "demon_rage", 0)
            if rage <= 0 or getattr(ent, "demon_possessing", False):
                continue
            radius = ent.radius + 10
            rect = pygame.Rect(int(cx - radius), int(cy - radius), int(radius * 2), int(radius * 2))
            start_ang = -math.pi / 2
            end_ang = start_ang + (rage / getattr(ent, "demon_rage_max", DEMON_RAGE_MAX)) * 2 * math.pi
            pygame.draw.arc(self.screen, DEMON_RING_COLOR, rect, start_ang, end_ang, 4)

    def draw_lightning(self):
        for b in self.lightning_beams:
            alpha = int(255 * (b["time"] / LIGHTNING_LIFE))
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            pygame.draw.line(
                overlay,
                (120, 200, 255, alpha),
                (int(b["start"][0]), int(b["start"][1])),
                (int(b["end"][0]), int(b["end"][1])),
                3,
            )
            self.screen.blit(overlay, (0, 0))

    def draw_curse_marks(self):
        for mk in self.curse_marks:
            alpha = int(255 * (mk["time"] / CURSE_MARK_DURATION))
            size = 24
            overlay = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.line(overlay, (255, 80, 80, alpha), (0, 0), (size, size), 3)
            pygame.draw.line(overlay, (255, 80, 80, alpha), (0, size), (size, 0), 3)
            self.screen.blit(overlay, (mk["x"] - size / 2, mk["y"] - size / 2))

    def draw_floating_texts(self):
        for ft in self.floating_texts:
            surf = self.font.render(ft.text, True, ft.color)
            surf.set_alpha(int(255 * ft.alpha()))
            self.screen.blit(surf, (ft.x, ft.y))
    
    def draw_damage_stats(self):
        if not self.damage_stats:
            return
        entries = list(self.damage_stats.values())
        entries.sort(key=lambda e: e["damage"], reverse=True)
        x, y = 12, 12
        row_h = 22
        header = self.font_small.render("伤害统计", True, THEME["text_main"])
        panel_w = 200
        panel_h = header.get_height() + 10 + row_h * len(entries) + 6
        panel_rect = pygame.Rect(x, y, panel_w, panel_h)
        draw_ui_rect(self.screen, panel_rect, THEME["card_bg"], border_radius=8)
        self.screen.blit(header, (x + 10, y + 6))
        for idx, entry in enumerate(entries):
            row_y = y + 10 + header.get_height() + idx * row_h
            color_strip = pygame.Rect(x + 10, row_y, 6, row_h - 6)
            pygame.draw.rect(self.screen, entry.get("color", THEME["accent"]), color_strip, border_radius=2)
            txt = f"{entry.get('name','')} +{entry.get('damage',0)}"
            surf = self.font_small.render(txt, True, THEME["text_main"])
            self.screen.blit(surf, (x + 24, row_y))


    def update(self, dt):
        if self.state != "PLAYING":
            return
        self.update_playing(dt)

    def update_playing(self, dt):
        bounds = self.get_bounds()

        self.update_professions(dt)

        if not self.item:
            self.item_timer += dt
            if self.item_timer >= self.next_item_interval:
                self.spawn_item()
                self.item_timer = 0.0
                self.next_item_interval = random.uniform(ITEM_INTERVAL_MIN, ITEM_INTERVAL_MAX)

        for b in self.blocks:
            self.update_elemental_state(b, dt)
            if b.hurt_speed_timer > 0:
                b.hurt_speed_timer = max(0, b.hurt_speed_timer - dt)
            if b.hurt_slow_timer > 0:
                b.hurt_slow_timer = max(0, b.hurt_slow_timer - dt)
            was_frozen = b.freeze_timer > 0
            b.freeze_timer = max(0, b.freeze_timer - dt)
            if getattr(b, "phoenix_rest_timer", 0) > 0:
                b.phoenix_rest_timer = max(0, b.phoenix_rest_timer - dt)
            if b.freeze_timer > 0:
                b.vx = 0; b.vy = 0
                continue
            elif was_frozen:
                b.vx, b.vy = b.frozen_velocity
                if getattr(b, "cold_frozen", False) and b.freeze_timer <= 0:
                    b.cold_frozen = False
                    b.cold_stacks = 0
            if getattr(b, "phoenix_rest_timer", 0) > 0:
                b.vx = 0; b.vy = 0
                continue
            if getattr(b, "profession", None) == "demon" and getattr(b, "demon_possessing", False):
                host = getattr(b, "demon_host", None)
                if host and getattr(host, "alive", False):
                    hx, hy = self.get_entity_center(host)
                    b.demon_orbit_angle = (b.demon_orbit_angle + DEMON_ORBIT_SPEED * dt) % (2 * math.pi)
                    orbit_r = getattr(host, "radius", ENTITY_RADIUS) + getattr(b, "radius", ENTITY_RADIUS) + 6
                    ox = math.cos(b.demon_orbit_angle) * orbit_r
                    oy = math.sin(b.demon_orbit_angle) * orbit_r
                    if isinstance(b, Ball):
                        b.x, b.y = hx + ox, hy + oy
                    else:
                        b.x = hx + ox - b.w / 2
                        b.y = hy + oy - b.h / 2
                    b.vx = 0; b.vy = 0
                    continue
                else:
                    self.end_demon_possession(b)
            hit_wall = b.update(dt * self.get_speed_factor(b), bounds)
            if b.power == "ripple" and hit_wall:
                self.spawn_ripple(b)
            if getattr(b, "profession", None) == "heavy" and getattr(b, "heavy_state", None) == "dash" and hit_wall:
                b.take_damage()
                b.heavy_state = None
                b.heavy_cd = 8.0
                b.external_speed_scale = 1.0
                b.vx *= 0.2; b.vy *= 0.2
            if getattr(b, "profession", None) == "phoenix" and getattr(b, "phoenix_perching", False) and not getattr(b, "phoenix_egg", False) and hit_wall:
                b.phoenix_perching = False
                b.phoenix_rest_timer = PHOENIX_PERCH_REST
                b.vx = 0; b.vy = 0
                b.hp = min(b.max_hp, b.hp + 1)
                b.phoenix_perch_cd = PHOENIX_PERCH_INTERVAL
            if hit_wall:
                if self.electric_active:
                    self.electric_damage_on_hit(b, bounds)
                self.process_assassin_wall_hit(b)
        for ball in self.balls:
            self.update_elemental_state(ball, dt)
            if ball.hurt_speed_timer > 0:
                ball.hurt_speed_timer = max(0, ball.hurt_speed_timer - dt)
            if ball.hurt_slow_timer > 0:
                ball.hurt_slow_timer = max(0, ball.hurt_slow_timer - dt)
            was_frozen = ball.freeze_timer > 0
            ball.freeze_timer = max(0, ball.freeze_timer - dt)
            if getattr(ball, "phoenix_rest_timer", 0) > 0:
                ball.phoenix_rest_timer = max(0, ball.phoenix_rest_timer - dt)
            if ball.freeze_timer > 0:
                ball.vx = 0; ball.vy = 0
                continue
            elif was_frozen:
                ball.vx, ball.vy = ball.frozen_velocity
                if getattr(ball, "cold_frozen", False) and ball.freeze_timer <= 0:
                    ball.cold_frozen = False
                    ball.cold_stacks = 0
            if getattr(ball, "phoenix_rest_timer", 0) > 0:
                ball.vx = 0; ball.vy = 0
                continue
            if getattr(ball, "profession", None) == "demon" and getattr(ball, "demon_possessing", False):
                host = getattr(ball, "demon_host", None)
                if host and getattr(host, "alive", False):
                    hx, hy = self.get_entity_center(host)
                    ball.demon_orbit_angle = (ball.demon_orbit_angle + DEMON_ORBIT_SPEED * dt) % (2 * math.pi)
                    orbit_r = getattr(host, "radius", ENTITY_RADIUS) + getattr(ball, "radius", ENTITY_RADIUS) + 6
                    ox = math.cos(ball.demon_orbit_angle) * orbit_r
                    oy = math.sin(ball.demon_orbit_angle) * orbit_r
                    if isinstance(ball, Ball):
                        ball.x, ball.y = hx + ox, hy + oy
                    else:
                        ball.x = hx + ox - ball.w / 2
                        ball.y = hy + oy - ball.h / 2
                    ball.vx = 0; ball.vy = 0
                    continue
                else:
                    self.end_demon_possession(ball)
            hit_wall = ball.update(dt * self.get_speed_factor(ball), bounds)
            if ball.power == "ripple" and hit_wall:
                self.spawn_ripple(ball)
            if getattr(ball, "profession", None) == "heavy" and getattr(ball, "heavy_state", None) == "dash" and hit_wall:
                ball.take_damage()
                ball.heavy_state = None
                ball.heavy_cd = 8.0
                ball.external_speed_scale = 1.0
                ball.vx *= 0.2; ball.vy *= 0.2
            if getattr(ball, "profession", None) == "phoenix" and getattr(ball, "phoenix_perching", False) and not getattr(ball, "phoenix_egg", False) and hit_wall:
                ball.phoenix_perching = False
                ball.phoenix_rest_timer = PHOENIX_PERCH_REST
                ball.vx = 0; ball.vy = 0
                ball.hp = min(ball.max_hp, ball.hp + 1)
                ball.phoenix_perch_cd = PHOENIX_PERCH_INTERVAL
            if hit_wall:
                if self.electric_active:
                    self.electric_damage_on_hit(ball, bounds)
                self.process_assassin_wall_hit(ball)

        self.handle_wall_collisions()
        self.handle_block_collisions()
        self.handle_ball_block_collisions()
        self.handle_ball_collisions()

        self.handle_item_pickups()

        self.apply_aura_damage()
        self.apply_spike_damage()
        self.update_hex_burst_tasks(dt)
        self.update_bullets(dt)
        self.update_powers(dt)
        self.update_freeze_emitters(dt)
        self.update_freeze_ripples(dt)
        self.update_floating_texts(dt)
        self.update_sweepers(dt)
        self.update_aoes(dt)
        self.update_trails(dt)
        self.update_ripples(dt)
        self.update_element_bursts(dt)
        self.update_phoenix_waves(dt)
        self.update_triangles(dt)
        self.update_tethers(dt)
        self.update_environment(dt)
        self.handle_deaths()
        self.update_debris(dt)
        self.update_lightning_beams(dt)
        self.update_curse_marks(dt)
        self.update_walls(dt)

        self.blocks = [b for b in self.blocks if b.alive]
        self.balls = [c for c in self.balls if c.alive]

        if self.state == "PLAYING":
            survivors = self.all_entities()
            if len(survivors) == 1:
                last = survivors[0]
                self.winner_ent = last
                self.winner = last
                self.state = "TIME_UP"

        if self.time_limit is not None:
            self.time_left -= dt
            if self.time_left <= 0:
                self.time_left = 0
                self.state = "TIME_UP"
    def check_winner(self):
        alive = [e for e in self.blocks + self.balls if e.alive]
        alive.sort(key=lambda x: x.hp, reverse=True)
        if alive: self.winner = alive[0]

    # ------------------ UI 绘制核心 (简约版) ------------------ #
    def draw(self):
        if self.state in ("MENU", "INFO", "SETUP"):
            self.ensure_menu_window()
        self.screen.fill(THEME["bg"])
        
        # 1. 绘制极简网格背景
        grid_size = 40
        for x in range(0, self.window_width, grid_size):
            pygame.draw.line(self.screen, THEME["grid"], (x, 0), (x, self.window_height))
        for y in range(0, self.window_height, grid_size):
            pygame.draw.line(self.screen, THEME["grid"], (0, y), (self.window_width, y))

        if self.state == "MENU":
            self.draw_menu()
            pygame.display.flip()  # ensure menu frame renders
            return
        if self.state == "INFO":
            self.draw_info()
            pygame.display.flip()
            return
        if self.state == "SETUP":
            self.draw_setup()
            pygame.display.flip()
            return

        # 游戏内左上角伤害统计
        self.draw_damage_stats()

        # 2. 绘制地图边界
        bounds = self.get_bounds()
        if bounds["shape"] == "rect":
            pygame.draw.rect(self.screen, THEME["grid"], bounds["rect"], 2)
        else:
            pygame.draw.circle(self.screen, THEME["grid"], bounds["center"], bounds["radius"], 2)
        self.draw_environment_overlays(bounds)

        # 3. 绘制游戏物体
        if self.item: self.item.draw(self.screen)
        self.draw_walls()
        self.draw_trails()
        self.draw_debris()
        self.draw_ripples()
        self.draw_freeze_ripples()
        self.draw_element_bursts()
        self.draw_phoenix_waves()
        self.draw_triangles()
        self.draw_tethers()
        self.draw_vampire_marks()
        
        # 绘制所有实体
        all_ents = self.blocks + self.balls
        for ent in all_ents:
            if ent.alive: ent.draw(self.screen)
        self.draw_demon_overlays()
        self.draw_mage_orbs()
        self.draw_drones()

        for b in self.bullets: b.draw(self.screen)
        for sw in self.sweepers: pygame.draw.rect(self.screen, (255, 200, 80), sw.rect(), 2)
        for aoe in self.aoes:
            alpha = int(180 * (aoe.time_left / aoe.total_time))
            surf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 180, 80, alpha), (int(aoe.cx), int(aoe.cy)), int(aoe.radius), 2)
            self.screen.blit(surf, (0, 0))
        self.draw_lightning()
        self.draw_curse_marks()
        
        # 浮动文字
        self.draw_floating_texts()
        self.draw_env_status()

        # 4. 绘制右侧 UI 面板
        self.draw_sidebar()
        
        # 5. 绘制结束界面
        if self.state == "TIME_UP":
            overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            
            txt = "TIME UP"
            if self.winner: txt = f"WINNER: {self.winner.name}"
            
            t_surf = self.font_large.render(txt, True, THEME["text_main"])
            self.screen.blit(t_surf, (self.window_width//2 - t_surf.get_width()//2, self.window_height//2 - 50))
            
            sub = self.font.render("Press SPACE to Menu", True, THEME["text_sub"])
            self.screen.blit(sub, (self.window_width//2 - sub.get_width()//2, self.window_height//2 + 20))
        elif self.state == "PAUSE":
            self.draw_pause_overlay()

        pygame.display.flip()

    def draw_sidebar(self):
        # 绘制侧边栏背景
        panel_rect = pygame.Rect(self.play_width, 0, COUNTER_WIDTH, self.window_height)
        draw_ui_rect(self.screen, panel_rect, (*THEME["ui_panel_bg"], 255), border_radius=0)
        # 左边框线
        pygame.draw.line(self.screen, THEME["grid"], (self.play_width, 0), (self.play_width, self.window_height))

        # 1. 顶部时间（同步设置界面选择）
        if self.time_limit is None:
            t_surf = self.font_large.render("∞", True, THEME["accent"])
            self.screen.blit(t_surf, (self.play_width + 20, 20))
            l_surf = self.font_small.render("UNLIMITED", True, THEME["text_sub"])
            self.screen.blit(l_surf, (self.play_width + 22, 70))
        elif self.time_left is not None:
            time_str = f"{int(self.time_left)}"
            color = THEME["accent"] if self.time_left > 10 else THEME["hp_bar_fill"]
            t_surf = self.font_large.render(time_str, True, color)
            self.screen.blit(t_surf, (self.play_width + 20, 20))
            
            l_surf = self.font_small.render("SECONDS LEFT", True, THEME["text_sub"])
            self.screen.blit(l_surf, (self.play_width + 22, 70))
        
        # 2. 实体列表
        y_offset = 110
        card_h = 74  # 留出状态条空间
        ents = [e for e in self.blocks + self.balls if e.alive]
        ents.sort(key=lambda x: x.hp, reverse=True)

        for ent in ents:
            # 卡片背景
            card_rect = pygame.Rect(self.play_width + 10, y_offset, COUNTER_WIDTH - 20, card_h)
            draw_ui_rect(self.screen, card_rect, THEME["card_bg"], border_radius=6)
            
            # 左侧颜色条标记
            pygame.draw.rect(self.screen, ent.color, (self.play_width + 10, y_offset, 6, card_h), border_top_left_radius=6, border_bottom_left_radius=6)
            
            # 名字与职业
            prof_cn = PROFESSION_NAMES.get(ent.profession, ent.profession).upper()
            name_surf = self.font.render(prof_cn, True, THEME["text_main"])
            self.screen.blit(name_surf, (self.play_width + 25, y_offset + 6))

            bx = self.play_width + 25
            by = y_offset + 28
            bar_w = 120
            if ent.profession == "tank":
                # 8个红条，4个蓝条（蓝条抵消一次伤害）
                red_slots = 8
                blue_slots = 4
                slot_w = 12
                gap = 2
                # 红条
                for i in range(red_slots):
                    filled = i < max(0, min(red_slots, int(ent.hp)))
                    rect = pygame.Rect(bx + i * (slot_w + gap), by, slot_w, 8)
                    draw_ui_rect(self.screen, rect, THEME["hp_bar_bg"], border_radius=2)
                    if filled:
                        draw_ui_rect(self.screen, rect, THEME["hp_bar_fill"], border_radius=2)
                # 蓝条在下方
                for i in range(blue_slots):
                    filled = i < min(blue_slots, ent.shield_charges)
                    rect = pygame.Rect(bx + i * (slot_w + gap), by + 11, slot_w, 6)
                    draw_ui_rect(self.screen, rect, THEME["hp_bar_bg"], border_radius=2)
                    if filled:
                        draw_ui_rect(self.screen, rect, THEME["shield_fill"], border_radius=2)
            else:
                # HP 条
                bar_h = 6
                hp_pct = max(0, ent.hp / ent.max_hp)
                draw_bar(self.screen, bx, by, bar_w, bar_h, hp_pct, THEME["hp_bar_fill"], THEME["hp_bar_bg"])
                # 护盾覆盖
                if ent.shield_hp > 0:
                    s_pct = min(1.0, ent.shield_hp / 5.0) # 假设5是最大可视盾
                    draw_bar(self.screen, bx, by-8, bar_w, 4, s_pct, THEME["shield_fill"], (0,0,0,0))

                # 数值
                hp_txt = self.font_small.render(f"{int(ent.hp)}", True, THEME["text_main"])
                self.screen.blit(hp_txt, (bx + bar_w + 8, by - 6))

            status_y = y_offset + 42
            status_bars = []
            fire_val = FIRE_STACK_MAX if getattr(ent, "burning", False) else max(0, getattr(ent, "fire_stacks", 0))
            if fire_val > 0:
                status_bars.append(("焚烧" if getattr(ent, "burning", False) else "烈火", fire_val, FIRE_STACK_MAX, THEME["fire_bar"]))
            cold_val = COLD_STACK_MAX if getattr(ent, "cold_frozen", False) else max(0, getattr(ent, "cold_stacks", 0))
            if cold_val > 0:
                status_bars.append(("冰冻" if getattr(ent, "cold_frozen", False) else "寒冰", cold_val, COLD_STACK_MAX, THEME["cold_bar"]))

            for label, val, max_val, color in status_bars:
                pct = max(0.0, min(1.0, val / max_val))
                draw_bar(self.screen, bx, status_y, bar_w, 5, pct, color, THEME["hp_bar_bg"])
                txt = self.font_small.render(f"{label} {val}/{max_val}", True, THEME["text_sub"])
                self.screen.blit(txt, (bx + bar_w + 8, status_y - 4))
                status_y += 12

            y_offset += card_h + 12

    def draw_menu(self):
        # 极简菜单
        cx, cy = self.window_width // 2, self.window_height // 2 - 50
        self.menu_buttons = []
        
        # 标题
        title = "JUST BALLS FIGHT"
        t_surf = self.font_large.render(title, True, THEME["text_main"])
        self.screen.blit(t_surf, (cx - t_surf.get_width()//2, cy))
        
        # 分割线
        pygame.draw.line(self.screen, THEME["accent"], (cx - 60, cy + 60), (cx + 60, cy + 60), 2)
        
        # 选项（鼠标点击）
        opts = [
            ("start", "开始游戏"),
            ("compendium", "图鉴"),
            ("exit", "退出"),
        ]
        
        start_y = cy + 100
        button_gap = 60
        for i, (action, txt) in enumerate(opts):
            color = THEME["text_main"] if i == 0 else THEME["text_sub"]
            s = self.font.render(txt, True, color)
            padding = 16
            btn_rect = pygame.Rect(0, 0, s.get_width() + padding*2, s.get_height() + 10)
            btn_rect.center = (cx, start_y + i * button_gap)
            draw_ui_rect(self.screen, btn_rect, THEME["card_bg"], border_radius=8)
            pygame.draw.rect(self.screen, THEME["grid"], btn_rect, 1, border_radius=8)
            self.screen.blit(s, (btn_rect.centerx - s.get_width()//2, btn_rect.centery - s.get_height()//2))
            self.menu_buttons.append((action, btn_rect))

    def draw_info(self):
        self.screen.fill(THEME["bg"])
        cx, cy = self.window_width // 2, 80
        title = self.font_large.render("信息", True, THEME["text_main"])
        self.screen.blit(title, (cx - title.get_width()//2, cy))
        hint = self.font_small.render("[ESC] 返回菜单", True, THEME["text_sub"])
        self.screen.blit(hint, (16, 16))
        left_x = cx - 220
        right_x = cx + 60
        base_y = cy + 100

        # Tabs
        tab_prof = pygame.Rect(left_x, base_y - 40, 120, 28)
        tab_item = pygame.Rect(right_x, base_y - 40, 120, 28)
        self.menu_buttons = [("info_prof", tab_prof), ("info_item", tab_item)]
        draw_ui_rect(self.screen, tab_prof, THEME["card_bg"], border_radius=6)
        draw_ui_rect(self.screen, tab_item, THEME["card_bg"], border_radius=6)
        t1 = self.font_small.render("职业", True, THEME["text_main" if self.info_tab == "prof" else "text_sub"])
        t2 = self.font_small.render("道具", True, THEME["text_main" if self.info_tab == "item" else "text_sub"])
        self.screen.blit(t1, (tab_prof.centerx - t1.get_width()//2, tab_prof.centery - t1.get_height()//2))
        self.screen.blit(t2, (tab_item.centerx - t2.get_width()//2, tab_item.centery - t2.get_height()//2))

        mouse_pos = pygame.mouse.get_pos()
        hover_text = None
        # scroll handling
        scroll_area_top = base_y + 6
        scroll_area_height = self.window_height - scroll_area_top - 40
        scroll_offset = int(self.info_scroll)

        if self.info_tab == "prof":
            y = scroll_area_top - scroll_offset
            self.info_entries_prof = []
            prof_details = {
                "assassin": "刺客：加速冲刺，短期提升速度与质量。",
                "tank": "坦克：额外生命与震荡波，移动较慢。",
                "mage": "法师：生成护盾球体，旋转护身。",
                "time": "时间：周期减速附近敌人。",
                "gravity": "引力：周期吸引或排斥附近敌人。",
                "hunter": "猎手：自动跟踪最近目标调整方向；每8秒向最近目标方向发射一枚矩形子弹。",
                "lightning": "雷霆：周期链式闪电攻击附近目标。",
                "drone": "无人机：生成小型无人机飞行攻击。",
                "heavy": "巨力：10血；蓄力4秒逐渐降速至50%，3秒时朝最近目标猛冲，撞人或撞墙各扣1并结束；每5秒获得1蓝盾（上限3）。",
                "vampire": "吸血鬼：碰撞给对方叠暗红菱形标记，3层时再次碰撞会使目标掉1血、自己回1血，并清空标记。",
                "demon": "恶魔：碰撞积攒怒火；爆发时缩小至原体型的一半并对所有敌人造成1点伤害，随后追向最近目标附身。附身时自身受伤转移给宿主，宿主立即回复5生命且每4秒从附身体射出2枚随机方向的矩形子弹，宿主死亡后解除附身并恢复体型。",
                "phoenix": "凤凰：每20秒向最近边界俯冲，撞墙停驻3秒并回1血；首次致死化作半身大小、12血的蛋，期间每4秒释放1秒扩散至体型*5的推开波纹，被任何碰撞会掉1血，15秒存活则满血复活，剩余血量的一半（四舍五入）转为蓝色护盾。",
                "assassin": "刺客：模型更小；每次撞到边界速度*1.25并叠层（上限3）。层数达3后首次碰撞实体造成1点伤害并恢复原始速度，层数清零。",
            }
            for key, label in PROFESSION_NAMES.items():
                rect = pygame.Rect(left_x, y, 260, 26)
                if rect.bottom >= scroll_area_top and rect.top <= scroll_area_top + scroll_area_height:
                    draw_ui_rect(self.screen, rect, THEME["card_bg"], border_radius=4)
                    s = self.font_small.render(label, True, THEME["text_main"])
                    self.screen.blit(s, (rect.x + 8, rect.y + 4))
                self.info_entries_prof.append((label, prof_details.get(key, ""), rect))
                if rect.collidepoint(mouse_pos):
                    hover_text = prof_details.get(key, "")
                y += 30
        else:
            y = scroll_area_top - scroll_offset
            self.info_entries_item = []
            power_details = {
                "电刃环": "环形锯齿光环，接触伤害。",
                "三连弹": "朝前方三发子弹，自动瞄准。",
                "刺轮": "实体边缘长出尖刺，碰撞伤害。",
                "爆裂": "立刻对所有敌人造成伤害并标记。",
                "恢复+1": "生命+1，若低于上限。",
                "扫射": "横向扫射条带伤害，随后顶部下扫。",
                "范围震荡": "扩散圆形范围伤害并击退。",
                "毒雾": "移动留下伤害轨迹。",
                "冲击波": "扩散冲击，命中后消失。",
                "护盾": "增加护盾值，可抵挡伤害。",
                "墙体": "生成半透明墙体阻挡。",
                "全向连发": "全向多发子弹，并延迟再爆。",
                "冰冻波": "扩散冰波，命中冻结目标。",
                "追踪三角": "投掷三角标记，结算时伤害未清零目标。",
                "牵引": "随机将两个其他实体用绳相连，距离过远被拉回；受伤时两者分摊并立刻解除。场上不足3人时无效。",
            }
            power_labels = list(power_details.keys())
            for label in power_labels:
                rect = pygame.Rect(left_x, y, 320, 26)
                if rect.bottom >= scroll_area_top and rect.top <= scroll_area_top + scroll_area_height:
                    draw_ui_rect(self.screen, rect, THEME["card_bg"], border_radius=4)
                    s = self.font_small.render(label, True, THEME["text_main"])
                    self.screen.blit(s, (rect.x + 8, rect.y + 4))
                self.info_entries_item.append((label, power_details.get(label, ""), rect))
                if rect.collidepoint(mouse_pos):
                    hover_text = power_details.get(label, "")
                y += 30

        if hover_text:
            tooltip = self.font_small.render(hover_text, True, THEME["text_main"])
            tw, th = tooltip.get_width() + 12, tooltip.get_height() + 8
            tx, ty = mouse_pos
            tip_rect = pygame.Rect(tx + 12, ty + 12, tw, th)
            draw_ui_rect(self.screen, tip_rect, (*THEME["ui_panel_bg"], 230), border_radius=6)
            self.screen.blit(tooltip, (tip_rect.x + 6, tip_rect.y + 4))

    def draw_setup(self):
        self.screen.fill(THEME["bg"])
        cx, cy = self.window_width // 2, 120
        title = self.font_large.render("选择地图 / 实体数量", True, THEME["text_main"])
        self.screen.blit(title, (cx - title.get_width()//2, cy))
        hint = self.font_small.render("[ESC] 返回", True, THEME["text_sub"])
        self.screen.blit(hint, (16, 16))

        self.setup_buttons = []
        hover_text = None
        mouse_pos = pygame.mouse.get_pos()
        self.setup_row_tracks = {}
        self.setup_row_areas = {}
        margin_x = 40
        min_gap = 8
        max_gap = 24

        def layout_row(count, item_w, label_w, available):
            usable = max(0, available)
            if count <= 1:
                gap = 0
                total = item_w
            else:
                gap = (usable - item_w * count) / (count - 1)
                gap = max(min_gap, min(max_gap, gap))
                total = item_w * count + gap * (count - 1)
            start_x = margin_x + label_w + 12 + max(0, (usable - total) / 2)
            return [start_x + i * (item_w + gap) for i in range(count)]

        label_color = THEME["text_sub"]

        # 地图按钮
        map_y = cy + 80
        map_labels = [("正方形", 0), ("长方形", 1), ("圆形", 2)]
        label_map = self.font_small.render("地图", True, label_color)
        self.screen.blit(label_map, (margin_x, map_y + 12))
        map_item_w = 120
        map_row_h = 44
        map_available = self.window_width - margin_x * 2 - label_map.get_width() - 12
        map_total = len(map_labels) * map_item_w + min_gap * (len(map_labels) - 1)
        map_overflow = max(0, map_total - map_available)
        self.setup_row_offsets["map"] = max(0.0, min(map_overflow, self.setup_row_offsets.get("map", 0.0)))
        map_xs = layout_row(len(map_labels), map_item_w, label_map.get_width(), map_available)
        row_rect = pygame.Rect(margin_x, map_y, label_map.get_width() + 12 + map_available, map_row_h)
        self.setup_row_areas["map"] = row_rect
        if self.setup_row_active == "map":
            draw_ui_rect(self.screen, row_rect, (*THEME["card_bg"], 80), border_radius=6)
        start_shift = self.setup_row_offsets["map"]
        map_xs = [x - start_shift for x in map_xs]
        for (label, idx), x in zip(map_labels, map_xs):
            rect = pygame.Rect(x, map_y, map_item_w, map_row_h)
            active = (self.selected_map_index == idx)
            draw_ui_rect(self.screen, rect, THEME["card_bg"], border_radius=8)
            pygame.draw.rect(self.screen, THEME["accent"] if active else THEME["grid"], rect, 2, border_radius=8)
            txt = self.font.render(label, True, THEME["text_main"])
            self.screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
            self.setup_buttons.append(("map", rect, idx))
        if self.setup_row_active == "map" and map_overflow > 0:
            track_left = margin_x + label_map.get_width() + 12
            track_w = map_available
            knob_w = max(30, track_w * (track_w / map_total))
            knob_x = track_left + (track_w - knob_w) * (self.setup_row_offsets["map"] / map_overflow)
            slider_y = map_y + map_row_h + 4
            pygame.draw.rect(self.screen, THEME["grid"], (track_left, slider_y, track_w, 6), border_radius=3)
            pygame.draw.rect(self.screen, THEME["accent"], (knob_x, slider_y-2, knob_w, 10), border_radius=4)
            self.setup_row_tracks["map"] = {
                "track_left": track_left, "track_w": track_w, "knob_w": knob_w,
                "overflow": map_overflow, "total": map_total, "row": "map"
            }

        # 数量按钮
        count_y = map_y + 70
        label_count = self.font_small.render("人数", True, label_color)
        self.screen.blit(label_count, (margin_x, count_y + 8))
        counts = list(range(2, 9))
        count_item_w = 52
        count_row_h = 38
        count_available = self.window_width - margin_x * 2 - label_count.get_width() - 12
        count_total = len(counts) * count_item_w + min_gap * (len(counts) - 1)
        count_overflow = max(0, count_total - count_available)
        self.setup_row_offsets["count"] = max(0.0, min(count_overflow, self.setup_row_offsets.get("count", 0.0)))
        count_xs = layout_row(len(counts), count_item_w, label_count.get_width(), count_available)
        count_xs = [x - self.setup_row_offsets["count"] for x in count_xs]
        row_rect = pygame.Rect(margin_x, count_y, label_count.get_width() + 12 + count_available, count_row_h)
        self.setup_row_areas["count"] = row_rect
        if self.setup_row_active == "count":
            draw_ui_rect(self.screen, row_rect, (*THEME["card_bg"], 80), border_radius=6)
        for c, x in zip(counts, count_xs):
            rect = pygame.Rect(x, count_y, count_item_w, count_row_h)
            active = (self.selected_entity_count == c)
            draw_ui_rect(self.screen, rect, THEME["card_bg"], border_radius=6)
            pygame.draw.rect(self.screen, THEME["accent"] if active else THEME["grid"], rect, 2, border_radius=6)
            txt = self.font.render(str(c), True, THEME["text_main"])
            self.screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
            self.setup_buttons.append(("count", rect, c))
        if self.setup_row_active == "count" and count_overflow > 0:
            track_left = margin_x + label_count.get_width() + 12
            track_w = count_available
            knob_w = max(30, track_w * (track_w / count_total))
            knob_x = track_left + (track_w - knob_w) * (self.setup_row_offsets["count"] / count_overflow)
            slider_y = count_y + count_row_h + 4
            pygame.draw.rect(self.screen, THEME["grid"], (track_left, slider_y, track_w, 6), border_radius=3)
            pygame.draw.rect(self.screen, THEME["accent"], (knob_x, slider_y-2, knob_w, 10), border_radius=4)
            self.setup_row_tracks["count"] = {
                "track_left": track_left, "track_w": track_w, "knob_w": knob_w,
                "overflow": count_overflow, "total": count_total, "row": "count", "slider_y": slider_y
            }

        # 时间按钮
        time_y = count_y + 60
        label_time = self.font_small.render("时长", True, label_color)
        self.screen.blit(label_time, (margin_x, time_y + 8))
        time_opts = [30, 45, 60, None]
        time_labels = {30: "30秒", 45: "45秒", 60: "60秒", None: "无限"}
        time_item_w = 84
        time_row_h = 38
        time_available = self.window_width - margin_x * 2 - label_time.get_width() - 12
        time_total = len(time_opts) * time_item_w + min_gap * (len(time_opts) - 1)
        time_overflow = max(0, time_total - time_available)
        self.setup_row_offsets["time"] = max(0.0, min(time_overflow, self.setup_row_offsets.get("time", 0.0)))
        time_xs = layout_row(len(time_opts), time_item_w, label_time.get_width(), time_available)
        time_xs = [x - self.setup_row_offsets["time"] for x in time_xs]
        row_rect = pygame.Rect(margin_x, time_y, label_time.get_width() + 12 + time_available, time_row_h)
        self.setup_row_areas["time"] = row_rect
        if self.setup_row_active == "time":
            draw_ui_rect(self.screen, row_rect, (*THEME["card_bg"], 80), border_radius=6)
        for t, x in zip(time_opts, time_xs):
            rect = pygame.Rect(x, time_y, time_item_w, time_row_h)
            active = (self.selected_time_limit == t)
            draw_ui_rect(self.screen, rect, THEME["card_bg"], border_radius=6)
            pygame.draw.rect(self.screen, THEME["accent"] if active else THEME["grid"], rect, 2, border_radius=6)
            txt = self.font.render(time_labels[t], True, THEME["text_main"])
            self.screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
            self.setup_buttons.append(("time", rect, t))
        if self.setup_row_active == "time" and time_overflow > 0:
            track_left = margin_x + label_time.get_width() + 12
            track_w = time_available
            knob_w = max(30, track_w * (track_w / time_total))
            knob_x = track_left + (track_w - knob_w) * (self.setup_row_offsets["time"] / time_overflow)
            slider_y = time_y + time_row_h + 4
            pygame.draw.rect(self.screen, THEME["grid"], (track_left, slider_y, track_w, 6), border_radius=3)
            pygame.draw.rect(self.screen, THEME["accent"], (knob_x, slider_y-2, knob_w, 10), border_radius=4)
            self.setup_row_tracks["time"] = {
                "track_left": track_left, "track_w": track_w, "knob_w": knob_w,
                "overflow": time_overflow, "total": time_total, "row": "time", "slider_y": slider_y
            }

        # 环境危机
        env_y = time_y + 60
        label_env = self.font_small.render("环境", True, label_color)
        self.screen.blit(label_env, (margin_x, env_y + 8))
        env_keys = ["none", "poison", "electric", "thunder", "overload", "random"]
        env_item_w = 120
        env_row_h = 38
        env_available = self.window_width - margin_x * 2 - label_env.get_width() - 12
        env_total = len(env_keys) * env_item_w + min_gap * (len(env_keys) - 1)
        env_overflow = max(0, env_total - env_available)
        self.setup_row_offsets["env"] = max(0.0, min(env_overflow, self.setup_row_offsets.get("env", 0.0)))
        env_xs = layout_row(len(env_keys), env_item_w, label_env.get_width(), env_available)
        env_xs = [x - self.setup_row_offsets["env"] for x in env_xs]
        row_rect = pygame.Rect(margin_x, env_y, label_env.get_width() + 12 + env_available, env_row_h)
        self.setup_row_areas["env"] = row_rect
        if self.setup_row_active == "env":
            draw_ui_rect(self.screen, row_rect, (*THEME["card_bg"], 80), border_radius=6)
        for key, x in zip(env_keys, env_xs):
            rect = pygame.Rect(x, env_y, env_item_w, env_row_h)
            active = (self.selected_env == key)
            draw_ui_rect(self.screen, rect, THEME["card_bg"], border_radius=8)
            pygame.draw.rect(self.screen, THEME["accent"] if active else THEME["grid"], rect, 2, border_radius=8)
            label = ENV_CRISIS_OPTIONS[key]["name"]
            txt = self.font.render(label, True, THEME["text_main"])
            self.screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
            self.setup_buttons.append(("env", rect, key))
            if rect.collidepoint(mouse_pos):
                hover_text = ENV_CRISIS_OPTIONS[key]["desc"]
        if self.setup_row_active == "env" and env_overflow > 0:
            track_left = margin_x + label_env.get_width() + 12
            track_w = env_available
            knob_w = max(30, track_w * (track_w / env_total))
            knob_x = track_left + (track_w - knob_w) * (self.setup_row_offsets["env"] / env_overflow)
            slider_y = env_y + env_row_h + 4
            pygame.draw.rect(self.screen, THEME["grid"], (track_left, slider_y, track_w, 6), border_radius=3)
            pygame.draw.rect(self.screen, THEME["accent"], (knob_x, slider_y-2, knob_w, 10), border_radius=4)
            self.setup_row_tracks["env"] = {
                "track_left": track_left, "track_w": track_w, "knob_w": knob_w,
                "overflow": env_overflow, "total": env_total, "row": "env", "slider_y": slider_y
            }

        # 开始按钮
        start_rect = pygame.Rect(cx - 70, env_y + 70, 140, 44)
        draw_ui_rect(self.screen, start_rect, THEME["accent"], border_radius=10)
        start_txt = self.font.render("开始", True, THEME["bg"])
        self.screen.blit(start_txt, (start_rect.centerx - start_txt.get_width()//2, start_rect.centery - start_txt.get_height()//2))
        self.setup_buttons.append(("start_play", start_rect, None))

        if hover_text:
            tooltip = self.font_small.render(hover_text, True, THEME["text_main"])
            tw, th = tooltip.get_width() + 12, tooltip.get_height() + 8
            tx, ty = mouse_pos
            tip_rect = pygame.Rect(tx + 12, ty + 12, tw, th)
            draw_ui_rect(self.screen, tip_rect, (*THEME["ui_panel_bg"], 230), border_radius=6)
            self.screen.blit(tooltip, (tip_rect.x + 6, tip_rect.y + 4))

    def draw_pause_overlay(self):
        overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        cx, cy = self.window_width // 2, self.window_height // 2
        title = self.font_large.render("暂停", True, THEME["text_main"])
        self.screen.blit(title, (cx - title.get_width()//2, cy - 100))
        hint = self.font_small.render("ESC 继续", True, THEME["text_sub"])
        self.screen.blit(hint, (cx - hint.get_width()//2, cy - 60))

        self.pause_buttons = []
        btns = [
            ("resume", "返回游戏", (cx - 140, cy)),
            ("settings", "返回游戏设置", (cx - 140, cy + 70)),
            ("exit", "退出", (cx - 140, cy + 140)),
        ]
        for action, label, (bx, by) in btns:
            rect = pygame.Rect(bx, by, 280, 44)
            draw_ui_rect(self.screen, rect, THEME["card_bg"], border_radius=8)
            pygame.draw.rect(self.screen, THEME["grid"], rect, 1, border_radius=8)
            txt = self.font.render(label, True, THEME["text_main"])
            self.screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
            self.pause_buttons.append((action, rect))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        global CURRENT_GAME
        CURRENT_GAME = self
        while running:
            dt = clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "INFO":
                            self.state = "MENU"
                        elif self.state == "SETUP":
                            self.state = "MENU"
                        elif self.state == "PAUSE":
                            self.state = "PLAYING"
                        elif self.state == "TIME_UP":
                            self.state = "MENU"
                        else:
                            self.state = "PAUSE"
                        continue
                    if self.state == "TIME_UP":
                        if event.key == pygame.K_SPACE:
                            self.state = "MENU"
                elif event.type == pygame.MOUSEWHEEL:
                    if self.state == "INFO":
                        self.info_scroll = max(0, self.info_scroll - event.y * 20)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if self.state == "MENU":
                        for action, rect in self.menu_buttons:
                            if rect.collidepoint(mx, my):
                                if action == "start":
                                    self.state = "SETUP"
                                elif action == "compendium":
                                    self.state = "INFO"
                                elif action == "exit":
                                    running = False
                                break
                    elif self.state == "SETUP":
                        for key, rect in getattr(self, "setup_row_areas", {}).items():
                            if rect.collidepoint(mx, my):
                                self.setup_row_active = key
                        for key, track in getattr(self, "setup_row_tracks", {}).items():
                            slider_y = track.get("slider_y")
                            if slider_y is None:
                                continue
                            knob_w = track["knob_w"]
                            knob_x = track["track_left"] + (track["track_w"] - knob_w) * (self.setup_row_offsets.get(key, 0.0) / max(track["overflow"], 1e-6))
                            knob_rect = pygame.Rect(knob_x, slider_y-2, knob_w, 10)
                            if knob_rect.collidepoint(mx, my):
                                self.setup_slider_drag = key
                                break
                        for action, rect, payload in self.setup_buttons:
                            if rect.collidepoint(mx, my):
                                if action == "map":
                                    self.selected_map_index = payload
                                elif action == "count":
                                    self.selected_entity_count = payload
                                elif action == "time":
                                    self.selected_time_limit = payload
                                elif action == "env":
                                    self.selected_env = payload
                                elif action == "start_play":
                                    self.map_index = self.selected_map_index
                                    self.setup_map_dimensions(MAPS[self.map_index])
                                    self.load_scene(self.scene_index, total_entities=self.selected_entity_count, time_limit_override=self.selected_time_limit)
                                break
                    elif self.state == "INFO":
                        # tab switching via click
                        for action, rect in self.menu_buttons:
                            if rect.collidepoint(mx, my):
                                if action == "info_prof":
                                    self.info_tab = "prof"
                                elif action == "info_item":
                                    self.info_tab = "item"
                                break
                    elif self.state == "PAUSE":
                        for action, rect in self.pause_buttons:
                            if rect.collidepoint(mx, my):
                                if action == "resume":
                                    self.state = "PLAYING"
                                elif action == "settings":
                                    self.state = "SETUP"
                                    self.setup_row_active = None
                                    self.setup_slider_drag = None
                                elif action == "exit":
                                    running = False
                                break
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.setup_slider_drag = None
                elif event.type == pygame.MOUSEMOTION:
                    if self.setup_slider_drag and self.setup_slider_drag in self.setup_row_tracks:
                        track = self.setup_row_tracks[self.setup_slider_drag]
                        knob_w = track["knob_w"]
                        track_w = track["track_w"]
                        mx, my = event.pos
                        ratio = (mx - track["track_left"] - knob_w / 2) / max(track_w - knob_w, 1e-6)
                        ratio = max(0.0, min(1.0, ratio))
                        self.setup_row_offsets[self.setup_slider_drag] = ratio * track["overflow"]

            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game(SCENES)
    game.run()
