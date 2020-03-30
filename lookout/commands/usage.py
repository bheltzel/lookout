import json
from json import dumps
from .base import Base


class Usage(Base):
    """Say hello, world!"""
 
    def run(self):
        import urllib3
        urllib3.disable_warnings()
        host = self.options['<host>']
        
        looker = self.conn(host)

        model = 'i__looker'
        explore = 'history'

        fields = [
            'user.first_name'
            , 'user.last_name'
            , 'history.created_time'
            , 'dashboard.id'
            , 'history.source'
            , 'look.title'
            , 'dashboard.title'
            , 'query.view'
        ]

        filters = {
            'user.is_looker': 'No'
            , 'history.created_date': '-NULL'

            # , 'history.source': 'Explore'
        }

        sort = [
            'history.created_time desc'
        ]

        body = {
            'model': model
            , 'view': explore
            , 'fields': fields
            , 'filters': filters
            , 'limit': '50'
            , 'sorts': sort
            , 'query_timezone': 'America/Los_Angeles'
        }

        r = looker.run_inline_query(body)

        print('{:<25s}{:<20s}{:<12s}{:<20s}{:<40s}'.format('Name', 'History Time', '', 'Source', 'Title'))
        print('{:<25s}{:<20s}{:<12s}{:<20s}{:<40s}'.format('----------', '----------', '', '----------', '----------'))
        for row in r:
            if row['user.first_name'] is not None and row['user.last_name'] is not None:
                name = row['user.first_name']
                # name = row['user.first_name'].encode('utf-8')  + row['user.last_name'].encode('utf-8')
            else:
                name = '--'
            created_time = row['history.created_time']
            history_source = row['history.source']
            if history_source == 'Dashboard' and row['dashboard.title'] is not None:
                title = row['dashboard.title'].encode('utf-8')
            elif history_source == 'Look':
                title = row['look.title'].encode('utf-8')
            elif history_source == 'Explore':
                title = row['query.view'].encode('utf-8')
            else:
                title = '--'

            print('{:<25s}{:<20s}{:<12s}{:<20s}{:<40s}'.format(name,created_time,'',history_source, title))


    def conn(self, host):
        from .lookerapi import LookerApi
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


    def keyCheck(self, key, arr, default=''):
        if key in arr.keys():
            return arr[key]
        else:
            return default


    


