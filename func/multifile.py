import os
import conf
import logging
import sys
import shutil
from model import DataModel
LOG = logging.getLogger(__name__)
CONF = conf.conf()
db_full_path = os.path.join(conf.project_file, CONF["multifile"]["fold"])


class MultiFile(DataModel):
    def __init__(self, **kwargs):
        super(MultiFile, self).__init__(**kwargs)
        self.path = None
        if not os.path.isdir(db_full_path):
            os.mkdir(db_full_path, mode=0o777)

    def key_path(self,key):
        path = os.path.join(self.path, key + ".txt")
        return path

    def user_path(self):
        self.data = self.model_data()
        user_id = self.data['user_id']
        if not user_id:
            logging.error("Not exist userID,the data is %s" % self.data)
            return False
        user_path = os.path.join(db_full_path, user_id)
        return user_path

    def restore(self, **kwargs):
        if kwargs:
            super(MultiFile, self).__init__(**kwargs)
        if not self.is_valid():
            logging.error("Can't restore invaild data: %s"% self.data)
            return False
        self.path = self.user_path()
        if os.path.exists(self.path):
            logging.warning("userID(%s) is exist, can't restore the data to DB: %s" % (self.user_id, self.data))
            return False
        os.mkdir(self.path)

        for key in self.data:
            if key is 'user_id':
                continue
            key_path = self.key_path(key)
            key_file = open(key_path,'w')
            key_file.write(str(self.data[key]))
            key_file.close()
        return True

    def read(self, user_id):
        self.user_id = user_id
        old_data = {}

        self.path = self.user_path()
        if not os.path.exists(self.path):
            return False, old_data
        else:
            old_data = self.model_data()

            for key in self.data:
                if key is 'user_id':
                    continue
                key_path = self.key_path(key)

                if not os.path.exists(key_path):
                    old_data[key] = None
                key_file = open(key_path,'r')
                if key == 'age':
                    old_data[key] = int(key_file.readline())
                else:
                    old_data[key] = key_file.readline()
                key_file.close()

            return True, old_data

    def delete(self, user_id):
        self.user_id = user_id
        self.path = self.user_path()
        flag, old_data = self.read(user_id)
        if flag:
            shutil.rmtree(self.path)
            logging.info("userID(%s) is exist, delete the old DB data: %s" % (self.user_id, old_data))
            return True
        else:
            return False

    def modify(self, **kwargs):
        if kwargs:
            super(MultiFile, self).__init__(**kwargs)
        if not self.data['user_id'] or self.user_id is None:
            logging.error("Not userID info when modify the data,the input data is :%s" % self.data)
            return False
        input_data = self.data
        self.path = self.user_path()

        flag, db_data = self.read(self.user_id)

        if not flag:
            logging.error("userID(%s) is not exist, can't modify the data: %s" % (self.user_id, self.data))
            return False
        else:
            for key in input_data:
                if input_data[key] is None:
                    input_data[key] = db_data[key]
            if db_data == input_data:
                logging.info("Needn't modify,the old data of userID(%s) is same with data: %s" % (self.user_id, input_data))
                return False
            else:
                logging.info("Modify the old data(%s) of userID(%s),new data is: %s" % (db_data, self.user_id, input_data))
                shutil.rmtree(self.path)
                self.restore(data=input_data)
                return True

    def search(self,**kwargs):
        if kwargs:
            super(MultiFile, self).__init__(**kwargs)
        result = []
        #input data include unique index key user_id
        if self.is_key('user_id'):
            flag, db_data = self.read(self.user_id)
            if flag:
                for key in db_data:
                    if self.is_key(key):
                        if db_data[key] is not self.data[key]:
                            return result
                result.append(db_data)
                return result

            else:
                logging.warning("can't search any data with %s" % self.data)
        #input data not include user_id
        #need read all files to search all of data
        else:
            i = 0
            for self.path, dirnames, filenames in os.walk(db_full_path):
                i += 1
                if i is 1:
                    continue
                db_data = {}
                db_user_id = self.path.split(db_full_path + '/',1)[1]

                db_data['user_id'] = db_user_id
                for key in self.data:
                    if key is 'user_id':
                        continue

                    db_data[key] = open(self.key_path(key), 'r').readline()
                    if key == 'age':
                        db_data[key] = int(db_data[key])
                    if self.data[key] is not None and self.data[key] != db_data[key]:
                        db_data = False
                        break
                if db_data:
                    result.append(db_data)
            return result











