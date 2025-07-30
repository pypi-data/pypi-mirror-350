import numpy as np
import pandas as pd
from typing_extensions import Literal
from collections import OrderedDict


class PortfolioAnalyzer:
    @staticmethod
    def nav2stats(nav, period: Literal["M", "Q", "Y", None] = None):
        if period == None:
            return PortfolioAnalyzer._nav_to_stats(nav)
        else:
            columns_order = [
                "Total Return (%)",
                "CAGR (%)",
                "Volatility (%)",
                "Sharpe Ratio",
                "Sortino Ratio",
                "Max Drawdown (%)",
                "Skewness",
                "Kurtosis",
                "VaR 95% (%)",
                "VaR 99% (%)",
                "Positive HHI",
                "Negative HHI",
            ]
            result = (
                nav.groupby(pd.Grouper(freq=period))
                .apply(PortfolioAnalyzer._nav_to_stats)
                .unstack()
            )
            return result[columns_order].dropna()

    @staticmethod
    def position2stats(position, period: Literal["D", "M", "Q", "Y", None] = None):
        if period == "D":
            return pd.DataFrame(
                PortfolioAnalyzer._position_to_stats(position, group=False)
            )
        elif period == None:
            return pd.Series(PortfolioAnalyzer._position_to_stats(position, group=True))
        else:
            result = position.groupby(pd.Grouper(freq=period)).apply(
                PortfolioAnalyzer._position_to_stats
            )
            return pd.DataFrame(
                result.tolist(), index=result.index, columns=result.values[0].keys()
            ).dropna()

    @staticmethod
    def nav2stats_dict(returns):
        if len(returns) < 2:
            return {
                "total_return": np.nan,
                "cagr": np.nan,
                "volatility": np.nan,
                "sharpe_ratio": np.nan,
                "sortino_ratio": np.nan,
                "max_drawdown": np.nan,
                "skewness": np.nan,
                "kurtosis": np.nan,
                "var_95": np.nan,
                "var_99": np.nan,
                "positive_hhi": np.nan,
                "negative_hhi": np.nan,
            }

        total_return = returns.iloc[-1] / returns.iloc[0] - 1
        trading_days = len(returns)
        returns_pct = returns.pct_change().dropna()

        returns_pct_std = returns_pct.std()
        returns_pct_std_neg = returns_pct[returns_pct < 0].std()
        skewness = PortfolioAnalyzer._calculate_skewness(returns_pct)
        kurtosis = PortfolioAnalyzer._calculate_kurtosis(returns_pct)
        positive_hhi = PortfolioAnalyzer._calculatea_run_HHI(returns_pct, 1)
        negative_hhi = PortfolioAnalyzer._calculatea_run_HHI(returns_pct, 0)
        stats_dict = {
            "total_return": total_return,
            "cagr": (
                (1 + total_return) ** (252 / trading_days) - 1
                if trading_days != 0
                else np.nan
            ),
            "volatility": returns_pct.std() * np.sqrt(252),
            "sharpe_ratio": (
                (returns_pct.mean() / returns_pct_std) * np.sqrt(252)
                if returns_pct_std != 0
                else np.nan
            ),
            "sortino_ratio": (
                (returns_pct.mean() / returns_pct_std_neg) * np.sqrt(252)
                if returns_pct_std_neg != 0
                else np.nan
            ),
            "max_drawdown": (returns / returns.cummax() - 1).min(),
            "skewness": skewness,
            "kurtosis": kurtosis,
            "var_95": np.percentile(returns_pct, 5),
            "var_99": np.percentile(returns_pct, 1),
            "positive_hhi": positive_hhi,
            "negative_hhi": negative_hhi,
        }

        return stats_dict

    @staticmethod
    def _nav_to_stats(returns):
        if len(returns) < 2:
            return pd.Series(
                {
                    "Total Return (%)": np.nan,
                    "CAGR (%)": np.nan,
                    "Volatility (%)": np.nan,
                    "Sharpe Ratio": np.nan,
                    "Sortino Ratio": np.nan,
                    "Max Drawdown (%)": np.nan,
                    "Skewness": np.nan,
                    "Kurtosis": np.nan,
                    "VaR 95% (%)": np.nan,
                    "VaR 99% (%)": np.nan,
                    "Positive HHI": np.nan,
                    "Negative HHI": np.nan,
                }
            )

        total_return = (returns.iloc[-1] / returns.iloc[0] - 1) * 100
        trading_days = len(returns)
        returns_pct = returns.pct_change().dropna()

        returns_pct_std = returns_pct.std()
        returns_pct_std_neg = returns_pct[returns_pct < 0].std()
        skewness = PortfolioAnalyzer._calculate_skewness(returns_pct)
        kurtosis = PortfolioAnalyzer._calculate_kurtosis(returns_pct)
        positive_hhi = PortfolioAnalyzer._calculatea_run_HHI(returns_pct, 1)
        negative_hhi = PortfolioAnalyzer._calculatea_run_HHI(returns_pct, 0)
        stats_dict = {
            "Total Return (%)": round(total_return, 3),
            "CAGR (%)": (
                round(((1 + total_return / 100) ** (252 / trading_days) - 1) * 100, 3)
                if trading_days != 0
                else None
            ),
            "Volatility (%)": round(returns_pct.std() * np.sqrt(252) * 100, 3),
            "Sharpe Ratio": (
                round((returns_pct.mean() / returns_pct_std) * np.sqrt(252), 3)
                if returns_pct_std != 0
                else None
            ),
            "Sortino Ratio": (
                round(
                    (returns_pct.mean() / returns_pct_std_neg) * np.sqrt(252),
                    3,
                )
                if returns_pct_std_neg != 0
                else None
            ),
            "Max Drawdown (%)": round((returns / returns.cummax() - 1).min() * 100, 3),
            "Skewness": round(skewness, 3) if skewness is not None else None,
            "Kurtosis": round(kurtosis, 3) if kurtosis is not None else None,
            "VaR 95% (%)": round(np.percentile(returns_pct, 5) * 100, 3),
            "VaR 99% (%)": round(np.percentile(returns_pct, 1) * 100, 3),
            "Positive HHI": (
                round(positive_hhi, 3) if positive_hhi is not None else None
            ),
            "Negative HHI": (
                round(negative_hhi, 3) if negative_hhi is not None else None
            ),
        }

        return pd.Series(stats_dict)

    @staticmethod
    def _position_to_stats(position, group=True):
        hhi = PortfolioAnalyzer._calculate_HHI(position)
        normalized_hhi = PortfolioAnalyzer._norm_calculate_HHI(position)
        ens = 1 / hhi.replace(0, np.nan)
        turnover = PortfolioAnalyzer._calculate_turnover(position)
        stats_dict = {
            "con50": position.apply(
                lambda row: PortfolioAnalyzer._calculate_cons(row, 50), axis=1
            ),
            "con80": position.apply(
                lambda row: PortfolioAnalyzer._calculate_cons(row, 80), axis=1
            ),
            "con100": position.apply(
                lambda row: PortfolioAnalyzer._calculate_cons(row, 100), axis=1
            ),
            "HHI": hhi,
            "ENS": ens,
            "Normalized HHI": normalized_hhi,
            "Turnover(%)": turnover,
        }
        if group:
            stats_dict["con50"] = stats_dict["con50"].replace(0, np.nan).mean()
            stats_dict["con80"] = stats_dict["con80"].replace(0, np.nan).mean()
            stats_dict["con100"] = stats_dict["con100"].replace(0, np.nan).mean()
            stats_dict["HHI"] = stats_dict["HHI"].replace(0, np.nan).mean()
            stats_dict["ENS"] = stats_dict["ENS"].mean()
            stats_dict["Normalized HHI"] = (
                stats_dict["Normalized HHI"].replace(0, np.nan).mean()
            )
            stats_dict["Turnover(%)"] = turnover.sum()
        return stats_dict

    @staticmethod
    def _calculate_kurtosis(pct_pnl):
        pct_pnl = pct_pnl.dropna()
        pnl_mean = pct_pnl.mean()

        m2 = ((pct_pnl - pnl_mean) ** 2).sum()
        m4 = ((pct_pnl - pnl_mean) ** 4).sum()

        n = len(pct_pnl)
        if n < 4:
            return None

        numerator = (n + 1) * n * (n - 1) * m4
        denominator = (n - 2) * (n - 3) * (m2**2)
        first_term = numerator / denominator

        second_term = (3 * ((n - 1) ** 2)) / ((n - 2) * (n - 3))

        return first_term - second_term

    @staticmethod
    def _calculate_skewness(pct_pnl):
        pct_pnl = pct_pnl.dropna()
        pnl_mean = pct_pnl.mean()
        n = len(pct_pnl)

        if n < 3:
            return None

        m3 = ((pct_pnl - pnl_mean) ** 3).sum() / n
        m2 = ((pct_pnl - pnl_mean) ** 2).sum() / n
        g1 = m3 / (m2**1.5)
        return np.sqrt(n * (n - 1)) / (n - 2) * g1

    @staticmethod
    def _calculatea_run_HHI(pct_pnl, sign):
        target = pct_pnl[(pct_pnl > 0 if sign else pct_pnl < 0)]

        tsum = target.sum()
        if tsum == 0:
            return None

        weight = target / tsum
        return (weight**2).sum()

    @staticmethod
    def _calculate_cons(row, percentage):
        if row.replace(0, np.nan).count() == 0:
            return 0

        sorted_row = row.sort_values(ascending=False)

        cumulative_sum = sorted_row.cumsum()
        total_sum = sorted_row.sum()

        if total_sum == 0:
            return None

        assets_count = (cumulative_sum / total_sum * 100 >= percentage).argmax() + 1

        return assets_count if assets_count > 0 else len(row)

    @staticmethod
    def _calculate_HHI(row):
        weight = row / 1e8
        return (weight**2).sum(axis=1)

    @staticmethod
    def _norm_calculate_HHI(row):
        weight = row.replace(0, np.nan) / 1e8
        return (weight**2).mean(axis=1)

    @staticmethod
    def _calculate_turnover(position):
        return position.diff().abs().sum(axis=1) / 1e6
