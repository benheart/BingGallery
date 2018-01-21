# -*- coding: utf-8 -*-
import requests
import shutil
import os
from bs4 import BeautifulSoup


def parse_page(url):
    """
    根据 url 下载页面并转换成 soup 对象
    :param url: 页面 url 链接
    :return: soup 对象
    """
    page = requests.get(url).content
    return BeautifulSoup(page, 'html.parser')


def parse_page_num(soup):
    """
    解析页面，返回总页数
    :param soup: 页面 soup 对象
    :return: 总页数
    """
    total_page_num = 0
    page_div = soup.find('div', attrs={'class': 'page'})
    if page_div and page_div.span:
        page_span_str = page_div.span.string
        page_num_list = page_span_str.split(' / ')
        if len(page_num_list) == 2:
            total_page_num = int(page_num_list[1])
    return total_page_num


def parse_pic_names(soup):
    """
    解析页面，返回当前页面图片名
    :param soup: 页面 soup 对象
    :return: 图片名称列表
    """
    pic_names = []
    pic_a_list = soup.find_all('a', attrs={'class': 'mark'})
    for pic_a in pic_a_list:
        pic_a_href = pic_a['href']
        pic_url = pic_a_href.split('?')[0]
        pic_path_list = pic_url.split('/')
        pic_name = pic_path_list[len(pic_path_list) - 1]
        pic_names.append(pic_name)
    return pic_names


def main():
    """ 爬虫主函数 """
    print '---------- Crawling Start ----------'
    base_page_url = 'https://bing.ioliu.cn'
    base_pic_url = 'http://h1.ioliu.cn/bing/%s_%s.jpg'
    all_pic_names = []
    # 下载页面并转换成 soup 对象
    soup = parse_page(base_page_url)
    # 获取总页数
    total_page_num = parse_page_num(soup)
    for page in xrange(total_page_num):
        print 'Processing page: %s' % (page + 1)
        page_url = base_page_url + '/?p=' + str(page + 1)
        soup = parse_page(page_url)
        # 获取当前页面所有图片名
        pic_names = parse_pic_names(soup)
        all_pic_names.extend(pic_names)
    # 遍历所有图片名，解析并保存图片
    resolution = '1920x1080'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    # 创建图片保存的目录
    file_dir = './gallery/'
    os.mkdir(file_dir)
    for pic_name in all_pic_names:
        img_url = base_pic_url % (pic_name, resolution)
        pic_file_name = pic_name + '_' + resolution + '.jpg'
        print 'Get %s from %s' % (pic_file_name, img_url)
        img_stream = requests.get(img_url, stream=True, headers=headers)
        if img_stream.status_code == 200:
            with open(file_dir + pic_file_name, 'wb') as fw:
                shutil.copyfileobj(img_stream.raw, fw)
    # 图片爬取结束
    print '---------- Crawling End ----------'

if __name__ == '__main__':
    main()
