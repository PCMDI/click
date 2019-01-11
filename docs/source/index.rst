.. Click Plots documentation master file, created by
   sphinx-quickstart on Thu Jan 10 17:36:30 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Click Plots's documentation!
=======================================


Click Plots allows to rapdidly create clickable protrait Plots
Usage is:

```
usage: generate_modal.py [-h] [--parameters PARAMETERS]
                         [--diags OTHER_PARAMETERS [OTHER_PARAMETERS ...]]
                         [--results_dir RESULTS_DIR] [--data_path DATA_PATH]
                         [--files_glob_pattern FILES_GLOB_PATTERN]
                         [--json-preprocessor JSON_PREPROCESSOR]
                         [--title TITLE] [--bad BAD] [--normalize NORMALIZE]
                         [--targets_template TARGETS_TEMPLATE] [--flip]
                         [--names-update NAMES_UPDATE] [--modal MODAL]
                         [--merge MERGE] [--split SPLIT]
                         [--png_template PNG_TEMPLATE] [--png_size PNG_SIZE]
                         [--html_template HTML_TEMPLATE]
                         [--no_target NO_TARGET] [--no_data NO_DATA]
                         [--sector SECTOR] [--levels LEVELS] [--colors COLORS]
                         [--colormap COLORMAP] [--model MODEL]
                         [--season SEASON] [--variable VARIABLE]
                         [--reference REFERENCE] [--rip RIP]
                         [--statistic STATISTIC] [--region REGION]

optional arguments:
  -h, --help            show this help message and exit
  --parameters PARAMETERS, -p PARAMETERS
  --diags OTHER_PARAMETERS [OTHER_PARAMETERS ...], -d OTHER_PARAMETERS [OTHER_PARAMETERS ...]
                        Path to other user-defined parameter file. (default:
                        None)
  --results_dir RESULTS_DIR, --rd RESULTS_DIR
                        The name of the folder where all runs will be stored.
                        (default: None)

graphics:
  Graphics Related Controls

  --title TITLE         title for plot (default: None)
  --flip
  --names-update NAMES_UPDATE
                        a dictionary to update axes labels (default: {})
  --split SPLIT         number of columns after which we split the portrait
                        plot into two rows (default: 20)
  --levels LEVELS       levels to use for portrait plots (default: None)
  --colors COLORS       colors to use for portrait plots (default: None)
  --colormap COLORMAP   colormap to use for portrait plots (default: None)

input:
  Input Data Related Controls

  --data_path DATA_PATH
                        input data path (default: None)
  --files_glob_pattern FILES_GLOB_PATTERN
                        glob pattern to select correct files in input
                        directory (default: None)
  --json-preprocessor JSON_PREPROCESSOR
                        if sending json files use this script to preprocess
                        (default: None)
  --bad BAD             list of bad models (default: [])
  --normalize NORMALIZE
                        normalize results by statistic (default: False)
  --merge MERGE         merge json dimensions together (default: None)
  --sector SECTOR       name of extra variable to use as 'sector' (triangles)
                        in portrait plot (default: None)
  --model MODEL
  --season SEASON
  --variable VARIABLE
  --reference REFERENCE
  --rip RIP
  --statistic STATISTIC
  --region REGION

output:
  Output Related Controls

  --png_template PNG_TEMPLATE
                        template for portrait plot png file (default:
                        clickable_portrait.png)
  --png_size PNG_SIZE   png output size (default: 800x600)

web:
  Web pages related arguments (modal)

  --targets_template TARGETS_TEMPLATE
                        template to find targets destination (default: data/pl
                        ots/Panel6_%(mode)_%(season)_%(model)_%(rip).png)
  --modal MODAL         use a custom modal file (default: None)
  --html_template HTML_TEMPLATE
                        template for html output filename (default:
                        clickable_portrait.html)
  --no_target NO_TARGET
                        png file to use when target png is missing (default:
                        None)
  --no_data NO_DATA     png file to use when no data is available (default:
                        None)
```

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
