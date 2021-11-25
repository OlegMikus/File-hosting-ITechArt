FILE_STORAGE__TYPE__TEMP = 'temp'
FILE_STORAGE__TYPE__PERMANENT = 'permanent'
ARCHIVE__TYPE = 'zip'
FILE__NON_CHUNK__MAX_SIZE = 50 * 1024 * 1024
CHUNKS__STORAGE_TIME__DAYS = 7
USER_STORAGE__LOCATION__NGINX = '/user_storage'
SMALL_FILE_MAX_SIZE = 128 * 1024 * 1024
FILE__FIRST_SLICE = 100 * 1024 * 1024
FILE__SECOND_SLICE = 4 * 1024 * 1024

JPG__MIME_TYPE = 'image/jpeg'
PNG__MIME_TYPE = 'image/png'
GIF__MIME_TYPE = 'image/gif'
TIFF__MIME_TYPE = 'image/tiff'
SVG__MIME_TYPE = 'image/svg+xml'
PDF__MIME_TYPE = 'application/pdf'
TXT__MIME_TYPE = 'text/plain'
XLS__MIME_TYPE = 'application/vnd.ms-excel'
DOCS__MIME_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

ALLOWED_FORMATS = {JPG__MIME_TYPE, PDF__MIME_TYPE, PNG__MIME_TYPE, GIF__MIME_TYPE, TIFF__MIME_TYPE, SVG__MIME_TYPE,
                   TXT__MIME_TYPE, XLS__MIME_TYPE, DOCS__MIME_TYPE}
