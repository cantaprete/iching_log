#!/bin/zsh

[ ! -d "./docs" ] && mkdir docs

python3 print_plots.py ../data/control-sample.csv random
python3 print_plots.py ../data/meaningful-sample.csv meaningful
python3 print_plots.py ../data/control-sample.csv random_subset $(wc -l ../data/meaningful-sample.csv | awk '{print $1;}')
python3 print_comparison_plots.py ../data/meaningful-sample.csv meaningful ../data/control-sample.csv random_subset $(wc -l ../data/meaningful-sample.csv | awk '{print $1;}')

montage docs/meaningful_bars.png docs/random_subset_bars.png -geometry +1+1 docs/comparison_bars.png
montage docs/meaningful_moving_no.png docs/random_subset_moving_no.png -geometry +1+1 docs/comparison_moving_no.png
montage docs/meaningful_moving.png docs/random_subset_moving.png -geometry +1+1 docs/comparison_moving.png
montage docs/meaningful_radar.png docs/random_subset_radar.png -geometry +1+1 docs/comparison_radar.png
montage docs/meaningful_pie.png docs/random_subset_pie.png -geometry +1+1 docs/comparison_pie.png
montage docs/meaningful_heatmap.png docs/random_subset_heatmap.png -geometry +1+1 docs/comparison_heatmap.png
