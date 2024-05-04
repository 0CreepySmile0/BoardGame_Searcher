import pandas as pd
import numpy as np


def get_board_game_df():
    temp_df = pd.read_csv("Data/board_game.csv", sep=";")
    temp_df.drop(temp_df[(temp_df["Domains"].isnull()) & (temp_df["Mechanics"].isnull())].index, inplace=True)
    temp_df.drop(temp_df[temp_df["Year Published"] <= 0].index, inplace=True)
    temp_df.drop(temp_df[temp_df["Min Players"] <= 0].index, inplace=True)
    temp_df.drop(temp_df[temp_df["Max Players"] <= 0].index, inplace=True)
    temp_df.drop(temp_df[temp_df["Max Players"] < temp_df["Min Players"]].index, inplace=True)
    temp_df.dropna(subset=["Owned Users"], inplace=True)
    temp_df["Owned Users"] = temp_df["Owned Users"].astype(np.int64)
    temp_df["Year Published"] = temp_df["Year Published"].astype(np.int64)
    temp_df["ID"] = temp_df["ID"].astype(np.int64)
    for i in temp_df["Rating Average"].unique():
        temp1 = i.replace(",", ".")
        temp_df["Rating Average"].replace(to_replace=i, value=float(temp1), inplace=True)
    for i in temp_df["Complexity Average"].unique():
        temp1 = i.replace(",", ".")
        temp_df["Complexity Average"].replace(to_replace=i, value=float(temp1), inplace=True)
    temp_df.fillna(value="Unknown", inplace=True)
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df
