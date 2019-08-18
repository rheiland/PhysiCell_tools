
# rm -rf out_biorobots out_cancer_biorobots out_heterogeneity out_cancer_immune out_virus_macrophage
mkdir -p out_biorobots		
mkdir -p out_cancer_biorobots	
mkdir -p out_heterogeneity		
mkdir -p out_cancer_immune		
mkdir -p out_virus_macrophage
#mkdir -p out_template2D
#mkdir -p out_beta_testing		
#mkdir -p out_template3D

make reset
make biorobots-sample
make
python run_sample.py biorobots run_biorobots.txt
#
make reset
make cancer-biorobots-sample
make
python run_sample.py cancer_biorobots run_cancer_biorobots.txt
#
make reset
make heterogeneity-sample
make
python run_sample.py heterogeneity run_heterogeneity.txt
#
make reset
make cancer-immune-sample
make
python run_sample.py cancer_immune_3D run_cancer_immune.txt
#
make reset
make virus-macrophage-sample
make
python run_sample.py virus-sample run_virus.txt