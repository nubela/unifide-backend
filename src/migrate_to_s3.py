"""
Script to migrate existing local media objects to S3
"""
import os
from base import media
from base.media import Media
from base.media.action import MediaStorage, _store_s3
from cfg import UPLOAD_FOLDER


if __name__ == "__main__":
    list_of_dic = Media.collection().find({})
    media_objs = [Media.unserialize(x) for x in list_of_dic]
    for m in media_objs:
        if m.storage == MediaStorage.LOCAL:
            filename = m.file_name
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            print "Working on %s.." % (file_path)
            if os.path.isfile(file_path):
                m.storage = MediaStorage.S3
                m.url = _store_s3(filename, file_path)
                media.save(m)
                print "Migrated %s!" % (file_path)
                os.remove(file_path)