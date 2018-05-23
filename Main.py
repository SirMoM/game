from game import Game, LevelParser

if __name__ == '__main__':
    map1 = "maps/level_1.map"
    map2 = "maps/level_2.map"
    game = Game()
    lp = LevelParser("saves/save_game.json")
    game.level = lp.get_level()
    game.execute()
