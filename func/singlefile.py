import os
import conf
import logging
import sys
import shutil
from model import DataModel
LOG = logging.getLogger(__name__)
CONF = conf.conf()
db_full_path = os.path.join(conf.project_file, CONF["singlefile"]["fold"])


class SingleFile(DataModel):
    def __init__(self, **kwargs):
        super(SingleFile, self).__init__(**kwargs)
        if not os.path.isdir(db_full_path):
            os.mkdir(db_full_path, mode=0o777)
        self.path = db_full_path + "/data_file.txt"

        self.file = open(self.path,'a+')
        self.delimiter = '---'

    def output_line(self,line):
        lists = line.split(self.delimiter)
        user_id = lists[0]
        name = lists[1]
        age = int(lists[2])
        password = lists[3]
        data = {'name': name,
                'age': age,
                'password': password,
                'user_id': user_id
                     }
        return data

    def input_line(self):
        line = self.user_id + self.delimiter\
              + self.name + self.delimiter\
              + str(self.age) + self.delimiter\
              + self.password
        return line

    def restore(self, **kwargs):
        if kwargs:
            super(SingleFile, self).__init__(**kwargs)
        if not self.is_valid():
            logging.error("Can't restore invaild data: %s" % self.data)
            return False
        flag, db_data = self.read(self.user_id)
        self.attribute_data()
        if flag:
            logging.warning("userID(%s) is exist, can't restore the data to DB: %s" % (self.user_id, self.data))
            return False
        self.file.write(self.input_line())

    def read(self, user_id):
        for line in open(self.path,'r').readlines():
            data = self.output_line(line)
            if self.user_id is data['user_id']:
                return True, data
        logging.info("Cannot find the user_id: %s" % user_id)
        return False, {}

    def search(self,**kwargs):
        if kwargs:
            super(SingleFile, self).__init__(**kwargs)
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
                logging.warning("Can't search any data with %s" % self.data)
        #input data not include user_id
        #need read all files to search all of data
        else:
            for line in open(self.path, 'r').readlines():
                db_data = self.output_line(line)
                for key in self.data:
                    if key == 'age':
                        db_data[key] = int(db_data[key])
                    if self.data[key] is not None and self.data[key] is not db_data[key]:
                        db_data = False
                        break
                if db_data:
                    result.append(db_data)

            return result



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













