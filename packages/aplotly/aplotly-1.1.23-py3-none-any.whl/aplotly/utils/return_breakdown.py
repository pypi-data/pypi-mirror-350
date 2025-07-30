import numpy as np
import pandas as pd


def separate_exposures_and_returns(exposures, returns):
    # if the indicies are not the same raise an error
    if not exposures.index.equals(returns.index):
        raise ValueError("The indicies of exposures and returns must be the same")

    indices = np.where(exposures.diff().abs().sum(axis=1) != 0)[0]

    return np.split(exposures, indices), np.split(returns, indices)


def get_sequence_returns(separated_exposures, separated_returns):
    sequence_returns = []
    for _exposures, _returns in zip(separated_exposures, separated_returns):
        if _exposures.empty or _returns.empty:
            continue

        # calculate the cumulative returns for each sequence
        _sequence_returns = (_returns + 1).cumprod() - 1
        _sequence_returns = _sequence_returns.iloc[-1]
        _sequence_returns = _sequence_returns * _exposures.iloc[-1]
        sequence_returns.append(_sequence_returns)

    return sequence_returns


def combine_sequence_returns(sequence_returns):
    return pd.concat(sequence_returns, axis=1).T.cumsum(axis=0)


def calculate_return_breakdown(exposures, returns):
    separated_exposures, separated_returns = separate_exposures_and_returns(exposures, returns)
    sequence_returns = get_sequence_returns(separated_exposures, separated_returns)
    return combine_sequence_returns(sequence_returns).iloc[-1]
