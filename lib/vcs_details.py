import vcs
import os
import sys

def setup_portrait(P):
    SET = P.PLOT_SETTINGS
    # Viewport on the Canvas
    SET.x1 = .20  # .05
    SET.x2 = .90
    SET.y1 = .2
    SET.y2 = .8

    #va = .01
    # P.PLOT_SETTINGS.x1 = 0.05 #  .1
    # P.PLOT_SETTINGS.x2 = .85  #.85
    #P.PLOT_SETTINGS.y1 = .6 + va
    #P.PLOT_SETTINGS.y2 = .9 + va

    # P.PLOT_SETTINGS.xtic2.y1=P.PLOT_SETTINGS.y1
    # P.PLOT_SETTINGS.xtic2.y2=P.PLOT_SETTINGS.y2
    # P.PLOT_SETTINGS.ytic2.x1=P.PLOT_SETTINGS.x1
    # P.PLOT_SETTINGS.ytic2.x2=P.PLOT_SETTINGS.x2

    # Both X (horizontal) and y (VERTICAL) ticks
    # Text table
    SET.tictable = vcs.createtexttable()
    SET.tictable.color = "black"  # "grey"

    # X (bottom) ticks
    # Text Orientation
    SET.xticorientation = vcs.createtextorientation()
    SET.xticorientation.angle = -90  # -70
    SET.xticorientation.halign = "right"
    SET.xticorientation.height = 12
    # Y (vertical) ticks
    SET.yticorientation = vcs.createtextorientation()
    SET.yticorientation.angle = 0
    SET.yticorientation.halign = "right"
    SET.yticorientation.height = 12

    # Parameters
    SET.parameterorientation = vcs.createtextorientation()
    SET.parameterorientation.height = 60
    SET.parametertable = vcs.createtexttable()
    SET.parametertable.color = "blue"

    # We can turn off the "grid"
    SET.draw_mesh = "y"

    # Control color for missing
    SET.missing_color = "light grey"

    # Tics length
    #SET.xtic1.y1 = SET.y1
    #SET.xtic1.y2 = SET.y2
    #SET.ytic1.x1 = SET.x1
    #SET.ytic1.x2 = SET.x2

    # Logo can be a string or an image
    SET.logo = P.PLOT_SETTINGS.logo = os.path.join(
        sys.prefix, "share", "pmp", "graphics", "png", "160915_PCMDI_logo_348x300px.png")
    SET.logo.x = .93
    SET.logo.y = .95
    SET.logo.width = 85

    # Timestamp
    SET.time_stamp = vcs.createtext()
    SET.time_stamp.color = "blue"
    SET.time_stamp.y = [.9]
    SET.time_stamp.x = [.98]
    SET.time_stamp.halign = "right"
    # or we can turn it off
    SET.time_stamp = None

    SET.legend.x1 = .95
    SET.legend.x2 = .97

    # level to use
    SET.levels = [-.7, -.6, -.5, -.4, -.3, -.2, -.1,
                  0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1., 1.1, 1.2, 1.3, 1.4, 1.5]
    SET.levels = [-.5, -.4, -.3, -.2, -.1,
                  0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1., 1.1, 1.2, 1.3, 1.4, 1.5]
    SET.levels = [-1.e20, -.5, -.4, -.3, -.2, -.1,
                  0, .1, .2, .3, .4, .5, 1.e20]

    # Colormap
    #SET.colormap = "inferno"
    vcs.scriptrun(os.path.join(sys.prefix, "share", "pmp",
                             "graphics", "vcs", "portraits.scr"))
    SET.colormap = 'bl_rd_12'
    cols = vcs.getcolors(SET.levels, range(144, 156), split=1)
    SET.fillareacolors = cols
    SET.parametertable.expansion = 100

    # colors to use
    #SET.fillareacolors = vcs.getcolors(SET.levels)
