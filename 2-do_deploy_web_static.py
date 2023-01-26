#!/usr/bin/python3
"""Distributes an archive to a web server"""

from fabric.api import *
import os

env.hosts = ['100.26.151.146', '100.25.146.124']


def do_deploy(archive_path):
    """Distributes and compress files in an archive to a web server"""
    try:
        try:
            if os.path.exists(archive_path):
                arc_tgz = archive_path.split("/")
                arg_save = arc_tgz[1]
                arc_tgz = arc_tgz[1].split('.')
                arc_tgz = arc_tgz[0]

                """Archive to the server"""
                put(archive_path, '/tmp')

                """Putting folder paths in variables"""
                archive_dirs = '/data/web_static/releases/{}'.format(arc_tgz)
                dir_location = '/tmp/{}'.format(arg_save)

                """Run commands on the server"""
                run('mkdir -p {}'.format(archive_dirs))
                run('tar -xvzf {} -C {}'.format(dir_location, archive_dirs))
                run('rm {}'.format(dir_location))
                run('mv {}/web_static/* {}'.format(archive_dirs, archive_dirs))
                run('rm -rf {}/web_static'.format(archive_dirs))
                run('rm -rf /data/web_static/current')
                run('ln -sf {} /data/web_static/current'.format(archive_dirs))
                run('sudo service nginx restart')
                return True
            else:
                print('File does not exist')
                return False
        except Exception as err:
            print(err)
            return False
    except Exception:
        print('Error')
        return False
