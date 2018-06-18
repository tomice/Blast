class Settings():
    """Storage class for Blast settings."""
    def __init__(self):
        """Init game settings."""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.ship_limit = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 255, 255
        self.bullets_allowed = 10
        self.fleet_drop_speed = 10
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Init dynamic settings"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.enemy_speed_factor = 1
        self.enemy_points = 50

        # 1 is right, -1 is left
        self.fleet_direction = 1
    
    def increase_speed(self):
        """Increase speed settings and enemy point vals"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.enemy_speed_factor *= self.speedup_scale
        self.enemy_points = int(self.enemy_points * self.score_scale)
