#! /usr/bin/python3
import argparse
import datetime
import json
import os

import requests


def sender(project='project', workload='service', body=None):
    url = 'https://oapi.dingtalk.com/robot/send?access_token='
    header = {"Content-Type": "application/json"}
    result = requests.post(url=url, data=json.dumps(body), headers=header)
    print(result.status_code, result.text)


def update(**kwargs):
    project = kwargs['project']
    workload = kwargs['workload']
    if project is not None and workload is not None:
        commond_text = 'kubectl get deployments.apps {} -o yaml -n {} | kubectl replace --force -f -'.format(
            workload, project)
        exit_code = os.system(commond_text)
        print(exit_code, type(exit_code))
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if exit_code == 0:
            print('准备发送消息')
            data = {"msgtype": "text",
                    "text": {"content": "K8S集群 @ {} 进行 \n项目: {} 的 {} 重新部署".format(now, project, workload)}}
        else:
            print('无法发送消息，命令执行错误')
            data = {"msgtype": "text", "text": {
                "content": "K8S集群 @ {} 进行 \n项目: {} 的 {} 重新部署失败，命令执行错误。".format(now, project, workload)}}
        sender(project=project, workload=workload, body=data)

    else:
        print('error 400 , parameter error')


parser = argparse.ArgumentParser()
parser.add_argument('-p', "--project", type=str, help='请输入项目名称')
parser.add_argument('-w', "--workload", type=str, help='请输入工作负载名称')
args = parser.parse_args()

update(project=args.project, workload=args.workload)
