import os
import sys
from os.path import abspath, dirname

from fabric.api import task, local, env
from fabric.context_managers import settings, cd, hide
from fabric.contrib.console import confirm
from fabric.colors import cyan, red
from fabric.utils import abort
from fabric.decorators import with_settings

env.base_dir = abspath(dirname(__file__))
env.show_cmd = False

@task
def show():
    """
    output generated commands rather than executing (i.e., dry-run)
    """
    env.show_cmd = True

def docker(cmd, sudo=False, **kwargs):
    with cd(env.base_dir):
        sudo = sudo and "sudo" or ""
        cmd = "%s docker %s" % (sudo, cmd)
        if env.show_cmd:
            print cyan(cmd) 
        else:
            return local(cmd, **kwargs)

def sudo_docker(cmd, **kwargs):
    return docker(cmd, True, **kwargs)
    
env.docker = docker

@task
def sudo():
    """
    execute commands via sudo
    """
    env.docker = sudo_docker

@task
@with_settings(warn_only=True)
def build():
    """
    build the container
    """
    env.docker("build -t adsabs/forwarder .")
        
@task
@with_settings(warn_only=True)
def rmi():
    """
    remove the image
    """
    env.docker("rmi adsabs/forwarder")
        
@task
@with_settings(warn_only=True)
def run(ep='', **kwargs):
    """
    execute the container
    
    ep - specify an alternate entrypoint, e.g., "ep=bash"
    **kwargs - additional kwargs will be converted to environment variables passed to container
    
    """ 
    vols = "-v /var/log/syslog:/var/log/syslog"
    evars = len(kwargs) and ' '.join(["-e %s=%s" % (x[0],x[1]) for x in kwargs.items()]) or '' 
    env.docker("run -d -t -i --name adsabs-forwarder %s %s adsabs/forwarder %s" \
               % (evars, vols, ep))
    
@task
@with_settings(warn_only=True)
def stop():
    """
    stop the container
    """
    env.docker("stop adsabs-forwarder")
    
@task
@with_settings(warn_only=True)
def rm():
    """
    remove the container
    """
    env.docker("rm adsabs-forwarder")
    
@task
@with_settings(warn_only=True)
def gen_certs():
    """
    generate a set of ssl certificates
    """
    local("mkdir -p certs")
    local("openssl req -x509 -batch -nodes -newkey rsa:2048 -keyout certs/forwarder.key -out certs/forwarder.crt")
    