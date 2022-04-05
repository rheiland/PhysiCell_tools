# montage -geometry +0+0 -tile 2x1 core8_baseline/snapshot00000072.svg core8_params3/snapshot00000071.svg  tmp.png
ymax=250
ymax=500
python plot_immune_cells_fixY.py run11 12 $ymax
python plot_immune_cells_fixY.py run12 12 $ymax
python plot_immune_cells_fixY.py run13 12 $ymax
python plot_immune_cells_fixY.py run14 12 $ymax
python plot_immune_cells_fixY.py run15 12 $ymax
python plot_immune_cells_fixY.py run16 12 $ymax
python plot_immune_cells_fixY.py run17 12 $ymax
python plot_immune_cells_fixY.py run18 12 $ymax
montage -geometry +0+0 -tile 4x2 run11_immune.png run12_immune.png run13_immune.png run14_immune.png run15_immune.png run16_immune.png run17_immune.png run18_immune.png tmp.png
convert -resize 70% tmp.png runs11_18_immune.png
echo "runs11_18_immune.png"
