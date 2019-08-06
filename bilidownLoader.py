import requests
import re
import json
from requests import RequestException
import time
import random
from bs4 import BeautifulSoup

class bilibili():
    def __init__(self,url,save_dir,index):
        self.getHtmlHeaders={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q = 0.9'
        }
        self.downloadVideoHeaders={
            'Origin': 'https://www.bilibili.com',
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        self.url=url
        self.save_dir=save_dir
        self.index=index

    def getHtml(self):
        try:
            response = requests.get(url=self.url, headers= self.getHtmlHeaders)
            print(response.status_code)
            if response.status_code == 200:
                return response.text
        except RequestException:
            print('请求Html错误:')

    def parseHtml(self,html):
        soup = BeautifulSoup(html,'html.parser')
        listul=soup.find_all('ul',class_="list-box")

        pattern = r'\<script\>window\.__playinfo__=(.*?)\</script\>'
        result = re.findall(pattern, html)[0]
        pattern2 = r'\<script\>window\.__INITIAL_STATE__=(.*?);\(function\(\)'
        result2 = re.findall(pattern2, html)[0]
        temp2 = json.loads(result2)
        video_title=temp2['videoData']['pages'][self.index]['part']
        temp = json.loads(result)
        video_url = temp['data']['dash']['video'][0]['baseUrl']
        audio_url = temp['data']['dash']['audio'][0]['baseUrl']
        return {'title': video_title,'videourl': video_url,'audiourl': audio_url}

    def download_video(self,video):
        title=video['title']
        video_url = video['videourl']
        filename = self.save_dir+title +'_video.flv'
        with open(filename, "wb") as f:
            f.write(requests.get(url=video_url, headers=self.downloadVideoHeaders, stream=True, verify=False).content)
        
        audio_url = video['audiourl']
        filename = self.save_dir+title +'_audio.wv'
        with open(filename, "wb") as f:
            f.write(requests.get(url=audio_url, headers=self.downloadVideoHeaders, stream=True, verify=False).content)

    def run(self):
        self.download_video(self.parseHtml(self.getHtml()))

if __name__ == '__main__':
    save_dir='E:\\bilibili马哲视频\\'
    for i in range(3,41):
        print('i = '+str(i))
        url='https://www.bilibili.com/video/av61799427/?p='+str(i+1)
        bilibili(url,save_dir,i).run()
        time.sleep(random.randint(5,30))