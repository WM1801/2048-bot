import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

 


from ai import *
from move import *


class Algorithm(Enum):
    ALPHABETA = 1,
    EXPECTIMAX = 2


class Game2048:

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.get(url='https://play2048.co/')
        self.browser.set_window_position(0, 0)
        self.browser.set_window_size(1024, 1024)
        #self.htmlElem = self.browser.find_element_by_tag_name('html')
        self.htmlElem = self.browser.find_element(by=By.TAG_NAME, value="html")
        self.engine2048 = Engine2048()
        self.actual_score = 0
        self.has_won_flag = False
        self.tile_scores = []

    def parse_web_content(self):
        """
        Parses the 2048 game in the Web-browser.
        """
        # Parse the current score
        try:
            elem = self.browser.find_element(By.CLASS_NAME,".score-container")
            self.actual_score = int(elem.text)
            print ("score")
        except:
            pass
            
        try:
            elem = self.browser.find_element(By.CLASS_NAME,"grid-cell")
            print("grid-cell find")
        except:
            print("grid-cell not find")
            

     
                  
        game = Grid2048()

        range_str = ["1", "2", "3", "4"]

        # Parse the grid
        for x in range_str:
            for y in range_str:
                try:
                    #elements = self.browser.find_element(By.CLASS_NAME,"tile-position-" + x + '-' + y)
                    elements = self.browser.find_elements(By.CLASS_NAME, f"tile-position-{x}-{y}")
                    max_grid_cell_val = 0

                    if len(elements) > 0:
                        for elem in elements:
                            if elem != '':
                                if int(elem.text) > max_grid_cell_val:
                                    max_grid_cell_val = int(elem.text)

                        game.insert(int(y) - 1, int(x) - 1, max_grid_cell_val)

                except:
                    print('Not found')

        return game

    def move_web_grid(self, move: EMove):
        """
        Moves the game in the web browser.
        """
        if move == EMove.LEFT:
            self.htmlElem.send_keys(Keys.LEFT)

        if move == EMove.RIGHT:
            self.htmlElem.send_keys(Keys.RIGHT)

        if move == EMove.UP:
            self.htmlElem.send_keys(Keys.UP)

        if move == EMove.DOWN:
            self.htmlElem.send_keys(Keys.DOWN)

    def run(self, nbr_runs: int, algorithm: Algorithm, heuristic: HeuristicScore):
        """
        Gets the parsed game and then runs the AI to get best move that will be used to move the
        game in the next direction.
        """
        scores = []
        wins = 0

        for i in range(nbr_runs):

            tiles = {}

            while True:
                game = self.parse_web_content()
                self.engine2048.bestMove = None

                if not self.has_won_flag:
                    if game.has_won():
                        time.sleep(5)
                        #self.browser.find_element_by_css_selector('.keep-playing-button').click()
                        self.browser.find_element(By.CSS_SELECTOR, '.keep-playing-button').click()
                        time.sleep(5)
                        self.has_won_flag = True
                        wins += 1

                time.sleep(0.1)

                print("/////////////Iteration", i, " Score", self.actual_score, " Average", round(sum(scores) / (i + 1)))

                # Find best move according to chosen algorithm.
                best_move = None

                if algorithm is Algorithm.ALPHABETA:
                    best_move = self.engine2048.best_move_alphabeta(game, heuristic)

                elif algorithm is Algorithm.EXPECTIMAX:
                    best_move = self.engine2048.best_move_expectimax(game, heuristic)

                self.move_web_grid(best_move)
                tiles = game.parse_tiles(tiles, 8)

                time.sleep(0.1)

                if best_move is None:
                    break

            # ////////////////////////// STATS /////////////////////////////////
            scores.append(self.actual_score)
            self.actual_score = 0
            self.tile_scores.append(tiles)

            # ////////////////////////// NEW GAME //////////////////////////////
            if i < nbr_runs:
                time.sleep(2)
                #self.browser.find_element_by_css_selector('.restart-button').click()
                self.browser.find_element(By.CSS_SELECTOR, '.restart-button').click()
                self.has_won_flag = False
                time.sleep(2)

        print("///////////////// STATS ////////////////////////")
        print("Number of wins ", wins)
        print("Win probability ", round(wins / nbr_runs, 2))
        print("smallest score", min(scores))
        print("Highest score ", max(scores))
        print("Average score ", round(sum(scores) / nbr_runs))
        print("Scores", scores)

        nbr_1024, nbr_2048, nbr_4096, nbr_8192 = 0, 0, 0, 0

        for i in range(nbr_runs):
            if 1024 in self.tile_scores[i]:
                nbr_1024 += self.tile_scores[i][1024]
            if 2048 in self.tile_scores[i]:
                nbr_2048 += self.tile_scores[i][2048]
            if 4096 in self.tile_scores[i]:
                nbr_4096 += self.tile_scores[i][4096]
            if 8192 in self.tile_scores[i]:
                nbr_8192 += self.tile_scores[i][8192]

        print("1024 reached : ", nbr_1024)
        print("2048 reached : ", nbr_2048)
        print("4096 reached : ", nbr_4096)
        print("8192 reached : ", nbr_8192)


""" MAIN PROGRAM --------------------------------- """


def main():
    game = Game2048()
    runs = 50
    # game.run(nbr_runs=runs, algorithm=Algorithm.ALPHABETA, heuristic=HeuristicScore.CORNER)
    # game.run(nbr_runs=runs, algorithm=Algorithm.ALPHABETA, heuristic=HeuristicScore.CORNERS)
    # game.run(nbr_runs=runs, algorithm=Algorithm.ALPHABETA, heuristic=HeuristicScore.SNAKE)
    # game.run(nbr_runs=runs, algorithm=Algorithm.EXPECTIMAX, heuristic=HeuristicScore.CORNER)
    # game.run(nbr_runs=runs, algorithm=Algorithm.EXPECTIMAX, heuristic=HeuristicScore.CORNERS)
    game.run(nbr_runs=runs, algorithm=Algorithm.EXPECTIMAX, heuristic=HeuristicScore.SNAKE)


if __name__ == '__main__':
    main()
