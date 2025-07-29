from kea2.utils import Device
from kea2.keaUtils import precondition


def global_block_widgets(d: "Device"):
    """
    global block widgets.
    return the widgets you want to block globally
    only available in mode `u2 agent`
    """
    return []


# conditional block list
@precondition(lambda d: d(text="In the home page").exists)
def block_sth(d: "Device"):
    # Important: function shold starts with "block_"
    return [d(text="widgets to block"), d.xpath(".//node[@text='widget to block']")]
