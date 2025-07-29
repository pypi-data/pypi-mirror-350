import warnings

import re
import random
import json
import primp
from .utils import parse_client_hints
from .base import BaseCracker

warnings.filterwarnings('ignore')


class ShapeV2Cracker(BaseCracker):
    
    cracker_name = "shape"
    cracker_version = "v2"    

    """
    shape cracker
    :param href: 触发 shape 验证的首页地址
    :param user_agent: 请求流程使用 ua
    :param script_url: 加载 shape vmp 脚本的 url
    :param vmp_url: shape vmp 脚本的 url
    :param pkey: shape 加密参数名, x-xxxx-a 中的 xxxx, 如星巴克的 Dq7hy5l1-a 传  dq7hy5l1 即可
    :param request: 需要 shape 签名的接口内容
    :param fast: 是否加速计算, 默认 false （网站风控低可使用该模式）
    :param submit: 是否直接提交 request 返回响应, 默认 false
    :param return_header: submit 为 true 时返回的响应是否返回响应头 headers, 默认 false
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
        "html": None,
        "pkey": None,
        "request": None,
        "action": None,
        "count": 1,
        "script_url": None,
        "script_content": None,
        "vmp_url": None,
        "vmp_regexp": None,
        "vmp_content": None,
        "user_agent": None,
        "impersonate": None,
        "proxy": None,
        "accept_language": "en-US,en;q=0.9",
        "country": None,
        "ip": None,
        "timezone": None,
        "geolocation": None,
        "headers": {},
        "cookies": {},
        "fast": None,
        "submit": False,
        "timeout": 30
    }
    
    def request(self):
        version = None
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

        self.wanda_args["user_agent"] = self.user_agent
        
        if self.wanda_args.get("fast") is None:
            self.wanda_args["fast"] = random.random() > .6
        
        if not self.impersonate:
            if not version:
                version = int(re.search(r'Chrome\/(\d+)\.\d+\.\d+\.\d+', self.user_agent)[1])
                
            if 'Edg' in self.user_agent:
                impersonate_brand = "edge"
                impersonate_versions = [122, 127, 131]
            else:
                impersonate_brand = "chrome"
                impersonate_versions = [114, 116, 117, 118, 119, 120, 123, 124, 126, 127, 128, 129, 130, 131, 133]
            
            min_version = None
            impersonate_version = None
            for v in impersonate_versions:
                cv = abs(v - version)
                if not min_version or cv < min_version:
                    min_version = cv
                    impersonate_version = v
                    
            self.impersonate = f'{impersonate_brand}_{impersonate_version}'
        
        sec_ch_ua = parse_client_hints(self.user_agent)
        sec_ch_ua_ptf = '"macOS"' if 'Mac' in self.user_agent else '"Windows"'
        
        origin = "/".join(self.href.split("/")[0:3])

        proxy = None
        if self.proxy:
            proxy = "http://" + self.proxy
        self.session = primp.Client(impersonate=self.impersonate, impersonate_os="macos" if 'Mac' in self.user_agent else "windows", proxy=proxy)

        if self.cookies:
            if isinstance(self.cookies, list):
                for cookie in self.cookies:
                    _domain = cookie['domain']
                    if _domain.startswith("."):
                        _domain = "https://" + _domain[1:]
                    else:
                        _domain = "https://" + _domain
                    self.session.set_cookies(_domain, {
                        cookie["name"]: cookie["value"]
                    })
            else:
                self.session.set_cookies(self.href, self.cookies)
        
        headers = {
            'sec-ch-ua': sec_ch_ua,
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': sec_ch_ua_ptf,
            'user-agent': self.user_agent,
            'origin': origin,
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': self.href,
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': self.accept_language,
            'priority': 'u=1, i',
        }
        cookies = {}
        if not self.wanda_args.get("pkey"):
            html = self.html
            if not html:
                script_resp = self.session.get(self.href, headers=headers)
                cookies.update(script_resp.cookies)
                html = script_resp.text

            if 'ISTL-REDIRECT-TO' not in html:
                raise Warning("未触发 shape 盾")

            country = self.wanda_args.get("country")
            _ip = self.wanda_args.get("ip")
            timezone = self.wanda_args.get("timezone")
            self.wanda_args = {
                "href": self.href,
                "html": html,
                "user_agent": self.user_agent,
                "fast": self.fast,

                "branch": self.branch,
                "is_auth": self.wanda_args["is_auth"],
            }
            
            if country:
                self.wanda_args["country"] = country
            
            if _ip:
                self.wanda_args["ip"] = _ip
            
            if timezone:
                self.wanda_args["timezone"] = timezone
        
        else:
            if not self.wanda_args.get("script_url"):
                
                data = {
                    "method": "read",
                    "key": self.pkey.lower(),
                }
                site_arg = primp.post(
                    f"http://{self.api_host}/api/wanda/shape/p",
                    json=data
                ).text
                if not site_arg:
                    raise Warning("暂不支持的站点, 请联系管理员添加")
                
                site_arg = json.loads(site_arg)
                
                self.wanda_args["script_url"] = site_arg.get("script_url")
                self.wanda_args["vmp_url"] = site_arg.get("vmp_url")
                self.wanda_args["vmp_regexp"] = site_arg.get("vmp_regexp")
                
                if not self.wanda_args.get("request"):
                    self.wanda_args["request"] = site_arg.get("request")
            
            if self.wanda_args["script_url"]:
                
                if not self.wanda_args.get("script_content"):
                    try:
                        script_resp = self.session.get(self.wanda_args["script_url"], headers=headers)
                        cookies.update(script_resp.cookies)
                        script = script_resp.text
                        self.wanda_args["script_content"] = script
                    except:
                        raise Warning("初始化脚本获取失败")

                vmp_url = self.wanda_args.get("vmp_url")
                if not vmp_url:
                    if self.wanda_args.get("vmp_regexp"):
                        try:
                            vmp_url = re.search(self.wanda_args["vmp_regexp"], script)[1]
                        except:
                            raise Warning("vmp 地址获取失败")

                if vmp_url:
                    if not vmp_url.startswith("http"):
                        vmp_url = origin + vmp_url
                    
                    if not self.wanda_args.get("vmp_content"):
                        try:
                            vmp_resp = self.session.get(vmp_url, headers=headers)
                            if vmp_resp.status_code != 200:
                                raise Warning("vmp 脚本请求失败")
                            cookies.update(vmp_resp.cookies)
                            self.wanda_args["vmp_url"] = vmp_url
                            self.wanda_args["vmp_content"] = vmp_resp.text
                        except:
                            raise Warning("vmp 获取失败")

                if self.wanda_args.get("vmp_regexp"):
                    del self.wanda_args["vmp_regexp"]
                    
            else:
                raise Warning("配置异常, 请联系管理员")
            
        if self.cookies:
            if isinstance(self.cookies, list):
                self.wanda_args["cookies"] = [
                    *self.cookies,
                    *[{
                        "name": name,
                        "value": value,
                        "domain": self.href.split("/")[2]
                    } for name, value in cookies.items()]
                ]
            else:
                self.wanda_args["cookies"] = {
                    **self.cookies,
                    **cookies
                }
                
        if self.wanda_args.get("proxy") and not self.submit:
            del self.wanda_args["proxy"]
    

class ShapeV1Cracker(BaseCracker):
    
    cracker_name = "shape"
    cracker_version = "v1"    

    """
    shape cracker
    :param href: 触发 shape 验证的首页地址
    :param user_agent: 请求流程使用 ua
    :param vmp_url: shape vmp 脚本的 url
    :param vmp_content: shape vmp 脚本内容
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
        "proxy": None,
        "vmp_url": None,
        "vmp_content": None,
        "script_url": None,
        "script_content": None,
        "request": None,
        "user_agent": None,
        "accept_language": "en-US,en;q=0.9",
        "country": None,
        "ip": None,
        "timezone": None,
        "geolocation": None,
        "impersonate": None,
        "headers": {},
        "cookies": {},
        "fast": True,
        "timeout": 30
    }

    def request(self):
        domain = self.href.split("/")[2]
        origin = "/".join(self.href.split("/")[0:3])
        
        version = None
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

        self.wanda_args["user_agent"] = self.user_agent
        
        if self.wanda_args.get("fast") is None:
            self.wanda_args["fast"] = random.random() > .6
            
        if not self.impersonate:
            if not version:
                version = int(re.search(r'Chrome\/(\d+)\.\d+\.\d+\.\d+', self.user_agent)[1])
                
            if 'Edg' in self.user_agent:
                impersonate_brand = "edge"
                impersonate_versions = [122, 127, 131]
            else:
                impersonate_brand = "chrome"
                impersonate_versions = [114, 116, 117, 118, 119, 120, 123, 124, 126, 127, 128, 129, 130, 131, 133]
            
            min_version = None
            impersonate_version = None
            for v in impersonate_versions:
                cv = abs(v - version)
                if not min_version or cv < min_version:
                    min_version = cv
                    impersonate_version = v
                    
            self.impersonate = f'{impersonate_brand}_{impersonate_version}'
        
        sec_ch_ua = parse_client_hints(self.user_agent)
        sec_ch_ua_ptf = '"macOS"' if 'Mac' in self.user_agent else '"Windows"'

        proxy = None
        if self.proxy:
            proxy = "http://" + self.proxy
        self.session = primp.Client(impersonate=self.impersonate, impersonate_os="macos" if 'Mac' in self.user_agent else "windows", proxy=proxy)

        if self.cookies:
            if isinstance(self.cookies, list):
                for cookie in self.cookies:
                    _domain = cookie['domain']
                    if _domain.startswith("."):
                        _domain = "https://" + _domain[1:]
                    else:
                        _domain = "https://" + _domain
                    self.session.set_cookies(_domain, {
                        cookie["name"]: cookie["value"]
                    })
            else:
                self.session.set_cookies(self.href, self.cookies)
        
        if not self.wanda_args.get("script_url"):
            
            data = {
                "method": "read",
                "key": domain,
            }
            site_arg = primp.post(
                f"http://{self.api_host}/api/wanda/shape/p",
                json=data
            ).text
            if not site_arg:
                raise Warning("暂不支持的站点, 请联系管理员添加")
            
            site_arg = json.loads(site_arg)
            if site_arg.get("script_url"):
                self.wanda_args["script_url"] = site_arg["script_url"]
                
            self.wanda_args["vmp_url"] = site_arg.get("vmp_url")
            self.wanda_args["vmp_regexp"] = site_arg.get("vmp_regexp")
        
        headers = {
            'sec-ch-ua': sec_ch_ua,
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': sec_ch_ua_ptf,
            'user-agent': self.user_agent,
            'origin': origin,
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': self.href,
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': self.accept_language,
            'priority': 'u=1, i',
        }
        
        cookies = {}
        if self.wanda_args.get("script_url"):
            if not self.wanda_args.get("script_content"):
                try:
                    script_resp = self.session.get(self.wanda_args["script_url"], headers=headers)
                    cookies.update(script_resp.cookies)
                    script = script_resp.text
                    self.wanda_args["script_content"] = script
                except:
                    raise Warning("初始化脚本获取失败")

        vmp_url = self.wanda_args.get("vmp_url")
        if not vmp_url:
            if self.wanda_args.get("vmp_regexp"):
                try:
                    vmp_url = re.search(self.wanda_args["vmp_regexp"], script)[1]
                except:
                    raise Warning("vmp 地址获取失败")

        if vmp_url:
            if not vmp_url.startswith("http"):
                vmp_url = origin + vmp_url
            
            if not self.wanda_args.get("vmp_content"):
                try:
                    vmp_resp = self.session.get(vmp_url, headers=headers)
                    if vmp_resp.status_code != 200:
                        raise Warning("vmp 脚本请求失败")
                    cookies.update(vmp_resp.cookies)
                    self.wanda_args["vmp_url"] = vmp_url
                    self.wanda_args["vmp_content"] = vmp_resp.text
                except:
                    import traceback
                    traceback.print_exc()
                    raise Warning("vmp 获取失败")
        
        if self.wanda_args.get("vmp_regexp"):
            del self.wanda_args["vmp_regexp"]
        
        if self.cookies:
            if isinstance(self.cookies, list):
                self.wanda_args["cookies"] = [
                    *self.cookies,
                    *[{
                        "name": name,
                        "value": value,
                        "domain": domain
                    } for name, value in cookies.items()]
                ]
            else:
                self.wanda_args["cookies"] = {
                    **self.cookies,
                    **cookies
                }
        
        request = self.wanda_args.get("request")
        if not request and self.wanda_args.get("proxy"):
            del self.wanda_args["proxy"]
