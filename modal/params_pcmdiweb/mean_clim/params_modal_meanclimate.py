"""
This parameter file is for generating an interactive portrait plot, 
based on "click" (https://github.com/PCMDI/click), "pcmdi_metrics", and "cdat".
The "click" was developed by C. Doutriaux and this parameter file was improved
by J. Lee for PCMDI Simulation Summaries (https://pcmdi.llnl.gov/research/metrics).

Usage: generate_modal.py -p params_modal_meanclimate.py

23 Aug 2019, Jiwoo Lee
"""

import datetime
import os
import vcs

#==============================================================================
# User option
#------------------------------------------------------------------------------
mip = 'cmip5'
exp = 'historical'

watermark_on = False
flip = True  # draw plot in vertical (portrait)
#flip = False  # draw plot in horizontal (landscape)

debug = False
#debug = True
case_id = "{:v%Y%m%d}".format(datetime.datetime.now())
pmprdir = "/p/user_pub/pmp/pmp_results/pmp_v1.1.2/pcmdiweb/interactive_portrait/mean_clim"

#==============================================================================
# JSON FILES
#------------------------------------------------------------------------------
data_path = "/p/user_pub/pmp/pmp_results/pmp_v1.1.2/metrics_results/mean_climate/CMIP5/historical/v20190821"
files_glob_pattern = "*regrid2*.json"

#==============================================================================
# DATA
#------------------------------------------------------------------------------
statistic = 'rms_xy' 
sector = "season"
season = ["djf", "son", "jja", "mam"]
reference = "default"
region = "global"
rip = "r1i1p1"
variable = [
    "pr", "psl", "rltcre", "rlut", "rstcre", "rsut", "ta-200", "ta-850", "tas",
    "ua-200", "ua-850", "uas", "va-200", "va-850", "vas", "zg-500"]
normalize = "median"
# merge = [["model", "rip"], ["season","mode"]]
normalize_axis = "model"

#--- OUTPUT DIRECTORY
if debug:
    pmprdir = "."

results_dir = os.path.join(
    pmprdir, mip, exp, case_id)

if flip:
    results_dir += '_vertical'
else:
    results_dir += '_horizontal'

#==============================================================================
# PLOTS
#------------------------------------------------------------------------------
title = 'Seasonal Errors (' + statistic + '): ' + mip.upper() +' ('+exp.title()+'), '+region.title()

# Color map customization 
levels = [-1.e20, -.5, -.4, -.3, -.2, -.1, 0, .1, .2, .3, .4, .5, 1.e20]
colormap = "bl_to_darkred"
#colormap = "default"
colors = vcs.getcolors(levels, split=0, colors=range(16,240))

# Panel control
split = 600  # maximum number of columns in one panel

# Image size and template
if flip:
    png_size = "1400x1800"
    portrait_templates_json_file ="template_one_vertical.json"
else:
    png_size = "1600x1000"

# Logo
hide_cdat_logo = True

# Sort top to bottom in alphabetical order
reverse_sorted_yaxis = True

# Watermark
if watermark_on:
    watermark = "PCMDI Metrics Package\n Preliminary Results"
    watermark_color = [0,0,0,30]
    watermark_size = 80

#==============================================================================
# Interactivity
#------------------------------------------------------------------------------
cell_tooltips_images_template = "../../../../../../graphics/mean_climate/cmip5/historical/clim/v20171129/%(variable)/%(variable).%(model)_%(season).png"
#cell_tooltips_images_template = "../../../../../../graphics/mean_climate/cmip5/historical/clim/v20190716/%(variable)/%(variable).%(model)_%(season).png"
cell_modal_json_template = "../../../../../../metrics_results/mean_climate/CMIP5/historical/v20190821/%(variable)/%(model).%(variable).CMIP5.historical.regrid2.2p5x2p5.v20190821.json"

no_target = "missing.png"
no_data = "nodata.png"

# tooltop for axis label
if flip:
    xlabels_tooltips_images_template = "../taylor_diagram/v20190821/%(variable)_cmip5_historical_taylor_4panel_all_global.png"
else:
    ylabels_tooltips_images_template = "../taylor_diagram/v20190821/%(variable)_cmip5_historical_taylor_4panel_all_global.png"

#toggle_image = True
toggle_image = ['bl_to_darkred', 'viridis']
