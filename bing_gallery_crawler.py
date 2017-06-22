# -*- coding: utf-8 -*-
import json
import re
import requests
import shutil

data_url = 'http://www.bing.com/gallery/home/browsedata?z=0'
# img_detail_base_url = 'http://www.bing.com/gallery/home/imagedetails/%s?z=0'
regex = r'a\.browseData=(.+);}\)\(window, \'BingGallery\'\);'
img_base_url = 'https://az619519.vo.msecnd.net/files/%s_%s.jpg'
resolution = '1366x768'

gallery_data_js = requests.get(data_url)
gallery_data_match = re.search(regex, gallery_data_js.content)
if gallery_data_match:
    gallery_data_json = json.loads(gallery_data_match.group(1))
    img_ids = gallery_data_json['imageIds']
    img_names = gallery_data_json['imageNames']
    short_names = gallery_data_json['shortNames']
    for index in xrange(len(img_ids)):
        # img_detail_url = img_detail_base_url % img_ids[index]
        img_url = img_base_url % (img_names[index], resolution)
        file_name = short_names[index] + '.jpg'
        img_stream = requests.get(img_url, stream=True)
        if img_stream.status_code == 200:
            with open(file_name, 'wb') as fw:
                shutil.copyfileobj(img_stream.raw, fw)
else:
    print "No match!"
