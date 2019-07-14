### 爬虫->qq音乐

爬取后来为了scrapy爬取方便,利用文件进行配置了

1. qq_com.py 爬取歌单名单
2. qqmusic_list.py 流行热歌
3. qqmusic_singer.py 歌手



### 技术点

没有使用什么加密,考察的是数据采集的完整性.数据由其他的访问中得到

数据由多次请求返回,需要多次使用callback

> yield scrapy.Request(url, callback=self.parse_music, meta={'name': songname})

