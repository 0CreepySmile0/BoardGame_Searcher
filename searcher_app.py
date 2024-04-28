from searcher_ui import SearcherUI
from data_process import get_board_game_df

board_game_df = get_board_game_df()
ui = SearcherUI(board_game_df)
ui.run()
