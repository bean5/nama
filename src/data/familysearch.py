import os

import pandas as pd
import numpy as np
from typing import List, Tuple
from src.data.utils import _train_test_split
from src.models.utils import add_padding


def train_test_split(dataset_path: str, train_path: str, test_path: str, starting_test_size: float = 0.1):
    """
    Split test and train data in dataset_path and save train_path and test_path to disk
    """
    df = pd.read_csv(dataset_path, sep=",", header=0)
    # name = tree name
    # alt_name = record name
    # frequency = number of times name1 -> name2
    # ordered_prob = frequency / sum(frequency) for all occurrences of name1
    df.dropna(inplace=True)

    # Split train test
    df_train, df_test = _train_test_split(df, "name", "alt_name", starting_test_size=starting_test_size)

    # set the ordered_prob column and limit the columns to save
    df_train = _prepare(df_train)
    df_test = _prepare(df_test)

    # Persist splits on disk
    df_train.to_csv(train_path)
    df_test.to_csv(test_path)


def load_train_test(
    train_path: str, test_path: str
) -> (
    (List[str], List[List[Tuple[str, float, int]]], np.array),
    (List[str], List[List[Tuple[str, float, int]]], np.array),
):
    """
    Load and process test and train datasets
    """
    df_train = pd.read_csv(train_path)
    df_test = pd.read_csv(test_path)
    input_names_train, weighted_actual_names_train, all_candidates_train = _load(df_train)
    input_names_test, weighted_actual_names_test, all_candidates_test = _load(df_test)

    return (input_names_train, weighted_actual_names_train, all_candidates_train), (
        input_names_test,
        weighted_actual_names_test,
        all_candidates_test,
    )


def _prepare(df: pd.DataFrame) -> pd.DataFrame:
    """
    Given a dataframe, calculate the correct ordered_prob and frequency and remove unused columns
    """

    def divide_weighted_count_by_sum(df):
        df["ordered_prob"] = df["frequency"] / df["frequency"].sum()
        return df

    # Add padding
    df.loc[:, "name"] = df.loc[:, "name"].map(add_padding)
    df.loc[:, "alt_name"] = df.loc[:, "alt_name"].map(add_padding)

    df = df.groupby(["name", "alt_name"]).sum().groupby(level=0).apply(divide_weighted_count_by_sum).reset_index()
    # TODO remove co_occurrence count if we don't use it
    return df[["name", "alt_name", "ordered_prob", "frequency"]]


def _load(df: pd.DataFrame) -> (List[str], List[List[Tuple[str, float, int]]], np.array):
    """
    Given a dataframe, return
    a list of input names (distinct name1),
    a list of lists of weighted actual names (name2, weighted_count (probability that name1 -> name2, and co_occurrence)
    for each input name
    a list of candidate names (distinct name2)
    """
    df_name_matches = df.groupby("name").agg(list).reset_index()
    weighted_actual_names = [
        [(n, w, c) for n, w, c in zip(ns, ws, cs)]
        for ns, ws, cs in zip(
            df_name_matches["alt_name"], df_name_matches["ordered_prob"], df_name_matches["frequency"]
        )
    ]
    input_names = df_name_matches["name"].tolist()
    candidate_names = np.array(df["alt_name"].unique())

    # if you want just relevant names:
    # [[name for name,weight in name_weights] for name_weights in weighted_actual_names]
    return input_names, weighted_actual_names, candidate_names
