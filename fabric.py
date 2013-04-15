from fabric.aip import local

def prepare_deployment(branch_name):
  local('python manage.py test hackernews')
  #local('git add -p && git commit')

from fabric.api import lcd, local

def deploy():
    with lcd('/path/to/my/prod/area/'):

        # With git...
        local('git pull /my/path/to/dev/area/')

        # With Mercurial...
        local('hg pull /my/path/to/dev/area/')
        local('hg update')

        # With both
        local('python manage.py migrate myapp')
        local('python manage.py test myapp')
        local('/my/command/to/restart/webserver')
