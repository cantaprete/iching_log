''' Print the plots '''
import datetime
import sys
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if len(sys.argv) < 3:
    print(f'Usage: {sys.argv[0]} <csv_file> <file_prefix> [length + 1]')
    sys.exit(1)

csv_file = sys.argv[1]
file_prefix = sys.argv[2]
records = -1
if len(sys.argv) > 3:
    records = int(sys.argv[3]) - 1

plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 200

df = pd.read_csv(csv_file, sep=',')
if records > 0:
    df = df.head(records)
types = df['type'].unique()

# Bars

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

ax.set_title(f'Number of hexagrams by type ({file_prefix.replace('_', ' ')} samples)')
ax.legend()
plt.figtext(0.5, 0.01, f'{datetime.datetime.now()} - {len(df['time'])} hexagrams', wrap=True, horizontalalignment='center', fontsize=12)
xticks = range(len(hex_values))
ax.set_xticks(xticks[::2])
ax.set_xticklabels(hex_values[::2])

print(f'Drawing plot {file_prefix}_bars.png')
plt.savefig(f'./docs/{file_prefix}_bars.png')
plt.clf()

# Pie

type_counts = df['type'].value_counts()

fig, ax = plt.subplots()
ax.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90)
ax.set_title(f'Distribution of Hexagram Types ({file_prefix.replace("_", " ")} samples)')
plt.figtext(0.5, 0.01, f'{datetime.datetime.now()} - {len(df["time"])} hexagrams', wrap=True, horizontalalignment='center', fontsize=12)

print(f'Drawing plot {file_prefix}_pie.png')
plt.savefig(f'./docs/{file_prefix}_pie.png')
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
    
ax.set_title(f'Number of hexagrams by type ({file_prefix.replace('_', ' ')} samples)')
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
ax.set_thetagrids(angles * 180/np.pi, hex_values)
plt.figtext(0.5, 0.01, f'{datetime.datetime.now()} - {len(df['time'])} hexagrams', wrap=True, horizontalalignment='center', fontsize=12)

print(f'Drawing plot {file_prefix}_radar.png')
plt.savefig(f'./docs/{file_prefix}_radar.png')
plt.clf()

# Moving lines analysis
iching = {
    1:  0b111111,
    2:  0b000000,
    3:  0b010001,
    4:  0b100010,
    5:  0b010111,
    6:  0b111010,
    7:  0b000010,
    8:  0b010000,
    9:  0b110111,
    10: 0b111011,
    11: 0b000111,
    12: 0b111000,
    13: 0b111101,
    14: 0b101111,
    15: 0b000100,
    16: 0b001000,
    17: 0b011001,
    18: 0b100110,
    19: 0b000011,
    20: 0b110000,
    21: 0b101001,
    22: 0b100101,
    23: 0b100000,
    24: 0b000001,
    25: 0b111001,
    26: 0b100111,
    27: 0b100001,
    28: 0b011110,
    29: 0b010010,
    30: 0b101101,
    31: 0b011100,
    32: 0b001110,
    33: 0b111100,
    34: 0b001111,
    35: 0b101000,
    36: 0b000101,
    37: 0b110101,
    38: 0b101011,
    39: 0b010100,
    40: 0b001010,
    41: 0b100011,
    42: 0b110001,
    43: 0b011111,
    44: 0b111110,
    45: 0b011000,
    46: 0b000110,
    47: 0b011010,
    48: 0b010110,
    49: 0b011101,
    50: 0b101110,
    51: 0b001001,
    52: 0b100100,
    53: 0b110100,
    54: 0b001011,
    55: 0b001101,
    56: 0b101100,
    57: 0b110110,
    58: 0b011011,
    59: 0b110010,
    60: 0b010011,
    61: 0b110011,
    62: 0b001100,
    63: 0b010101,
    64: 0b101010,
}
df_filtered = df[df['type'] != 'static']
pairs = []

for index, row in df_filtered.iterrows():
    hex_value = row['hex']
    type_value = row['type']
    
    if type_value == 'primary':
        pairs.append({'primary': hex_value, 'secondary': 0})
    elif type_value == 'secondary':
        pairs[-1]['secondary'] = hex_value

bit_changes = np.zeros(6, dtype=int)
no_of_changes = np.zeros(6, dtype=int)

for pair in pairs:
    primary_hex = iching.get(pair['primary'])
    secondary_hex = iching.get(pair['secondary'])
    changes = 0
    
    if isinstance(secondary_hex, int):
        xor_result = primary_hex ^ secondary_hex
    
    for i in range(6):
        if xor_result & (1 << i):
            bit_changes[i] += 1
            changes += 1
    no_of_changes[changes - 1] += 1

bit_labels = [f'Line {i+1}' for i in range(6)]
fig, ax = plt.subplots()
bits = ax.bar(bit_labels, bit_changes)

total_lines = sum(bit_changes)
total_no_of_changes = sum(no_of_changes)

for bit in bits:
    height = bit.get_height()
    percent = 100 * float(bit.get_height())/float(total_lines)
    ax.text(bit.get_x() + bit.get_width()/2., 1.0*height, '%.2f %%' % float(percent), size='small', ha='center', va='bottom')

ax.set_title(f'Moving lines ({file_prefix.replace('_', ' ')} samples)')
plt.figtext(0.5, 0.01, f'{datetime.datetime.now()} - {len(df['time'])} hexagrams', wrap=True, horizontalalignment='center', fontsize=12)

print(f'Drawing plot {file_prefix}_moving.png')
plt.savefig(f'./docs/{file_prefix}_moving.png')
plt.clf()

fig, ax = plt.subplots()
bits = ax.bar([1,2,3,4,5,6], no_of_changes)

for bit in bits:
    height = bit.get_height()
    percent = 100 * float(bit.get_height())/float(total_no_of_changes)
    ax.text(bit.get_x() + bit.get_width()/2., 1.0*height, '%d (%.2f%%)' % (int(height), float(percent)), size='small', ha='center', va='bottom')

ax.set_title(f'Quantity of moving lines ({file_prefix.replace('_', ' ')} samples)')
plt.figtext(0.5, 0.01, f'{datetime.datetime.now()} - {len(df['time'])} hexagrams', wrap=True, horizontalalignment='center', fontsize=12)

print(f'Drawing plot {file_prefix}_moving_no.png')
plt.savefig(f'./docs/{file_prefix}_moving_no.png')
plt.clf()

# Heatmap: moving lines per hexagram (raw counts + normalised per occurrence)

# Build (64, 6) matrices: raw counts and occurrence counts per primary hexagram
line_counts = np.zeros((64, 6), dtype=int)
occurrences = np.zeros(64, dtype=int)

for pair in pairs:
    primary_hex   = iching.get(pair['primary'])
    secondary_hex = iching.get(pair['secondary'])
    if not isinstance(secondary_hex, int):
        continue
    row_idx = pair['primary'] - 1          # 0-based index for hexagram 1..64
    occurrences[row_idx] += 1
    xor_result = primary_hex ^ secondary_hex
    for i in range(6):
        if xor_result & (1 << i):
            line_counts[row_idx, i] += 1

# Normalised: avg moving occurrences per consultation of that hexagram
with np.errstate(invalid='ignore'):
    normalised = np.where(
        occurrences[:, None] > 0,
        line_counts / occurrences[:, None],
        np.nan
    )

# Figure: 64 rows × 12 cols (6 raw + 6 normalised), with a separator column
fig, axes = plt.subplots(1, 2, figsize=(6, 10), dpi=200)
fig.subplots_adjust(wspace=0.12)

hex_labels  = [str(i) for i in range(1, 65)]
line_labels = [str(i) for i in range(1, 7)]

for ax, data, title, fmt in [
    (axes[0], line_counts.astype(float), 'Raw counts',   '.0f'),
    (axes[1], normalised,                'Normalised\n(avg per consultation)', '.2f'),
]:
    # Replace NaN with 0 only for colour mapping; keep NaN cells visually distinct
    plot_data = np.where(np.isnan(data), 0, data)
    im = ax.imshow(plot_data, aspect='auto', cmap='YlOrRd', interpolation='nearest')
    ax.set_title(title, fontsize=12)
    ax.set_xticks(range(6))
    ax.set_xticklabels(line_labels, fontsize=8)
    ax.set_xlabel('Line', fontsize=9)
    ax.set_yticks(range(64))
    ax.set_yticklabels(hex_labels, fontsize=6)
    # ax.set_ylabel('Hexagram', fontsize=9)
    # Annotate each cell
    vmax = np.nanmax(data) if np.nanmax(data) > 0 else 1
    for r in range(64):
        for c in range(6):
            val = data[r, c]
            if np.isnan(val):
                txt = '—'
                colour = 'grey'
            else:
                txt = format(val, fmt)
                colour = 'white' if val > vmax * 0.6 else 'black'
            ax.text(c, r, txt, ha='center', va='center', fontsize=5, color=colour)
    # fig.colorbar(im, ax=ax, fraction=0.02, pad=0.02)

fig.suptitle(f'Moving lines per hexagram ({file_prefix.replace("_", " ")} samples)')
plt.figtext(0.5, 0.05, f'{datetime.datetime.now()} - {len(df["time"])} hexagrams',
            wrap=True, horizontalalignment='center', fontsize=9)

print(f'Drawing plot {file_prefix}_heatmap.png')
plt.savefig(f'./docs/{file_prefix}_heatmap.png', bbox_inches='tight')
plt.clf()
