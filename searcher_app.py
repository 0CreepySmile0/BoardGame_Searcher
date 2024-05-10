from searcher_ui import SearcherUI
from searcher_controller import SearcherController
from data_process import get_board_game_df

board_game_df = get_board_game_df()
controller = SearcherController(board_game_df, ["Min Age", "Complexity Average"],
                                ["Rating Average", "Users Rated"],
                                ["Users Rated", "Owned Users"], ["Domains", "Owned Users"])
ui = SearcherUI(controller)
ui.run()
