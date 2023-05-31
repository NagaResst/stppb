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
    flag = kwargs['flag']
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if flag is not None:
        print('accept data, send message')
        data = {"msgtype": "text", "text": {
            "content": "在{}，{}".format(now, flag)}}
        sender(body=data)
    elif flag is None and project is not None and workload is not None:
        commond_text = 'kubectl get deployments.apps {} -o yaml -n {} | kubectl replace --force -f -'.format(
            workload, project)
        exit_code = os.system(commond_text)
        text_rep = '{"spec":{"replicas":1}}'
        set_replicas = """kubectl patch deployment {} -p '{}' -n {}""".format(workload, text_rep, project)
        os.system(set_replicas)
        if exit_code == 0:
            print('Preparing to send sucess message')
            data = {"msgtype": "text",
                    "text": {"content": "K8S集群 @ {} 进行 \n项目: {} 的 {} 重新部署".format(now, project, workload)}}
        else:
            print('Execution error, send failed message')
            data = {"msgtype": "text", "text": {
                "content": "K8S集群 @ {} 进行 \n项目: {} 的 {} 重新部署失败，命令执行错误。".format(now, project, workload)}}
        sender(body=data)
    else:
        print('Error 400 , parameter error')


parser = argparse.ArgumentParser()
parser.add_argument('-p', "--project", type=str, required=False, help='请输入项目名称')
parser.add_argument('-w', "--workload", type=str, required=False, help='请输入工作负载名称')
parser.add_argument('-f', '--failed', type=str, required=False, help="此参数标志构建失败，发送失败消息")
args = parser.parse_args()

update(project=args.project, workload=args.workload, flag=args.failed)
