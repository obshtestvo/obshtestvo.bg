from fabric.api import *

try:
    import fabric_settings
except ImportError:
    print("Please create a fabric_settings.py file in order to use fab.")
    exit(1)

def run_within_virtual_env(command):
    with cd(env.project_root):
        if env.virtual_env_name != '':
            command_prefix = 'workon %s && ' % env.virtual_env_name
        else:
            command_prefix = ''

        run(command_prefix + command)

def run_manage(command):
    run_within_virtual_env('python manage.py %s' % command)

def deploy_static_files():
    run_manage('collectstatic -v0 --noinput')

def compile_static_files():
    run_manage('compress')

def install_static_dependencies():
    with cd(env.project_root+'/web'):
        command = 'bower install'
        run(command)

def deploy_code():
    with settings(warn_only=True):
        if run('test -d %s' % env.project_root).failed:
            run('git clone %s %s' % (env.repository_url, env.project_root))
    with cd(env.project_root):
        run('git checkout %s' % env.deploy_branch)
        run('git pull origin %s' % env.deploy_branch)

def install_dependencies():
    run_within_virtual_env('pip install -r requirements.txt')

def run_migrations():
    run_manage('syncdb')
    run_manage('migrate projects')

def restart_app_server():
    with cd(env.project_root):
        run('touch app.wsgi')

def deploy():
    deploy_code()
    install_dependencies()
    install_static_dependencies()
    deploy_static_files()
    compile_static_files()
    run_migrations()
    restart_app_server()
