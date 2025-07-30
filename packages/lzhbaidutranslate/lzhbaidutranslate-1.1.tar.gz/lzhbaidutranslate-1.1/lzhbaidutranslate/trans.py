import requests
import random
import aiohttp
import asyncio
from hashlib import md5

def baidu_translate(appid:str, appkey:str, query:list[str]|str, from_lang:str="auto", to_lang:str="zh"):
    """
    #### 参数 :
    - `appid` : APP ID
    - `appkey` : 密钥
    - `query` : 要翻译的字符串或字符串列表
    - `from_lang` : 源语言
    - `to_lang` : 目标语言
    
    #### return :
    - 翻译结果，字符串或字符串列表，结构与`query`对应
    - 如果请求不成功，则返回`None`
    
    #### [常见语种代码对照](https://api.fanyi.baidu.com/doc/21#:~:text=%E5%8F%AF%E8%83%BD%E5%AD%98%E5%9C%A8%E8%AF%AF%E5%B7%AE%E3%80%82-,%E5%B8%B8%E8%A7%81%E8%AF%AD%E7%A7%8D%E5%88%97%E8%A1%A8,-%E5%90%8D%E7%A7%B0)
    | 语种 | 自动 | 中 | 英 | 日 | 韩 |
    | - | - | - | - | - | - |
    | 代码 | `auto` | `zh` | `en` | `jp` | `kor` |
    """
    if isinstance(query, list):
        q = '\n'.join(query)
    else:
        q = query

    # Generate salt and sign
    salt = random.randint(32768, 65536)
    sign = md5((appid + q + str(salt) + appkey).encode("utf-8")).hexdigest()
    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': q, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
    # Send request
    url = 'https://api.fanyi.baidu.com/api/trans/vip/translate'
    res = requests.post(url, params=payload, headers=headers).json()

    ret={}  
    if "error_code" in res:
        return None
    else: 
        if isinstance(query, list):
            ret = [tr["dst"] for tr in res["trans_result"]]
        else:
            ret = res["trans_result"][0]["dst"]
    return ret

async def baidu_translate_async(appid: str, appkey: str, query: list[str] | str, from_lang: str = "auto", to_lang: str = "zh"):
    """
    `baidu_translate()`的异步版
    #### 参数 :
    - `appid` : APP ID
    - `appkey` : 密钥
    - `query` : 要翻译的字符串或字符串列表
    - `from_lang` : 源语言
    - `to_lang` : 目标语言
    
    #### return :
    - 翻译结果，字符串或字符串列表，结构与`query`对应
    - 如果请求不成功，则返回`None`
    
    #### [常见语种代码对照](https://api.fanyi.baidu.com/doc/21#:~:text=%E5%8F%AF%E8%83%BD%E5%AD%98%E5%9C%A8%E8%AF%AF%E5%B7%AE%E3%80%82-,%E5%B8%B8%E8%A7%81%E8%AF%AD%E7%A7%8D%E5%88%97%E8%A1%A8,-%E5%90%8D%E7%A7%B0)
    | 语种 | 自动 | 中 | 英 | 日 | 韩 |
    | - | - | - | - | - | - |
    | 代码 | `auto` | `zh` | `en` | `jp` | `kor` |
    """
    if isinstance(query, list):
        q = '\n'.join(query)
    else:
        q = query

    salt = random.randint(32768, 65536)
    sign = md5((appid + q + str(salt) + appkey).encode("utf-8")).hexdigest()

    url = 'https://api.fanyi.baidu.com/api/trans/vip/translate'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': q, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=payload, headers=headers) as response:
            res = await response.json()
    
    if "error_code" in res:
        return None
    else: 
        if isinstance(query, list):
            return [tr["dst"] for tr in res["trans_result"]]
        else:
            return res["trans_result"][0]["dst"]

if __name__ == '__main__':
    query = 'Hello World! This is 1st sentence. This is 2nd sentence.'
    querys = ['Hello World! This is 1st sentence.','This is 2nd sentence.']
    
    # Set your own appid/appkey.
    appid = ""
    appkey = ""
    
    print(baidu_translate(appid, appkey, query))
    print(baidu_translate(appid, appkey, querys))
    
    async def main():
        print(await baidu_translate_async(appid, appkey, query))
        print(await baidu_translate_async(appid, appkey, querys))

    asyncio.run(main())
