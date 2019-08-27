# conda env 
# - crunchy: pmp_nightly_2019617
# - grim: pmp_nightly_20190628


generate_modal.py -p params_modal_meanclimate.py --colormap='bl_to_darkred'
generate_modal.py -p params_modal_meanclimate.py --colormap='viridis'


#cd /p/user_pub/pmp/pmp_results/pmp_v1.1.2
#python ~/git/click/flask/flask_server.py 

# check on browser (chrome recommanded): 
# http://crunchy.llnl.gov:5000/pcmdiweb/interactive_portrait/mean_clim/cmip5/historical/v20190824_vertical/clickable_portrait.html
# or
# http://grim.llnl.gov:5000/pcmdiweb/interactive_portrait/mean_clim/cmip5/historical/v20190824_vertical/clickable_portrait.html
