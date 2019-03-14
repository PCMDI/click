import os
data_path = "data/modes"
statistic = 'std_model_pcs'
flip = True
results_dir = "crp"
title = 'Test'
targets_template = "data/plots/Panel6_%(mode)_%(season)_%(model)_%(realization).png"
merge = [["model", "realization"], ["mode", "season"]]
#normalize = 'median'
#season = ["JJA","SON"]
#realization = ["r1i1p1","r2i1p1"]
split = 4
#colormap = "viridis"
#png_size = "2000x1200"

def norm_func(data, args=None):
    return data/1000. 

normalize = norm_func