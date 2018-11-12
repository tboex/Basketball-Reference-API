import seaborn as sns
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd


def graph_player_stat(player, stat):
    stats = pd.DataFrame(player.stats, columns=player.stat_headers)
    if not stat in ['Season', 'Tm', 'Lg', 'Pos']:
        stats[stat] = pd.to_numeric(stats[stat])

    sns.set(style="whitegrid")
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(6, 15))

    sns.set_color_codes("pastel")
    sns.barplot(x=stat, y="Season", data=stats,
                label=stat, color="b")

    # Add a legend and informative axis label
    ax.legend(ncol=2, loc="lower right", frameon=True)
    ax.set(xlim=(0, stats[stat].max()), ylabel="",
        xlabel=stat)
    sns.despine(left=True, bottom=True)
    plt.show()


def graph_player_stat_comparison(player, stat1, stat2):
    stats = pd.DataFrame(player.stats, columns=player.stat_headers)

    if not stat1 in ['Season', 'Tm', 'Lg', 'Pos']:
        stats[stat1] = pd.to_numeric(stats[stat1])
    
    if not stat2 in ['Season', 'Tm', 'Lg', 'Pos']:
        stats[stat2] = pd.to_numeric(stats[stat2])

    sns.set(style="whitegrid")
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(6, 15))

    sns.set_color_codes("pastel")
    sns.barplot(x=stat2, y="Season", data=stats,
                label=stat2, color="b")

    sns.set_color_codes("muted")
    sns.barplot(x=stat1, y="Season", data=stats,
                label=stat1, color="r")

    maxVal = max(stats[stat1].max(), stats[stat2].max())
    ax.legend(ncol=2, loc="lower right", frameon=True)
    ax.set(xlim=(0, maxVal), ylabel="",
        xlabel=stat1)
    sns.despine(left=True, bottom=True)
    plt.show()