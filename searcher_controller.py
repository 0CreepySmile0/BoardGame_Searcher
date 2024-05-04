import pandas as pd


class SearcherController:
    def __init__(self, data: pd.DataFrame):
        self.__df = data

    @staticmethod
    def __search_data(df: pd.DataFrame, search_by: str, search_text: str):
        if not search_text:
            return df
        word = search_text.split(" ")
        mask = eval(" & ".join([f"(df['{search_by}'].astype(str).str.contains('{i}'))" for i in word]))
        temp_df = df[mask]
        temp_df.reset_index(drop=True, inplace=True)
        return temp_df

    @staticmethod
    def __sort_data(df: pd.DataFrame, sort_list: list):
        if not sort_list:
            return df
        temp_df = df.sort_values(by=sort_list, axis=0)
        temp_df.reset_index(drop=True, inplace=True)
        return temp_df

    @property
    def original_data(self):
        return self.__df

    def modified_data(self, search_text: str="", search_by: str="", sort_list: list=[]):
        if (not search_text) and (not sort_list):
            return self.original_data
        temp_search = self.__search_data(self.__df, search_by, search_text)
        temp_sort = self.__sort_data(temp_search, sort_list)
        return temp_sort
