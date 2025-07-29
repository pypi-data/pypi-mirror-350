
# https://mimetype.io/all-types

# This list is likely incomplete. Expand with need for more file compatibility

def get_mimetype(filename: str):
  ext = filename.split('.')[-1]
  if (ext == 'jpg' or ext == 'jpeg'):
    return 'image/jpeg'
  elif ext == 'png':
    return 'image/png'
  elif ext == 'gif':
    return 'image/gif'
  elif ext == 'tif' or ext == 'tiff':
    return 'image/tiff'
  elif ext == 'bmp':
    return 'image/bmp'
  elif ext == 'mp4' or ext == 'mp4v' or ext == 'mpg4':
    return 'video/mp4'
  elif ext == 'avi':
    return 'video/x-msvideo'
  elif ext == 'wmv':
    return 'video/x-ms-wmv'
  elif ext == 'mpeg' or ext == 'mpg' or ext == 'mpe' or ext == 'm1v' or ext == 'm2v' or ext == 'mpa':
    return 'video/mpeg'
  elif ext == 'wav':
    return 'audio/wav'
  elif ext == 'mp3' or ext == 'mpga' or ext == 'm2a' or ext == 'm3a' or ext == 'mp2':
    return 'audio/mpeg'
  elif ext == 'wma':
    return 'audio/x-ma-wma'
  elif ext == 'wax':
    return 'audio/x-ms-wax'
  elif ext == 'pdf':
    return 'application/pdf'
  return None
