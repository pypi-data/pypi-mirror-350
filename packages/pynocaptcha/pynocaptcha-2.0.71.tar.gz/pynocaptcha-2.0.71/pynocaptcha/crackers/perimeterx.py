
import sys
import warnings
warnings.filterwarnings('ignore')

from typing import Optional, Literal, Union, Tuple, Dict, List

if sys.version_info >= (3, 8):  # pragma: no cover (py38+)
    from typing import Literal
else:  # pragma: no cover (py38+)
    from typing_extensions import Literal

import re
import json
import primp
import random
import time
import uuid

from .typed import Response
from .base import BaseCracker
from .utils import create_session, parse_client_hints


class PerimeterxCracker(BaseCracker):
    
    cracker_name = "perimeterx"
    cracker_version = "universal"    

    """
    perimeterx cracker
    :param tag: px 版本号
    :param href: 触发 perimeterx 验证的页面地址
    :param captcha: 按压验证码参数, 示例: {
        appId: 'PXaOtQIWNf',
        jsClientSrc: '/aOtQIWNf/init.js',
        firstPartyEnabled: true,
        uuid: '013b4cad-ece3-11ee-a877-09542f9a30cf',
        hostUrl: '/aOtQIWNf/xhr',
        blockScript: '/aOtQIWNf/captcha/captcha.js?a=c&u=013b4cad-ece3-11ee-a877-09542f9a30cf&v=&m=0',
        altBlockScript: 'https://captcha.px-cloud.net/PXaOtQIWNf/captcha.js?a=c&u=013b4cad-ece3-11ee-a877-09542f9a30cf&v=&m=0',
        customLogo: 'https://chegg-mobile-promotions.cheggcdn.com/px/Chegg-logo-79X22.png'
    }
    :param user_agent: 请求流程使用 ua, 请使用 chrome 的 ua
    :param headers: 触发验证必须的 headers, 默认 {} 
    :param cookies: 触发验证必须的 cookies, 默认 {}
    :param timeout: 最大破解超时时间
    调用示例:
    cracker = CloudFlareCracker(
        href=href,
        user_token="xxx",
    )
    ret = cracker.crack()
    """
    
    # 必传参数
    must_check_params = ["href"]
    # 默认可选参数
    option_params = {
        "branch": "Master",
        "tag": None,
        "app_id": None,
        "uuid": None,
        "vid": None,
        "modal": False,
        "press": False,
        "captcha": None,
        "captcha_html": None,
        "user_agent": None,
        "did": None,
        "proxy": None,
        "country": None,
        "ip": None,
        "timezone": None,
        "geolocation": None,
        "headers": {},
        "cookies": {},
        "actions": 1,
        "timeout": 30
    }


def crack_perimeterx(
    user_token: str, href: str, app_id: str, proxy: str,
    parse_index: Optional[callable] = None, verifiers: List[callable] = [], max_retry_times: int = 2, 
    show_ad: bool = False, internal_host: bool = True, branch: Optional[str] = None,
    developer_id: Optional[str] = None, cookies: Dict[str, str] = {},
    user_agent: Union[str, Tuple[int, Literal["windows", "macos"], Literal["chrome", "edge"]]] = None,
    region: Literal['jp', 'us', 'tw', 'hk', 'it', 'de', 'es', 'in', 'cn', 'fr', 'tr', 'ru', 'gb', 'ua', 'ca', 'au'] = "hk", 
    debug: bool = True,
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
            version = random.randint(115, 137)
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
        
        extra = {
            'sec-ch-ua': sec_ch_ua,
            'sec-ch-ua-platform': sec_ch_ua_ptf,
            'accept-language': language, 
            'user-agent': user_agent, 
        }
        
        session = create_session(user_agent, proxy)
        origin = "/".join(href.split("/")[0:3])
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
            'accept-language': language, 
            'priority': 'u=0, i'
        }

        resp = session.get(href, headers=headers)
        
        retry_times = 0
        while resp.status_code == 403 and retry_times < max_retry_times:
            try:
                dd_match = re.search(r'var dd=(\{.*?\})', resp.text)
                captcha = json.loads(dd_match[1].replace("'", '"'))
                if captcha.get("t") == "bv":
                    raise Warning("代理被封锁, 请切换代理重试")
            except:
                raise Warning(f"验证异常: {resp.status_code} {resp.text}")
            
            cracker = PerimeterxCracker(
                show_ad=show_ad,
                internal_host=internal_host,
                user_token=user_token,
                developer_id=developer_id,
                branch=branch,
                href=href,           
                app_id=app_id,  
                user_agent=user_agent,
                captcha_html=resp.text,
                cookies=session.get_cookies(origin + "/"),
                proxy=proxy,
                country=region,
                ip=current_ip,
                timezone=timezone,
                geolocation=loc,
                debug=debug
            )
            res = cracker.crack()
            if res:
                extra = cracker.extra()
                cookies = session.get_cookies(origin + "/")
                cookies.update(res['cookies'])
                session = create_session(user_agent, proxy)
                session.set_cookies(origin + "/", cookies)
                if parse_index:
                    resp = session.get(href, headers=headers)
                    retry_times += 1
                else:
                    break            
            else:
                raise Warning("验证失败")
        
        if retry_times == 0:
            cracker = PerimeterxCracker(
                show_ad=show_ad,
                internal_host=internal_host,
                user_token=user_token,
                developer_id=developer_id,
                branch=branch,
                href=href,           
                app_id=app_id,  
                user_agent=user_agent,
                cookies=session.get_cookies(origin + "/"),
                proxy=proxy,
                country=region,
                ip=current_ip,
                timezone=timezone,
                geolocation=loc,
                debug=debug
            )
            res = cracker.crack()
            if res:
                extra = cracker.extra()
                cookies = session.get_cookies(origin + "/")
                cookies.update(res['cookies'])
                session = create_session(user_agent, proxy)
                session.set_cookies(origin + "/", cookies)
            else:
                raise Warning("验证失败")

        global_args = {}
        
        if parse_index:
            parse_index(resp, global_args)
        
        for verifier in verifiers:            
            resp = verifier(session, extra, global_args)

            retry_times = 0
            while resp.status_code == 403 and retry_times < max_retry_times:
                did = extra.get("did")
                
                captcha_args = {}
                try:
                    captcha_args["captcha"] = resp.json()
                except:
                    captcha_args["captcha_html"] = resp.text
                
                res = PerimeterxCracker(
                    show_ad=show_ad,
                    internal_host=internal_host,
                    user_token=user_token,
                    developer_id=developer_id,
                    branch=branch,
                    href=href,           
                    app_id=app_id,     
                    user_agent=user_agent,
                    cookies=session.get_cookies(origin + "/"),
                    **captcha_args,
                    did=did,
                    proxy=proxy,
                    debug=debug
                ).crack()
                if res:
                    cookies = session.get_cookies(origin + "/")
                    cookies.update(res['cookies'])
                    session = create_session(user_agent, proxy)
                    session.set_cookies(origin + "/", cookies)
                    resp = verifier(session, extra, global_args)
                else:
                    raise Warning("验证失败")
                
                retry_times += 1

        return session, resp
    
    except Exception as e:
        if 'client error' in str(e):
            raise Warning('代理错误')
        else:
            raise e
