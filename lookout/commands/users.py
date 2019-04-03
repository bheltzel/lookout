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

        model = 'system__activity'
        explore = 'history'

        fields = [
            'user.first_name'
            ,'user.last_name'
            , 'user_facts.last_ui_login_date'
        ]

        filters = {
            'user.is_looker': 'No'
            , 'history.created_date': '-NULL'
            , 'user.email': '-NULL'
        }

        sort = [
            'user_facts.last_ui_login_date desc'
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

        # query_id = 'plHY4a36qwXKdYCItBjqFP'

        # body = {
        #     'query_id': query_id
        #     , 'result_format': 'json'
        #     , 'limit': '50'
        #     # , 'query_timezone': 'America/Los_Angeles'
        # }

        # r = looker.run_query_async(body)

        print(r)

        print('{:<25s}{:<20s}{:<12s}{:<20s}{:<40s}'.format('Email', 'Last Login', '', 'Source', 'Title'))
        print('{:<25s}{:<20s}{:<12s}{:<20s}{:<40s}'.format('----------', '----------', '', '----------', '----------'))
        for row in r:
            if row['user.first_name'] is not None and row['user.last_name'] is not None:
                name = row['user.first_name'].encode('utf-8') + ' ' + row['user.last_name'].encode('utf-8')
            else:
                name = '--'
            if row['user_facts.last_ui_login_date'] is not None:
                last_login = row['user_facts.last_ui_login_date']
            else:
                last_login = ' -- '
        #     if history_source == 'Dashboard' and row['dashboard.title'] is not None:
        #         title = row['dashboard.title'].encode('utf-8')
        #     elif history_source == 'Look':
        #         title = row['look.title'].encode('utf-8')
        #     elif history_source == 'Explore':
        #         title = row['query.view'].encode('utf-8')
        #     else:
        #         title = '--'

            print('{:<25s}{:<20s}{:<12s}{:<20s}{:<40s}'.format(name,last_login,'','',''))


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