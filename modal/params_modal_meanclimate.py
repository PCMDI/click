import os
# JSON FILES
data_path = "/work/gleckler1/processed_data/metrics_package/metrics_results/cmip5clims_metrics_package-historical/cmec_11022017"
data_path = "data/peter"
exp = 'historical'
statistic = 'rms_xy' 
#results_dir = os.path.expanduser(".")
results_dir = './modal_html'
title = 'Seasonal Errors (' + statistic + ')'
files_glob_pattern = "*regrid2*.json"
bad = []
sectors = True
if sectors:
    season = ["djf", "jja", "son", "mam"]
    sector = 'season'
else:
    season = 'djf'
reference = "defaultReference"
region = "global"
rip = "r1i1p1"
# variable= ["rt","pr"]
# nomalize = {"statistic":"std_xy"}
normalize = "median"
# merge = [["model", "rip"]]
### PLOTS
targets_template = "/work/gleckler1/www/pptest/plots/cmip5/historical/clim/%(variable)/%(variable).%(model)_%(season).png"
pth = os.getcwd()
targets_template = os.path.join(pth,"data/plots/peter/%(variable).%(model)_%(season).png")
# SAMPLE: /work/gleckler1/www/pptest/plots/cmip5/historical/clim/rlut/rlut.IPSL-CM5A-MR_son.png
#targets_template = "plots/cmip5/historical/%(stat)/%(variable)/%(variable).%(model)_%(season).png"

levels = [-1.e20, -.5, -.4, -.3, -.2, -.1, 0, .1, .2, .3, .4, 1.e20]
colormap = "viridis"
