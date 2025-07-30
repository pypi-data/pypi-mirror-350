import pdftools_toolbox.geometry.real
import pdftools_toolbox.geometry.integer

def _import_types():
    global HorizontalAlignment
    from pdftools_toolbox.geometry.horizontal_alignment import HorizontalAlignment
    global Rotation
    from pdftools_toolbox.geometry.rotation import Rotation

    pdftools_toolbox.geometry.real._import_types()
    pdftools_toolbox.geometry.integer._import_types()

