import os
import uuid
from datetime import datetime

from src.config import MEDIA_ROOT


def upload_file_location(filename):

    filename, file_extension = os.path.splitext(filename)
    uid = uuid.uuid4()
    destination = os.path.join(MEDIA_ROOT, '/data/{0}-{1}{2}'.format(datetime.utcnow(), uid, file_extension))
    if not os.path.exists(destination):
        os.makedirs(destination)
    return destination

