import sys
import math
import random
import pygame

UI_HEIGHT = 80  # 底部UI高度

BUFF_DURATION = 4.0
ITEM_INTERVAL_MIN = 5.0
ITEM_INTERVAL_MAX = 8.0
ITEM_MAX_COUNT = 3
BULLET_SPEED = 420.0
HEX_BURST_COUNT = 6
HEX_BURST_DELAY = 2.0
AURA_COLOR = (255, 215, 0)
AURA_TEETH = 12
AURA_OUTER_OFFSET = 8
AURA_INNER_OFFSET = 3
AURA_WIDTH = 3
SPIKE_DURATION = 2.0
SPEED_SCALE = 1.25
SPIKE_BAND = 12
SPIKE_TOOTH_W = 12
SPIKE_TOOTH_H = 10
FLASH_DURATION = 0.3
SWEEP_SPEED = 480
COUNTER_WIDTH = 180
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
COLOR_PALETTE = [
    (80, 200, 80),
    (200, 80, 80),
    (80, 160, 220),
    (220, 220, 80),
    (200, 120, 240),
    (120, 220, 200),
    (240, 160, 80),
    (160, 80, 200),
    (90, 220, 140),
    (220, 140, 140),
]
ASSASSIN_BURST = 1.0
ASSASSIN_COOLDOWN = 3.5
ASSASSIN_SPEED_MULT = 1.8
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
LIGHTNING_CD = 10.0
LIGHTNING_MAX_TARGET = 3
LIGHTNING_PUSH = 220
LIGHTNING_LIFE = 0.25


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


def scale_color(color, factor):
    """Clamp color multiplier for quick shading tweaks."""
    return tuple(min(255, max(0, int(c * factor))) for c in color)

# 优先选择支持中文的字体，避免界面文字显示成方框
PREFERRED_FONTS = [
    "Microsoft YaHei UI",
    "Microsoft YaHei",
    "SimHei",
    "SimSun",
    "Noto Sans CJK SC",
    "Source Han Sans SC",
    "Arial Unicode MS",
]

# ------------------ 场景配置：在这里自定义 ------------------ #
SCENES = [
    {
        "name": "基础场景",
        "shape": "rect",
        "time_limit": 60,     # 秒
        # 方块人物：自动移动 + 碰到边界几何反弹
        "blocks": [
            {
                "pos": (200, 200),
                "vel": (220, 150),
                "color": (80, 200, 80),
            },
            {
                "pos": (450, 300),
                "vel": (-180, -140),
                "color": (200, 80, 80),
            },
        ],
        # 小球：自动移动 + 碰到边界反弹 + 小球之间弹性碰撞（但不掉血）
        "balls": [
            {
                "pos": (320, 160),
                "vel": (160, 140),
                "color": (80, 160, 220),
            },
            {
                "pos": (520, 260),
                "vel": (-140, -160),
                "color": (220, 220, 80),
            },
        ],
    },
    {
        "name": "高速乱斗",
        "shape": "rect",
        "time_limit": 60,
        "blocks": [
            {
                "pos": (150, 250),
                "vel": (260, 210),
                "color": (200, 120, 80),
            },
        ],
        "balls": [
            {
                "pos": (300, 200),
                "vel": (260, 220),
                "color": (80, 160, 220),
            },
            {
                "pos": (380, 260),
                "vel": (-240, 170),
                "color": (220, 80, 160),
            },
            {
                "pos": (460, 220),
                "vel": (230, -190),
                "color": (120, 220, 80),
            },
            {
                "pos": (540, 260),
                "vel": (-260, -200),
                "color": (220, 220, 80),
            },
        ],
    },
    {
        "name": "无尽模式",
        "shape": "circle",
        "time_limit": None,  # 无时间限制
        "blocks": [
            {
                "pos": (240, 260),
                "vel": (240, 200),
                "color": (160, 120, 240),
            },
            {
                "pos": (520, 320),
                "vel": (-200, 180),
                "color": (240, 140, 120),
            },
        ],
        "balls": [
            {
                "pos": (360, 200),
                "vel": (200, -180),
                "color": (90, 200, 200),
            },
            {
                "pos": (620, 240),
                "vel": (-220, 190),
                "color": (230, 200, 90),
            },
        ],
    },
]

# 可选地图（尺寸 / 形状）
MAPS = [
    {"name": "标准方形", "width": 600, "height": 600, "shape": "rect", "border_margin": 40},
    {"name": "宽屏方形", "width": 960, "height": 600, "shape": "rect", "border_margin": 40},
    {"name": "大圆形", "width": 880, "height": 640, "shape": "circle", "border_margin": 50},
]

EFFECTS = [
    {"name": "1. 锯齿护环", "desc": "持续4秒的锯齿护环，接触其他实体使其计数-1，需分开后再触发下一次"},
    {"name": "2. 三连发子弹", "desc": "立即向最近实体连发3颗子弹，命中使其计数-1"},
    {"name": "3. 锯齿边", "desc": "持续2秒，在上下或左右长出锯齿，接触使对方计数-1"},
    {"name": "4. 诅咒冲击", "desc": "让除自己外的所有实体计数-1，并在头顶出现渐隐的X标记"},
    {"name": "5. 回复+1", "desc": "为自己恢复1点计数（上限5）"},
    {"name": "6. 扫荡条", "desc": "下半场左到右、上半场右到左依次扫过矩形，被扫到的其他实体计数-1"},
    {"name": "7. 扩散震荡", "desc": "脚下生成扩散圆，5秒后消失；范围内其他实体计数-2并被弹开"},
    {"name": "8. 燃烧轨迹", "desc": "2秒内沿途留下矩形轨迹，其他实体经过计数-1；轨迹持续1秒后消失"},
    {"name": "9. 碰撞波纹", "desc": "碰墙或撞球时在原地留下扩散波纹，范围到自身3倍，其他实体首次进入范围计数-1，波纹持续2秒"},
    {"name": "10. 护盾", "desc": "获得1点护盾（绿条显示），受到伤害优先消耗护盾"},
    {"name": "11. 粉色三角计数", "desc": "随机生成粉色三角给其他实体一个1~3的倒计时，吃掉三角计数-1，2秒后计数>0则受1点伤害"},
    {"name": "12. 阻挡墙", "desc": "随机生成一堵长方形墙阻挡实体，存在15秒后消失"},
    {"name": "13. 六向双重弹", "desc": "随机朝六个方向发射弹体，两秒后自动重复一次，命中使受击实体计数-1"},
    {"name": "14. 定身波纹", "desc": "获得后持续6秒，每2秒扩散一圈波纹，命中其他实体令其速度在1秒内变为0，随后恢复"},
]

PROFESSIONS = [
    "assassin",
    "tank",
    "mage",
    "time",
    "gravity",
    "hunter",
    "lightning",
    "drone",
]

PROFESSION_NAMES = {
    "assassin": "刺客",
    "tank": "坦克",
    "mage": "法师",
    "time": "时间者",
    "gravity": "引力球",
    "hunter": "追猎者",
    "lightning": "闪电",
    "drone": "无人机",
}

PROFS_INFO = [
    ("刺客", "敏捷冲刺者，周期性获得1.8倍速度冲刺，碰撞冲击力更高。"),
    ("坦克", "高质量低移速，额外+5计数并以蓝条显示；周期性释放冲击波推开周围目标。"),
    ("法师", "每5秒生成旋转护盾球，最多2个，抵挡一次伤害；带魔法光辉。"),
    ("时间者", "周期性在身边减速其他实体，自己不受影响。"),
    ("引力球", "以1.5倍自身半径为范围，周期制造引力（吸/斥）场影响周围实体。"),
    ("追猎者", "自动微调朝最近目标前进，持续逼近。"),
    ("闪电", "周期向最近1~3个目标释放闪电链，造成伤害并轻推。"),
    ("无人机", "周身环绕橄榄绿小三角，每8秒随机方向穿越全场造成1点伤害；每20秒自动增加一个小三角，最多3个。"),
]


# ------------------ 实体类 ------------------ #
class Block:
    """方块人物：自动移动，碰到边界反弹"""

    def __init__(self, x, y, w, h, vx, vy, color):
        self.x = float(x)
        self.y = float(y)
        self.w = w
        self.h = h
        self.radius = max(w, h) / 2
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        self.alive = True
        self.max_hp = MAX_HP
        self.hp = self.max_hp
        self.shield_hp = 0
        self.name = ""
        self.power = None   # None / "aura" / "bullet"
        self.power_timer = 0.0
        self.spike_axis = None
        self.pending_bullet = False
        self.death_effect_done = False
        self.trail_emit_timer = 0.0
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

    def update(self, dt, bounds_rect):
        # 按速度移动
        hit_wall = False
        self.x += self.vx * dt
        self.y += self.vy * dt

        shape = bounds_rect["shape"]
        if shape == "rect":
            rect = bounds_rect["rect"]
            if self.x < rect.left:
                self.x = rect.left
                self.vx *= -1
                hit_wall = True
            elif self.x + self.w > rect.right:
                self.x = rect.right - self.w
                self.vx *= -1
                hit_wall = True

            if self.y < rect.top:
                self.y = rect.top
                self.vy *= -1
                hit_wall = True
            elif self.y + self.h > rect.bottom:
                self.y = rect.bottom - self.h
                self.vy *= -1
                hit_wall = True
        else:
            cx = self.x + self.w / 2
            cy = self.y + self.h / 2
            bx, by = bounds_rect["center"]
            r_bound = bounds_rect["radius"]
            dx = cx - bx
            dy = cy - by
            dist = math.hypot(dx, dy)
            if dist + self.radius > r_bound:
                if dist == 0:
                    dx, dy = 0.01, 0.01
                    dist = math.hypot(dx, dy)
                nx = dx / dist
                ny = dy / dist
                new_dist = r_bound - self.radius
                cx = bx + nx * new_dist
                cy = by + ny * new_dist
                self.x = cx - self.w / 2
                self.y = cy - self.h / 2
                dot = self.vx * nx + self.vy * ny
                self.vx -= 2 * dot * nx
                self.vy -= 2 * dot * ny
                hit_wall = True

        # 防止速度过低停下
        self.vx, self.vy = enforce_min_speed(self.vx, self.vy, BALL_MIN_SPEED)
        return hit_wall

    def draw(self, surface):
        cx = self.x + self.w / 2
        cy = self.y + self.h / 2
        pygame.draw.circle(surface, self.color, (int(cx), int(cy)), int(self.radius))

        base_r = self.radius
        if self.power == "aura":
            draw_saw_ring(surface, cx, cy, base_r + 2)
        elif self.power == "bullet":
            p1 = (cx, self.y - 6)
            p2 = (self.x, self.y + self.h + 6)
            p3 = (self.x + self.w, self.y + self.h + 6)
            pygame.draw.polygon(surface, AURA_COLOR, [p1, p2, p3])
        elif self.power == "spike":
            draw_spike_edges(surface, (self.x, self.y, self.w, self.h), self.spike_axis or "tb")

    def take_damage(self):
        if not self.alive:
            return
        if getattr(self, "shield_charges", 0) > 0:
            self.shield_charges -= 1
            if getattr(self, "profession", "") == "mage" and self.orb_angles:
                self.orb_angles.pop()
            return
        if getattr(self, "shield_hp", 0) > 0:
            self.shield_hp -= 1
            return
        self.hurt_speed_timer = HURT_SPEED_DURATION
        self.hurt_slow_timer = HURT_SPEED_DURATION + HURT_SLOW_DURATION
        self.hp -= 1
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
        self.power_duration = 0
        self.spike_axis = None
        self.pending_bullet = False
        self.trail_emit_timer = 0.0


class Ball:
    """小球：自动移动 + 边界反弹 + 球-球弹性碰撞"""

    def __init__(self, x, y, radius, vx, vy, color):
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        self.alive = True
        self.max_hp = MAX_HP
        self.hp = self.max_hp
        self.shield_hp = 0
        self.name = ""
        self.power = None   # None / "aura" / "bullet"
        self.power_timer = 0.0
        self.spike_axis = None
        self.pending_bullet = False
        self.death_effect_done = False
        self.trail_emit_timer = 0.0
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
        self.trail_emit_timer = 0.0
        self.freeze_timer = 0.0
        self.frozen_velocity = (0.0, 0.0)

    def update(self, dt, bounds_rect):
        # 位置更新
        hit_wall = False
        self.x += self.vx * dt
        self.y += self.vy * dt

        shape = bounds_rect["shape"]
        if shape == "rect":
            rect = bounds_rect["rect"]
            if self.x - self.radius < rect.left:
                self.x = rect.left + self.radius
                self.vx *= -1
                hit_wall = True
            elif self.x + self.radius > rect.right:
                self.x = rect.right - self.radius
                self.vx *= -1
                hit_wall = True

            if self.y - self.radius < rect.top:
                self.y = rect.top + self.radius
                self.vy *= -1
                hit_wall = True
            elif self.y + self.radius > rect.bottom:
                self.y = rect.bottom - self.radius
                self.vy *= -1
                hit_wall = True
        else:
            bx, by = bounds_rect["center"]
            r_bound = bounds_rect["radius"]
            dx = self.x - bx
            dy = self.y - by
            dist = math.hypot(dx, dy)
            if dist + self.radius > r_bound:
                if dist == 0:
                    dx, dy = 0.01, 0.01
                    dist = math.hypot(dx, dy)
                nx = dx / dist
                ny = dy / dist
                new_dist = r_bound - self.radius
                self.x = bx + nx * new_dist
                self.y = by + ny * new_dist
                dot = self.vx * nx + self.vy * ny
                self.vx -= 2 * dot * nx
                self.vy -= 2 * dot * ny
                hit_wall = True

        # 防止速度过低停下
        self.vx, self.vy = enforce_min_speed(self.vx, self.vy, BALL_MIN_SPEED)
        return hit_wall

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

        if self.power == "aura":
            draw_saw_ring(surface, self.x, self.y, self.radius + 4)
        elif self.power == "bullet":
            r = self.radius
            p1 = (self.x, self.y - r - 6)
            p2 = (self.x - r - 6, self.y + r + 6)
            p3 = (self.x + r + 6, self.y + r + 6)
            pygame.draw.polygon(surface, AURA_COLOR, [p1, p2, p3])
        elif self.power == "spike":
            draw_spike_edges(surface, (self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2), self.spike_axis or "tb")

    def take_damage(self):
        if not self.alive:
            return
        if getattr(self, "shield_charges", 0) > 0:
            self.shield_charges -= 1
            if getattr(self, "profession", "") == "mage" and self.orb_angles:
                self.orb_angles.pop()
            return
        if getattr(self, "shield_hp", 0) > 0:
            self.shield_hp -= 1
            return
        self.hurt_speed_timer = HURT_SPEED_DURATION
        self.hurt_slow_timer = HURT_SPEED_DURATION + HURT_SLOW_DURATION
        self.hp -= 1
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
        self.power_duration = 0
        self.spike_axis = None
        self.pending_bullet = False
        self.trail_emit_timer = 0.0


class Item:
    def __init__(self, x, y, radius=8):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 215, 0), (int(self.x), int(self.y)), self.radius)


class Wall:
    def __init__(self, x, y, w, h, duration=WALL_DURATION):
        self.rect = pygame.Rect(int(x), int(y), int(w), int(h))
        self.time_left = duration

    def update(self, dt):
        self.time_left -= dt

    def alive(self):
        return self.time_left > 0

    def draw(self, surface):
        overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        overlay.fill((180, 180, 200, 180))
        surface.blit(overlay, (self.rect.x, self.rect.y))
        pygame.draw.rect(surface, (220, 220, 240), self.rect, 2)


class Bullet:
    def __init__(self, x, y, vx, vy, owner, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.owner = owner
        self.color = color
        self.w = 14
        self.h = 6
        self.alive = True

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface):
        rect = pygame.Rect(int(self.x - self.w / 2), int(self.y - self.h / 2), self.w, self.h)
        pygame.draw.rect(surface, self.color, rect)


class FloatingText:
    def __init__(self, text, x, y, duration=1.2, color=(255, 215, 0)):
        self.text = text
        self.x = x
        self.y = y
        self.duration = duration
        self.time_left = duration
        self.color = color

    def update(self, dt):
        self.time_left -= dt
        self.y -= 20 * dt  # 轻微上飘

    def alpha(self):
        return max(0, min(1, self.time_left / self.duration))


class Debris:
    def __init__(self, x, y, vx, vy, size, color, life):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.color = color
        self.life = life
        self.time_left = life

    def update(self, dt):
        self.time_left -= dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def alpha(self):
        return max(0, min(1, self.time_left / self.life))

    def draw(self, surface):
        alpha = int(255 * self.alpha())
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (self.size, self.size), self.size)
        surface.blit(surf, (self.x - self.size, self.y - self.size))


class TriangleToken:
    def __init__(self, x, y, target, radius=8):
        self.x = x
        self.y = y
        self.target = target
        self.radius = radius
        self.alive = True

    def update(self, dt):
        pass

    def draw(self, surface):
        r = self.radius
        p1 = (int(self.x), int(self.y - r))
        p2 = (int(self.x - r), int(self.y + r))
        p3 = (int(self.x + r), int(self.y + r))
        pygame.draw.polygon(surface, (255, 105, 180), [p1, p2, p3])


class TrailSegment:
    def __init__(self, x, y, size, owner, duration=TRAIL_SEG_LIFE):
        self.x = x
        self.y = y
        self.size = size
        self.owner = owner
        self.duration = duration
        self.time_left = duration
        self.hit_ids = set()

    def update(self, dt):
        self.time_left -= dt

    def alive(self):
        return self.time_left > 0

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.size), int(self.size))

    def draw(self, surface):
        alpha = int(180 * max(0, min(1, self.time_left / self.duration)))
        color = (*self.owner.color, alpha)
        overlay = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        overlay.fill(color)
        pygame.draw.rect(overlay, (255, 200, 80, alpha), overlay.get_rect(), 2)
        surface.blit(overlay, (self.x, self.y))


class SweepRect:
    def __init__(self, x, y, w, h, vx, owner, area_rect):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vx = vx
        self.owner = owner
        self.area_rect = area_rect
        self.alive = True
        self.hit_ids = set()

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.w), int(self.h))


class ExpandingCircle:
    def __init__(self, owner, cx, cy, max_radius, expand_duration=AOE_DURATION, linger=0.0):
        self.owner = owner
        self.cx = cx
        self.cy = cy
        self.max_radius = max_radius
        self.radius = 0
        self.expand_duration = expand_duration
        self.linger_duration = linger
        self.total_time = expand_duration + linger
        self.time_left = self.total_time
        self.hit_ids = set()
        self.alive = True

    def update(self, dt):
        self.time_left -= dt
        elapsed = self.total_time - max(self.time_left, 0)
        if elapsed < self.expand_duration:
            progress = min(1, elapsed / self.expand_duration)
            self.radius = self.max_radius * progress
        else:
            self.radius = self.max_radius
        if self.time_left <= 0:
            self.alive = False


class RippleWave:
    def __init__(self, owner, cx, cy, base_radius):
        self.owner = owner
        self.cx = cx
        self.cy = cy
        self.base_radius = base_radius
        self.max_radius = base_radius * RIPPLE_SCALE
        self.radius = base_radius
        self.duration = RIPPLE_DURATION
        self.time_left = RIPPLE_DURATION
        self.hit_ids = set()
        self.alive = True

    def update(self, dt):
        self.time_left -= dt
        progress = 1 - max(self.time_left, 0) / self.duration
        self.radius = self.base_radius + (self.max_radius - self.base_radius) * min(1, progress)
        if self.time_left <= 0:
            self.alive = False


class FreezeRipple:
    """仅用于定身波纹，不造成伤害。"""

    def __init__(self, owner, cx, cy, base_radius):
        self.owner = owner
        self.cx = cx
        self.cy = cy
        self.base_radius = base_radius
        self.max_radius = base_radius * RIPPLE_SCALE
        self.radius = base_radius
        self.duration = RIPPLE_DURATION
        self.time_left = RIPPLE_DURATION
        self.hit_ids = set()
        self.alive = True

    def update(self, dt):
        self.time_left -= dt
        progress = 1 - max(self.time_left, 0) / self.duration
        self.radius = self.base_radius + (self.max_radius - self.base_radius) * min(1, progress)
        if self.time_left <= 0:
            self.alive = False


# ------------------ 游戏主类 ------------------ #
class Game:
    def __init__(self, scenes):
        pygame.init()
        pygame.display.set_caption("Just Ball Game")
        self.font = self._load_font(28)

        self.scenes = scenes
        self.scene_index = 0
        self.map_index = 0
        self.entity_count = 0

        self.state = "MENU"  # MENU / MAP_SELECT / COUNT_SELECT / PLAYING / TIME_UP

        first = self.scenes[0]
        first_map = MAPS[0]
        self.play_width = first_map["width"]
        self.play_height = first_map["height"]
        self.window_width = self.play_width + COUNTER_WIDTH
        self.window_height = self.play_height
        self.border_margin = first_map.get("border_margin", 40)
        self.arena_shape = first_map.get("shape", "rect")

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        self.blocks = []
        self.balls = []
        self.items = []
        self.item_timer = 0.0
        self.next_item_interval = random.uniform(ITEM_INTERVAL_MIN, ITEM_INTERVAL_MAX)
        self.bullets = []
        self.flash_timer = 0.0
        self.aura_contacts = set()
        self.floating_texts = []
        self.debris = []
        self.trails = []
        self.lightning_beams = []
        self.temp_speed_factors = {}
        self.effect_scroll = 0
        self.prof_scroll = 0
        self.ripples = []
        self.freeze_ripples = []
        self.freeze_emitters = []
        self.triangle_effect = None
        self.triangle_tokens = []
        self.curse_marks = []
        self.curse_marks = []
        self.winner_ent = None
        self.winner_ent = None
        self.triangle_effect = None
        self.triangle_tokens = []
        self.ripples = []
        self.sweepers = []
        self.pending_top_sweeps = []
        self.aoes = []
        self.walls = []
        self.hex_burst_tasks = []
        self.winner = None

        self.time_limit = 60
        self.time_left = self.time_limit

    def _load_font(self, size):
        # 依次尝试加载预设字体，确保中文可正常显示
        for name in PREFERRED_FONTS:
            matched = pygame.font.match_font(name)
            if matched:
                return pygame.font.Font(matched, size)
        # 找不到时退回默认字体
        return pygame.font.SysFont(None, size)

    # ------ 边界（方形或圆形）------ #
    def get_bounds(self):
        if self.arena_shape == "circle":
            cx = self.play_width / 2
            cy = (self.window_height - UI_HEIGHT) / 2
            radius = min(self.play_width, self.window_height - UI_HEIGHT) / 2 - self.border_margin
            rect = pygame.Rect(
                cx - radius,
                cy - radius,
                radius * 2,
                radius * 2,
            )
            return {"shape": "circle", "center": (cx, cy), "radius": radius, "rect": rect}
        else:
            left = self.border_margin
            top = self.border_margin
            right = self.play_width - self.border_margin
            bottom = self.window_height - self.border_margin - UI_HEIGHT
            rect = pygame.Rect(left, top, right - left, bottom - top)
            return {"shape": "rect", "rect": rect}

    # ------ 场景加载 ------ #
    def load_scene(self, index, total_entities=None):
        cfg = self.scenes[index]
        self.scene_index = index

        # 应用当前地图
        map_cfg = MAPS[self.map_index]
        self.play_width = map_cfg["width"]
        self.play_height = map_cfg["height"]
        self.window_width = self.play_width + COUNTER_WIDTH
        self.window_height = self.play_height
        self.border_margin = map_cfg.get("border_margin", 40)
        self.arena_shape = map_cfg.get("shape", "rect")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        self.blocks = []
        self.balls = []
        self.bullets = []
        self.items = []
        self.item_timer = 0.0
        self.next_item_interval = random.uniform(ITEM_INTERVAL_MIN, ITEM_INTERVAL_MAX)
        self.flash_timer = 0.0
        self.aura_contacts = set()
        self.floating_texts = []
        self.debris = []
        self.trails = []
        self.lightning_beams = []
        self.temp_speed_factors = {}
        self.freeze_ripples = []
        self.freeze_emitters = []
        self.sweepers = []
        self.pending_top_sweeps = []
        self.aoes = []
        self.walls = []
        self.hex_burst_tasks = []
        self.winner = None

        seeds = []
        for b in cfg.get("blocks", []):
            seeds.append(("block", b))
        for c in cfg.get("balls", []):
            seeds.append(("ball", c))
        if not seeds:
            seeds = [("ball", {"pos": (self.play_width / 2, self.play_height / 2), "vel": (200, 150), "color": (200, 200, 200)})]
        total = total_entities or len(seeds)
        total = max(1, min(8, total))

        for i in range(total):
            kind, data = seeds[i % len(seeds)]
            palette_color = COLOR_PALETTE[i % len(COLOR_PALETTE)]
            if kind == "block":
                x, y = data["pos"]
                w = h = ENTITY_RADIUS * 2
                vx, vy = data.get("vel", (200, 150))
                vx *= SPEED_SCALE
                vy *= SPEED_SCALE
                color = palette_color
                jitter = random.uniform(-15, 15)
                block = Block(x + jitter, y + jitter, w, h, vx, vy, color)
                block.name = f"方块{i + 1}"
                self.assign_profession(block)
                self.blocks.append(block)
            else:
                x, y = data["pos"]
                radius = ENTITY_RADIUS
                vx, vy = data.get("vel", (180, -140))
                vx *= SPEED_SCALE
                vy *= SPEED_SCALE
                color = palette_color
                jitter = random.uniform(-15, 15)
                ball = Ball(x + jitter, y + jitter, radius, vx, vy, color)
                ball.name = f"小球{i + 1}"
                self.assign_profession(ball)
                self.balls.append(ball)

        self.time_limit = cfg.get("time_limit", 60)
        self.time_left = self.time_limit if self.time_limit is not None else None

        self.winner_ent = None
        self.state = "PLAYING"

    def assign_profession(self, ent):
        prof = random.choice(PROFESSIONS)
        ent.profession = prof
        ent.mass = TANK_MASS if prof == "tank" else 1.0
        ent.speed_base = TANK_SPEED_SCALE if prof == "tank" else 1.0
        ent.speed_bonus = 1.0
        ent.external_speed_scale = 1.0
        ent.max_hp = MAX_HP + (TANK_EXTRA_HP * 2 if prof == "tank" else 0)
        ent.hp = ent.max_hp
        ent.shield_hp = 0
        ent.hurt_speed_timer = 0.0
        ent.hurt_slow_timer = 0.0
        ent.shield_charges = 0
        ent.orb_angles = []
        ent.mage_cd = MAGE_ORB_INTERVAL
        ent.assassin_cd = ASSASSIN_COOLDOWN
        ent.assassin_active = 0.0
        ent.shock_cd = TANK_SHOCK_CD
        ent.time_cd = TIME_SLOW_CD
        ent.time_active = 0.0
        ent.gravity_cd = GRAVITY_CD
        ent.gravity_active = 0.0
        ent.gravity_mode = 1
        ent.lightning_cd = LIGHTNING_CD
        ent.trail_emit_timer = 0.0
        ent.hunter_turn = HUNTER_TURN_RATE
        ent.drone_gain_timer = DRONE_GAIN_INTERVAL
        ent.drones = []
        ent.drone_fire_cd = DRONE_CD
        if prof == "drone":
            ent.drones.append(self.create_drone_unit())

    def create_drone_unit(self):
        return {
            "phase": "orbit",
            "angle": random.uniform(0, 2 * math.pi),
            "pos": None,
            "dir": (0, 0),
            "hit_ids": set(),
        }
    # ------ 工具：返回当前所有实体 ------ #
    def all_entities(self):
        return [e for e in self.blocks + self.balls if e.alive]

    # ------ 判断实体间是否接触 ------ #
    def entities_overlap(self, a, b):
        if not a.alive or not b.alive:
            return False
        if isinstance(a, Ball) and isinstance(b, Ball):
            dx = a.x - b.x
            dy = a.y - b.y
            return dx * dx + dy * dy <= (a.radius + b.radius) ** 2
        if isinstance(a, Block) and isinstance(b, Block):
            dx = (a.x + a.w / 2) - (b.x + b.w / 2)
            dy = (a.y + a.h / 2) - (b.y + b.h / 2)
            return dx * dx + dy * dy <= (a.radius + b.radius) ** 2
        # 圆 - 圆（球与方块）
        ball = a if isinstance(a, Ball) else b
        block = b if isinstance(a, Ball) else a
        dx = ball.x - (block.x + block.w / 2)
        dy = ball.y - (block.y + block.h / 2)
        return dx * dx + dy * dy <= (ball.radius + block.radius) ** 2

    # ------ 道具生成 ------ #
    def spawn_item(self):
        if len(self.items) >= ITEM_MAX_COUNT:
            return False
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
        self.items.append(Item(x, y))
        return True

    # ------ 道具拾取与效果分配 ------ #
    def handle_item_pickups(self):
        if not self.items:
            return
        remaining = []
        picked_any = False
        for item in self.items:
            picked = False
            for ent in self.all_entities():
                if isinstance(ent, Ball):
                    dx = ent.x - item.x
                    dy = ent.y - item.y
                    reach = ent.radius + item.radius
                else:
                    cx = ent.x + ent.w / 2
                    cy = ent.y + ent.h / 2
                    dx = cx - item.x
                    dy = cy - item.y
                    reach = max(ent.w, ent.h) / 2 + item.radius
                if dx * dx + dy * dy <= reach * reach:
                    self.apply_power_up(ent)
                    picked = True
                    picked_any = True
                    break
            if not picked:
                remaining.append(item)
        self.items = remaining
        if picked_any:
            self.item_timer = 0.0

    def apply_power_up(self, ent):
        modes = ["aura", "bullet", "spike", "flash", "heal", "sweep", "aoe", "trail", "ripple", "shield", "wall", "hexshot", "freeze_ripple"]
        weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        mode = random.choices(modes, weights=weights, k=1)[0]
        label_map = {
            "aura": "锯齿护环",
            "bullet": "三连发子弹",
            "spike": "锯齿边",
            "flash": "诅咒成功",
            "heal": "回复+1",
            "sweep": "扫荡条",
            "aoe": "扩散震荡",
            "trail": "燃烧轨迹",
            "ripple": "碰撞波纹",
            "shield": "护盾",
            "wall": "阻挡墙",
            "hexshot": "六向双重弹",
            "freeze_ripple": "定身波纹",
        }
        if mode == "aura":
            ent.set_power("aura", BUFF_DURATION)
            self.add_floating_text(label_map[mode], ent)
        elif mode == "spike":
            axis = random.choice(["tb", "lr"])
            ent.set_power("spike", SPIKE_DURATION, axis)
            self.add_floating_text(label_map[mode], ent)
        elif mode == "flash":
            # 给其他实体计数-1，并在头顶出现渐隐X
            for victim in self.all_entities():
                if victim is ent:
                    continue
                victim.take_damage()
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
        # 找最近目标
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
        angles = (-0.25, 0, 0.25)  # 弧度偏移，形成三发弹体
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

        # 下半场：左 -> 右
        y_bottom = area.top + h_half
        sweeper1 = SweepRect(area.left - bar_w, y_bottom, bar_w, bar_h, SWEEP_SPEED, owner, area)
        self.sweepers.append(sweeper1)
        # 上半场延迟 2 秒再出现
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
        max_r = ENTITY_RADIUS * 4  # 范围*2（原来约2倍，现4倍）
        expand_time = AOE_DURATION * 1.5  # 加快扩散
        linger = AOE_DURATION * 0.5     # 消失时间*0.5
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
            # 球体
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
            # 方块
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

    # ------ 球与方块碰撞 ------ #
    # ------ 方块之间的碰撞 ------ #
    def handle_block_collisions(self):
        n = len(self.blocks)
        for i in range(n):
            for j in range(i + 1, n):
                a = self.blocks[i]
                b = self.blocks[j]
                if not a.alive or not b.alive:
                    continue

                acx = a.x + a.w / 2
                acy = a.y + a.h / 2
                bcx = b.x + b.w / 2
                bcy = b.y + b.h / 2

                dx = bcx - acx
                dy = bcy - acy
                dist_sq = dx * dx + dy * dy
                min_dist = a.radius + b.radius

                if dist_sq == 0:
                    dx, dy = 0.01, 0.01
                    dist_sq = dx * dx + dy * dy

                if dist_sq < min_dist * min_dist:
                    dist = math.sqrt(dist_sq)
                    nx = dx / dist
                    ny = dy / dist
                    overlap = (min_dist - dist)
                    total_mass = a.mass + b.mass
                    if total_mass == 0:
                        total_mass = 1
                    a_shift = overlap * (b.mass / total_mass)
                    b_shift = overlap * (a.mass / total_mass)
                    a.x -= nx * a_shift
                    a.y -= ny * a_shift
                    b.x += nx * b_shift
                    b.y += ny * b_shift

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
                    if a.power == "ripple":
                        self.spawn_ripple(a)
                    if b.power == "ripple":
                        self.spawn_ripple(b)

    # ------ 球与方块碰撞 ------ #
    def handle_ball_block_collisions(self):
        for ball in self.balls:
            if not ball.alive:
                continue
            for block in self.blocks:
                if not block.alive:
                    continue
                bcx = block.x + block.w / 2
                bcy = block.y + block.h / 2
                dx = bcx - ball.x
                dy = bcy - ball.y
                dist_sq = dx * dx + dy * dy
                min_dist = ball.radius + block.radius
                if dist_sq == 0:
                    dx, dy = 0.01, 0.01
                    dist_sq = dx * dx + dy * dy
                if dist_sq < min_dist * min_dist:
                    dist = math.sqrt(dist_sq)
                    nx = dx / dist
                    ny = dy / dist
                    overlap = (min_dist - dist)
                    total_mass = ball.mass + block.mass
                    if total_mass == 0:
                        total_mass = 1
                    ball_shift = overlap * (block.mass / total_mass)
                    block_shift = overlap * (ball.mass / total_mass)
                    ball.x -= nx * ball_shift
                    ball.y -= ny * ball_shift
                    block.x += nx * block_shift
                    block.y += ny * block_shift

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
                    if ball.power == "ripple":
                        self.spawn_ripple(ball)
                    if block.power == "ripple":
                        self.spawn_ripple(block)

    # ------ 小球之间弹性碰撞（不掉血，只改变速度方向）------ #
    def handle_ball_collisions(self):
        n = len(self.balls)
        for i in range(n):
            for j in range(i + 1, n):
                b1 = self.balls[i]
                b2 = self.balls[j]
                if not b1.alive or not b2.alive:
                    continue

                dx = b2.x - b1.x
                dy = b2.y - b1.y
                dist_sq = dx * dx + dy * dy
                min_dist = b1.radius + b2.radius

                if dist_sq == 0:
                    # 避免零距离导致除零，稍微挪开一点
                    dx = 0.01
                    dy = 0.01
                    dist_sq = dx * dx + dy * dy

                if dist_sq < min_dist * min_dist:
                    dist = math.sqrt(dist_sq)
                    nx = dx / dist
                    ny = dy / dist

                    # 将两球沿法线方向分离，避免重叠
                    overlap = (min_dist - dist)
                    total_mass = b1.mass + b2.mass
                    if total_mass == 0:
                        total_mass = 1
                    b1_shift = overlap * (b2.mass / total_mass)
                    b2_shift = overlap * (b1.mass / total_mass)
                    b1.x -= nx * b1_shift
                    b1.y -= ny * b1_shift
                    b2.x += nx * b2_shift
                    b2.y += ny * b2_shift

                    vn1 = b1.vx * nx + b1.vy * ny
                    vn2 = b2.vx * nx + b2.vy * ny
                    vt1 = -b1.vx * ny + b1.vy * nx
                    vt2 = -b2.vx * ny + b2.vy * nx

                    new_vn1 = (vn1 * (b1.mass - b2.mass) + 2 * b2.mass * vn2) / total_mass
                    new_vn2 = (vn2 * (b2.mass - b1.mass) + 2 * b1.mass * vn1) / total_mass

                    b1.vx = new_vn1 * nx - vt1 * ny
                    b1.vy = new_vn1 * ny + vt1 * nx
                    b2.vx = new_vn2 * nx - vt2 *ny
                    b2.vy = new_vn2 *ny + vt2 *nx
                    if b1.power == "ripple":
                        self.spawn_ripple(b1)
                    if b2.power == "ripple":
                        self.spawn_ripple(b2)

    def get_entity_center(self, ent):
        if isinstance(ent, Ball):
            return ent.x, ent.y
        return ent.x + ent.w / 2, ent.y + ent.h / 2

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

    def update_trails(self, dt):
        # 生成轨迹
        for ent in self.all_entities():
            if ent.power == "trail":
                ent.trail_emit_timer -= dt
                if ent.trail_emit_timer <= 0:
                    size = ent.radius * 2
                    cx, cy = self.get_entity_center(ent)
                    seg = TrailSegment(cx - size / 2, cy - size / 2, size, ent)
                    self.trails.append(seg)
                    ent.trail_emit_timer = TRAIL_EMIT_INTERVAL

        # 更新轨迹并结算伤害
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
                    ent.take_damage()
                    seg.hit_ids.add(id(ent))

        self.trails = [t for t in self.trails if t.alive()]

    def draw_walls(self):
        for w in self.walls:
            w.draw(self.screen)

    def draw_trails(self):
        for t in self.trails:
            t.draw(self.screen)

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
                dx = cx - rp.cx
                dy = cy - rp.cy
                dist = math.hypot(dx, dy)
                if dist <= rp.radius + ent.radius:
                    ent.take_damage()
                    rp.hit_ids.add(id(ent))
            new_ripples.append(rp)
        self.ripples = [r for r in new_ripples if r.alive]

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
                dx = cx - rp.cx
                dy = cy - rp.cy
                dist = math.hypot(dx, dy)
                if dist <= rp.radius + ent.radius:
                    self.apply_freeze(ent)
                    rp.hit_ids.add(id(ent))
            updated.append(rp)
        self.freeze_ripples = [r for r in updated if r.alive]

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

    def start_triangle_effect(self, owner):
        targets = [e for e in self.all_entities() if e is not owner]
        if not targets:
            return False
        total_tokens = random.randint(3, 9)
        random.shuffle(targets)
        chosen = targets[: total_tokens] if len(targets) >= total_tokens else targets
        tri_targets = []
        tokens = []
        bounds = self.get_bounds()
        for tgt in chosen:
            cnt = random.randint(1, 3)
            tri_targets.append({"target": tgt, "count": cnt})
            for _ in range(cnt):
                tx, ty = self.get_entity_center(tgt)
                offset_x = random.uniform(-tgt.radius, tgt.radius)
                offset_y = random.uniform(-tgt.radius, tgt.radius)
                tokens.append(TriangleToken(tx + offset_x, ty + offset_y, tgt))

        self.triangle_effect = {"timer": 2.0, "targets": tri_targets}
        self.triangle_tokens = tokens
        return True

    def update_triangles(self, dt):
        if not self.triangle_effect:
            return
        self.triangle_effect["timer"] -= dt

        # 拾取三角
        remaining_tokens = []
        for tk in self.triangle_tokens:
            if not tk.alive:
                continue
            tgt_entry = next((t for t in self.triangle_effect["targets"] if t["target"] is tk.target), None)
            if not tgt_entry or tgt_entry["count"] <= 0:
                continue
            cx, cy = self.get_entity_center(tk.target)
            dx = cx - tk.x
            dy = cy - tk.y
            dist = math.hypot(dx, dy)
            if dist <= tk.target.radius + tk.radius:
                tgt_entry["count"] -= 1
                tk.alive = False
            else:
                remaining_tokens.append(tk)
        self.triangle_tokens = remaining_tokens

        # 计时结束结算伤害
        if self.triangle_effect["timer"] <= 0:
            for entry in self.triangle_effect["targets"]:
                if entry["count"] > 0 and entry["target"].alive:
                    entry["target"].take_damage()
            self.triangle_effect = None
            self.triangle_tokens = []

    def draw_triangles(self):
        # 画漂浮的三角形
        for tk in self.triangle_tokens:
            tk.draw(self.screen)
        # 头顶计数
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
    def get_speed_factor(self, ent):
        factor = ent.speed_base * ent.speed_bonus * ent.external_speed_scale
        if getattr(ent, "hurt_speed_timer", 0) > 0:
            factor *= 2.0
        elif getattr(ent, "hurt_slow_timer", 0) > 0:
            factor *= HURT_SLOW_MULT
        return factor

    def do_tank_shockwave(self, tank):
        cx, cy = self.get_entity_center(tank)
        for ent in self.all_entities():
            if ent is tank or not ent.alive:
                continue
            tx, ty = self.get_entity_center(ent)
            dx = tx - cx
            dy = ty - cy
            dist = math.hypot(dx, dy)
            if dist <= TANK_SHOCK_RADIUS and dist > 0:
                nx = dx / dist
                ny = dy / dist
                ent.vx += nx * TANK_SHOCK_FORCE
                ent.vy += ny * TANK_SHOCK_FORCE

    def update_hunter(self, hunter, entities, dt):
        nearest = None
        nearest_dist = 1e9
        hx, hy = self.get_entity_center(hunter)
        for ent in entities:
            if ent is hunter or not ent.alive:
                continue
            tx, ty = self.get_entity_center(ent)
            d2 = (tx - hx) ** 2 + (ty - hy) ** 2
            if d2 < nearest_dist:
                nearest_dist = d2
                nearest = ent
        if not nearest:
            return
        tx, ty = self.get_entity_center(nearest)
        dir_x = tx - hx
        dir_y = ty - hy
        if dir_x == 0 and dir_y == 0:
            return
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
            ent.take_damage()
            dx = ex - cx
            dy = ey - cy
            dlen = math.hypot(dx, dy) or 1
            ent.vx += dx / dlen * LIGHTNING_PUSH
            ent.vy += dy / dlen * LIGHTNING_PUSH
            self.lightning_beams.append(
                {"start": (cx, cy), "end": (ex, ey), "time": LIGHTNING_LIFE}
            )

    def update_lightning_beams(self, dt):
        for b in self.lightning_beams:
            b["time"] -= dt
        self.lightning_beams = [b for b in self.lightning_beams if b["time"] > 0]

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
                        dx = tx - cx
                        dy = ty - cy
                        dist = math.hypot(dx, dy) + 1e-5
                        if dist <= ent.radius * GRAVITY_RADIUS_SCALE:
                            nx = dx / dist
                            ny = dy / dist
                            target.vx += nx * GRAVITY_FORCE * ent.gravity_mode * dt
                            target.vy += ny * GRAVITY_FORCE * ent.gravity_mode * dt
                elif ent.gravity_cd <= 0:
                    ent.gravity_active = GRAVITY_DURATION
                    ent.gravity_cd = GRAVITY_CD
                    ent.gravity_mode = random.choice([-1, 1])
            elif p == "hunter":
                self.update_hunter(ent, entities, dt)
            elif p == "lightning":
                ent.lightning_cd -= dt
                if ent.lightning_cd <= 0:
                    self.fire_lightning(ent, entities)
                    ent.lightning_cd = LIGHTNING_CD
                    if random.random() < 0.1 and ent.alive:
                        ent.take_damage()
            elif p == "drone":
                if not hasattr(ent, "drones"):
                    ent.drones = []
                if not hasattr(ent, "drone_gain_timer"):
                    ent.drone_gain_timer = DRONE_GAIN_INTERVAL
                if not hasattr(ent, "drone_fire_cd"):
                    ent.drone_fire_cd = DRONE_CD
                if not ent.drones:
                    ent.drones.append(self.create_drone_unit())

                ent.drone_gain_timer -= dt
                if ent.drone_gain_timer <= 0:
                    if len(ent.drones) < DRONE_MAX_COUNT:
                        ent.drones.append(self.create_drone_unit())
                    ent.drone_gain_timer = DRONE_GAIN_INTERVAL

                ent.drone_fire_cd -= dt
                fire_now = ent.drone_fire_cd <= 0
                if fire_now:
                    ent.drone_fire_cd = DRONE_CD

                cx, cy = self.get_entity_center(ent)
                for idx, drone in enumerate(ent.drones):
                    if drone["phase"] is None:
                        drone["phase"] = "orbit"
                    if drone["phase"] == "orbit":
                        drone["angle"] = (drone["angle"] + dt * 1.1 + idx * 0.15) % (2 * math.pi)
                        offset = ent.radius + 14 + idx * 6
                        px = cx + math.cos(drone["angle"]) * offset
                        py = cy + math.sin(drone["angle"]) * offset
                        drone["pos"] = (px, py)
                        if fire_now:
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
                                target.take_damage()
                                drone["hit_ids"].add(id(target))
                        bounds = self.get_bounds()
                        out = False
                        if bounds["shape"] == "rect":
                            rect = bounds["rect"]
                            if px < rect.left - 10 or px > rect.right + 10 or py < rect.top - 10 or py > rect.bottom + 10:
                                out = True
                        else:
                            bx, by = bounds["center"]
                            r = bounds["radius"]
                            if (px - bx) ** 2 + (py - by) ** 2 > (r + 10) ** 2:
                                out = True
                        if out:
                            drone["phase"] = "return"
                    elif drone["phase"] == "return":
                        px, py = drone["pos"]
                        dx = cx - px
                        dy = cy - py
                        dist = math.hypot(dx, dy)
                        if dist < 6:
                            drone["phase"] = "orbit"
                        else:
                            nx = dx / dist
                            ny = dy / dist
                            px += nx * DRONE_SPEED * dt
                            py += ny * DRONE_SPEED * dt
                            drone["pos"] = (px, py)
                    ent.drones[idx] = drone

    # ------ 光环伤害：触碰即伤害 ------ #
    def apply_aura_damage(self):
        entities = self.all_entities()
        new_contacts = set()
        for attacker in entities:
            if attacker.power != "aura":
                continue
            for victim in entities:
                if victim is attacker or not victim.alive:
                    continue
                pair = (id(attacker), id(victim))
                if self.entities_overlap(attacker, victim):
                    if pair not in self.aura_contacts:
                        victim.take_damage()
                    new_contacts.add(pair)
        # 只在结束重叠后才允许再次伤害
        self.aura_contacts = new_contacts

    def entity_bbox(self, e):
        if isinstance(e, Ball):
            return e.x - e.radius, e.y - e.radius, e.radius * 2, e.radius * 2
        cx = e.x + e.w / 2
        cy = e.y + e.h / 2
        r = e.radius
        return cx - r, cy - r, r * 2, r * 2

    def rect_overlap(self, a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        # 允许边缘接触也算“撞到”
        return ax <= bx + bw and ax + aw >= bx and ay <= by + bh and ay + ah >= by

    def spike_hits(self, attacker, victim):
        if attacker.power != "spike":
            return False
        ax, ay, aw, ah = self.entity_bbox(attacker)
        vx, vy, vw, vh = self.entity_bbox(victim)
        axis = attacker.spike_axis or "tb"
        if axis == "tb":
            bands = [
                (ax, ay - SPIKE_BAND, aw, SPIKE_BAND * 2),
                (ax, ay + ah - SPIKE_BAND, aw, SPIKE_BAND * 2),
            ]
        else:
            bands = [
                (ax - SPIKE_BAND, ay, SPIKE_BAND * 2, ah),
                (ax + aw - SPIKE_BAND, ay, SPIKE_BAND * 2, ah),
            ]
        return any(self.rect_overlap(band, (vx, vy, vw, vh)) for band in bands)

    # ------ 锯齿边伤害 ------ #
    def apply_spike_damage(self):
        entities = self.all_entities()
        for attacker in entities:
            if attacker.power != "spike":
                continue
            for victim in entities:
                if victim is attacker or not victim.alive:
                    continue
                if self.spike_hits(attacker, victim):
                    victim.take_damage()

    # ------ 更新增益计时 ------ #
    def update_powers(self, dt):
        for ent in self.blocks + self.balls:
            if ent.power == "aura":
                ent.power_timer -= dt
                if ent.power_timer <= 0:
                    ent.clear_power()
            elif ent.power == "spike":
                ent.power_timer -= dt
                if ent.power_timer <= 0:
                    ent.clear_power()
            elif ent.power == "trail":
                ent.power_timer -= dt
                if ent.power_timer <= 0:
                    ent.clear_power()
            elif ent.power == "ripple":
                ent.power_timer -= dt
                if ent.power_timer <= 0:
                    ent.clear_power()
            elif ent.power == "bullet":
                # 若场上已无属于它的子弹则结束效果
                has_bullet = any(b.owner is ent for b in self.bullets)
                if not has_bullet:
                    ent.clear_power()

        if self.flash_timer > 0:
            self.flash_timer -= dt
            if self.flash_timer < 0:
                self.flash_timer = 0
        if self.curse_marks:
            for mk in self.curse_marks:
                mk["time"] -= dt
            self.curse_marks = [m for m in self.curse_marks if m["time"] > 0]

    def update_hex_burst_tasks(self, dt):
        if not self.hex_burst_tasks:
            return
        pending = []
        for task in self.hex_burst_tasks:
            owner = task["owner"]
            if not owner or not owner.alive:
                continue
            task["delay"] -= dt
            if task["delay"] <= 0:
                self.fire_hex_shot(owner)
            else:
                pending.append(task)
        self.hex_burst_tasks = pending

    # ------ 更新子弹 ------ #
    def update_bullets(self, dt):
        bounds = pygame.Rect(0, 0, self.window_width, self.window_height)
        for b in self.bullets:
            if not b.alive:
                continue
            b.update(dt)
            if not bounds.collidepoint(b.x, b.y):
                b.alive = False
                if b.owner and b.owner.power == "bullet":
                    b.owner.clear_power()
                continue

            for target in self.all_entities():
                if target is b.owner:
                    continue
                bullet_rect = pygame.Rect(int(b.x - b.w / 2), int(b.y - b.h / 2), b.w, b.h)

                cx = target.x if isinstance(target, Ball) else target.x + target.w / 2
                cy = target.y if isinstance(target, Ball) else target.y + target.h / 2
                r = target.radius
                closest_x = max(bullet_rect.left, min(cx, bullet_rect.right))
                closest_y = max(bullet_rect.top, min(cy, bullet_rect.bottom))
                dx = cx - closest_x
                dy = cy - closest_y
                if dx * dx + dy * dy <= r * r:
                    target.take_damage()
                    b.alive = False

                if not b.alive:
                    if b.owner and b.owner.power == "bullet":
                        b.owner.clear_power()
                    break

        self.bullets = [b for b in self.bullets if b.alive]

    # ------ 事件处理 ------ #
    def handle_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            total_options = len(self.scenes) + 1  # 额外一个“职业”入口
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.scene_index = (self.scene_index + 1) % total_options
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.scene_index = (self.scene_index - 1) % total_options
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.scene_index == len(self.scenes):
                    self.state = "PROF_MENU"
                else:
                    self.state = "MAP_SELECT"
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEWHEEL:
            self.effect_scroll = max(0, self.effect_scroll - event.y * 30)

    def handle_map_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.map_index = (self.map_index + 1) % len(MAPS)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.map_index = (self.map_index - 1) % len(MAPS)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                # 进入数量选择
                base_total = len(self.scenes[self.scene_index].get("blocks", [])) + len(self.scenes[self.scene_index].get("balls", []))
                if base_total <= 0:
                    base_total = 2
                self.entity_count = max(1, min(8, base_total))
                self.state = "COUNT_SELECT"
            elif event.key == pygame.K_ESCAPE:
                self.state = "MENU"
        elif event.type == pygame.MOUSEWHEEL:
            self.effect_scroll = max(0, self.effect_scroll - event.y * 30)

    def handle_prof_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = "MENU"
        elif event.type == pygame.MOUSEWHEEL:
            self.prof_scroll = max(0, self.prof_scroll - event.y * 30)

    def handle_count_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.entity_count = min(8, self.entity_count + 1)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.entity_count = max(1, self.entity_count - 1)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.load_scene(self.scene_index, self.entity_count)
            elif event.key == pygame.K_ESCAPE:
                self.state = "MAP_SELECT"

    def handle_play_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = "MENU"
            elif event.key == pygame.K_r:
                # 重新开始当前场景
                self.load_scene(self.scene_index)

    def handle_timeup_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.load_scene(self.scene_index)
            elif event.key == pygame.K_ESCAPE:
                self.state = "MENU"

    # ------ 更新逻辑（PLAYING 状态）------ #
    def update_playing(self, dt):
        bounds = self.get_bounds()

        # 职业状态刷新
        self.update_professions(dt)

        # 道具计时与生成
        self.item_timer += dt
        while (
            len(self.items) < ITEM_MAX_COUNT
            and self.item_timer >= self.next_item_interval
        ):
            spawned = self.spawn_item()
            self.item_timer -= self.next_item_interval
            self.next_item_interval = random.uniform(ITEM_INTERVAL_MIN, ITEM_INTERVAL_MAX)
            if not spawned:
                self.item_timer = 0.0
                break

        # 自动移动 + 碰撞边界
        for b in self.blocks:
            if b.hurt_speed_timer > 0:
                b.hurt_speed_timer = max(0, b.hurt_speed_timer - dt)
            if b.hurt_slow_timer > 0:
                b.hurt_slow_timer = max(0, b.hurt_slow_timer - dt)
            was_frozen = b.freeze_timer > 0
            b.freeze_timer = max(0, b.freeze_timer - dt)
            if b.freeze_timer > 0:
                b.vx = 0
                b.vy = 0
                continue
            elif was_frozen:
                b.vx, b.vy = b.frozen_velocity
            hit_wall = b.update(dt * self.get_speed_factor(b), bounds)
            if b.power == "ripple" and hit_wall:
                self.spawn_ripple(b)
        for ball in self.balls:
            if ball.hurt_speed_timer > 0:
                ball.hurt_speed_timer = max(0, ball.hurt_speed_timer - dt)
            if ball.hurt_slow_timer > 0:
                ball.hurt_slow_timer = max(0, ball.hurt_slow_timer - dt)
            was_frozen = ball.freeze_timer > 0
            ball.freeze_timer = max(0, ball.freeze_timer - dt)
            if ball.freeze_timer > 0:
                ball.vx = 0
                ball.vy = 0
                continue
            elif was_frozen:
                ball.vx, ball.vy = ball.frozen_velocity
            hit_wall = ball.update(dt * self.get_speed_factor(ball), bounds)
            if ball.power == "ripple" and hit_wall:
                self.spawn_ripple(ball)

        # 碰撞墙体
        self.handle_wall_collisions()

        # 各实体碰撞
        self.handle_block_collisions()
        self.handle_ball_block_collisions()
        self.handle_ball_collisions()

        # 道具拾取
        self.handle_item_pickups()

        # 伤害判定
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
        self.update_triangles(dt)
        self.handle_deaths()
        self.update_debris(dt)
        self.update_lightning_beams(dt)
        self.update_walls(dt)

        # 清除已死亡实体
        self.blocks = [b for b in self.blocks if b.alive]
        self.balls = [c for c in self.balls if c.alive]

        if self.state == "PLAYING":
            survivors = self.all_entities()
            if len(survivors) == 1:
                last = survivors[0]
                self.winner_ent = last
                self.winner = "胜利！"
                self.state = "TIME_UP"

        # 倒计时
        if self.time_limit is not None:
            self.time_left -= dt
            if self.time_left <= 0:
                self.time_left = 0
                self.state = "TIME_UP"

    # ------ 绘制 ------ #
    def draw_menu(self):
        self.screen.fill((16, 16, 24))

        # 简单的背景光晕，避免纯色背景过于单调
        glow = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pygame.draw.circle(glow, (70, 120, 200, 45), (int(self.window_width * 0.75), 140), 220)
        pygame.draw.circle(glow, (200, 140, 90, 38), (int(self.window_width * 0.35), int(self.window_height * 0.75)), 260)
        self.screen.blit(glow, (0, 0))

        # 顶部标题条
        header_rect = pygame.Rect(36, 30, self.window_width - COUNTER_WIDTH - 120, 60)
        pygame.draw.rect(self.screen, (24, 26, 40), header_rect, border_radius=12)
        pygame.draw.rect(self.screen, (80, 90, 140), header_rect, 1, border_radius=12)
        title = self.font.render("选择模式 / 查看职业", True, (235, 235, 245))
        subtitle = self.font.render("↑↓ 切换  |  回车确认  |  ESC 退出", True, (170, 170, 190))
        self.screen.blit(title, (header_rect.x + 16, header_rect.y + 6))
        self.screen.blit(subtitle, (header_rect.x + 16, header_rect.y + 30))

        # 左侧卡片式列表
        card_w = min(420, self.window_width - COUNTER_WIDTH - 200)
        card_h = self.window_height - UI_HEIGHT - 200
        card_rect = pygame.Rect(60, 120, card_w, max(240, card_h))
        pygame.draw.rect(self.screen, (24, 28, 44), card_rect, border_radius=14)
        pygame.draw.rect(self.screen, (80, 110, 160), card_rect, 1, border_radius=14)

        list_y = card_rect.y + 28
        line_h = 38
        for i, sc in enumerate(self.scenes):
            is_sel = i == self.scene_index
            row_y = list_y + i * line_h
            row_rect = pygame.Rect(card_rect.x + 14, row_y - 8, card_rect.width - 28, line_h + 10)
            if is_sel:
                pygame.draw.rect(self.screen, (46, 70, 120), row_rect, border_radius=10)
                pygame.draw.rect(self.screen, (120, 170, 255), row_rect, 1, border_radius=10)
            text = f"{i + 1}. {sc['name']}"
            color = (255, 240, 140) if is_sel else (205, 210, 230)
            surf = self.font.render(text, True, color)
            self.screen.blit(surf, (row_rect.x + 12, row_rect.y + 6))

        # 职业入口放在列表底部
        prof_idx = len(self.scenes)
        prof_y = list_y + prof_idx * line_h
        row_rect = pygame.Rect(card_rect.x + 14, prof_y - 8, card_rect.width - 28, line_h + 10)
        is_sel = self.scene_index == prof_idx
        if is_sel:
            pygame.draw.rect(self.screen, (46, 70, 120), row_rect, border_radius=10)
            pygame.draw.rect(self.screen, (120, 170, 255), row_rect, 1, border_radius=10)
        prof_surf = self.font.render(f"{prof_idx + 1}. 职业介绍", True, (255, 240, 140) if is_sel else (205, 210, 230))
        self.screen.blit(prof_surf, (row_rect.x + 12, row_rect.y + 6))

        # 左下角提示条
        hint_rect = pygame.Rect(card_rect.x, card_rect.bottom + 20, card_rect.width, 48)
        pygame.draw.rect(self.screen, (22, 25, 38), hint_rect, border_radius=10)
        pygame.draw.rect(self.screen, (70, 80, 120), hint_rect, 1, border_radius=10)
        hint = self.font.render("回车进入地图选择 / 职业介绍   ·   ESC 退出", True, (180, 180, 195))
        self.screen.blit(hint, (hint_rect.x + 14, hint_rect.y + 12))

        # 中右侧插画 + 右侧效果列表
        self.draw_menu_hero_art()
        self.draw_effect_panel(pygame.mouse.get_pos())

    def draw_map_menu(self):
        self.screen.fill((15, 15, 25))
        title = self.font.render("选择地图（上下键），回车开始，ESC 返回模式", True, (230, 230, 230))
        self.screen.blit(title, (40, 40))

        for i, mp in enumerate(MAPS):
            color = (255, 255, 0) if i == self.map_index else (200, 200, 200)
            desc = f"{mp['name']} - {mp['shape']}"
            surf = self.font.render(desc, True, color)
            self.screen.blit(surf, (60, 100 + i * 30))
        self.draw_effect_panel(pygame.mouse.get_pos())

    def draw_prof_menu(self):
        self.screen.fill((12, 12, 24))
        title = self.font.render("职业介绍（ESC 返回）", True, (230, 230, 230))
        self.screen.blit(title, (40, 40))

        start_y = 90
        line_h = 26
        max_width = self.window_width - 120
        y = start_y - self.prof_scroll
        total_height = 0
        for name, desc in PROFS_INFO:
            name_surf = self.font.render(name, True, (255, 215, 0))
            self.screen.blit(name_surf, (60, y))
            y += line_h
            height_block = line_h
            for dline in self.wrap_text(desc, max_width):
                ds = self.font.render(dline, True, (200, 200, 220))
                self.screen.blit(ds, (80, y))
                y += line_h
                height_block += line_h
            y += 12
            height_block += 12
            total_height += height_block

        visible_h = self.window_height - 80
        if total_height > visible_h:
            bar_h = max(20, visible_h * visible_h / total_height)
            max_scroll = total_height - visible_h
            self.prof_scroll = min(self.prof_scroll, max_scroll)
            scroll_ratio = self.prof_scroll / max_scroll if max_scroll > 0 else 0
            bar_y = 60 + scroll_ratio * (visible_h - bar_h)
            bar_rect = pygame.Rect(self.window_width - 30, bar_y, 8, bar_h)
            pygame.draw.rect(self.screen, (80, 80, 140), bar_rect)

    def draw_count_menu(self):
        self.screen.fill((15, 15, 25))
        title = self.font.render("选择参战实体数量（1~8）", True, (230, 230, 230))
        self.screen.blit(title, (40, 40))
        info = self.font.render("上下键调整，回车确认，ESC 返回地图", True, (180, 180, 180))
        self.screen.blit(info, (40, 80))

        value_text = self.font.render(f"数量: {self.entity_count}", True, (255, 215, 0))
        self.screen.blit(value_text, (60, 140))

    def wrap_text(self, text, max_width):
        lines = []
        cur = ""
        for ch in text:
            if self.font.size(cur + ch)[0] <= max_width:
                cur += ch
            else:
                if cur:
                    lines.append(cur)
                cur = ch
        if cur:
            lines.append(cur)
        return lines

    def draw_menu_ball(self, pos, radius, base_color):
        cx, cy = pos
        shadow_w = radius * 2
        shadow_h = max(6, int(radius * 0.75))
        shadow = pygame.Surface((shadow_w, shadow_h), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 90), shadow.get_rect())
        self.screen.blit(shadow, (cx - shadow_w // 2, cy + radius - shadow_h // 2 + 6))

        size = radius * 2 + 8
        orb = pygame.Surface((size, size), pygame.SRCALPHA)
        mid = (size // 2, size // 2)
        for r in range(radius, 0, -1):
            shade = scale_color(base_color, 0.55 + 0.45 * (r / radius))
            pygame.draw.circle(orb, (*shade, 255), mid, r)
        rim = scale_color(base_color, 1.15)
        pygame.draw.circle(orb, (*rim, 220), mid, radius, 2)
        hx = int(mid[0] - radius * 0.35)
        hy = int(mid[1] - radius * 0.45)
        pygame.draw.circle(orb, (255, 255, 255, 140), (hx, hy), max(4, radius // 3))
        pygame.draw.circle(orb, (255, 255, 255, 90), (hx + radius // 5, hy + radius // 5), max(2, radius // 4))
        self.screen.blit(orb, (cx - mid[0], cy - mid[1]))

    def draw_menu_crown(self, center, base_radius):
        cx, cy = center
        crown_w = int(base_radius * 1.7)
        base_h = int(max(6, base_radius * 0.22))
        crown_h = int(base_radius * 0.9)
        surf_w = crown_w + 8
        surf_h = crown_h + base_h + 8
        surf = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
        base_rect = pygame.Rect(0, 0, crown_w, base_h)
        base_rect.midbottom = (surf_w // 2, surf_h - 2)
        top_y = base_rect.top - crown_h
        raw_points = [
            (base_rect.left, base_rect.top),
            (base_rect.left + crown_w * 0.18, top_y + crown_h * 0.3),
            (base_rect.left + crown_w * 0.34, base_rect.top),
            (base_rect.centerx, top_y),
            (base_rect.right - crown_w * 0.34, base_rect.top),
            (base_rect.right - crown_w * 0.18, top_y + crown_h * 0.3),
            (base_rect.right, base_rect.top),
        ]
        points = [(int(x), int(y)) for x, y in raw_points]
        gold = (255, 210, 120)
        edge = (180, 140, 60)
        pygame.draw.polygon(surf, gold, points)
        pygame.draw.rect(surf, gold, base_rect)
        pygame.draw.polygon(surf, edge, points, 2)
        pygame.draw.rect(surf, edge, base_rect, 2)
        jewel_y = top_y + crown_h * 0.55
        for jx in (points[1][0], base_rect.centerx, points[5][0]):
            pygame.draw.circle(surf, (120, 180, 255), (int(jx), int(jewel_y)), 4)
        shine_rect = pygame.Rect(0, 0, int(crown_w * 0.7), max(4, int(base_h * 1.5)))
        shine_rect.center = (base_rect.centerx, base_rect.top + base_h)
        pygame.draw.ellipse(surf, (255, 255, 255, 70), shine_rect)
        dest = surf.get_rect(midbottom=(cx, cy - base_radius + 8))
        self.screen.blit(surf, dest)

    def draw_menu_hero_art(self):
        available_right = self.window_width - COUNTER_WIDTH - 40
        center_x = min(available_right, self.window_width // 2 + 40)
        center_x = max(center_x, 260)
        center_y = self.window_height // 2
        big_r = 62

        ground = pygame.Surface((big_r * 3, big_r), pygame.SRCALPHA)
        pygame.draw.ellipse(ground, (0, 0, 0, 70), ground.get_rect())
        self.screen.blit(
            ground,
            (center_x - ground.get_width() // 2, center_y + big_r - ground.get_height() // 2 + 12),
        )

        halo = pygame.Surface((big_r * 4, big_r * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(halo, (80, 140, 255, 28), halo.get_rect())
        halo_rect = halo.get_rect(center=(center_x, int(center_y + big_r * 0.6)))
        self.screen.blit(halo, halo_rect)

        satellites = [
            {"offset": (-90, -12), "radius": 22, "color": (120, 205, 255)},
            {"offset": (-44, 58), "radius": 18, "color": (150, 245, 190)},
            {"offset": (64, 48), "radius": 22, "color": (255, 165, 150)},
            {"offset": (98, -6), "radius": 17, "color": (200, 180, 255)},
            {"offset": (-8, -72), "radius": 15, "color": (255, 230, 150)},
        ]
        for sat in satellites:
            pos = (int(center_x + sat["offset"][0]), int(center_y + sat["offset"][1]))
            self.draw_menu_ball(pos, sat["radius"], sat["color"])

        self.draw_menu_ball((center_x, center_y), big_r, (250, 205, 120))
        self.draw_menu_crown((center_x, center_y), big_r)

        sparkle = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(sparkle, (255, 255, 255, 160), (6, 6), 5)
        for dx, dy in ((-70, -90), (92, -60), (10, 88)):
            rect = sparkle.get_rect(center=(center_x + dx, center_y + dy))
            self.screen.blit(sparkle, rect)

    def draw_effect_panel(self, mouse_pos):
        panel_x = self.window_width - COUNTER_WIDTH + 10
        panel_y = 40
        panel_w = COUNTER_WIDTH - 20
        panel_h = min(320, self.window_height - UI_HEIGHT - panel_y - 20)
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(self.screen, (30, 30, 50), panel_rect)
        pygame.draw.rect(self.screen, (120, 120, 150), panel_rect, 1)

        y_offset = self.effect_scroll
        hover_desc = None
        y = panel_y + 10 - y_offset
        total_height = 0
        for eff in EFFECTS:
            name_lines = self.wrap_text(eff["name"], panel_w - 20)
            line_height = 22
            block_height = line_height * len(name_lines)
            line_y = y
            hovered = False
            # 计算整个名称块区域用于 hover
            max_w = max(self.font.size(line)[0] for line in name_lines)
            name_rect = pygame.Rect(panel_x + 10, y, max_w, block_height)

            if name_rect.collidepoint(mouse_pos):
                hovered = True
                hover_desc = eff["desc"]

            for line in name_lines:
                color = (255, 255, 0) if hovered else (200, 200, 200)
                surf = self.font.render(line, True, color)
                self.screen.blit(surf, (panel_x + 10, line_y))
                line_y += line_height

            y += block_height + 12
            total_height += block_height + 12

        if hover_desc:
            max_tip_w = min(self.window_width - 20, COUNTER_WIDTH + 180)
            desc_lines = self.wrap_text(hover_desc, max_tip_w - 20)
            line_h = 20
            max_line_w = max(self.font.size(line)[0] for line in desc_lines)
            tip_w = max_line_w + 16
            tip_h = line_h * len(desc_lines) + 12
            tip_x = self.window_width - tip_w - 10
            tip_y = max(10, self.window_height - UI_HEIGHT - 10 - tip_h)
            tip_rect = pygame.Rect(tip_x, tip_y, tip_w, tip_h)
            pygame.draw.rect(self.screen, (30, 30, 50), tip_rect)
            pygame.draw.rect(self.screen, (120, 120, 150), tip_rect, 1)
            for i, line in enumerate(desc_lines):
                ds = self.font.render(line, True, (230, 230, 230))
                self.screen.blit(ds, (tip_x + 8, tip_y + 6 + i * line_h))

        # 滚动条
        if total_height > panel_h:
            max_scroll = total_height - panel_h
            self.effect_scroll = min(self.effect_scroll, max_scroll)
            bar_h = max(20, panel_h * panel_h / total_height)
            scroll_ratio = self.effect_scroll / max_scroll if max_scroll > 0 else 0
            bar_y = panel_y + scroll_ratio * (panel_h - bar_h)
            bar_rect = pygame.Rect(panel_x + panel_w - 8, bar_y, 6, bar_h)
            pygame.draw.rect(self.screen, (80, 80, 120), bar_rect)

    def update_floating_texts(self, dt):
        for ft in self.floating_texts:
            ft.update(dt)
        self.floating_texts = [ft for ft in self.floating_texts if ft.time_left > 0]

    def draw_floating_texts(self):
        for ft in self.floating_texts:
            alpha = int(255 * ft.alpha())
            surf = self.font.render(ft.text, True, ft.color)
            surf.set_alpha(alpha)
            self.screen.blit(surf, (ft.x, ft.y))

    def update_sweepers(self, dt):
        area = self.get_bounds()["rect"]
        area = self.get_bounds()["rect"]
        for sw in self.sweepers:
            if not sw.alive:
                continue
            sw.x += sw.vx * dt
            # 碰撞检测
            sw_rect = sw.rect()
            for ent in self.all_entities():
                if ent is sw.owner:
                    continue
                if id(ent) in sw.hit_ids:
                    continue
                cx, cy = self.get_entity_center(ent)
                if sw_rect.collidepoint(cx, cy):
                    ent.take_damage()
                    sw.hit_ids.add(id(ent))

            if sw.vx > 0 and sw.x > area.right:
                sw.alive = False
            elif sw.vx < 0 and sw.x + sw.w < area.left:
                sw.alive = False

        self.sweepers = [s for s in self.sweepers if s.alive]

        # 处理待生成的上半场扫荡条
        new_pending = []
        for item in getattr(self, "pending_top_sweeps", []):
            item["delay"] -= dt
            if item["delay"] <= 0:
                owner = item["owner"]
                sw = SweepRect(
                    item["area"].right,
                    item["y_top"],
                    item["bar_w"],
                    item["bar_h"],
                    -SWEEP_SPEED,
                    owner,
                    item["area"],
                )
                self.sweepers.append(sw)
            else:
                new_pending.append(item)
        self.pending_top_sweeps = new_pending

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
                dx = cx - aoe.cx
                dy = cy - aoe.cy
                dist = math.hypot(dx, dy)
                if dist <= aoe.radius + ent.radius:
                    # 计数减2，逐点结算以支持护盾/法师护球
                    hits = 2
                    for _ in range(hits):
                        if ent.alive:
                            ent.take_damage()
                    if ent.alive:
                        # 仅给予速度冲量，不改变当前位置，避免形成阻挡
                        if dist == 0:
                            dx, dy = 1, 0
                            dist = 1
                        nx = dx / dist
                        ny = dy / dist
                        ent.vx += nx * 200
                        ent.vy += ny * 200
                    aoe.hit_ids.add(id(ent))
            new_aoes.append(aoe)
        self.aoes = [a for a in new_aoes if a.alive]

    def draw_playing(self):
        self.screen.fill((10, 10, 20))

        bounds = self.get_bounds()

        # 画运动区域背景 + 边框
        if bounds["shape"] == "rect":
            rect = bounds["rect"]
            pygame.draw.rect(self.screen, (30, 30, 50), rect)
            pygame.draw.rect(self.screen, (200, 200, 200), rect, 2)
        else:
            cx, cy = bounds["center"]
            r = bounds["radius"]
            pygame.draw.circle(self.screen, (30, 30, 50), (int(cx), int(cy)), int(r))
            pygame.draw.circle(self.screen, (200, 200, 200), (int(cx), int(cy)), int(r), 2)

        # 墙体
        self.draw_walls()

        # 轨迹与碎片
        self.draw_trails()
        # 残骸碎片
        self.draw_debris()
        # 波纹
        self.draw_ripples()
        self.draw_freeze_ripples()
        # 三角
        self.draw_triangles()

        # 方块和小球
        for b in self.blocks:
            b.draw(self.screen)
        for ball in self.balls:
            ball.draw(self.screen)
        self.draw_mage_orbs()
        self.draw_drones()

        # 道具与子弹
        for item in self.items:
            item.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for sw in self.sweepers:
            pygame.draw.rect(self.screen, (255, 200, 80), sw.rect(), 2)
        for aoe in self.aoes:
            alpha = int(180 * (aoe.time_left / aoe.total_time))
            surf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 180, 80, alpha), (int(aoe.cx), int(aoe.cy)), int(aoe.radius), 2)
            self.screen.blit(surf, (0, 0))
        self.draw_lightning()
        # 诅咒X标记
        self.draw_curse_marks()

        self.draw_floating_texts()

        self.draw_counter_bar()

        # 画底部UI
        ui_rect = pygame.Rect(
            0,
            self.window_height - UI_HEIGHT,
            self.window_width,
            UI_HEIGHT,
        )
        pygame.draw.rect(self.screen, (15, 15, 25), ui_rect)

        cfg = self.scenes[self.scene_index]
        scene_text = self.font.render(f"场景: {cfg['name']}", True, (220, 220, 220))
        self.screen.blit(scene_text, (20, self.window_height - UI_HEIGHT + 10))

        if self.time_limit is None:
            time_str = "剩余时间: ∞"
        else:
            time_str = f"剩余时间: {int(self.time_left):02d}s"
        time_text = self.font.render(time_str, True, (200, 200, 200))
        self.screen.blit(time_text, (20, self.window_height - UI_HEIGHT + 40))

        hint_text = self.font.render(
            "R 重新开始  |  ESC 返回菜单", True, (150, 150, 150)
        )
        self.screen.blit(
            hint_text, (260, self.window_height - UI_HEIGHT + 25)
        )

    def draw_counter_bar(self):
        panel_height = self.window_height - UI_HEIGHT
        panel_rect = pygame.Rect(self.play_width, 0, COUNTER_WIDTH, panel_height)
        pygame.draw.rect(self.screen, (25, 25, 45), panel_rect)
        pygame.draw.rect(self.screen, (120, 120, 150), panel_rect, 1)

        y = self.border_margin
        padding_x = 12
        slot_h = 42
        for ent in (self.blocks + self.balls):
            if not ent.alive:
                continue
            box = pygame.Rect(self.play_width + padding_x, y, COUNTER_WIDTH - padding_x * 2, slot_h)
            pygame.draw.rect(self.screen, (35, 35, 60), box)
            pygame.draw.rect(self.screen, (160, 160, 190), box, 1)

            # 左侧用实体外观的缩略图代替文字
            icon_x = box.x + 12
            icon_y = box.y + 8
            if isinstance(ent, Ball):
                pygame.draw.circle(self.screen, ent.color, (int(icon_x), int(icon_y)), 8)
            else:
                pygame.draw.circle(self.screen, ent.color, (int(icon_x), int(icon_y)), 8)
            # 职业文字
            prof_label = PROFESSION_NAMES.get(ent.profession, "-")
            p_surf = self.font.render(prof_label, True, (200, 220, 255))
            self.screen.blit(p_surf, (icon_x + 16, box.y + 4))

            # 生命槽，基础5，额外生命显示蓝色
            slot_w = (box.width - 20) / MAX_HP
            slot_y = box.y + 26
            for i in range(MAX_HP):
                rect = pygame.Rect(box.x + 8 + i * slot_w, slot_y, slot_w - 6, 10)
                color = (255, 215, 0) if i < min(ent.hp, MAX_HP) else (80, 80, 110)
                pygame.draw.rect(self.screen, color, rect, 0 if i < min(ent.hp, MAX_HP) else 1)

            if ent.hp > MAX_HP:
                extra_hits = ent.hp - MAX_HP
                extra_w = (box.width - 20) / TANK_EXTRA_HP
                extra_y = slot_y + 12
                for i in range(TANK_EXTRA_HP):
                    hits_for_bar = min(2, max(0, extra_hits - i * 2))
                    if hits_for_bar <= 0:
                        continue
                    fill_ratio = hits_for_bar / 2
                    rect = pygame.Rect(box.x + 8 + i * extra_w, extra_y, (extra_w - 6) * fill_ratio, 8)
                    pygame.draw.rect(self.screen, (100, 170, 255), rect)

            # 护盾条（绿色）
            if ent.shield_hp > 0:
                shield_slots = min(ent.shield_hp, SHIELD_MAX)
                shield_w = (box.width - 20) / SHIELD_MAX
                shield_y = slot_y - 14
                for i in range(shield_slots):
                    rect = pygame.Rect(box.x + 8 + i * shield_w, shield_y, shield_w - 6, 8)
                    pygame.draw.rect(self.screen, (80, 200, 120), rect)

            y += slot_h + 8

    def draw_timeup_overlay(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        center = self.screen.get_rect().center
        title = self.winner if self.winner else "时间到！"
        title_surf = self.font.render(title, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=center)
        self.screen.blit(title_surf, title_rect)

        hint = "按 R 重开，ESC 返回菜单"
        hint_surf = self.font.render(hint, True, (255, 255, 255))
        hint_rect = hint_surf.get_rect(center=(center[0], center[1] + 40))
        self.screen.blit(hint_surf, hint_rect)

    def draw(self):
        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "MAP_SELECT":
            self.draw_map_menu()
        elif self.state == "COUNT_SELECT":
            self.draw_count_menu()
        elif self.state == "PROF_MENU":
            self.draw_prof_menu()
        else:
            self.draw_playing()
            if self.state == "TIME_UP":
                self.draw_timeup_overlay()

        pygame.display.flip()

    # ------ 主循环 ------ #
    def run(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(60) / 1000.0  # 秒

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.state == "MENU":
                    self.handle_menu_event(event)
                elif self.state == "MAP_SELECT":
                    self.handle_map_event(event)
                elif self.state == "COUNT_SELECT":
                    self.handle_count_event(event)
                elif self.state == "PROF_MENU":
                    self.handle_prof_event(event)
                elif self.state == "PLAYING":
                    self.handle_play_event(event)
                elif self.state == "TIME_UP":
                    self.handle_timeup_event(event)

            if self.state == "PLAYING":
                self.update_playing(dt)

            self.draw()


if __name__ == "__main__":
    game = Game(SCENES)
    game.run()
