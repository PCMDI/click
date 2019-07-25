from .create_html import write_modal_html  # noqa
from .version import __git_tag_describe__, __git_sha1__, __version__  # noqa
from .portrait_plots import ClickablePortrait  # noqa
import pkg_resources
click_egg_path = pkg_resources.resource_filename(pkg_resources.Requirement.parse("click_plots"), "share/click_plots")

