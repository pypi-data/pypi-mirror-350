import warnings

from .base import BaseCracker

warnings.filterwarnings('ignore')


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
