''' Print the plots '''
import datetime
import sys
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <csv_file> <plot_title> <file_prefix")
    sys.exit(1)

csv_file = sys.argv[1]
plot_title = sys.argv[2]
file_prefix = sys.argv[3]

plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 200

df = pd.read_csv(csv_file, sep=',')
types = df['type'].unique()

counts_by_type = {}
hex_values = sorted(df['hex'].unique())
for t in types:
    df_type = df[df['type'] == t]
    counts_by_type[t] = df_type['hex'].value_counts().reindex(hex_values, fill_value=0)

counts_df = pd.DataFrame(counts_by_type, index=hex_values)

fig, ax = plt.subplots()
counts_df.plot(
    kind='bar',
    stacked=True,
    ax=ax
)

ax.set_title(plot_title)
ax.legend()
plt.figtext(0.5, 0.01, f"{datetime.datetime.now()} - {len(df['time'])} hexagrams", wrap=True, horizontalalignment='center', fontsize=12)
xticks = range(len(hex_values))
ax.set_xticks(xticks[::2])  # Mostra solo ogni seconda etichetta
ax.set_xticklabels(hex_values[::2])

print(f'Drawing plot {file_prefix}_bars.png')
plt.savefig(f'./{file_prefix}_bars.png')
plt.clf()

# Radar
hex_values = range(1, 65)
data = []
for t in types:
    df_type = df[df['type'] == t]
    counts = [df_type[df_type['hex'] == hex_value].shape[0] for hex_value in hex_values]
    data.append(counts)

angles = np.linspace(0, 2*np.pi, len(hex_values), endpoint=False)
ax = fig.add_subplot(111, polar=True)
for i, counts in enumerate(data):
    ax.plot(angles, counts, 'o-', linewidth=2, label=types[i])
    
ax.set_title(plot_title)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
ax.set_thetagrids(angles * 180/np.pi, hex_values)
plt.figtext(0.5, 0.01, f"{datetime.datetime.now()} - {len(df['time'])} hexagrams", wrap=True, horizontalalignment='center', fontsize=12)

print(f'Drawing plot {file_prefix}_radar.png')
plt.savefig(f'./{file_prefix}_radar.png')