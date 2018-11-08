from .create_html import createModalTargets, write_modal_html
from .version import __git_tag_describe__, __git_sha1__, __version__
from .vcs_details import setup_portrait
import pkg_resources
click_egg_path = pkg_resources.resource_filename(pkg_resources.Requirement.parse("click_plots"), "share/click_plots")