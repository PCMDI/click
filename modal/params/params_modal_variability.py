import os
# JSON FILES
data_path = "/work/gleckler1/processed_data/metrics_package/metrics_results/cmip5clims_metrics_package-historical/cmec_11022017"
exp = 'historical'
stat = 'rms_xy' 
#results_dir = os.path.expanduser(".")
results_dir = './'
title = 'Seasonal Errors (' + stat + ')'
files_glob_pattern = "*regrid2*.json"
bad = []
seasons = ['djf', 'son', 'jja', 'mam']
region = "global"
normalize = False 
### PLOTS
targets_template = "/work/gleckler1/www/pptest/plots/cmip5/%(exp)/clim/%(variable)/%(variable).%(model)_%(season).png"
# SAMPLE: /work/gleckler1/www/pptest/plots/cmip5/historical/clim/rlut/rlut.IPSL-CM5A-MR_son.png
#targets_template = "plots/cmip5/historical/%(stat)/%(variable)/%(variable).%(model)_%(season).png"
