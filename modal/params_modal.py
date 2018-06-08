import os
data_path = "data/cmec_11022017"
exp = 'historical'
stat = 'rms_devam_xy' 
results_dir = os.path.expanduser("~/www/click")
title = 'Seasonal RMS: Deviations from annual mean (' + stat + ')'
files_glob_pattern = "*regrid2*.json"
bad = []
seasons = ['djf', 'son', 'jja', 'mam']
region = "global"
normalize = True
targets_template = "plots/cmip5/historical/%(stat)/%(variable)/%(variable).%(model)_%(season).png"