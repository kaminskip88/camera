#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import json
import argparse

conf_path='./camera.conf'

def read_conf(path):
    try:
        source=open(conf_path)
    except IOError as e:
        sys.exit('ERROR: %s' % e)
    try:
        jsource = json.load(source)
    except ValueError as e:
        sys.exit('Wrong JSON format: %s' %e)
    return jsource

config = read_conf(conf_path)

parser = argparse.ArgumentParser()
parser.add_argument("action", help='rec|some1|some2', choices=['rec'], type=str)
args = parser.parse_args()

# PTZ

def curl(url, params=None):
    """
    :param url: string request URL
    :param params: request parameters as dict
    :return: request object
    """
    result = requests.get(url, params=params)
    if result.status_code == 200:
        return result
    else:
        print "Error, site respond with {0}".format(result.status_code)
        sys.exit(1)


cam_options = {
    'addr': '10.6.87.94',
    'port': '81',
    'login': 'admin',
    'pass': '888888'
}


def turn(dir):
    dir_dict = {
        'l': '4',
        'r': '6',
        'u': '0',
        'd': '2'
    }

    param_set = {
        'loginuse': cam_options['login'],
        'loginpas': cam_options['pass'],
        'command': dir_dict[dir],
        'onestep': '1'
    }
    curl('http://{0}:{1}/decoder_control.cgi'.format(cam_options['addr'], cam_options['port']),params=param_set)

# END PTZ

# RECORD
from datetime import datetime
from datetime import timedelta
import os
import subprocess

def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def convert_to_timedelta(time_val):
    num = int(time_val[:-1])
    if time_val.endswith('s'):
        return timedelta(seconds=num)
    elif time_val.endswith('m'):
        return timedelta(minutes=num)
    elif time_val.endswith('h'):
        return timedelta(hours=num)
    elif time_val.endswith('d'):
        return timedelta(days=num)

if args.action == 'rec':
    # ffmpeg = which('ffmpeg')
    # if not ffmpeg:
    #     print 'ffmpeg not found'
    #     sys.exit(1)
    ffmpeg = '/usr/bin/ffmpeg'

    for cam, cam_value in config['cameras'].iteritems():
        output_dir = '{0}{1}/'.format(config['global']['video_dir'], cam)
        output_file = datetime.now().strftime("%Y-%m-%d_%H:%M.mp4")
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir, 0755)
        format_dict = {
            'bin_path': ffmpeg,
            'login': cam_value['login'],
            'pass': cam_value['pass'],
            'ip': cam_value['host'],
            'port': cam_value['rtsp_port'],
            'uri': cam_value['rtsp_uri'],
            'frame_rate': cam_value['frame_rate'],
            'time': int(convert_to_timedelta(cam_value['write_intervals']).total_seconds()),
            'odir': output_dir,
            'ofile': output_file,
            'log_dir': config['global']['log_dir'],
            'cam': cam
        }
        ffmpeg_cmd = '{bin_path} -i rtsp://{login}:{pass}@{ip}:{port}{uri} -r {frame_rate} -vcodec copy -an -t {time} {odir}{ofile} </dev/null >/dev/null 2>>{log_dir}{cam}.log &'.format(**format_dict)
        print ffmpeg_cmd
        #subprocess.call(cmd,shell=True)



