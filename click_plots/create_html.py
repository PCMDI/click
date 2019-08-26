import os
import shutil
import vcs
import pkg_resources
import warnings
import genutil

click_egg = pkg_resources.resource_filename(
    pkg_resources.Requirement.parse("click_plots"), "share/click_plots")


def write_modal_html(html_file, map_element, share_pth, pathout, modal=None, title="Clickable Portrait Plots", toggle_image=None, png_template=genutil.StringConstructor("clickable_portraits%(colormap).png")):
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
        if toggle_image is not None:
            f.write(
                "<script type='text/javascript' src='%s/toggle_image.js'></script>" % share_pth)
        else:
            f.write(
                "<script type='text/javascript' src='%s/mapper.js'></script>" % share_pth)
        f.write(
            "<script type='text/javascript' src='%s/cvi_tip_lib.js'></script>" % share_pth)
        f.write(
            '<link rel="stylesheet" type="text/css" href="%s/tooltip.css" />' % share_pth)
        f.write("</head><body>")
        f.write("<h1>{}</h1>".format(title))

        # toggle image button
        if toggle_image is not None:
            f.write('<button id="default">Default</button>')
            for name in toggle_image:
                f.write('<button id="{0}">{0}</button>'.format(name))
            f.write("<br>")

        f.write(map_element)
        # f.write("$('area').hover(function(){$(this).css('border','5px');},function(){$(this).css('border','0px');});")
        f.write("</body></html>")

    if toggle_image is not None:
        png_template.colormap = ""
        with open(os.path.join(full_share_path, "toggle_image.js"), "w") as f:
            f.write('$(document).ready(function(){\n')
            f.write('  $("#default").click(function(){\n')
            print("SOURCE:", png_template())
            f.write("      $('#clickable_portrait').attr('src', '{}');\n".format(png_template()))
            f.write("  });\n")
            for name in toggle_image:
                png_template.colormap = "_" + name
                print("SOURCES:", png_template())
                f.write('  $("#{}").click(function(){{\n'.format(name))
                f.write("      $('#clickable_portrait').attr('src', '{}');\n".format(png_template()))
                f.write("  });\n")
            f.write("});")
