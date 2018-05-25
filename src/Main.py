from src.main_game import Game, LevelParser, LevelWriter

if __name__ == '__main__':
    map1 = "maps/level_1.map"
    map2 = "maps/level_2.map"
    save_game_2 = "saves/save_game2.json"
    save_game_3 = "saves/savega.json"

    game = Game()
    lp = LevelParser(save_game_3)
    game.level = lp.get_level()
    game.execute()
