#!/bin/zsh

python3 print_plots.py ../data/control-sample.csv random
python3 print_plots.py ../data/meaningful-sample.csv meaningful
python3 print_plots.py ../data/control-sample.csv random_subset $(wc -l ../data/meaningful-sample.csv | awk '{print $1;}')

magick montage meaningful_bars.png random_subset_bars.png -geometry +1+1 comparison_bars.png
magick montage meaningful_moving_no.png random_subset_moving_no.png -geometry +1+1 comparison_moving_no.png
magick montage meaningful_moving.png random_subset_moving.png -geometry +1+1 comparison_moving.png
magick montage meaningful_radar.png random_subset_radar.png -geometry +1+1 comparison_radar.png
magick montage meaningful_pie.png random_subset_pie.png -geometry +1+1 comparison_pie.png
