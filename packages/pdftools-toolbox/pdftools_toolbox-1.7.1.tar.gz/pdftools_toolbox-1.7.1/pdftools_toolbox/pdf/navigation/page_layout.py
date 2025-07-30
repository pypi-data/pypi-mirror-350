from ctypes import *
from enum import IntEnum

class PageLayout(IntEnum):
    """
    Specifies the horizontal arrangement for displaying pages.



    Attributes:
        ONE_PAGE (int):
            Displays one page.

        TWO_PAGE (int):
            Displays two pages side by side.

        TWO_PAGE_FIRST_PAGE_SINGLE (int):
            Use :attr:`pdftools_toolbox.pdf.navigation.page_layout.PageLayout.ONEPAGE`  display for the first page and :attr:`pdftools_toolbox.pdf.navigation.page_layout.PageLayout.TWOPAGE`  display for the remaining pages.


    """
    ONE_PAGE = 0
    TWO_PAGE = 1
    TWO_PAGE_FIRST_PAGE_SINGLE = 2

