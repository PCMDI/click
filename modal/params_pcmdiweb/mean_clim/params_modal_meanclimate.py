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
# User options
#------------------------------------------------------------------------------
mip = "cmip5"
#mip = "cmip6"
exp = "historical"

if mip == "cmip5" and exp == "historical":
 json_ver = "v20190821"
 graphic_ver = "v20190828"
 td1_ver = "v20190821"
 td2_ver = "v20190821" 

if mip == "cmip6" and exp == "historical":
 json_ver = "v20190930"  #"v20190927" #v20190919"
 graphic_ver = "v20190930" #"v20190919"
 td1_ver = "v20191001"
 td2_ver = "v20191001"


watermark_on = True #False
flip = True  # draw plot in vertical (portrait). If False plot in horizontal (landscape)

debug = False
#debug = True
case_id = "{:v%Y%m%d}".format(datetime.datetime.now())
pmprdir = "/p/user_pub/pmp/pmp_results/pmp_v1.1.2/interactive_plot/portrait_plot/mean_clim"

#==============================================================================
# JSON FILES
#------------------------------------------------------------------------------
data_path = "/p/user_pub/pmp/pmp_results/pmp_v1.1.2/metrics_results/mean_climate/" + mip.upper() + "/" + exp + "/" + json_ver + "/"
files_glob_pattern = "*regrid2*.json"

#==============================================================================
# DATA
#------------------------------------------------------------------------------
statistic = "rms_xy" 
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

#==============================================================================
# PLOTS
#------------------------------------------------------------------------------
title = "Seasonal Errors (" + statistic + "): " + mip.upper() +" ("+exp.title()+"), "+region.title()

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
custom_logo_x = 0.15  # move pcmdi logo to left 
custom_logo_y = 0.95  # move pcmdi logo to top (further upward to avoid overlapping with x-axis label on top)
#custom_logo_width = 250

# Sort top to bottom in alphabetical order
reverse_sorted_yaxis = True

# time stamp
time_stamp = True

# triangle indicator
triangle_indicator = "/export_backup/lee1043/git/click_20190930/click/share/Seasons4.png"
triangle_indicator_x = 0.93
triangle_indicator_y = 0.89
triangle_indicator_width = 120

# Watermark
if watermark_on and mip == "cmip6":
    watermark = "PCMDI Metrics Package\n Preliminary Results"
    watermark_color = [0,0,0,20]
    watermark_size = 40 # 80

#==============================================================================
# Interactivity
#------------------------------------------------------------------------------
cell_tooltips_images_template = "../../../../../../graphics/mean_climate/" + mip + "/" + exp + "/clim/" + graphic_ver + "/%(variable)/%(variable).%(model)_%(season).png"
cell_modal_json_template = "../../../../../../metrics_results/mean_climate/" + mip.upper() + "/" + exp + "/" + json_ver + "/%(variable)/%(model).%(variable)." + mip.upper() + "." + exp + ".regrid2.2p5x2p5."+json_ver+".json"

no_target = "../missing.png"
no_data = "../nodata.png"

# tooltop for axis label
if flip:
    xlabels_tooltips_images_template = "../../../taylor_diagram/" + mip + "/" + exp + "/" + td1_ver + "/%(variable)_"+mip+"_"+exp+"_taylor_4panel_all_global.png"
else:
    ylabels_tooltips_images_template = "../../../taylor_diagram/" + mip + "/" + exp + "/" + td2_ver + "/%(variable)_"+mip+"_"+exp+"_taylor_4panel_all_global.png"

#toggle_image = True
toggle_image = ["bl_to_darkred", "viridis"]
