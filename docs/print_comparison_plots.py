''' Print comparison plots with unified scales '''
import datetime
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if len(sys.argv) < 5:
    print(f'Usage: {sys.argv[0]} <csv_file_a> <prefix_a> <csv_file_b> <prefix_b> [length + 1]')
    sys.exit(1)

csv_file_a = sys.argv[1]
prefix_a   = sys.argv[2]
csv_file_b = sys.argv[3]
prefix_b   = sys.argv[4]
records = -1
if len(sys.argv) > 5:
    records = int(sys.argv[5]) - 1

plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 200

df_a = pd.read_csv(csv_file_a, sep=',')
df_b = pd.read_csv(csv_file_b, sep=',')
if records > 0:
    df_a = df_a.head(records)
    df_b = df_b.head(records)

iching = {
    1:  0b111111,  2:  0b000000,  3:  0b010001,  4:  0b100010,
    5:  0b010111,  6:  0b111010,  7:  0b000010,  8:  0b010000,
    9:  0b110111, 10:  0b111011, 11:  0b000111, 12:  0b111000,
    13: 0b111101, 14:  0b101111, 15:  0b000100, 16:  0b001000,
    17: 0b011001, 18:  0b100110, 19:  0b000011, 20:  0b110000,
    21: 0b101001, 22:  0b100101, 23:  0b100000, 24:  0b000001,
    25: 0b111001, 26:  0b100111, 27:  0b100001, 28:  0b011110,
    29: 0b010010, 30:  0b101101, 31:  0b011100, 32:  0b001110,
    33: 0b111100, 34:  0b001111, 35:  0b101000, 36:  0b000101,
    37: 0b110101, 38:  0b101011, 39:  0b010100, 40:  0b001010,
    41: 0b100011, 42:  0b110001, 43:  0b011111, 44:  0b111110,
    45: 0b011000, 46:  0b000110, 47:  0b011010, 48:  0b010110,
    49: 0b011101, 50:  0b101110, 51:  0b001001, 52:  0b100100,
    53: 0b110100, 54:  0b001011, 55:  0b001101, 56:  0b101100,
    57: 0b110110, 58:  0b011011, 59:  0b110010, 60:  0b010011,
    61: 0b110011, 62:  0b001100, 63:  0b010101, 64:  0b101010,
}


def compute_bars_data(df):
    types = df['type'].unique()
    hex_values = sorted(df['hex'].unique())
    counts_by_type = {}
    for t in types:
        df_type = df[df['type'] == t]
        counts_by_type[t] = df_type['hex'].value_counts().reindex(hex_values, fill_value=0)
    counts_df = pd.DataFrame(counts_by_type, index=hex_values)
    return counts_df, hex_values


def compute_radar_data(df):
    types = df['type'].unique()
    hex_values = range(1, 65)
    data = []
    for t in types:
        df_type = df[df['type'] == t]
        counts = [df_type[df_type['hex'] == h].shape[0] for h in hex_values]
        data.append(counts)
    return data, types, hex_values


def compute_moving_data(df):
    df_filtered = df[df['type'] != 'static']
    pairs = []
    for _, row in df_filtered.iterrows():
        if row['type'] == 'primary':
            pairs.append({'primary': row['hex'], 'secondary': 0})
        elif row['type'] == 'secondary':
            pairs[-1]['secondary'] = row['hex']

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
    return bit_changes, no_of_changes


def compute_heatmap_data(df):
    df_filtered = df[df['type'] != 'static']
    pairs = []
    for _, row in df_filtered.iterrows():
        if row['type'] == 'primary':
            pairs.append({'primary': row['hex'], 'secondary': 0})
        elif row['type'] == 'secondary':
            pairs[-1]['secondary'] = row['hex']

    line_counts = np.zeros((64, 6), dtype=int)
    occurrences = np.zeros(64, dtype=int)
    for pair in pairs:
        primary_hex   = iching.get(pair['primary'])
        secondary_hex = iching.get(pair['secondary'])
        if not isinstance(secondary_hex, int):
            continue
        row_idx = pair['primary'] - 1
        occurrences[row_idx] += 1
        xor_result = primary_hex ^ secondary_hex
        for i in range(6):
            if xor_result & (1 << i):
                line_counts[row_idx, i] += 1

    with np.errstate(invalid='ignore'):
        normalised = np.where(
            occurrences[:, None] > 0,
            line_counts / occurrences[:, None],
            np.nan
        )
    return line_counts, normalised


def footer(df):
    return f'{datetime.datetime.now()} - {len(df["time"])} hexagrams'


# ── Bars ──────────────────────────────────────────────────────────────────────

counts_df_a, hex_a = compute_bars_data(df_a)
counts_df_b, hex_b = compute_bars_data(df_b)

# unified y scale: the stacked bar maximum is the row-sum maximum
ymax_bars = max(
    counts_df_a.sum(axis=1).max(),
    counts_df_b.sum(axis=1).max()
)

for df, counts_df, hex_values, prefix in [
    (df_a, counts_df_a, hex_a, prefix_a),
    (df_b, counts_df_b, hex_b, prefix_b),
]:
    fig, ax = plt.subplots()
    counts_df.plot(kind='bar', stacked=True, ax=ax)
    ax.set_ylim(0, ymax_bars * 1.05)
    ax.set_title(f'Number of hexagrams by type ({prefix.replace("_", " ")} samples)')
    ax.legend()
    xticks = range(len(hex_values))
    ax.set_xticks(list(xticks)[::2])
    ax.set_xticklabels(list(hex_values)[::2])
    plt.figtext(0.5, 0.01, footer(df), wrap=True, horizontalalignment='center', fontsize=12)
    print(f'Drawing comparison plot {prefix}_bars.png')
    plt.savefig(f'./docs/{prefix}_bars.png')
    plt.clf()

# ── Pie ───────────────────────────────────────────────────────────────────────
# No scale unification needed for pie charts.

for df, prefix in [(df_a, prefix_a), (df_b, prefix_b)]:
    type_counts = df['type'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90)
    ax.set_title(f'Distribution of Hexagram Types ({prefix.replace("_", " ")} samples)')
    plt.figtext(0.5, 0.01, footer(df), wrap=True, horizontalalignment='center', fontsize=12)
    print(f'Drawing comparison plot {prefix}_pie.png')
    plt.savefig(f'./docs/{prefix}_pie.png')
    plt.clf()

# ── Radar ─────────────────────────────────────────────────────────────────────

data_a, types_a, hex_vals_a = compute_radar_data(df_a)
data_b, types_b, hex_vals_b = compute_radar_data(df_b)

rmax = max(
    max(max(c) for c in data_a),
    max(max(c) for c in data_b)
)

angles = np.linspace(0, 2 * np.pi, 64, endpoint=False)

for df, data, types, prefix in [
    (df_a, data_a, types_a, prefix_a),
    (df_b, data_b, types_b, prefix_b),
]:
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    for i, counts in enumerate(data):
        ax.plot(angles, counts, 'o-', linewidth=2, label=types[i])
    ax.set_ylim(0, rmax * 1.05)
    ax.set_title(f'Number of hexagrams by type ({prefix.replace("_", " ")} samples)')
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.set_thetagrids(angles * 180 / np.pi, list(hex_vals_a))
    plt.figtext(0.5, 0.01, footer(df), wrap=True, horizontalalignment='center', fontsize=12)
    print(f'Drawing comparison plot {prefix}_radar.png')
    plt.savefig(f'./docs/{prefix}_radar.png')
    plt.clf()

# ── Moving lines ──────────────────────────────────────────────────────────────

bit_changes_a, no_of_changes_a = compute_moving_data(df_a)
bit_changes_b, no_of_changes_b = compute_moving_data(df_b)

total_lines_a = sum(bit_changes_a)
total_lines_b = sum(bit_changes_b)
total_no_a    = sum(no_of_changes_a)
total_no_b    = sum(no_of_changes_b)

ymax_moving    = max(bit_changes_a.max(),    bit_changes_b.max())
ymax_moving_no = max(no_of_changes_a.max(),  no_of_changes_b.max())

bit_labels = [f'Line {i+1}' for i in range(6)]

for df, bit_changes, no_of_changes, total_lines, total_no, prefix in [
    (df_a, bit_changes_a, no_of_changes_a, total_lines_a, total_no_a, prefix_a),
    (df_b, bit_changes_b, no_of_changes_b, total_lines_b, total_no_b, prefix_b),
]:
    # moving
    fig, ax = plt.subplots()
    bits = ax.bar(bit_labels, bit_changes)
    ax.set_ylim(0, ymax_moving * 1.15)
    for bit in bits:
        height = bit.get_height()
        percent = 100 * float(height) / float(total_lines)
        ax.text(bit.get_x() + bit.get_width() / 2., 1.0 * height,
                '%.2f %%' % percent, size='small', ha='center', va='bottom')
    ax.set_title(f'Moving lines ({prefix.replace("_", " ")} samples)')
    plt.figtext(0.5, 0.01, footer(df), wrap=True, horizontalalignment='center', fontsize=12)
    print(f'Drawing comparison plot {prefix}_moving.png')
    plt.savefig(f'./docs/{prefix}_moving.png')
    plt.clf()

    # moving_no
    fig, ax = plt.subplots()
    bits = ax.bar([1, 2, 3, 4, 5, 6], no_of_changes)
    ax.set_ylim(0, ymax_moving_no * 1.15)
    for bit in bits:
        height = bit.get_height()
        percent = 100 * float(height) / float(total_no)
        ax.text(bit.get_x() + bit.get_width() / 2., 1.0 * height,
                '%d (%.2f%%)' % (int(height), percent), size='small', ha='center', va='bottom')
    ax.set_title(f'Quantity of moving lines ({prefix.replace("_", " ")} samples)')
    plt.figtext(0.5, 0.01, footer(df), wrap=True, horizontalalignment='center', fontsize=12)
    print(f'Drawing comparison plot {prefix}_moving_no.png')
    plt.savefig(f'./docs/{prefix}_moving_no.png')
    plt.clf()

# ── Heatmap ───────────────────────────────────────────────────────────────────

line_counts_a, normalised_a = compute_heatmap_data(df_a)
line_counts_b, normalised_b = compute_heatmap_data(df_b)

# Unified colour scales across both datasets
raw_vmax  = max(line_counts_a.max(), line_counts_b.max())
norm_vmax = max(np.nanmax(normalised_a), np.nanmax(normalised_b))

hex_labels  = [str(i) for i in range(1, 65)]
line_labels = [str(i) for i in range(1, 7)]

for df, line_counts, normalised, prefix in [
    (df_a, line_counts_a, normalised_a, prefix_a),
    (df_b, line_counts_b, normalised_b, prefix_b),
]:
    fig, axes = plt.subplots(1, 2, figsize=(6, 10), dpi=200)
    fig.subplots_adjust(wspace=0.12)

    for ax, data, title, fmt, vmax in [
        (axes[0], line_counts.astype(float), 'Raw counts',                        '.0f',   raw_vmax),
        (axes[1], normalised,                'Normalised\n(avg per consultation)', '.2f', norm_vmax),
    ]:
        plot_data = np.where(np.isnan(data), 0, data)
        im = ax.imshow(plot_data, aspect='auto', cmap='YlOrRd',
                       interpolation='nearest', vmin=0, vmax=vmax)
        ax.set_title(title, fontsize=12, pad=8)
        ax.set_xticks(range(6))
        ax.set_xticklabels(line_labels, fontsize=8)
        ax.set_xlabel('Line', fontsize=9)
        ax.set_yticks(range(64))
        ax.set_yticklabels(hex_labels, fontsize=6)
        # ax.set_ylabel('Hexagram', fontsize=9)
        for r in range(64):
            for c in range(6):
                val = data[r, c]
                if np.isnan(val):
                    txt, colour = '—', 'grey'
                else:
                    txt    = format(val, fmt)
                    colour = 'white' if val > vmax * 0.6 else 'black'
                ax.text(c, r, txt, ha='center', va='center', fontsize=5, color=colour)
        # fig.colorbar(im, ax=ax, fraction=0.02, pad=0.02)

    fig.suptitle(
        f'Moving lines per hexagram ({prefix.replace("_", " ")} samples)',
        fontsize=13, y=1.002
    )
    plt.figtext(0.5, 0.05, footer(df),
                wrap=True, horizontalalignment='center', fontsize=9)
    print(f'Drawing comparison plot {prefix}_heatmap.png')
    plt.savefig(f'./docs/{prefix}_heatmap.png', bbox_inches='tight')
    plt.clf()