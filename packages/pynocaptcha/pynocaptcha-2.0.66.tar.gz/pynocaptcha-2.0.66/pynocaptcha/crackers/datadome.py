# -*- coding: UTF-8 -*-

import re
import sys
import random
import primp
import json
import uuid
import time

from typing import Optional, Literal, List, Tuple, Dict

if sys.version_info >= (3, 8):  # pragma: no cover (py38+)
    from typing import Literal
else:  # pragma: no cover (py38+)
    from typing_extensions import Literal

from .typed import Response
from .base import BaseCracker
from .utils import create_session, parse_client_hints


class DatadomeCracker(BaseCracker):
    cracker_name = "datadome"
    cracker_version = "universal"

    """
    datadome
    :param href: 触发验证的页面地址
    调用示例:
    cracker = KasadaCtCracker(
        user_token="xxx",
        href="https://rendezvousparis.hermes.com/client/register",
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        proxy="user:pass@ip:port",
        debug=True,
    )
    ret = cracker.crack()
    """

    # 必传参数
    must_check_params = ["href", "proxy"]
    # 默认可选参数
    option_params = {
        "branch": "Master",
        "captcha": None,
        "captcha_url": None,
        "captcha_html": None,
        "js_url": None,
        "js_key": None,
        "did": None,
        "user_agent": None,
        "interstitial": False,
        "accept_language": "en-US,en;q=0.9",
        "country": None,
        "ip": None,
        "timezone": None,
        "geolocation": None,
        "html": False,
        "timeout": 30
    }

    def request(self):
        country = self.wanda_args.get("country")
        _ip = self.wanda_args.get("ip")
        timezone = self.wanda_args.get("timezone")
        geolocation = self.wanda_args.get("geolocation")
        
        origin = "/".join(self.href.split("/")[0:3])
        if not self.interstitial and not self.js_key and not self.captcha and not self.captcha_url and not self.captcha_html:
            print(self.user_agent)
            if not self.user_agent:
                version = random.randint(115, 134)
                if random.random() > .4:
                    if random.random() > .5:
                        self.user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36"
                    else:
                        self.user_agent = f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36'
                else:
                    if random.random() > .5:
                        self.user_agent = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36 Edg/{version}.0.0.0'
                    else:
                        self.user_agent = f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36 Edg/{version}.0.0.0"
            else:
                version = int(re.search(r'Chrome\/(\d+)\.\d+\.\d+\.\d+', self.user_agent)[1])
                
            if 'Edg' in self.user_agent:
                impersonate_brand = "edge"
                impersonate_versions = [122, 127, 131]
            else:
                impersonate_brand = "chrome"
                impersonate_versions = [114, 116, 117, 118, 119, 120, 123, 124, 126, 127, 128, 129, 130, 131]
            
            min_version = None
            impersonate_version = None
            for v in impersonate_versions:
                cv = abs(v - version)
                if not min_version or cv < min_version:
                    min_version = cv
                    impersonate_version = v
                    
            impersonate = f'{impersonate_brand}_{impersonate_version}'
            
            proxy = None
            if self.proxy:
                proxy = "http://" + self.proxy
            self.session = primp.Client(impersonate=impersonate, impersonate_os="macos" if 'Mac' in self.user_agent else "windows", proxy=proxy)
                
            if self.cookies:
                self.session.set_cookies(origin + "/", self.cookies)

            # 跟 ua 版本对应
            sec_ch_ua = parse_client_hints(self.user_agent)
            sec_ch_ua_ptf = '"macOS"' if 'Mac' in self.user_agent else '"Windows"'

            headers = {
                'sec-ch-ua': sec_ch_ua,
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': sec_ch_ua_ptf,
                'upgrade-insecure-requests': '1',
                'user-agent': self.user_agent,                
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'sec-fetch-site': "none",
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': "document",
                'accept-encoding': 'gzip, deflate, br, zstd',
                'accept-language': self.accept_language,
                "priority": "1"
            }
            
            response = self.session.get(self.href, headers=headers)
            if response.status_code == 403:
                dd_match = re.search(r'var dd=(\{.*?\})', response.text)
                if dd_match:
                    self.wanda_args = {
                        "href": self.href,
                        "captcha_html": response.text,
                        "user_agent": self.user_agent,
                        "cookies": {
                            "datadome": response.cookies.get("datadome") or "",
                        },
                        "proxy": self.proxy,
                        
                        "did": self.did,
                        "html": self.html,
                        
                        "branch": self.branch,
                        "is_auth": self.wanda_args["is_auth"],
                    }
                else:
                    raise Warning("代理异常或触发未知验证")
            else:
                if not self.js_key:
                    dd_js_key = re.search(r"ddjskey = .(.{30}).", response.text)
                    if dd_js_key:
                        self.js_key = dd_js_key[1]
                
                if self.js_url and self.js_key:
                    self.wanda_args = {
                        "href": self.href,
                        "js_url": self.js_url,
                        "js_key": self.js_key,
                        "user_agent": self.user_agent,
                        "cookies": {
                            "datadome": self.session.cookies.get("datadome") or "",
                        },
                        "proxy": self.proxy,
                        
                        "did": self.did,
                        "html": self.html,
                        
                        "branch": self.branch,
                        "is_auth": self.wanda_args["is_auth"],
                    }
                else:
                    self.wanda_args = {
                        "href": self.href,
                        "interstitial": True,
                        "user_agent": self.user_agent,
                        "proxy": self.proxy,
                        
                        "did": self.did,
                        "html": self.html,
                        
                        "branch": self.branch,
                        "is_auth": self.wanda_args["is_auth"],
                    }

        if country:
            self.wanda_args["country"] = country
            
        if _ip:
            self.wanda_args["ip"] = _ip
        
        if timezone:
            self.wanda_args["timezone"] = timezone
        
        if geolocation:
            self.wanda_args["geolocation"] = geolocation
    

def crack_datadome(
    user_token: str, href: str, proxy: str, interstitial: bool = False,
    js_url: Optional[str] = None, js_key: Optional[str] = None, 
    parse_index: Optional[callable] = None, verifiers: List[callable] = [], max_retry_times: int = 2, 
    show_ad: bool = False, internal_host: bool = True, branch: Optional[str] = None,
    developer_id: Optional[str] = None, user_agent: Optional[str] = None, cookies: Dict[str, str] = {},
    region: Literal['jp', 'us', 'tw', 'hk', 'it', 'de', 'es', 'in', 'cn', 'fr', 'tr', 'ru', 'gb', 'ua', 'ca', 'au'] = "hk", 
    debug: bool = True,
) -> Tuple[primp.Client, Response]:    
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
        version = random.randint(128, 136)
        user_agent = random.choice([
            f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36",
            f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36',  
            f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36 Edg/{version}.0.0.0',
            f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36 Edg/{version}.0.0.0",
        ])
    
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
        return session, None

    current_ip = resp.get("ip")
    timezone = resp.get("timezone")
    loc = resp.get("loc")
    
    if interstitial:
        html = parse_index is None
        cracker = DatadomeCracker(
            show_ad=show_ad,
            internal_host=internal_host,
            user_token=user_token,
            developer_id=developer_id,
            branch=branch,
            href=href,
            interstitial=True,
            html=html,
            user_agent=user_agent,
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
            session.set_cookies(origin + "/", cookies)
        else:
            raise Warning("验证失败")
    else:
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
        while resp.status_code in [403, 405] and retry_times < max_retry_times:
            try:
                dd_match = re.search(r'var dd=(\{.*?\})', resp.text)
                captcha = json.loads(dd_match[1].replace("'", '"'))
                if captcha.get("t") == "bv":
                    raise Warning("代理被封锁, 请切换代理重试")
            except:
                raise Warning(f"验证异常: {resp.status_code} {resp.text}")
            
            datadome = resp.cookies.get('datadome')
            cracker = DatadomeCracker(
                show_ad=show_ad,
                internal_host=internal_host,
                user_token=user_token,
                developer_id=developer_id,
                branch=branch,
                href=href,
                user_agent=user_agent,
                captcha_html=resp.text,
                cookies={
                    'datadome': datadome
                },
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
                cookies.update(res)
                session = create_session(user_agent, proxy)
                session.set_cookies(origin + "/", cookies)
                if parse_index:
                    resp = session.get(href, headers=headers)
                    retry_times += 1
                else:
                    break            
            else:
                raise Warning("验证失败")
            
        if retry_times == 0 and js_url and js_key:
            datadome = session.get_cookies(origin + "/").get('datadome')
            cookies = None
            if datadome:
                cookies = {
                    "datadome": datadome
                }
            cracker = DatadomeCracker(
                show_ad=show_ad,
                internal_host=internal_host,
                user_token=user_token,
                developer_id=developer_id,
                branch=branch,
                href=href,
                js_url=js_url,
                js_key=js_key,
                user_agent=user_agent,
                cookies=cookies,
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
                cookies.update(res)
                session = create_session(user_agent, proxy)
                session.set_cookies(origin + "/", cookies)
            else:
                raise Warning("验证失败")

    global_args = {}
    
    if parse_index:
        if interstitial:
            parse_index(extra["html"])
        else:
            parse_index(resp, global_args)
    
    for verifier in verifiers:
        
        retry_times = 0
        
        resp = verifier(session, extra, global_args)

        while resp.status_code in [403, 405] and retry_times < max_retry_times:
            did = extra.get("did")
            
            datadome = session.get_cookies(origin + "/")["datadome"]
            
            captcha_args = {}
            try:
                captcha_url = resp.json()["url"]
                if 't=bv' in captcha_url:
                    raise Warning("代理被封锁, 请切换代理重试")
                captcha_args["captcha_url"] = captcha_url
            except:
                try:
                    captcha_html = resp.text
                    dd_match = re.search(r'var dd=(\{.*?\})', resp.text)
                    captcha = json.loads(dd_match[1].replace("'", '"'))
                    if captcha.get("t") == "bv":
                        raise Warning("代理被封锁, 请切换代理重试")
                    
                    captcha_args["captcha_html"] = captcha_html
                except:
                    raise Warning("验证异常: " + resp.text)
            
            res = DatadomeCracker(
                show_ad=show_ad,
                internal_host=internal_host,
                user_token=user_token,
                developer_id=developer_id,
                branch=branch,
                href=href,                
                user_agent=user_agent,
                cookies={
                    "datadome": datadome
                },
                **captcha_args,
                did=did,
                proxy=proxy,
                debug=debug
            ).crack()
            if res:
                cookies = session.get_cookies(origin + "/")
                cookies.update(res)
                session = create_session(user_agent, proxy)
                session.set_cookies(origin + "/", cookies)
                resp = verifier(session, extra, global_args)
            else:
                raise Warning("验证失败")
            
            retry_times += 1

    return session, resp
