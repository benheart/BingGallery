# -*- coding: utf-8 -*-
import requests
import shutil
import os
from bs4 import BeautifulSoup


def parse_page(url, headers):
    """
    根据 url 下载页面并转换成 soup 对象
    :param url: 页面 url 链接
    :param headers: 请求headers
    :return: soup 对象
    """
    page = requests.get(url, headers=headers).content
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


def parse_pic_date_name_map(soup):
    """
    解析页面，返回当前页面图片 日期 + 名称
    :param soup: 页面 soup 对象
    :return: 图片日期 + 名称字典
    """
    pic_date_name_map = {}
    pic_div_list = soup.find_all('div', attrs={'class': 'card progressive'})
    for pic_div in pic_div_list:
        # 日期
        pic_em = pic_div.find('em', attrs={'class': 't'})
        pic_date = pic_em.text
        # 名称
        pic_a = pic_div.find('a', attrs={'class': 'mark'})
        pic_a_href = pic_a['href']
        pic_url = pic_a_href.split('?')[0]
        pic_path_list = pic_url.split('/')
        pic_name = pic_path_list[len(pic_path_list) - 1]
        pic_date_name_map[pic_date] = pic_name
    return pic_date_name_map


def main():
    """ 爬虫主函数 """
    print '---------- Crawling Start ----------'
    base_page_url = 'https://bing.ioliu.cn'
    base_pic_url = 'http://h1.ioliu.cn/bing/%s_%s.jpg'
    all_pic_date_name_map = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    # 下载页面并转换成 soup 对象
    soup = parse_page(base_page_url, headers)
    # 获取总页数
    total_page_num = parse_page_num(soup)
    for page in xrange(total_page_num):
        print 'Processing page: %s' % (page + 1)
        page_url = base_page_url + '/?p=' + str(page + 1)
        soup = parse_page(page_url, headers=headers)
        # 获取当前页面所有图片名
        pic_date_name_map = parse_pic_date_name_map(soup)
        all_pic_date_name_map.update(pic_date_name_map)
    # 遍历所有图片名，解析并保存图片
    resolution = '1920x1080'
    # 创建图片保存的目录
    file_dir = './gallery/'
    os.mkdir(file_dir)
    for pic_date, pic_name in all_pic_date_name_map.items():
        img_url = base_pic_url % (pic_name, resolution)
        pic_file_name = pic_date + '_' + pic_name + '_' + resolution + '.jpg'
        print 'Get %s from %s' % (pic_file_name, img_url)
        img_stream = requests.get(img_url, stream=True, headers=headers)
        if img_stream.status_code == 200:
            with open(file_dir + pic_file_name, 'wb') as fw:
                shutil.copyfileobj(img_stream.raw, fw)
    # 图片爬取结束
    print '---------- Crawling End ----------'


if __name__ == '__main__':
    main()
