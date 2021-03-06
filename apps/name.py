# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
from time import localtime, strftime
import json
import urllib
import os
from subprocess import check_output
from slackutils import insert_dot, get_nickname
#import imp
#settings = imp.load_source('settings','./settings.py')
#WEP_API_TOKEN = settings.WEP_API_TOKEN
#from settings import WEP_API_TOKEN

@on_command(['!기억', '!ㄱㅇ', '!rd'])
def run(robot, channel, tokens, user):
    '''단어 기억해드림'''
    msg = ''
    if len(tokens) == 0:
        msg = '`!기억` 에 대한 사용법은 `!도움 기억`을 통해 볼 수 있음'
        return channel, msg
    #url = 'https://slack.com/api/users.info?token='+WEP_API_TOKEN+'&user='+str(user)+'&pretty=1'
    #response = urllib.urlopen(url)
    #data = json.loads(response.read())
    nickname = get_nickname(user)
    if os.path.exists('./apps/name_cache/'+str(tokens[0])):
        f = open('./apps/name_cache/'+str(tokens[0]), 'r')
    else:
        f = None
    full_line = ''
    if len(tokens) == 1:
        if str(tokens[0]) == '?':
            all_file = check_output(['ls', '/home/simneol/hongmoa/apps/name_cache/'])
            msg = '제가 여태까지 기억한 것들은 아래와 같아요!\n'
            for s in all_file.split('\n'):
                msg += s+' || '
            msg = msg[:-8]
            return channel, msg
        if not f:
            msg = str(tokens[0])+'에 대해 기억나는게 없어요 ㅠㅡㅠ'
            return channel, msg
        time = line = f.readline()
        while line:
            line = f.readline()
            full_line += line
        msg = full_line+'\n'+time
    elif len(tokens)>1:
        if f:
            line = f.readline()
            while line:
                line = f.readline()
                full_line += line
        full_line = '가장 최근에 '+insert_dot(nickname)+'이(가) '+strftime('%Y-%m-%d %H:%M:%S', localtime())+'에 알려줬어요!\n'+full_line
        desc = ''
        for i in range(1, len(tokens)):
            desc += tokens[i]+' '
        full_line = full_line+desc[:-1]+'\n'
        if f:
            f.close()
        f = open('./apps/name_cache/'+str(tokens[0]), 'w')
        f.write(full_line)
        f.close()
        msg = str(tokens[0])+'에 대해 '+desc[:-1]+'(이)라고 기억했어요!'
#    msg = str(data['user']['name'])+'이(가) '+strftime('%Y-%m-%d %H:%M:%S',localtime())+'에 불러주었어요!'
    return channel, msg

if "__main__" == __name__:
    url = 'https://slack.com/api/users.info?token=xoxp-26726533763-26813510823-33040779782-4d90d5301c&user=U0SPF91EE&pretty=1'
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    print data['user']['name']
