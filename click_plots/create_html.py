import os
import shutil
import vcs
import pkg_resources
import warnings

click_egg = pkg_resources.resource_filename(
    pkg_resources.Requirement.parse("click_plots"), "share/click_plots")


def write_modal_html(html_file, map_element, share_pth, pathout, modal=None, title="Clickable Portrait Plots", toggle_image=False):
    full_share_path = os.path.join(pathout, share_pth)
    if not os.path.exists(full_share_path):
        os.makedirs(full_share_path)
    for file in ["mapper.js", "cvi_tip_lib.js", "tooltip.css"]:
        shutil.copy2(os.path.join(vcs.vcs_egg_path, file), full_share_path)
    if modal is not None:
        if not os.path.exists(modal):
            warnings.warn(
                "Could not locate your modal file {}, falling back on default".format(modal))
            modal = os.path.join(click_egg, "js", "modal.js")
    else:
        modal = os.path.join(click_egg, "js", "modal.js")
    shutil.copy2(modal, full_share_path)

    with open(html_file, "w") as f:
        f.write("<html><head>")
        f.write('<script src="https://code.jquery.com/jquery-3.4.1.min.js" crossorigin="anonymous"></script>')
        f.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js" integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh" crossorigin="anonymous"></script>')
        f.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">')
        f.write('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js" integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ" crossorigin="anonymous"></script>')
        f.write(
            '<script type="text/javascript" src="%s/modal.js"></script>' % share_pth)
        f.write(
            "<script type='text/javascript' src='%s/mapper.js'></script>" % share_pth)
        f.write(
            "<script type='text/javascript' src='%s/cvi_tip_lib.js'></script>" % share_pth)
        f.write(
            '<link rel="stylesheet" type="text/css" href="%s/tooltip.css" />' % share_pth)
        f.write("</head><body>")
        f.write("<h1>{}</h1>".format(title))

        # toggle switch
        if toggle_image:
            f.write('<button id="Color1">Color1</button>')
            f.write('<button id="Color2">Color2</button><br>')

        f.write(map_element)
        # f.write("$('area').hover(function(){$(this).css('border','5px');},function(){$(this).css('border','0px');});")
        f.write("</body></head></html>")

    if toggle_image:
        with open(os.path.join(full_share_path, "toggle_image.js"), "w") as f:
            f.write('$(document).ready(function(){')
            f.write('  $("#Color1").click(function(){')
            f.write("      $('#clickable_portrait').attr('src', 'clickable_portrait.png'); });")
            f.write('  $("#Color2").click(function(){')
            f.write("      $('#clickable_portrait').attr('src', 'clickable_portrait.png');});});")
