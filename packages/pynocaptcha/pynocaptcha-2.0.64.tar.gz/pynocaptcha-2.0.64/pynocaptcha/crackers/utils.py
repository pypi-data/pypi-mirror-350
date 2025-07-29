# -*- coding: UTF-8 -*-

import re
import primp


def parse_client_hints(ua):
    version = int(re.search(r"(\d+)\.0\.0\.0", ua)[1])
    greasey_chars = [
        " ",
        "(",
        ":",
        "-",
        ".",
        "/",
        ")",
        ";",
        "=",
        "?",
        "_",
    ]
    greased_versions = ["8", "99", "24"]
    orders = [
        [0, 1, 2],
        [0, 2, 1],
        [1, 0, 2],
        [1, 2, 0],
        [2, 0, 1],
        [2, 1, 0],
    ][version % 6]
    brands = [
        {
            "brand": "".join([
                "Not",
                greasey_chars[version % 11],
                "A",
                greasey_chars[(version + 1) % 11],
                "Brand",
            ]),
            "version": greased_versions[version % 3],
        },
        { "brand": "Chromium", "version": str(version) },
        { "brand": "Google Chrome", "version": str(version) },
    ]
    _brands = [None, None, None]
    _brands[orders[0]] = brands[0]
    _brands[orders[1]] = brands[1]
    _brands[orders[2]] = brands[2]
    
    return ", ".join(map(lambda _: f'"{_["brand"]}";v="{_["version"]}"', _brands))


def create_session(user_agent, proxy=None):
    version = int(re.search(r'Chrome\/(\d+)\.\d+\.\d+\.\d+', user_agent)[1])
        
    if 'Edg' in user_agent:
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
            
    impersonate = f'{impersonate_brand}_{impersonate_version}'
    
    _proxy = None
    if proxy:
        if not proxy.startswith("http"):
            if "://" in proxy:
                _proxy = "http://" + proxy.split("://")[1]
            else:
                _proxy = "http://" + proxy
        
    return primp.Client(
        impersonate=impersonate, 
        impersonate_os="macos" if 'Mac' in user_agent else "windows", 
        proxy=_proxy, verify=False
    )
