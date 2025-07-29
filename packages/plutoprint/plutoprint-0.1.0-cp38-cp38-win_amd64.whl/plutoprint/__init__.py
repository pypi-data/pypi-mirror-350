"""""" # start delvewheel patch
def _delvewheel_patch_1_10_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'plutoprint.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-plutoprint-0.1.0')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-plutoprint-0.1.0')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_10_0()
del _delvewheel_patch_1_10_0
# end delvewheel patch

from ._plutoprint import (
    __version__,
    __version_info__,
    __build_info__,

    Error,

    PageSize,
    PageMargins,
    MediaType,
    PDFMetadata,
    ImageFormat,
    Canvas,
    ImageCanvas,
    PDFCanvas,
    ResourceData,
    ResourceFetcher,
    Book,

    default_resource_fetcher,

    PAGE_SIZE_NONE,
    PAGE_SIZE_LETTER,
    PAGE_SIZE_LEGAL,
    PAGE_SIZE_LEDGER,
    PAGE_SIZE_A3,
    PAGE_SIZE_A4,
    PAGE_SIZE_A5,
    PAGE_SIZE_B4,
    PAGE_SIZE_B5,

    PAGE_MARGINS_NONE,
    PAGE_MARGINS_NORMAL,
    PAGE_MARGINS_NARROW,
    PAGE_MARGINS_MODERATE,
    PAGE_MARGINS_WIDE,

    MEDIA_TYPE_PRINT,
    MEDIA_TYPE_SCREEN,

    PDF_METADATA_TITLE,
    PDF_METADATA_AUTHOR,
    PDF_METADATA_SUBJECT,
    PDF_METADATA_KEYWORDS,
    PDF_METADATA_CREATOR,
    PDF_METADATA_CREATION_DATE,
    PDF_METADATA_MODIFICATION_DATE,

    IMAGE_FORMAT_INVALID,
    IMAGE_FORMAT_ARGB32,
    IMAGE_FORMAT_RGB24,
    IMAGE_FORMAT_A8,
    IMAGE_FORMAT_A1,

    MIN_PAGE_COUNT,
    MAX_PAGE_COUNT,

    UNITS_PT,
    UNITS_PC,
    UNITS_IN,
    UNITS_CM,
    UNITS_MM,
    UNITS_PX,

    PLUTOBOOK_VERSION,
    PLUTOBOOK_VERSION_MAJOR,
    PLUTOBOOK_VERSION_MINOR,
    PLUTOBOOK_VERSION_MICRO,
    PLUTOBOOK_VERSION_STRING
)
