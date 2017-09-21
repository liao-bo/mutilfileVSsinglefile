import random
import string
import os
import logging
import sys
LOG = logging.getLogger(__name__)
db_full_path = os.path.join(os.path.abspath(os.path.dirname(sys.modules[__name__].__file__)),
                                 'test_data.txt')


def random_data_list():
    path = db_full_path

    open(path, 'w+')
    for i in range(500) :
        user_id = "".join(random.sample(string.ascii_lowercase, 20))
        username = "".join(random.sample(string.ascii_lowercase,random.randint(2,15)))
        age = str(random.randint(12, 99))
        password = "".join(random.sample(string.ascii_lowercase, 20))
        delimiter = '////'
        random_data = user_id + delimiter + username + delimiter + age + delimiter + password

        open(path,'a+', encoding='utf=8').write(random_data + '\n')

        LOG.debug("test random list is :" + random_data)


if __name__ == '__main__':

    random_data_list()
