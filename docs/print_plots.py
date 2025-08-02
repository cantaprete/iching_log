import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# plt.rcParams['font.family'] = 'Unifont'
plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 200

rand_log = pd.read_csv('./data/control-sample.csv', sep=',')
# rand_log.set_index('time', inplace=True)
types = rand_log['type'].unique()

fig, ax = plt.subplots()
for type in types:
    df_type = rand_log[rand_log['type'] == type]
    counts = df_type['hex'].value_counts().sort_index()
    ax.plot(counts.index, counts.values, label=type, marker='o')

# ax.set_xlabel('hexagrams')
# ax.set_ylabel('quantity')
ax.set_title('Number of hexagrams by type (control sample)')
ax.legend()
plt.figtext(0.5, 0.01, f"{datetime.datetime.now()} - {len(rand_log['time'])} hexagrams", wrap=True, horizontalalignment='center', fontsize=12)
plt.savefig('./docs/rand_rect.png')
plt.clf()

hex_values = range(1, 65)
data = []
for type in types:
    df_type = rand_log[rand_log['type'] == type]
    counts = [df_type[df_type['hex'] == hex_value].shape[0] for hex_value in hex_values]
    data.append(counts)

angles = np.linspace(0, 2*np.pi, len(hex_values), endpoint=False)
ax = fig.add_subplot(111, polar=True)
for i, counts in enumerate(data):
    ax.plot(angles, counts, 'o-', linewidth=2, label=types[i])
    
ax.set_thetagrids(angles * 180/np.pi, hex_values)
ax.set_title('Number of hexagrams by type (control sample)')
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
plt.figtext(0.5, 0.01, f"{datetime.datetime.now()} - {len(rand_log['time'])} hexagrams", wrap=True, horizontalalignment='center', fontsize=12)
plt.savefig('./docs/rand_radar.png')
plt.clf()


sig_log = pd.read_csv('./data/meaningful-sample.csv', sep=',')
# sig_log.set_index('time', inplace=True)
types = sig_log['type'].unique()

fig, ax = plt.subplots()
for type in types:
    df_type = sig_log[sig_log['type'] == type]
    counts = df_type['hex'].value_counts().sort_index()
    ax.plot(counts.index, counts.values, label=type, marker='o')

# ax.set_xlabel('hexagrams')
# ax.set_ylabel('quantity')
ax.set_title('Number of hexagrams by type (meaningful sample)')
ax.legend()
plt.figtext(0.5, 0.01, f"{datetime.datetime.now()} - {len(sig_log['time'])} hexagrams", wrap=True, horizontalalignment='center', fontsize=12)
plt.savefig('./docs/sig_rect.png')
plt.clf()

hex_values = range(1, 65)
data = []
for type in types:
    df_type = sig_log[sig_log['type'] == type]
    counts = [df_type[df_type['hex'] == hex_value].shape[0] for hex_value in hex_values]
    data.append(counts)

angles = np.linspace(0, 2*np.pi, len(hex_values), endpoint=False)
ax = fig.add_subplot(111, polar=True)
for i, counts in enumerate(data):
    ax.plot(angles, counts, 'o-', linewidth=2, label=types[i])

ax.set_thetagrids(angles * 180/np.pi, hex_values)
ax.set_title('Number of hexagrams by type (meaningful sample)')
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
plt.figtext(0.5, 0.01, f"{datetime.datetime.now()} - {len(sig_log['time'])} hexagrams", wrap=True, horizontalalignment='center', fontsize=12)
plt.savefig('./docs/sig_radar.png')
