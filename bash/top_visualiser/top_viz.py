#!/home/james/Documents/analysis/python/.venv/bin/python

# modules
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import datetime

# read data
df = pd.read_csv('top_info.csv', sep=' ',header=None)
df.columns = ['cpu', 'mem', 'time', 'command']

# aggregate by command category and sort
df_grp = df.groupby(by='command').sum()
df_grp = df_grp.sort_values(by='mem', ascending=False)

# viz
plt.figure(figsize=(8, 5))
sns.set_style('whitegrid')
plot = sns.barplot(data=df_grp,
            x='command',
            y='mem',
            palette='Spectral')

plot.set_xticklabels(plot.get_xticklabels(), rotation=45, ha='right')
plt.ylabel('Memory Usage (%)')
plt.xlabel(None)
plt.tight_layout()

filePath = str(datetime.datetime.now())
filePath = str.replace(filePath, ':', '-')
filePath = f'plt_{filePath}.png'

plt.savefig(filePath)
