# -*- coding: utf-8 -*-

import re, requests, urlparse, json
from resources.lib.modules import client, source_utils
from resources.lib.modules import jsunpack, log_utils
from resources.lib.modules import directstream


def more_rapidvideo(link, hostDict, lang, info):
    if "rapidvideo.com" in link:
        sources = []
        try:
            headers = {'User-Agent': client.agent()}
            response = requests.get(link, headers=headers).content
            test = re.findall("""(https:\/\/www.rapidvideo.com\/e\/.*)">""", response)
            numGroups = len(test)
            for i in range(1, numGroups):
                url = test[i]
                valid, host = source_utils.is_host_valid(url, hostDict)
                q = source_utils.check_sd_url(url)
                sources.append({'source': host, 'quality': q, 'language': lang, 'url': url, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return []
    return []


def more_vidnode(link, hostDict):
    if "vidnode.net" in link:
        sources = []  # By Shellc0de
        try:
            headers = {'Host': 'vidnode.net',
                   'User-Agent': client.agent(),
                   'Upgrade-Insecure-Requests': '1',
                   'Accept-Language': 'en-US,en;q=0.9'
            }
            response = client.request(link, headers=headers, timeout=5)
            urls = re.findall('''\{file:\s*['"]([^'"]+).*?label:\s*['"](\d+\s*P)['"]''', response, re.DOTALL | re.I)
            if urls:
                for url, qual in urls:
                    quality, info = source_utils.get_release_quality(qual, url)
                    host = url.split('//')[1].replace('www.', '')
                    host = host.split('/')[0].lower()  # 'CDN'
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': True, 'debridonly': False})
            return sources
        except:
            return []
    return []


def more_vidlink(link, hostDict):
    if "vidlink.org" in link:
        sources = []  # By Shellc0de
        try:
            ua = {'User-Agent': client.agent()}
            postID = link.split('/embed/')[1]
            post_link = 'https://vidlink.org/embed/update_views'
            payload = {'postID': postID}
            headers = ua
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Referer'] = link
            ihtml = client.request(post_link, post=payload, headers=headers)
            linkcode = jsunpack.unpack(ihtml).replace('\\', '')
            try:
                extra_link = re.findall(r'var oploadID="(.+?)"', linkcode)[0]
                oload = 'https://openload.co/embed/' + extra_link
                sources.append({'source': 'openload.co', 'quality': '1080p', 'language': 'en', 'url': oload, 'direct': False, 'debridonly': False})
            except Exception:
                pass
            links = re.findall(r'var file1="(.+?)"', linkcode)[0]
            stream_link = links.split('/pl/')[0]
            headers = {'Referer': 'https://vidlink.org/', 'User-Agent': client.agent()}
            response = client.request(links, headers=headers)
            urls = re.findall(r'[A-Z]{10}=\d+x(\d+)\W[A-Z]+=\"\w+\"\s+\/(.+?)\.', response)
            if urls:
                for qual, url in urls:
                    url = stream_link + '/' + url + '.m3u8'
                    quality, info = source_utils.get_release_quality(qual, url)
                    sources.append({'source': 'GVIDEO', 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': True, 'debridonly': False})
            return sources
        except:
            return []
    return []


def more_gomo(link, hostDict):
    if "gomostream.com" in link:
        sources = []  # By Mpie
        try:
            gomo_link = 'https://gomostream.com/decoding_v3.php'
            User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            result = client.request(link)
            tc = re.compile('tc = \'(.+?)\';').findall(result)[0]
            if (tc):
                token = re.compile('"_token": "(.+?)",').findall(result)[0]
                post = {'tokenCode': tc, '_token': token}
                def tsd(tokenCode):
                    _13x48X = tokenCode
                    _71Wxx199 = _13x48X[4:18][::-1]
                    return _71Wxx199 + "18" + "432782"
                headers = {'Host': 'gomostream.com', 'Referer': link, 'User-Agent': User_Agent, 'x-token': tsd(tc)}
                result = client.request(gomo_link, XHR=True, post=post, headers=headers)
                urls = json.loads(result)
                for url in urls:
                    if 'gomostream' in url:
                        continue
                        #sources.append({'source': 'CDN', 'quality': 'SD', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                    else:
                        quality, info = source_utils.get_release_quality(url, url)
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return []
    return []


def more_cdapl(link, hostDict, lang, info):
    if "cda.pl" in link:
        sources = []
        try:
            headers = {'User-Agent': client.agent()}
            response = requests.get(link, headers=headers).content
            test = client.parseDOM(response, 'div', attrs={'class': 'wrapqualitybtn'})
            urls = client.parseDOM(test, 'a', ret='href')
            if urls:
                for url in urls:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    q = source_utils.check_sd_url(url)
                    direct = re.findall("""file":"(.*)","file_cast""", requests.get(url, headers=headers).content)[0].replace("\\/", "/")
                    sources.append({'source': 'CDA', 'quality': q, 'language': lang, 'url': direct, 'info': info, 'direct': True, 'debridonly': False})
            return sources
        except:
            return []
    return []


"""Example...

more = False
for source in more_sources.more_cdapl(video_link[0],hostDict,lang,info[0]):
    sources.append(source)
    more = True
for source in more_sources.more_rapidvideo(video_link[0],hostDict,lang,info[0]):
    sources.append(source)
    more = True
if not more:
    sources.append({'source': host, 'quality': quality, 'language': lang, 'url': video_link[0], 'info': info[0], 'direct': False, 'debridonly': False})

"""


