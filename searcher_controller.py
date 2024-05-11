import pandas as pd


class SearcherController:

    def __init__(self, data: pd.DataFrame, graph1: list=None, graph2: list=None,
                 graph3: list=None, graph4: list=None):
        self.__df = data
        col = list(self.__df.columns)
        if graph1 is not None:
            if (len(graph1) != 2) or (graph1[0] not in col) or \
                    (graph1[1] not in col) or (graph1[0] == graph1[1]):
                self._att1 = None
        if graph2 is not None:
            if (len(graph2) != 2) or (graph2[0] not in col) or \
                    (graph2[1] not in col) or (graph2[0] == graph2[1]):
                self._att2 = None
        if graph3 is not None:
            if (len(graph3) != 2) or (graph3[0] not in col) or \
                    (graph3[1] not in col) or (graph3[0] == graph3[1]):
                self._att3 = None
        if graph4 is not None:
            if (len(graph4) != 2) or (graph4[0] not in col) or \
                    (graph4[1] not in col) or (graph4[0] == graph4[1]):
                self._att4 = None
        self._att1 = graph1
        self._att2 = graph2
        self._att3 = graph3
        self._att4 = graph4

    @staticmethod
    def _search_data(df: pd.DataFrame, search_by: str, search_text: str):
        if not search_text:
            return df
        word = search_text.split(" ")
        mask = eval(" & ".join([f"(df['{search_by}'].astype(str).str.contains('{i}'))"
                                for i in word]))
        temp_df = df[mask]
        temp_df.reset_index(drop=True, inplace=True)
        return temp_df

    @staticmethod
    def _sort_data(df: pd.DataFrame, sort_list: list, ascending: bool):
        if not sort_list:
            return df
        temp_df = df.sort_values(by=sort_list, axis=0, ascending=ascending)
        temp_df.reset_index(drop=True, inplace=True)
        return temp_df

    @property
    def original_data(self):
        return self.__df

    def modified_data(self, search_text: str="", search_by: str="", sort_list: list=[],
                      descending: bool=False):
        if (not search_text) and (not sort_list):
            return self.original_data
        temp_search = self._search_data(self.__df, search_by, search_text)
        temp_sort = self._sort_data(temp_search, sort_list, not descending)
        return temp_sort

    def get_attribute(self, which: int, df: pd.DataFrame):
        if which == 1:
            corr = df[self._att1[0]].corr(df[self._att1[1]])
            if corr > 0:
                pos_neg = "positive"
            else:
                pos_neg = "negative"
            if corr >= 0.5 or corr <= -0.5:
                strength = "strong"
            else:
                strength = "weak"
            temp_df = df
            att = self._att1
            text = f"Correlation coefficient = {df[self._att1[0]].corr(df[self._att1[1]]):.3f}\n" \
                   f"{strength.capitalize()} {pos_neg} correlation\n" \
                   f"The more {self._att1[0]} the more {self._att1[1]}"
        elif which == 2:
            u = df[self._att2[1]]
            r = df[self._att2[0]]
            mean = (u*r).sum()/u.sum()
            sd = ((((r-mean)**2)*u).sum() / u.sum())**0.5
            temp_df = df
            att = self._att2
            text = f"{self._att2[0]}\nMean = {mean:.3f}, SD = {sd:.3f}, Min = {r.min():.3f}, Max = {r.max():.3f}"
        elif which == 3:
            temp_df = pd.DataFrame({f"{self._att3[0]} vs {self._att3[1]}": [self._att3[0], self._att3[1]],
                                    "Count": [df[self._att3[0]].sum(), df[self._att3[1]].sum()]})
            att = [f"{self._att3[0]} vs {self._att3[1]}", "Count"]
            text = f"Number of {self._att3[0]} vs number of {self._att3[1]}"
        elif which == 4:
            unique = [i.split()[0] for i in df[self._att4[0]].unique() if "," not in i]
            temp_df = pd.DataFrame({self._att4[0]: unique,
                                    self._att4[1]: [df[df[self._att4[0]].str.contains(i)][self._att4[1]].sum() for i in unique]})
            att = self._att4
            text = f"Number of {self._att4[1]} for each {self._att4[0]}"
        return att, text, temp_df
