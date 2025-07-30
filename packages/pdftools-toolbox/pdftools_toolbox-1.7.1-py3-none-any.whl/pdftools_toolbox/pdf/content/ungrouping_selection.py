from ctypes import *
from enum import IntEnum

class UngroupingSelection(IntEnum):
    """
    Used to control the behavior of content extraction.
    Groups in the content can either be extracted as :class:`pdftools_toolbox.pdf.content.group_element.GroupElement` s,
    or their content can be unpacked, in which case groups' content elements are extracted as if not belonging to a group.



    Attributes:
        NONE (int):
            Groups are extracted as :class:`pdftools_toolbox.pdf.content.group_element.GroupElement` s

        SAFELY_UNGROUPABLE (int):
            Un-grouping is restricted to those groups that can be un-grouped without visual loss.

        ALL (int):
            Un-group all groups.
            Note that copying :class:`pdftools_toolbox.pdf.content.content_element.ContentElement` s with un-grouping set to :attr:`pdftools_toolbox.pdf.content.ungrouping_selection.UngroupingSelection.ALL`  can alter content's visual appearance in the output document.


    """
    NONE = 0
    SAFELY_UNGROUPABLE = 1
    ALL = 2

