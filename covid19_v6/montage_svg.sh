#montage -geometry +0+0 -tile 4x1 run11/snapshot00000004.svg run11/snapshot00000008.svg run11/snapshot00000012.svg  run11/snapshot00000048.svg  tmp.png
montage -geometry +0+0 -tile 4x1 run15/snapshot00000004.svg run15/snapshot00000008.svg run15/snapshot00000012.svg  run15/snapshot00000048.svg  tmp.png
#convert -resize 50% tmp.png run11_svg.png
convert -resize 50% tmp.png run15_svg.png
echo "run15_svg.png"
