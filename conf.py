import configparser
import os,sys

project_file = os.path.abspath(os.path.dirname(sys.modules[__name__].__file__))
conf_file = os.path.join(project_file, 'config.ini')


def conf():
    config = configparser.ConfigParser()
    config.read(conf_file)
    return config

if __name__ == "__main__":
    print(conf()["ICP_server"]["ICP_Search_Host"])
