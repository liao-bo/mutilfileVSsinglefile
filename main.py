import logging
import logging.handlers
import os
import conf
import sys
import time
import shutil
from func.multifile import MultiFile
from func.singlefile import SingleFile

CONF = conf.conf()
LOG = logging.getLogger(__name__)
logging_format = "[%(asctime)s.%(msecs)03d] [%(levelname)s][%(process) -6d] [%(threadName) -10s][%(name)s] %(message)s"


def main():
    log_full_path = os.path.join(os.path.abspath(os.path.dirname(sys.modules[__name__].__file__)), CONF["log"]["log_file"])
    fh = logging.handlers.TimedRotatingFileHandler(filename=log_full_path, when='midnight', interval=1, backupCount=14)
    fmt = logging.Formatter(logging_format)
    fh.setFormatter(fmt)

    conf_level = CONF["log"]["level"]
    if conf_level == 'INFO':
        level = logging.INFO
    elif conf_level == 'WARNING':
        level = logging.WARNING
    elif conf_level == 'ERROR':
        level = logging.ERROR
    elif conf_level == 'CRITICAL':
        level = logging.CRITICAL
    else:
        level = logging.DEBUG

    logging.basicConfig(level=level, format=logging_format)

    root_logger = logging.getLogger()
    root_logger.addHandler(fh)


import time
from functools import wraps
import random


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("Total time running %s: %s seconds" %
              (function.__name__, str(t1 - t0))
              )
        return result

    return function_timer


@fn_timer
def restore(**kwargs):
    MultiFile(**kwargs).restore()


def test_data_list():
    input_file = open('test/test_data.txt', 'r')
    input_list = []
    for line in input_file.readlines():
        input_data = {}
        attribute = line.split('////')
        input_data['user_id'] = attribute[0]
        input_data['name'] = attribute[1]
        input_data['age'] = int(attribute[2])
        input_data['password'] = attribute[3]
        input_list.append(input_data)
    return input_list

if __name__ == '__main__':
    main()
    if os.path.isdir('multifile_DB'):
        shutil.rmtree('multifile_DB')
    if os.path.isdir('singlefile_DB'):
        shutil.rmtree('singlefile_DB')
    test_list = test_data_list()
    time.sleep(5)
    # test multifile restore
    t0 = time.time()
    for data in test_list:
        MultiFile().restore(data=data)
    t1 = time.time()
    print("multi_file restore time is : %s" % str(t1 - t0))

    time.sleep(5)
    # test single file restore
    t2 = time.time()
    for data in test_list:
        SingleFile().restore(data=data)
    t3 = time.time()
    print("single_file restore time is : %s" % str(t3 - t2))

    time.sleep(5)
    #test multifile restore
    t4 = time.time()
    multi_result = MultiFile().search(age=33)
    t5 = time.time()
    print("multi_file search time is :%s" % str(t5 - t4))


    time.sleep(5)
    #test single file search
    t6 = time.time()
    single_result = SingleFile().search(age=33)
    t7 = time.time()
    print("single_file search time is :%s" % str(t7 - t6))

    '''
    print(multi_result)
    print(single_result)

    data = len(DB.search(age = 33))
    print(data)
    t2 = time.time()
    data = {'name': '1111',
            'age': 33,
            'password': 'dajsdlfjasdiojfa',
            'user_id': 'dfdfsdfdfdfdfdfddddd123'
            }
    restore(data=data)
    '''
    #print("multi_file restore time is : %s" % str(t2 - t1))

