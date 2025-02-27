import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import seaborn as sns
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path

from src.infrastructure.logging import get_logger

logger = get_logger(__name__)


class TradingVisualization:
    """
    Utility class for creating trading-related visualizations.
    Centralizes visualization logic to maintain consistent styling and functionality.
    """
    
    def __init__(self, style: str = 'darkgrid', context: str = 'notebook', 
                 palette: str = 'deep', font_scale: float = 1.2):
        """
        Initialize visualization settings.
        
        Args:
            style: Seaborn style ('darkgrid', 'whitegrid', 'dark', 'white', 'ticks')
            context: Plot context ('notebook', 'paper', 'talk', 'poster')
            palette: Color palette
            font_scale: Font size scaling
        """
        self.set_style(style, context, palette, font_scale)
    
    def set_style(self, style: str = 'darkgrid', context: str = 'notebook', 
                  palette: str = 'deep', font_scale: float = 1.2):
        """
        Set the visual style for plots.
        
        Args:
            style: Seaborn style
            context: Plot context
            palette: Color palette
            font_scale: Font size scaling
        """
        sns.set_style(style)
        sns.set_context(context, font_scale=font_scale)
        sns.set_palette(palette)
        
        # Set default figure size for all plots
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['figure.dpi'] = 100
    
    def plot_price_history(self, data: pd.DataFrame, ticker: str = None, 
                          date_col: str = 'date', price_cols: List[str] = None,
                          title: str = None, figsize: Tuple[int, int] = None,
                          save_path: Optional[Union[str, Path]] = None) -> plt.Figure:
        """
        Plot price history for one or more assets.
        
        Args:
            data: DataFrame with date and price data
            ticker: Ticker symbol (for title if not provided)
            date_col: Name of the date column
            price_cols: List of column names to plot (default: ['close'])
            title: Custom title (default: f"{ticker} Price History")
            figsize: Custom figure size (width, height)
            save_path: Path to save the figure (optional)
            
        Returns:
            matplotlib.figure.Figure: The generated figure
        """
        # Default values
        if price_cols is None:
            price_cols = ['close']
        
        if figsize:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig, ax = plt.subplots()
        
        # Ensure date is datetime type
        if not pd.api.types.is_datetime64_any_dtype(data[date_col]):
            data = data.copy()
            data[date_col] = pd.to_datetime(data[date_col])
        
        # Plot each price column
        for col in price_cols:
            if col in data.columns:
                ax.plot(data[date_col], data[col], label=col.capitalize())
            else:
                logger.warning(f"Column '{col}' not found in data")
        
        # Set title
        if title:
            ax.set_title(title, fontsize=14)
        elif ticker:
            ax.set_title(f"{ticker} Price History", fontsize=14)
        else:
            ax.set_title("Price History", fontsize=14)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig.autofmt_xdate()
        
        # Add labels and grid
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        
        # Save figure if path provided
        if save_path:
            try:
                fig.savefig(save_path, bbox_inches='tight', dpi=300)
                logger.info(f"Figure saved to {save_path}")
            except Exception as e:
                logger.error(f"Failed to save figure: {str(e)}")
        
        return fig
    
    def plot_returns(self, data: pd.DataFrame, benchmark_data: pd.DataFrame = None,
                    date_col: str = 'date', returns_col: str = 'returns', 
                    benchmark_col: str = 'returns', cumulative: bool = True,
                    title: str = None, figsize: Tuple[int, int] = None,
                    save_path: Optional[Union[str, Path]] = None) -> plt.Figure:
        """
        Plot strategy returns, optionally compared to a benchmark.
        
        Args:
            data: DataFrame with strategy returns
            benchmark_data: DataFrame with benchmark returns (optional)
            date_col: Name of the date column
            returns_col: Name of the returns column in data
            benchmark_col: Name of the returns column in benchmark_data
            cumulative: Whether to plot cumulative returns
            title: Custom title
            figsize: Custom figure size
            save_path: Path to save the figure (optional)
            
        Returns:
            matplotlib.figure.Figure: The generated figure
        """
        if figsize:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig, ax = plt.subplots()
        
        # Ensure date is datetime type
        if not pd.api.types.is_datetime64_any_dtype(data[date_col]):
            data = data.copy()
            data[date_col] = pd.to_datetime(data[date_col])
        
        # Calculate cumulative returns if requested
        if cumulative:
            strategy_returns = (1 + data[returns_col]).cumprod() - 1
            if benchmark_data is not None:
                if not pd.api.types.is_datetime64_any_dtype(benchmark_data[date_col]):
                    benchmark_data = benchmark_data.copy()
                    benchmark_data[date_col] = pd.to_datetime(benchmark_data[date_col])
                benchmark_returns = (1 + benchmark_data[benchmark_col]).cumprod() - 1
        else:
            strategy_returns = data[returns_col]
            if benchmark_data is not None:
                benchmark_returns = benchmark_data[benchmark_col]
        
        # Plot strategy returns
        ax.plot(data[date_col], strategy_returns, label='Strategy', linewidth=2)
        
        # Plot benchmark if provided
        if benchmark_data is not None:
            ax.plot(benchmark_data[date_col], benchmark_returns, label='Benchmark', 
                   linewidth=2, linestyle='--')
        
        # Set title
        if title:
            ax.set_title(title, fontsize=14)
        else:
            if cumulative:
                ax.set_title('Cumulative Returns', fontsize=14)
            else:
                ax.set_title('Returns', fontsize=14)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig.autofmt_xdate()
        
        # Format y-axis as percentage
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{100 * y:.2f}%'))
        
        # Add labels and grid
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Returns', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        
        # Save figure if path provided
        if save_path:
            try:
                fig.savefig(save_path, bbox_inches='tight', dpi=300)
                logger.info(f"Figure saved to {save_path}")
            except Exception as e:
                logger.error(f"Failed to save figure: {str(e)}")
        
        return fig
    
    def plot_drawdowns(self, data: pd.DataFrame, date_col: str = 'date', 
                      value_col: str = 'equity', title: str = None,
                      figsize: Tuple[int, int] = None,
                      save_path: Optional[Union[str, Path]] = None) -> plt.Figure:
        """
        Plot drawdowns for portfolio equity.
        
        Args:
            data: DataFrame with equity data
            date_col: Name of the date column
            value_col: Name of the equity column
            title: Custom title
            figsize: Custom figure size
            save_path: Path to save the figure (optional)
            
        Returns:
            matplotlib.figure.Figure: The generated figure
        """
        if figsize:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig, ax = plt.subplots()
        
        # Ensure date is datetime type
        if not pd.api.types.is_datetime64_any_dtype(data[date_col]):
            data = data.copy()
            data[date_col] = pd.to_datetime(data[date_col])
        
        # Calculate drawdowns
        data_copy = data.copy()
        data_copy['peak'] = data_copy[value_col].cummax()
        data_copy['drawdown'] = (data_copy[value_col] / data_copy['peak']) - 1
        
        # Plot drawdowns
        ax.fill_between(data_copy[date_col], data_copy['drawdown'], 0, color='red', alpha=0.3)
        ax.plot(data_copy[date_col], data_copy['drawdown'], color='red', linewidth=1)
        
        # Set title
        if title:
            ax.set_title(title, fontsize=14)
        else:
            ax.set_title('Drawdowns', fontsize=14)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig.autofmt_xdate()
        
        # Format y-axis as percentage
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{100 * y:.2f}%'))
        
        # Add labels and grid
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Drawdown', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save figure if path provided
        if save_path:
            try:
                fig.savefig(save_path, bbox_inches='tight', dpi=300)
                logger.info(f"Figure saved to {save_path}")
            except Exception as e:
                logger.error(f"Failed to save figure: {str(e)}")
        
        return fig
    
    def plot_trade_distribution(self, trades: pd.DataFrame, 
                               profit_col: str = 'profit_pct',
                               trade_type_col: str = 'trade_type',
                               title: str = None, figsize: Tuple[int, int] = None,
                               save_path: Optional[Union[str, Path]] = None) -> plt.Figure:
        """
        Plot distribution of trade profits.
        
        Args:
            trades: DataFrame with trade data
            profit_col: Name of the profit column
            trade_type_col: Name of the column indicating long/short (optional)
            title: Custom title
            figsize: Custom figure size
            save_path: Path to save the figure (optional)
            
        Returns:
            matplotlib.figure.Figure: The generated figure
        """
        if figsize:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig, ax = plt.subplots()
        
        # Determine if we should split by trade type
        has_trade_types = (trade_type_col in trades.columns and 
                          trades[trade_type_col].nunique() > 1)
        
        if has_trade_types:
            # Plot separate distributions for long and short trades
            for trade_type, group in trades.groupby(trade_type_col):
                sns.histplot(group[profit_col], label=trade_type, alpha=0.5, ax=ax)
        else:
            # Plot all trades together
            sns.histplot(trades[profit_col], ax=ax)
        
        # Draw vertical line at zero
        ax.axvline(x=0, color='red', linestyle='--')
        
        # Set title
        if title:
            ax.set_title(title, fontsize=14)
        else:
            ax.set_title('Trade Profit Distribution', fontsize=14)
        
        # Format x-axis as percentage
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{100 * x:.1f}%'))
        
        # Add labels and grid
        ax.set_xlabel('Profit/Loss (%)', fontsize=12)
        ax.set_ylabel('Number of Trades', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        if has_trade_types:
            ax.legend()
        
        plt.tight_layout()
        
        # Save figure if path provided
        if save_path:
            try:
                fig.savefig(save_path, bbox_inches='tight', dpi=300)
                logger.info(f"Figure saved to {save_path}")
            except Exception as e:
                logger.error(f"Failed to save figure: {str(e)}")
        
        return fig
    
    def plot_performance_metrics(self, metrics: Dict[str, float], title: str = None,
                                figsize: Tuple[int, int] = None,
                                save_path: Optional[Union[str, Path]] = None) -> plt.Figure:
        """
        Plot key performance metrics as a horizontal bar chart.
        
        Args:
            metrics: Dictionary of metric names and values
            title: Custom title
            figsize: Custom figure size
            save_path: Path to save the figure (optional)
            
        Returns:
            matplotlib.figure.Figure: The generated figure
        """
        # Filter metrics to include only numeric values
        metrics = {k: v for k, v in metrics.items() if isinstance(v, (int, float))}
        
        if figsize:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig, ax = plt.subplots(figsize=(10, len(metrics) * 0.5 + 2))
        
        # Sort metrics by name
        sorted_metrics = dict(sorted(metrics.items()))
        
        # Create horizontal bar chart
        metrics_names = list(sorted_metrics.keys())
        metrics_values = list(sorted_metrics.values())
        
        # Determine
