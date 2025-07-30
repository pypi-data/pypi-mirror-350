from ctypes import *
from enum import IntEnum

class MdpPermissions(IntEnum):
    """

    Attributes:
        NO_CHANGES (int):
            No changes to the document shall be permitted;
            any change to the document shall invalidate the signature.

        FORM_FILLING (int):
            Permitted changes shall be filling in forms, instantiating page templates, and signing;
            other changes shall invalidate the signature.

        ANNOTATE (int):
            Permitted changes shall be the same as for :attr:`pdftools_toolbox.pdf.forms.mdp_permissions.MdpPermissions.FORMFILLING` ,
            as well as annotation creation, deletion, and modification;
            other changes shall invalidate the signature.


    """
    NO_CHANGES = 1
    FORM_FILLING = 2
    ANNOTATE = 3

