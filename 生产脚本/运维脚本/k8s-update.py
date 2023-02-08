#! /usr/bin/python3
import argparse
import datetime
import json
import os

import requests


def sender(body=None):
    url = 'https://oapi.dingtalk.com/robot/send?access_token='
    header = {"Content-Type": "application/json"}
    requests.post(url=url, data=json.dumps(body), headers=header)
    print('Message has been sent')


def update(**kwargs):
    project = kwargs['project']
    workload = kwargs['workload']
    if project is not None and workload is not None:
        text_rep = '{"spec":{"replicas":1}}'
        set_replicas = """kubectl patch deployment {} -p '{}' -n {}""".format(workload, text_rep, project)
        os.system(set_replicas)
        commond_text = 'kubectl get deployments.apps {} -o yaml -n {} | kubectl replace --force -f -'.format(
            workload, project)
        exit_code = os.system(commond_text)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if exit_code == 0:
            print('Preparing to send message')
            data = {"msgtype": "text",
                    "text": {"content": "K8S集群 @ {} 进行 \n项目: {} 的 {} 重新部署".format(now, project, workload)}}
        else:
            print('Execution error, can not send message')
            data = {"msgtype": "text", "text": {
                "content": "K8S集群 @ {} 进行 \n项目: {} 的 {} 重新部署失败，命令执行错误。".format(now, project, workload)}}
        sender(body=data)
    else:
        print('Error 400 , parameter error')


parser = argparse.ArgumentParser()
parser.add_argument('-p', "--project", type=str, help='请输入项目名称')
parser.add_argument('-w', "--workload", type=str, help='请输入工作负载名称')
args = parser.parse_args()

update(project=args.project, workload=args.workload)
