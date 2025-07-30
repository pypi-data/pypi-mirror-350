import pdftools_toolbox.internal
import pdftools_toolbox.geometry
import pdftools_toolbox.pdf
import pdftools_toolbox.sys

def _import_types():
    global Sdk
    from pdftools_toolbox.sdk import Sdk
    global StringMap
    from pdftools_toolbox.string_map import StringMap

    pdftools_toolbox.geometry._import_types()
    pdftools_toolbox.pdf._import_types()
    pdftools_toolbox.sys._import_types()


_import_types()