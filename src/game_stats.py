from pathlib import Path

class GameStats():
    """Track stats for Blast"""
    def __init__(self, blast_settings):
        """Init stats"""
        self.blast_settings = blast_settings
        self.reset_stats()
        self.game_active = False
        #self.high_score = 0
        self.set_high_score()

    def reset_stats(self):
        """Init stats that change during game"""
        self.ships_left = self.blast_settings.ship_limit
        self.score = 0
        self.level = 1
    
    def set_high_score(self):
        """Read high score from a file"""
        # FIXME: Major hack. Refactor this. Violates DRY
        #        Also, use error handling, as it'll crash if data is not an int
        high_score_file = Path("highscore.txt")
        if high_score_file.is_file():
            high_score_file = open("highscore.txt", "r")
            self.high_score = int(high_score_file.read())
            high_score_file.close()
        else:
            high_score_file = open("highscore.txt", "w")
            high_score_file.write("0")
            high_score_file.close()
            high_score_file = open("highscore.txt", "r")
            self.high_score = int(high_score_file.read())
            high_score_file.close()
