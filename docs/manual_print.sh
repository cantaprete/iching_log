#!/bin/zsh

python3 print_plots.py ../data/control-sample.csv random
python3 print_plots.py ../data/meaningful-sample.csv meaningful
python3 print_plots.py ../data/control-sample.csv random_subset $(wc -l ../data/meaningful-sample.csv | awk '{print $1;}')