from src.main_game import Game, LevelParser

if __name__ == '__main__':
    map1 = "maps/level_1.map"
    map2 = "maps/level_2.map"
    save_game_1 = "saves/save_game.json"
    game = Game()
    lp = LevelParser(save_game_1)
    game.level = lp.get_level()
    game.execute()
