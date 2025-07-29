# -*- coding: UTF-8 -*-

import sys
import re
import random
import requests
import primp
import time
import uuid
from loguru import logger

from typing import Optional, Literal, Union, Tuple, Dict

if sys.version_info >= (3, 8):  # pragma: no cover (py38+)
    from typing import Literal
else:  # pragma: no cover (py38+)
    from typing_extensions import Literal

from .typed import Response

from .utils import create_session, parse_client_hints
from .base import BaseCracker


class AkamaiV2Cracker(BaseCracker):
    
    cracker_name = "akamai"
    cracker_version = "v2"    

    """
    akamai v2 cracker
    :param href: 触发验证的页面地址
    :param api: akamai 提交 sensor_data 的地址
    :param telemetry: 是否 headers 中的 telemetry 参数验证形式, 默认 false
    :param cookies: 请求 href 首页返回的 cookie _abck, bm_sz 值, 传了 api 参数必须传该值, 示例: { "value": "_abck=xxx; bm_sz=xxx", "uri": "https://example.com" }
    :param device: 请求流程使用的设备类型, 可选 pc/mobile, 默认 mobile
    调用示例:
    cracker = AkamaiV2Cracker(
        user_token="xxx",
        href="xxx",
        api="xxx",
        
        # debug=True,
        # proxy=proxy,
    )
    ret = cracker.crack()
    """
    
    # 必传参数
    must_check_params = ["href"]
    # 默认可选参数
    option_params = {
        "branch": "Master",
        "api": "",
        "telemetry": False,
        "uncheck": False,
        "sec_cpt_provider": None,
        "sec_cpt_script": None,
        "sec_cpt_key": None,
        "sec_cpt_challenge": {},
        "sec_cpt_host": None,
        "sec_cpt_html": None,
        "sec_cpt_duration": None,
        "sec_cpt_src": None,
        "sec_cpt_html": None,
        "proxy": None,
        "cookies": {},
        "country": None,
        "ip": None,
        "timezone": None,
        "geolocation": None,
        "user_agent": None,
        "timeout": 30
    }

    
def crack_akamai_v3(
    user_token: str, requests_args: Dict[str, str], proxy: str, 
    other_requests: Optional[callable] = None, branch: Optional[str] = None,
    internal_host: bool = True, developer_id: Optional[str] = None,
    user_agent: Union[str, Tuple[int, Literal["windows", "macos"], Literal["chrome", "edge"]]] = None,
    cookies: Dict[str, str] = {},
    region: Literal['jp', 'us', 'tw', 'hk', 'it', 'de', 'es', 'in', 'cn', 'fr', 'tr', 'ru', 'gb', 'ua', 'ca', 'au'] = "hk", 
    debug: bool = False
) -> Tuple[primp.Client, Response]:
    try:
        language = {
            "jp": "ja-JP,ja;q=0.9",
            "us": "en-US,en;q=0.9",
            "tw": "zh-TW,zh;q=0.9",
            "hk": "zh-HK,zh;q=0.9",
            "it": "it-IT,it;q=0.9",
            "de": "de-DE,de;q=0.9",
            "es": "es-ES,es;q=0.9",
            "in": "en-IN,en;q=0.9",
            "cn": "zh-CN,zh;q=0.9",
            "fr": "fr-FR,fr;q=0.9",
            "tr": "tr-TR,tr;q=0.9",
            "ru": "ru-RU,uk;q=0.9",
            "gb": "en-GB,en;q=0.9",
            "ua": "uk-UA,uk;q=0.9",
            "ca": "en-US,en;q=0.9",
            "au": "en-AU,en;q=0.9"
        }.get(region, "zh-CN,zh;q=0.9")

        if not user_agent:
            version = random.randint(128, 137)
            user_agent = random.choice([
                f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36",
                f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36',
                f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36 Edg/{version}.0.0.0',
                f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36 Edg/{version}.0.0.0",
            ])

        if isinstance(user_agent, tuple):
            user_agent_version, user_agent_os, user_agent_brand = user_agent        
            user_agent = {
                "macos": {
                    "chrome": f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{user_agent_version}.0.0.0 Safari/537.36',
                    "edge": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{user_agent_version}.0.0.0 Safari/537.36 Edg/{user_agent_version}.0.0.0",
                },
                "windows": {
                    "chrome": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{user_agent_version}.0.0.0 Safari/537.36",
                    "edge": f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{user_agent_version}.0.0.0 Safari/537.36 Edg/{user_agent_version}.0.0.0',
                },
            }[user_agent_os][user_agent_brand]
            
        sec_ch_ua_ptf = '"macOS"' if 'Mac' in user_agent else '"Windows"'
        sec_ch_ua = parse_client_hints(user_agent)
        
        href = requests_args["referer"]
        origin = "/".join(href.split("/")[0:3])
        session = create_session(user_agent, proxy)
        if cookies:
            session.set_cookies(origin + "/", cookies)
            
        session.set_cookies(origin + "/", { f"Hm_lpvt_{str(uuid.uuid4()).replace('-', '')}": str(int(time.time())) })    
        try:
            resp = session.get("https://ipinfo.io/json", headers={
                "user-agent": f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            }, timeout=5).json()
        except:
            raise Warning("代理超时")

        current_ip = resp.get("ip")
        timezone = resp.get("timezone")
        loc = resp.get("loc")

        href = requests_args["referer"]
        headers = {
            'sec-ch-ua': sec_ch_ua, 
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 
            'upgrade-insecure-requests': '1', 
            'sec-ch-ua-mobile': '?0', 
            'user-agent': user_agent, 
            'sec-ch-ua-platform': sec_ch_ua_ptf,
            'Sec-Fetch-Site': 'none', 
            'Sec-Fetch-Mode': 'navigate', 
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': language, 
            'priority': 'u=0, i'
        }

        response = session.get(href, headers=headers)

        if 'Oops, Something Went Wrong.' in response.text:
            raise Warning('ip 被 ban, 切 ip 重试')

        nocaptcha_host = "api.nocaptcha.cn" if internal_host else "api.nocaptcha.io"
        if "var chlgeId = ''" in response.text:
            if debug:
                logger.debug('触发 bm_sc 模式')
            
            bm_sc_src = re.search(r'src="(.*?)"', response.text)[1]

            resp = requests.post(
                f'http://{nocaptcha_host}/api/wanda/akamai/v2', headers={
                    'user-token': user_token,
                    **({ "Developer-Id": developer_id } if developer_id else {})
                }, json={
                    'href': href,
                    'bm_sc_src': bm_sc_src,
                    'cookies': session.get_cookies(origin + "/"),
                    'user_agent': user_agent,
                    'proxy': proxy,
                    'country': region,
                    'ip': current_ip,
                    'timezone': timezone,
                    'geolocation': loc,
                }
            ).json()
            if debug:
                logger.debug(f"bm_sc 模式验证结果: {resp}")
            if resp["status"]:                
                session = create_session(user_agent, proxy)
                session.set_cookies(origin + "/", resp["data"])
                response = session.get(href, headers=headers)
            else:
                raise Warning(f'akamai bm_sc 验证失败, id: {resp["id"]}, err: {resp["msg"]}')
            
        api = requests_args.get("api")
        if not api:
            try:
                apis = re.findall("type=\"text\/javascript\"  src\=\"((?:\/[A-Za-z0-9\-\_\+]*?)+)\"\>\<\/script\>", response.text)
                if not apis:
                    apis = re.findall("nonce=\"[a-f0-9]{32}\" src\=\"((?:\/[A-Za-z0-9\-\_\+]*?)+)\"\>\<\/script\>", response.text)
                if not apis:
                    raise Warning('api 查找失败: ' + response.text)
                api = apis[0]
                if not api.startswith("http"):
                    api = origin + api
                requests_args["api"] = api
            except:
                raise Warning('api 查找失败: ' + response.text)
        
        headers = {
            'sec-ch-ua': sec_ch_ua,
            'sec-ch-ua-mobile': '?0',
            'user-agent': user_agent,
            'sec-ch-ua-platform': sec_ch_ua_ptf,
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-dest': 'script',
            'referer': href,
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': language,
            'priority': 'u=1',
        }

        api_response = session.get(api, headers=headers)
        if api_response.status_code != 200:
            raise Warning("脚本请求失败")

        if other_requests:
            other_requests(session, {
                'sec-ch-ua': sec_ch_ua,
                'user-agent': user_agent,
                'sec-ch-ua-platform': sec_ch_ua_ptf,
                'accept-language': language,
            }, requests_args)

        for k, v in requests_args.items():
            if isinstance(v, dict):
                for k1, v1 in v.items():
                    if callable(v1):
                        requests_args[k][k1] = v1(response)
        
        if branch is not None:
            requests_args["branch"] = branch
        
        sub_domain = '.' + '.'.join(href.split('/')[2].split('.')[-2:])
        
        resp = requests.post(
            f'http://{nocaptcha_host}/api/wanda/akamai/v3', headers={
                'user-token': user_token,
                **({ "Developer-Id": developer_id } if developer_id else {})
            }, json={
                **requests_args,
                'api_headers': dict(api_response.headers),
                'cookies': [
                    {
                        'name': name,
                        'value': value,
                        'domain': sub_domain
                    } for name, value in session.get_cookies(origin + "/").items()
                ],
                'user_agent': user_agent,
                'proxy': proxy,
                'country': region,
                'ip': current_ip,
                'timezone': timezone,
                'geolocation': loc,
            }
        ).json()
        if debug:
            logger.debug(f"akamai v3 验证结果: {resp}")
            
        if resp["status"]:
            session.set_cookies(origin + "/", resp["data"]["cookies"])
            return session, resp
        else:
            raise Warning(f'akamai v3 验证失败, id: {resp["id"]}, err: {resp["msg"]}')

    except Exception as e:
        if 'client error' in str(e):
            raise Warning('代理错误')
        else:
            raise e
