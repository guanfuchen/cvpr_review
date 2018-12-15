# -*- coding: utf-8 -*-
import argparse
import re
from bs4 import BeautifulSoup
import requests
import os


# python cvpr_crawl.py --year 2017
# cd cvpr2017
# wget -c -i cvpr2017_download_url.txt
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='cvpr crawl setting')
    parser.add_argument('--year', type=str, default='2018', help='cvpr year [ 2015 2016 2017 2018 ]')
    args = parser.parse_args()

    year = args.year
    offline_html_default_file_name = 'cvpr{}/CVPR{}.py'.format(year, year)
    cvpr_download_dir = os.path.dirname(offline_html_default_file_name)
    if not os.path.exists(cvpr_download_dir):
        os.makedirs(cvpr_download_dir)

    content = ''
    if not os.path.exists(offline_html_default_file_name):
        print('not exists:' + offline_html_default_file_name)
        proxies = None
        # proxies = {"http": "http://127.0.0.1:1087/"}
        content = requests.get('http://openaccess.thecvf.com/CVPR' + year + '.py', proxies=proxies).content
        offline_html_default_file = open(offline_html_default_file_name, 'wb')
        offline_html_default_file.write(content)
        offline_html_default_file.close()
    else:
        print('exists:' + offline_html_default_file_name)
        offline_html_default_file = open(offline_html_default_file_name, 'rb')
        content = offline_html_default_file.read()
        offline_html_default_file.close()

    cvpr_download_file_name = 'cvpr{}/cvpr{}_download_url.txt'.format(year, year)
    cvpr_download_file = open(cvpr_download_file_name, 'wb')

    cvpr_listmd_file_name = 'cvpr{}/cvpr{}.md'.format(year, year)
    cvpr_listmd_file = open(cvpr_listmd_file_name, 'wb')
    cvpr_listmd_file.write('|id|title|author|year|\n')
    cvpr_listmd_file.write('|---|---|---|---|\n')

    soup = BeautifulSoup(content, "html.parser")
    bibref_id = 0
    for element in soup.find_all('dd'):
        element_str = str(element)
        if 'class="bibref"' in element_str:
            bibref_strs = re.findall('<div class="bibref">[\s\S]*?</div>', element_str, re.I)
            pdf_href_strs = re.findall('href="[\s\S]*?"', element_str, re.I)
            # print(element_str)
            pdf_href_str_real = None
            if len(pdf_href_strs) != 0:
                pdf_href_str_real = 'http://openaccess.thecvf.com/' + pdf_href_strs[0][6:-1]
                print pdf_href_str_real
                cvpr_download_file.write(pdf_href_str_real + '\n')
            for bibref_str in bibref_strs:
                bibref_id += 1
                # print(element_str)
                author_strs = re.findall('author = {[\s\S]*?<br/>', bibref_str, re.I)
                title_strs = re.findall('\ntitle = {[\s\S]*?<br/>', bibref_str, re.I)
                month_strs = re.findall('month = {[\s\S]*?<br/>', bibref_str, re.I)
                year_strs = re.findall('year = {[\s\S]*?<br/>', bibref_str, re.I)
                author_str = None
                title_str = None
                month_str = None
                year_str = None
                author_str_real = None
                title_str_real = None
                month_str_real = None
                year_str_real = None
                if len(author_strs) !=0:
                    author_str = author_strs[0]
                    # print(author_str)
                    author_str_reals = re.findall('{[\s\S]*?}', author_str, re.I)
                    if len(author_str_reals) !=0:
                        author_str_real = author_str_reals[0][1:-1]
                        # print(author_str_real)
                if len(title_strs) !=0:
                    title_str = title_strs[0]
                    title_str_reals = re.findall('{[\s\S]*?}', title_str, re.I)
                    if len(title_str_reals) !=0:
                        title_str_real = title_str_reals[0][1:-1]
                        # print(title_str_real)
                        # print(title_str)
                if len(month_strs) !=0:
                    month_str = month_strs[0]
                    month_str_reals = re.findall('{[\s\S]*?}', month_str, re.I)
                    if len(month_str_reals) !=0:
                        month_str_real = month_str_reals[0][1:-1]
                        # print(month_str_real)
                        # print(month_str)
                if len(year_strs) !=0:
                    year_str = year_strs[0]
                    year_str_reals = re.findall('{[\s\S]*?}', year_str, re.I)
                    if len(year_str_reals) !=0:
                        year_str_real = year_str_reals[0][1:-1]
                        # print(year_str_real)
                        # print(year_str)
                if author_str_real is not None and title_str_real is not None and month_str_real is not None and year_str_real is not None and pdf_href_str_real is not None:
                    pass
                    print(author_str_real)
                    print(title_str_real)
                    print(month_str_real)
                    print(year_str_real)
                    cvpr_listmd_file.write('|{}|{}|{}|{}|\n'.format(bibref_id, title_str_real, author_str_real, year_str_real))
    cvpr_download_file.close()
    cvpr_listmd_file.close()
