FILE_STORAGE__TYPE__TEMP = 'temp'
FILE_STORAGE__TYPE__PERMANENT = 'permanent'
FILE__NON_CHUNK__MAX_SIZE = 50 * 1024 * 1024
CHUNKS__STORAGE_TIME__DAYS = 7

JPG = 'image/jpeg'
PNG = 'image/png'
GIF = 'image/gif'
TIFF = 'image/tiff'
SVG = 'image/svg+xml'
PDF = 'application/pdf'
TXT = 'text/plain'
XLS = 'application/vnd.ms-excel'
DOCS = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

ALLOWED_FORMATS = {JPG, PDF, PNG, GIF, TIFF, SVG, TXT, XLS, DOCS}
