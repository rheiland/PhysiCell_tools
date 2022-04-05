# montage -geometry +0+0 -tile 2x1 core8_baseline/snapshot00000072.svg core8_params3/snapshot00000071.svg  tmp.png
ymax=6000
#python plot_viral_load.py core8_baseline 12 $ymax
#python plot_viral_load.py core8_params3 12 $ymax
python plot_viral_load.py run11 12 $ymax
python plot_viral_load.py run12 12 $ymax
python plot_viral_load.py run13 12 $ymax
python plot_viral_load.py run14 12 $ymax
python plot_viral_load.py run15 12 $ymax
python plot_viral_load.py run16 12 $ymax
python plot_viral_load.py run17 12 $ymax
python plot_viral_load.py run18 12 $ymax
#montage -geometry +0+0 -tile 2x1 core8_baseline_viral_load.png core8_params3_viral_load.png tmp.png
#montage -geometry +0+0 -tile 4x2 core8_baseline_viral_load.png core8_params3_viral_load.png tmp.png
montage -geometry +0+0 -tile 4x2 run11_viral_load.png run12_viral_load.png run13_viral_load.png run14_viral_load.png run15_viral_load.png run16_viral_load.png run17_viral_load.png run18_viral_load.png  tmp.png
convert -resize 50% tmp.png viral_loads11_18.png 
echo "viral_loads11_18.png"
