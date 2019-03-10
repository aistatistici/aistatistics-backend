import os
import uuid
from typing import Text
from datetime import datetime

from src.config import MEDIA_ROOT


def upload_file_location(filename: Text, subfolder: Text) -> Text:

    """
        upload_file_location function is used to auto generate the CDN folder for the media files and returns
        the file path to be saved.
    :param filename: filename that is recieved through file upload
    :param subfolder: root subfolder to be created if its not created
    :return: complete path of the file generated to be saved
    """
    filename, file_extension = os.path.splitext(filename)
    uid = uuid.uuid4()
    destination = os.path.join(MEDIA_ROOT, subfolder)
    if not os.path.exists(destination):
         os.makedirs(destination)
    return '%s%s' % (destination, '{0}-{1}{2}'.format(datetime.utcnow().date(), uid, file_extension))

