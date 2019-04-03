import yaml
from json import dumps
from .base import Base
import requests
 

class New(Base):
    """Say hello, world!"""
    debug = False
 
    def run(self):
        from lookerapi import LookerApi
        from pprint import pprint
        from github import Github
        import urllib3
        urllib3.disable_warnings()

        if self.debug:
            print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
            print('You supplied the following args:', dumps(self.args, indent=2, sort_keys=True))
            print('You supplied the following kwargs:', dumps(self.kwargs, indent=2, sort_keys=True))
            print(self.options['<host>'])

        # interpret args
        host = self.options['<host>']
        
        if self.options['--au']:
            location = 'au'
        elif self.options['--sa']:
            location = 'sa'
        elif self.options['--eu']:
            location = 'eu'
        else:
            location = 'na'
        
        if location == 'na':
            print('https://' + host + '.looker.com/admin/users/api3_key/2')
        else:
            print('https://' + host + '.' + location + '.looker.com/admin/users/api3_key/2')

        do_create_deploy_key = True  
        do_create_repo = True
        se = 'bryce'


        # TODO: check if host already exists

        # TODO: turn off warnings // /Users/bryceheltzel 1/Library/Python/2.7/lib/python/site-packages/urllib3/connectionpool.py:857: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings InsecureRequestWarning)

        token = str(raw_input('Enter Looker API Token: '))
        secret = str(raw_input('Enter Looker API Secret: '))

        from os.path import expanduser
        home = expanduser("~")

        f = open(home + '/config.yml', 'a')
        f.write('\n')
        f.write(' \'' + host + '\':\n')
        f.write('    host: \'' + host + '\'\n')
        f.write('    secret: \'' + secret + '\'\n')
        f.write('    token: \'' + token + '\'\n')
        f.write('    location: \'' + location + '\'')
        
        f.close()

        
        f = open(home + '/config.yml')
        params = yaml.load(f, Loader=yaml.Loader)
        f.close()

        project_id = host
        repo_name = project_id + '_internal'
        git_remote_url = 'git@github.com:llooker/' + repo_name + '.git'

        if location == 'au':
            my_host = 'https://' + params['hosts'][host]['host'] + '.au.looker.com:19999/api/3.0/'
        elif location == 'sa':
            my_host = 'https://' + params['hosts'][host]['host'] + '.sa.looker.com:19999/api/3.0/'
        elif location == 'eu':
            my_host = 'https://' + params['hosts'][host]['host'] + '.eu.looker.com:19999/api/3.0/'
        else:
            my_host = 'https://' + params['hosts'][host]['host'] + '.looker.com:19999/api/3.0/'

        my_secret = params['hosts'][host]['secret']
        my_token = params['hosts'][host]['token']
 
        looker = LookerApi(host=my_host, token=my_token, secret=my_secret)
        if looker is None:
            print('ERROR: Connection to Looker failed')
            exit()

        # ------ SETUP GIT IN LOOKER ------
        # update session -> turn on dev mode
        data = looker.update_session('dev')
        if data is None:
            print('ERROR: dev session did not start')
            exit()

        # create deploy key (responds with resource already created if running again)
        if do_create_deploy_key:
            new_key = looker.create_git_deploy_key(project_id)
            if new_key is None:
                print('ERROR: New Git Deploy Key was not created')
                exit()
            elif self.debug:
                pprint(new_key)

        # get key
        key = looker.get_git_deploy_key(project_id)
        if key is None:
            print('Key could not be found')
            exit()
        elif self.debug:
            print(key)

        # set git_remote_url in looker
        git_remote = looker.update_project(project_id, 'git_remote_url', git_remote_url)
        if git_remote is None:
            print('Git Remote URL could not be attached to Looker')
            exit()
        elif self.debug:
            pprint(git_remote)

        # ------ CREATE REPO ON GITHUB ------
        # create github connection
        git = Github(params['se'][se]['token_git'])

        # get github org
        org = git.get_organization('llooker')
        if self.debug:
            print(org)

        # create new repo
        if do_create_repo:
            repo = org.create_repo(repo_name, private=True)
            if self.debug:
                pprint(repo)

            # attach key to repo
            if key is None:
                print('ERROR: Key did not get created succesfully')
                exit()
            else:
                attached = repo.create_key(repo_name, key, False)
                if self.debug:
                    pprint(attached)
        else:
            # get repo if needed
            repo = org.get_repo(repo_name)

        # update 1_home.md file



        #   YOU MUST ADD A BREAK POINT TO THE NEXT LINE.
        #   at this point, go into the UI, turn on dev mode, commit the model, and deploy to prod.
        #   then run the rest of the script
        print("(1) go into the instance, (2) turn on dev mode and (3) deploy to prod.")
        raw_input('press enter to proceed...')

        # create model file
        model_text = "connection: \"connection_name\"\n\ninclude: \"*.view.lkml\"         # include all views in this project\n"
        repo.create_file(project_id + '.model.lkml', 'initial model', model_text, 'master')

        # delete test model file
        # 6.6.18 // it seems like this file doesn't get generated unless a email/password user logs in, not an API user. commenting it out for now.
        # 3.15.19 // it works

        git_model_file_name = 'test_delete.model.lkml'
        git_model_file = repo.get_file_contents(git_model_file_name)
        repo.delete_file(git_model_file_name, 'remove test model', git_model_file.sha, 'master')

        # deploy master to prod
        requests.get('https://' + host + '.looker.com/git/pull/' + project_id)

        # turn on labs features + update
        # no can do
        print 'Turn on Labs: ' + 'https://' + host + '.looker.com/admin/labs'
        # print '/stories/' + host + '/1_home.md'

        # invite users
        # no can do
        print 'Invite Users: ' + 'https://' + host + '.looker.com/admin/users'

        # ------- Done -------
        print "fin"

    def conn(self, host):
        from lookerapi import LookerApi
        import yaml

        f = open('config.yml')
        params = yaml.load(f, Loader=yaml.Loader)
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