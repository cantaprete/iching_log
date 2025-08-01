import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# rand_log = pd.read_csv('rand.csv', sep=',')
# rand_log.set_index('time', inplace=True)
# types = rand_log['type'].unique()

# fig, ax = plt.subplots()
# for type in types:
#     df_type = rand_log[rand_log['type'] == type]
#     counts = df_type['hex'].value_counts().sort_index()
#     ax.plot(counts.index, counts.values, label=type, marker='o')

# ax.set_xlabel('Esagrammi')
# ax.set_ylabel('Occorrenze')
# ax.set_title('Occorrenze degli esagrammi per tipo (casuale)')
# ax.legend()
# plt.savefig('./docs/rand_rect.png')

# hex_values = range(1, 65)
# data = []
# for type in types:
#     df_type = rand_log[rand_log['type'] == type]
#     counts = [df_type[df_type['hex'] == hex_value].shape[0] for hex_value in hex_values]
#     data.append(counts)

# angles = np.linspace(0, 2*np.pi, len(hex_values), endpoint=False)
# fig = plt.figure(figsize=(6, 6))
# ax = fig.add_subplot(111, polar=True)
# for i, counts in enumerate(data):
#     ax.plot(angles, counts, 'o-', linewidth=2, label=types[i])

# ax.set_thetagrids(angles * 180/np.pi, hex_values)
# ax.set_title('Occorrenze degli esagrammi per tipo (casuale)')
# ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
# plt.savefig('./docs/rand_radar.png')


sig_log = pd.read_csv('sig.csv', sep=',')
sig_log.set_index('time', inplace=True)
types = sig_log['type'].unique()

fig, ax = plt.subplots()
for type in types:
    df_type = sig_log[sig_log['type'] == type]
    counts = df_type['hex'].value_counts().sort_index()
    ax.plot(counts.index, counts.values, label=type, marker='o')

ax.set_xlabel('Esagrammi')
ax.set_ylabel('Occorrenze')
ax.set_title('Occorrenze degli esagrammi per tipo (significativo)')
ax.legend()
plt.savefig('./docs/sig_rect.png')

hex_values = range(1, 65)
data = []
for type in types:
    df_type = sig_log[sig_log['type'] == type]
    counts = [df_type[df_type['hex'] == hex_value].shape[0] for hex_value in hex_values]
    data.append(counts)

angles = np.linspace(0, 2*np.pi, len(hex_values), endpoint=False)
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, polar=True)
for i, counts in enumerate(data):
    ax.plot(angles, counts, 'o-', linewidth=2, label=types[i])

ax.set_thetagrids(angles * 180/np.pi, hex_values)
ax.set_title('Occorrenze degli esagrammi per tipo (significativo)')
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
plt.savefig('./docs/sig_radar.png')
