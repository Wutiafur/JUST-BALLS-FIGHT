# -*- coding: utf-8 -*-
import sys
import pygame


TILE_SIZE = 48
UI_HEIGHT = 80
FONT_SIZE = 26
AI_INTERVAL = 0.35

PREFERRED_FONTS = [
    "Microsoft YaHei UI",
    "Microsoft YaHei",
    "SimHei",
    "SimSun",
    "Noto Sans CJK SC",
    "Source Han Sans SC",
    "Arial Unicode MS",
]

# 可以在这里自定义更多战斗场景
SCENES = [
    {
        "name": "对战：中间一堵墙",
        "width": 15,
        "height": 9,
        "player_spawns": [(2, 4), (12, 4)],
        "walls": [(7, y) for y in range(0, 9)],
    },
    {
        "name": "对战：双通道",
        "width": 15,
        "height": 9,
        "player_spawns": [(2, 4), (12, 4)],
        "walls": [(7, y) for y in range(0, 9)] + [(4, 0), (4, 8), (10, 0), (10, 8)],
    },
]


class Entity:
    def __init__(self, x, y, max_hp, atk):
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.hp = max_hp
        self.atk = atk

    @property
    def pos(self):
        return self.x, self.y

    def is_alive(self):
        return self.hp > 0


class Player(Entity):
    pass


class Enemy(Entity):
    pass


class Game:
    def __init__(self, scenes):
        pygame.init()
        pygame.display.set_caption("可自定义战斗场景 Demo")
        self.font = self._load_font(FONT_SIZE)

        self.scenes = scenes
        self.scene_index = 0

        self.state = "MENU"      # MENU / PLAYING / GAME_OVER
        self.last_result = None  # "P1" / "P2" / "DRAW" / None

        # 先按照第一关大小创建窗口，后续切换关卡会自动调整
        first = self.scenes[0]
        self.map_width = first["width"]
        self.map_height = first["height"]
        self.screen = pygame.display.set_mode(
            (self.map_width * TILE_SIZE, self.map_height * TILE_SIZE + UI_HEIGHT)
        )

        self.players = []
        self.walls = set()
        self.ai_accum = 0.0

    def _load_font(self, size):
        # 尝试优先加载支持中文的字体，避免显示成方块
        for name in PREFERRED_FONTS:
            matched = pygame.font.match_font(name)
            if matched:
                return pygame.font.Font(matched, size)
        # 兜底：使用默认字体（可能缺少中文）
        return pygame.font.SysFont(None, size)

    # ---------- 场景相关 ---------- #

    def load_scene(self, index):
        cfg = self.scenes[index]
        self.scene_index = index
        self.map_width = cfg["width"]
        self.map_height = cfg["height"]

        # 重新创建窗口以适配不同尺寸
        self.screen = pygame.display.set_mode(
            (self.map_width * TILE_SIZE, self.map_height * TILE_SIZE + UI_HEIGHT)
        )

        self.walls = set(cfg.get("walls", []))

        self.players = []
        spawns = cfg.get("player_spawns", [])
        # 默认两名玩家，若配置不足则填充在起点
        while len(spawns) < 2:
            spawns.append((1 + len(spawns), 1))
        p1x, p1y = spawns[0]
        p2x, p2y = spawns[1]
        self.players.append(Player(p1x, p1y, max_hp=12, atk=3))
        self.players.append(Player(p2x, p2y, max_hp=12, atk=3))

        self.state = "PLAYING"
        self.last_result = None
        self.ai_accum = 0.0

    # ---------- 规则判断 ---------- #

    def inside_map(self, x, y):
        return 0 <= x < self.map_width and 0 <= y < self.map_height

    def tile_blocked(self, x, y, ignore=None):
        for p in self.players:
            if not p.is_alive():
                continue
            if ignore is p:
                continue
            if p.pos == (x, y):
                return True

        return False

    def try_move(self, unit, dx, dy):
        nx = unit.x + dx
        ny = unit.y + dy
        if not self.inside_map(nx, ny):
            return False
        if self.tile_blocked(nx, ny, ignore=unit):
            return False
        unit.x, unit.y = nx, ny
        return True

    def player_attack(self, attacker, defender):
        """攻击上下左右一格的对手"""
        if not attacker or not attacker.is_alive() or not defender or not defender.is_alive():
            return False

        ax, ay = attacker.pos
        dx, dy = defender.pos
        if abs(ax - dx) + abs(ay - dy) == 1:
            defender.hp -= attacker.atk
            return True
        return False

    def ai_move_toward(self, unit, target):
        if not unit or not unit.is_alive() or not target or not target.is_alive():
            return
        dx = target.x - unit.x
        dy = target.y - unit.y
        # 优先尝试距离更大的轴向，失败后尝试另一轴
        primary_axis_is_x = abs(dx) >= abs(dy)
        steps = []
        if dx != 0:
            steps.append((1 if dx > 0 else -1, 0))
        if dy != 0:
            steps.append((0, 1 if dy > 0 else -1))
        if not primary_axis_is_x:
            steps.reverse()
        for sx, sy in steps:
            if self.try_move(unit, sx, sy):
                return

    def ai_turn(self):
        if len(self.players) < 2:
            return
        p1, p2 = self.players[0], self.players[1]
        # 玩家1行为
        if p1.is_alive():
            if not self.player_attack(p1, p2):
                self.ai_move_toward(p1, p2)
        # 玩家2行为
        if p2.is_alive():
            if not self.player_attack(p2, p1):
                self.ai_move_toward(p2, p1)
        self.check_result()

    def update_ai(self, dt):
        if self.state != "PLAYING":
            return
        self.ai_accum += dt
        while self.ai_accum >= AI_INTERVAL:
            self.ai_accum -= AI_INTERVAL
            self.ai_turn()

    def check_result(self):
        p1_alive = self.players[0].is_alive()
        p2_alive = self.players[1].is_alive()
        if not p1_alive and not p2_alive:
            self.last_result = "DRAW"
            self.state = "GAME_OVER"
        elif not p1_alive:
            self.last_result = "P2"
            self.state = "GAME_OVER"
        elif not p2_alive:
            self.last_result = "P1"
            self.state = "GAME_OVER"

    # ---------- 事件处理 ---------- #

    def handle_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.scene_index = (self.scene_index + 1) % len(self.scenes)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.scene_index = (self.scene_index - 1) % len(self.scenes)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.load_scene(self.scene_index)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def handle_play_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            # 返回菜单但不关闭窗口
            self.state = "MENU"
            return
        # 对战由AI自动进行，按键仅用于退出

    def handle_gameover_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.load_scene(self.scene_index)
            elif event.key == pygame.K_ESCAPE:
                self.state = "MENU"

    # ---------- 绘制 ---------- #

    def draw_menu(self):
        self.screen.fill((20, 20, 30))
        title = self.font.render("选择战斗场景（上下方向键，回车确认）", True, (220, 220, 220))
        self.screen.blit(title, (20, 20))

        for i, sc in enumerate(self.scenes):
            name = sc["name"]
            text = f"{i + 1}. {name}"
            color = (255, 255, 0) if i == self.scene_index else (200, 200, 200)
            surf = self.font.render(text, True, color)
            self.screen.blit(surf, (40, 70 + i * 30))

        hint = self.font.render("ESC 退出", True, (160, 160, 160))
        self.screen.blit(hint, (20, 70 + len(self.scenes) * 30 + 10))

    def draw_grid(self):
        for y in range(self.map_height):
            for x in range(self.map_width):
                rect = pygame.Rect(
                    x * TILE_SIZE,
                    y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE,
                )
                # 地板
                pygame.draw.rect(self.screen, (40, 40, 50), rect)
                # 网格线
                pygame.draw.rect(self.screen, (60, 60, 80), rect, 1)

                if (x, y) in self.walls:
                    inner = rect.inflate(-8, -8)
                    pygame.draw.rect(self.screen, (90, 90, 110), inner)

    def draw_units(self):
        colors = [(80, 200, 80), (80, 120, 220)]
        for idx, p in enumerate(self.players):
            if not p.is_alive():
                continue
            rect = pygame.Rect(
                p.x * TILE_SIZE,
                p.y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE,
            )
            inner = rect.inflate(-10, -10)
            pygame.draw.rect(self.screen, colors[idx % len(colors)], inner)

    def draw_ui(self):
        # UI 背景
        ui_rect = pygame.Rect(
            0,
            self.map_height * TILE_SIZE,
            self.map_width * TILE_SIZE,
            UI_HEIGHT,
        )
        pygame.draw.rect(self.screen, (15, 15, 25), ui_rect)

        cfg = self.scenes[self.scene_index]

        # 显示当前场景、血量、提示
        scene_text = self.font.render(
            f"场景: {cfg['name']}", True, (230, 230, 230)
        )
        self.screen.blit(scene_text, (10, self.map_height * TILE_SIZE + 10))

        p1_hp = self.players[0].hp if self.players else 0
        p2_hp = self.players[1].hp if len(self.players) > 1 else 0
        hp_text = self.font.render(
            f"玩家1 HP: {p1_hp}    玩家2 HP: {p2_hp}", True, (200, 200, 200)
        )
        self.screen.blit(hp_text, (10, self.map_height * TILE_SIZE + 40))

        tip_text = self.font.render(
            "AI 自动对战，等待结果；ESC 返回菜单",
            True,
            (160, 160, 160),
        )
        self.screen.blit(tip_text, (260, self.map_height * TILE_SIZE + 10))

        rest_text = self.font.render(
            "目标: 打败对方玩家", True, (160, 160, 160)
        )
        self.screen.blit(rest_text, (260, self.map_height * TILE_SIZE + 40))

    def draw_gameover_overlay(self):
        if self.last_result == "P1":
            text = "玩家1 获胜！按 R 重新开始，ESC 返回菜单"
        elif self.last_result == "P2":
            text = "玩家2 获胜！按 R 重新开始，ESC 返回菜单"
        else:
            text = "平局！按 R 重新开始，ESC 返回菜单"

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        surf = self.font.render(text, True, (255, 255, 255))
        rect = surf.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(surf, rect)

    def draw(self):
        if self.state == "MENU":
            self.draw_menu()
        else:
            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_units()
            self.draw_ui()
            if self.state == "GAME_OVER":
                self.draw_gameover_overlay()
        pygame.display.flip()

    # ---------- 主循环 ---------- #

    def run(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.state == "MENU":
                    self.handle_menu_event(event)
                elif self.state == "PLAYING":
                    self.handle_play_event(event)
                elif self.state == "GAME_OVER":
                    self.handle_gameover_event(event)

            self.update_ai(dt)
            self.draw()


if __name__ == "__main__":
    game = Game(SCENES)
    game.run()
