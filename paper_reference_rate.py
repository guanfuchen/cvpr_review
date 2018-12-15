# -*- coding: utf-8 -*-
import argparse
import os
import time

import requests
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='cvpr paper reference rate check')
    parser.add_argument('--year', type=str, default='2017', help='cvpr year [ 2015 2016 2017 2018 ]')
    parser.add_argument('--proxy', type=int, default=1087, help='proxy port [ 1087 8123]')
    args = parser.parse_args()

    cvpr_file_name = 'cvpr{}/cvpr{}.md'.format(args.year, args.year)
    if not os.path.exists(cvpr_file_name):
        print('misssing file {}'.format(cvpr_file_name))
        exit(0)

    cvpr_file_fp = open(cvpr_file_name, 'rb')
    cvpr_file_content = cvpr_file_fp.readlines()[2:] # for content


    proxies = {"http": "http://127.0.0.1:{}/".format(args.proxy), "https": "http://127.0.0.1:{}/".format(args.proxy)}

    cvpr_listmd_file_name = 'cvpr{}/cvpr{}_rate.md'.format(args.year, args.year)
    cvpr_listmd_file = open(cvpr_listmd_file_name, 'wb')
    cvpr_listmd_file.write('|id|title|author|year|rate|\n')
    cvpr_listmd_file.write('|---|---|---|---|---|\n')

    for cvpr_file_content_item in cvpr_file_content:
        cvpr_file_content_item_list = cvpr_file_content_item.split('|')
        # print(cvpr_file_content_item_list)
        bibref_id, title_str_real, author_str_real, year_str_real = cvpr_file_content_item_list[1:5]
        # print(bibref_id)
        print(title_str_real)
        # print(author_str_real)
        # print(year_str_real)
        content = requests.get('https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={}'.format(title_str_real), proxies=proxies).content
        # print(content)
        search_reference_rate = re.search('Cited by.*</a> <a href', content, flags=0)
        # print('search_reference_rate:', search_reference_rate)
        reference_rate = 0
        if search_reference_rate:
            search_reference_rate_id_start = 9
            search_reference_rate_id_end = search_reference_rate.group().find('<')
            reference_rate = search_reference_rate.group()[search_reference_rate_id_start:search_reference_rate_id_end]
            print('reference_rate:', reference_rate)
        cvpr_listmd_file.write('|{}|{}|{}|{}|{}|\n'.format(bibref_id, title_str_real, author_str_real, year_str_real, reference_rate))
        # break
        time.sleep(3)

    cvpr_file_fp.close()
    cvpr_listmd_file.close()
