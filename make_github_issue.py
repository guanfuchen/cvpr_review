# -*- coding: utf-8 -*-
# !!!code is from [make_github_issue.py](https://gist.github.com/JeffPaine/3145490)!!!
import argparse
import getpass
import json
import requests
import os
import time


def make_github_issue(title, body=None, assignee=None, milestone=None, labels=None, USERNAME = 'CHANGEME', PASSWORD = 'CHANGEME', REPO_OWNER = 'CHANGEME', REPO_NAME = 'CHANGEME'):
    """
    Create an issue on github.com using the given parameters.
    :param title: github issue title
    :param body: github issue body
    :param assignee: github issue assignee
    :param milestone: github issue milestone
    :param labels: github issue labels
    :param USERNAME: github username
    :param PASSWORD: github password
    :param REPO_OWNER: github repo owner
    :param REPO_NAME: github repo name
    :return:
    """
    # Our url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    # Create our issue
    issue = {
        'title': title,
        'body': body,
        'assignee': assignee,
        'milestone': milestone,
        'labels': labels,
    }
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        print 'Successfully created Issue "%s"' % title
        return True
    else:
        print 'Could not create Issue "%s"' % title
        print 'Response:', r.content
        return False

class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass()
        setattr(namespace, self.dest, values)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='cvpr crawl setting')
    parser.add_argument('--username', type=str, default='guanfuchen@zju.edu.cn', help='github username [ USERNAME ]')
    parser.add_argument('--password', action=Password, nargs='?', help='Enter your github password [ PASSWORD ]')
    parser.add_argument('--repo_owner', type=str, default='guanfuchen', help='github repo owner [ REPO_OWNER ]')
    parser.add_argument('--repo_name', type=str, default='cvpr_review', help='github  repo name [ REPO_NAME ]')
    parser.add_argument('--year', type=str, default='2017', help='cvpr year [ 2015 2016 2017 2018 ]')
    parser.add_argument('--start_id', type=int, default=0, help='cvpr paper start issue id [ 1 ]')
    args = parser.parse_args()

    if args.password is None:
        # print('missing password')
        exit(0)
    else:
        pass
        # print('password:', args.password)

    # issue_title = 'Graph-Structured Representations for Visual Question Answering'
    # issue_body = '|id|title|author|year|\n|---|---|---|---|\n|1|Graph-Structured Representations for Visual Question Answering|Teney, Damien and Liu, Lingqiao and van den Hengel, Anton|2017|'

    cvpr_file_name = 'cvpr{}/cvpr{}.md'.format(args.year, args.year)
    if not os.path.exists(cvpr_file_name):
        print('misssing file {}'.format(cvpr_file_name))
        exit(0)

    cvpr_file_fp = open(cvpr_file_name, 'rb')
    cvpr_file_content = cvpr_file_fp.readlines()[2:] # for content
    # print('cvpr_file_content:', cvpr_file_content)
    count_id = args.start_id
    # for cvpr_file_content_item_id, cvpr_file_content_item in enumerate(cvpr_file_content):
    print(len(cvpr_file_content))
    while count_id<len(cvpr_file_content):
        cvpr_file_content_item = cvpr_file_content[count_id]
        # print(cvpr_file_content_item)
        cvpr_file_content_item_list = cvpr_file_content_item.split('|')
        # print(cvpr_file_content_item_list)
        bibref_id, title_str_real, author_str_real, year_str_real = cvpr_file_content_item_list[1:5]
        # print(bibref_id)
        # print(title_str_real)
        # print(author_str_real)
        # print(year_str_real)
        issue_title = title_str_real
        issue_body = '|id|title|author|year|\n|---|---|---|---|\n{}'.format(cvpr_file_content_item)
        # print(issue_body)
        issue_flag = make_github_issue(title=issue_title, body=issue_body, assignee=None, milestone=None, labels=['cvpr{}'.format(args.year)], USERNAME=args.username, PASSWORD=args.password, REPO_OWNER=args.repo_owner, REPO_NAME=args.repo_name)
        time.sleep(2)
        if not issue_flag:
            print('end_id:', count_id)
            time.sleep(4)
            break
        else:
            count_id += 1
        # break

    cvpr_file_fp.close()
