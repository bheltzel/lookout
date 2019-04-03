# import yaml
# import json
# from .lookerapi import LookerApi
# from pprint import pprint
# from datetime import datetime
# import pytz
# from .base import Base
 

import json
from json import dumps
from .base import Base


class Conns(Base):
    """Say hello, world!"""

    lb = '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
    prefix = '- - '
 
    def run(self):
        import urllib3
        urllib3.disable_warnings()
        host = self.options['<host>']
        
        looker = self.conn(host)
        r = looker.get_connections()

        if len(r) == 0:
            print('No active connections have been saved.')
        else:
            for row in r:
                if row['name'] != 'looker':
                    print(self.lb)
                    print(self.prefix + 'Connection: ' + row['name'])
                    print(self.lb)
                    print(self.prefix + 'Dialect: ' + row['dialect']['name'])
                    print(self.prefix + 'Created at: ' + row['created_at'])
                    # print(row['user_id'])
                    
                    t = looker.test_connection(row['name'])
                    print(self.prefix + 'Connection test for ' + row['name'] + ': ' + t[0]['message'])
                    print(self.lb)
                    print(self.lb)


    def conn(self, host):
        from lookerapi import LookerApi
        import yaml

        f = open('config.yml')
        params = yaml.full_load(f)
        f.close()

        location = params['hosts'][host]['location']
        if location == 'sa':
            au = 0
            sa = 1
        elif location == 'au':
            au = 1
            sa = 0
        else:
            au = 0
            sa = 0

        if au == 1:
            my_host = 'https://' + params['hosts'][host]['host'] + '.au.looker.com:19999/api/3.0/'
        elif sa == 1:
            my_host = 'https://' + params['hosts'][host]['host'] + '.sa.looker.com:19999/api/3.0/'
        else:
            my_host = 'https://' + params['hosts'][host]['host'] + '.looker.com:19999/api/3.0/'

        my_secret = params['hosts'][host]['secret']
        my_token = params['hosts'][host]['token']

        looker = LookerApi(host=my_host, token=my_token, secret=my_secret)
        if looker is None:
            print('Connection to Looker failed')
            exit()

        return looker
