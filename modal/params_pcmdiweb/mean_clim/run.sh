# conda env 
# - crunchy: pmp_nightly_2019617 or pmp_nightly_20190617
# - grim: pmp_nightly_20190628


#generate_modal.py -p params_modal_meanclimate.py --colormap='viridis' --png_template='clickable_portrait_cb.png'

#generate_modal.py -p params_modal_meanclimate.py --colormap='viridis'
#generate_modal.py -p params_modal_meanclimate.py --colormap='bl_to_darkred'

#generate_modal.py -p params_modal_meanclimate.py --colormap='viridis' --ylabels_tooltips_html_template="" --ylabels_modal_images_template=""
#generate_modal.py -p params_modal_meanclimate.py --colormap='bl_to_darkred' --ylabels_tooltips_html_template="" --ylabels_modal_images_template=""

generate_modal.py -p params_modal_meanclimate.py --colormap='viridis' --ylabels_tooltips_html_template=None --ylabels_modal_images_template=None
generate_modal.py -p params_modal_meanclimate.py --colormap='bl_to_darkred' --ylabels_tooltips_html_template=None --ylabels_modal_images_template=None


## on crunchy
#cd /p/user_pub/pmp/pmp_results/pmp_v1.1.2
#python ~/git/click/flask/flask_server.py 

# check on browser (chrome recommanded): 
# http://crunchy.llnl.gov:5000/interactive_plot/portrait_plot//mean_clim/cmip5/historical/v20190827/clickable_portrait.html
