#!/bin/zsh

python3 print_plots.py ../data/control-sample.csv random
python3 print_comparison_plots.py ../data/control-sample.csv random
python3 print_plots.py ../data/meaningful-sample.csv meaningful
python3 print_comparison_plots.py ../data/meaningful-sample.csv meaningful
python3 print_plots.py ../data/control-sample.csv random_subset $(wc -l ../data/meaningful-sample.csv | awk '{print $1;}')
python3 print_comparison_plots.py ../data/control-sample.csv random_subset $(wc -l ../data/meaningful-sample.csv | awk '{print $1;}')

montage meaningful_bars.png random_subset_bars.png -geometry +1+1 comparison_bars.png
montage meaningful_moving_no.png random_subset_moving_no.png -geometry +1+1 comparison_moving_no.montage meaningful_moving.png random_subset_moving.png -geometry +1+1 comparison_moving.png
montage meaningful_radar.png random_subset_radar.png -geometry +1+1 comparison_radar.png
montage meaningful_pie.png random_subset_pie.png -geometry +1+1 comparison_pie.png
montage meaningful_heatmap.png random_subset_heatmap.png -geometry +1+1 comparison_heatmap.png
