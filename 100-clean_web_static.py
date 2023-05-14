#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive
from the contents of the web_static folder of the AirBnB Clone repo
"""
from fabric.operations import local, put, run, sudo
from datetime import datetime as d
from fabric.api import *

env.hosts = ['34.74.120.150', '54.173.196.75']
created_archive = None


def do_pack():
    """ generates a .tgz archive """
    name = "versions/web_static_" + str(d.now().year)
    name += str(d.now().month) + str(d.now().day) + str(d.now().hour)
    name += str(d.now().minute) + str(d.now().second) + ".tgz"
    result = local("mkdir -p versions; tar -cvzf \"%s\" web_static" % name)
    if result.failed:
        return None
    else:
        return name


def do_deploy(archive_path):
    """ uploads the archive to servers """
    destination = "/tmp/" + archive_path.split("/")[-1]
    result = put(archive_path, "/tmp/")
    if result.failed:
        return False
    filename = archive_path.split("/")[-1]
    f = filename.split(".")[0]
    directory = "/data/web_static/releases/" + f
    run_res = run("mkdir -p \"%s\"" % directory)
    if run_res.failed:
        return False
    run_res = run("tar -xzf %s -C %s" % (destination, directory))
    if run_res.failed:
        return False
    run_res = run("rm %s" % destination)
    if run_res:
        return False
    web = directory + "/web_static/*"
    run_res = run("mv %s %s" % (web, directory))
    if run_res.failed:
        return False
    web = web[0:-2]
    run_res = run("rm -rf %s" % web)
    if run_res.failed:
        return False
    run_res = run("rm -rf /data/web_static/current")
    if run_res.failed:
        return False
    run_res = run("ln -s %s /data/web_static/current" % directory)
    if run_res.failed:
        return False
    return True


def deploy():
    """ creates an archive and uploads it to servers"""
    global created_archive
    if created_archive is None:
        name = do_pack()
        if name is None:
            return False
        else:
            created_archive = name
        return do_deploy(name)
    else:
        return do_deploy(created_archive)


def do_clean(number=0):
    """ deletes out-of-date archives """
    n = int(number)
    if n == 0:
        n += 1
    n += 1
    local("ls versions/*.tgz -A1t | tail -n +%d | xargs rm" % n)
    with cd('/data/web_static/releases/'):
        run("ls -t1 | grep '^web_static' | tail -n +%d | xargs rm -rf" % n)
