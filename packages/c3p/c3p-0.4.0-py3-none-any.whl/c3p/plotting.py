import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def plot_scatter(df, x, y, title="Scatterplot", results_dir=None):
    """
    Create a scatter plot with optional logarithmic x-axis.

    Args:
        df: DataFrame containing the data
        x: Name of x-axis column
        y: Name of y-axis column
        title: Plot title
        results_dir: Optional directory to save the plot
    """
    plt.clf()
    # check if x and y are in the dataframe
    if x not in df.columns or y not in df.columns:
        print(f"Columns {x} and {y} not found in DataFrame")
        return
    # drop na values
    df = df.dropna(subset=[x, y])
    if df.size == 0:
        return
    correlation = np.corrcoef(df[x], df[y])[0, 1]
    # print(f"Correlation between {x} and {y}: {correlation:.2f}")
    title = f"{title} (r = {correlation:.2f})"

    # Create scatter plot
    plt.scatter(df[x], df[y], s=5, alpha=0.5)

    # Draw horizontal line at mean y
    plt.axhline(df[y].mean(), color='red', linestyle='dashed', linewidth=1)

    # Fit trend line using transformed x values
    z = np.polyfit(df[x], df[y], 1)
    p = np.poly1d(z)

    # Generate x points for trend line
    plt.plot(df[x], p(df[x]), "r--", alpha=0.8)

    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.grid(True, alpha=0.3)

    if results_dir:
        plt.savefig(results_dir / f"scatterplot-{x}-{y}.png",
                    dpi=300,  # High resolution
                    bbox_inches='tight',  # Removes extra white spaces
                    pad_inches=0.1,  # Small padding around the figure
                    format='png',  # Format type
                    transparent=False,  # White background
                    facecolor='white',  # Figure face color
                    edgecolor='none',  # No edge color
                    )
    plt.close()
    return plt



from scipy import stats


def create_scatter_matrix(df: pd.DataFrame, compare='experiment_name', metric: str = 'f1', index='chemical_class') -> plt.Figure:
    # Pivot the data to get experiments as columns and classes as rows
    df = df.dropna(subset=[metric])
    pivot_df = df.pivot(index=index, columns=compare, values=metric)

    # Calculate number of experiments
    n_experiments = len(pivot_df.columns)

    # Create figure and axis grid
    fig, axes = plt.subplots(n_experiments, n_experiments, figsize=(15, 15))

    # Add padding between subplots
    plt.subplots_adjust(hspace=0.6, wspace=0.3)

    # Iterate through each pair of experiments
    for i, exp1 in enumerate(pivot_df.columns):
        for j, exp2 in enumerate(pivot_df.columns):
            ax = axes[i, j]
            exp1_vals = pivot_df[exp1].fillna(0)
            exp2_vals = pivot_df[exp2].fillna(0)

            if i > j:  # Lower triangle: scatter plots
                # Create scatter plot
                ax.scatter(exp2_vals, exp1_vals, alpha=0.5)

                # Calculate correlation
                corr, _ = stats.pearsonr(exp2_vals, exp1_vals)

                # Add correlation coefficient text above the plot
                # ax.set_title(f'r = {corr:.3f}', pad=8, fontweight='bold', fontsize=10)

                ax.text(0.5, 1.15, f'r = {corr:.3f}',
                        ha='center', va='bottom',
                        transform=ax.transAxes,
                        fontweight='bold', fontsize=10)

                # Add correlation coefficient text
                #ax.text(0.05, 0.95, f'r = {corr:.3f}',
                #        transform=ax.transAxes,
                #        verticalalignment='top')

                # Set limits from 0 to 1 for F1 scores
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)

                # Add diagonal line
                ax.plot([0, 1], [0, 1], 'k--', alpha=0.3)

            elif i == j:  # Diagonal: experiment names
                ax.text(0.5, 0.5, exp1,
                        ha='center', va='center',
                        transform=ax.transAxes,
                        rotation=45)
                ax.set_xticks([])
                ax.set_yticks([])

            else:  # Upper triangle: keep empty
                ax.set_visible(False)

            # Only show labels on outer edges
            if i == n_experiments - 1:
                ax.set_xlabel(exp2)
            if j == 0:
                ax.set_ylabel(exp1)

    plt.suptitle('Model Comparison Matrix', size=16, y=1.02)
    return fig

