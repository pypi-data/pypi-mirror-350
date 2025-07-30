import pdftools_toolbox.pdf.structure
import pdftools_toolbox.pdf.content
import pdftools_toolbox.pdf.forms
import pdftools_toolbox.pdf.navigation
import pdftools_toolbox.pdf.annotations

def _import_types():
    global PageCopyOptions
    from pdftools_toolbox.pdf.page_copy_options import PageCopyOptions
    global Encryption
    from pdftools_toolbox.pdf.encryption import Encryption
    global PageList
    from pdftools_toolbox.pdf.page_list import PageList
    global FileReferenceList
    from pdftools_toolbox.pdf.file_reference_list import FileReferenceList
    global OptionalContentGroup
    from pdftools_toolbox.pdf.optional_content_group import OptionalContentGroup
    global OptionalContentGroupList
    from pdftools_toolbox.pdf.optional_content_group_list import OptionalContentGroupList
    global Document
    from pdftools_toolbox.pdf.document import Document
    global Page
    from pdftools_toolbox.pdf.page import Page
    global Metadata
    from pdftools_toolbox.pdf.metadata import Metadata
    global FileReference
    from pdftools_toolbox.pdf.file_reference import FileReference

    global Permission
    from pdftools_toolbox.pdf.permission import Permission
    global Conformance
    from pdftools_toolbox.pdf.conformance import Conformance
    global CopyStrategy
    from pdftools_toolbox.pdf.copy_strategy import CopyStrategy
    global RemovalStrategy
    from pdftools_toolbox.pdf.removal_strategy import RemovalStrategy
    global NameConflictResolution
    from pdftools_toolbox.pdf.name_conflict_resolution import NameConflictResolution
    global OcgState
    from pdftools_toolbox.pdf.ocg_state import OcgState

    pdftools_toolbox.pdf.structure._import_types()
    pdftools_toolbox.pdf.content._import_types()
    pdftools_toolbox.pdf.forms._import_types()
    pdftools_toolbox.pdf.navigation._import_types()
    pdftools_toolbox.pdf.annotations._import_types()

