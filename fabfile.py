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
    env.docker = sudo_docker

@task
@with_settings(warn_only=True)
def build():
    env.docker("build -t adsabs/forwarder .")
        
@task
@with_settings(warn_only=True)
def rmi():
    env.docker("rmi adsabs/forwarder")
        
@task
@with_settings(warn_only=True)
def run(ep='', **kwargs):
    
    ports = ""
    links = "--link adsabs-logstash:logstash"
    vols = "-v /dev/log:/dev/log"
    vfrom = "--volumes-from adsabs-adsloggingdata"
    
    evars = ""
    if len(kwargs):
        for k,v in kwargs.items():
            evars += "-e %s=%s" % (k,v)
            
    env.docker("run -d -t -i --name adsabs-forwarder %s %s %s %s %s adsabs/forwarder %s" \
               % (evars, ports, links, vols, vfrom, ep))
    
@task
@with_settings(warn_only=True)
def stop():
    env.docker("stop adsabs-forwarder")
    
@task
@with_settings(warn_only=True)
def rm():
    env.docker("rm adsabs-forwarder")
         
