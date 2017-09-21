import logging
LOG = logging.getLogger(__name__)


class DataModel(object):
    def __init__(self, **kwargs):
        super(DataModel, self).__init__()
        self.name,self.age,self.password,self.user_id,self.data = None,None,None,None,None
        self.model_data()

        if 'data' in kwargs:
            data = kwargs['data']
        else:
            data = kwargs
        for key in self.data:
            if key in data:
                self.data[key] = data[key]

        self.attribute_data()


        self.check_isinstance(self.name, str)
        self.check_isinstance(self.age, int)
        self.check_isinstance(self.password, str)
        self.check_isinstance(self.data, dict)

    def attribute_data(self):
        self.user_id = self.data['user_id']
        self.name = self.data['name']
        self.age = self.data['age']
        self.password = self.data['password']

    def model_data(self):
        self.data = {'name': self.name,
                     'age': self.age,
                     'password': self.password,
                     'user_id': self.user_id
                     }
        return self.data

    def check_isinstance(self, value, type):
        if value is None:
            return True
        if not isinstance(value, type):
            logging.warning("the value(%s) is not the correct type:%s" %(value, type))
            raise TypeError
        else:
            return True

    def is_key(self, key):
        if key in self.data and self.data[key] is not None:
            return True
        else:
            return False

    def is_valid(self):
        for key in self.data:
            if not self.is_key(key):
                return False
        return True

