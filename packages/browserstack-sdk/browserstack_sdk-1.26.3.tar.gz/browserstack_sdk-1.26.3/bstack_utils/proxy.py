# coding: UTF-8
import sys
bstack1l1l11_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1llll1l_opy_ (bstack111llll_opy_):
    global bstack1lll111_opy_
    bstack1llll_opy_ = ord (bstack111llll_opy_ [-1])
    bstack11l1lll_opy_ = bstack111llll_opy_ [:-1]
    bstack111lll_opy_ = bstack1llll_opy_ % len (bstack11l1lll_opy_)
    bstack1l1ll_opy_ = bstack11l1lll_opy_ [:bstack111lll_opy_] + bstack11l1lll_opy_ [bstack111lll_opy_:]
    if bstack1l1l11_opy_:
        bstack11l111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack11111ll_opy_ + bstack1llll_opy_) % bstack11ll11_opy_) for bstack11111ll_opy_, char in enumerate (bstack1l1ll_opy_)])
    else:
        bstack11l111l_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack11111ll_opy_ + bstack1llll_opy_) % bstack11ll11_opy_) for bstack11111ll_opy_, char in enumerate (bstack1l1ll_opy_)])
    return eval (bstack11l111l_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111llll111l_opy_
bstack1lll1l111l_opy_ = Config.bstack11l11l11l1_opy_()
def bstack111l111ll11_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111l11l1111_opy_(bstack111l11l11l1_opy_, bstack111l111lll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111l11l11l1_opy_):
        with open(bstack111l11l11l1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111l111ll11_opy_(bstack111l11l11l1_opy_):
        pac = get_pac(url=bstack111l11l11l1_opy_)
    else:
        raise Exception(bstack1llll1l_opy_ (u"ࠨࡒࡤࡧࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠨ᷏").format(bstack111l11l11l1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1llll1l_opy_ (u"ࠤ࠻࠲࠽࠴࠸࠯࠺᷐ࠥ"), 80))
        bstack111l11l111l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111l11l111l_opy_ = bstack1llll1l_opy_ (u"ࠪ࠴࠳࠶࠮࠱࠰࠳ࠫ᷑")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111l111lll1_opy_, bstack111l11l111l_opy_)
    return proxy_url
def bstack111llll1l_opy_(config):
    return bstack1llll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ᷒") in config or bstack1llll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᷓ") in config
def bstack111111l1l_opy_(config):
    if not bstack111llll1l_opy_(config):
        return
    if config.get(bstack1llll1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᷔ")):
        return config.get(bstack1llll1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᷕ"))
    if config.get(bstack1llll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᷖ")):
        return config.get(bstack1llll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᷗ"))
def bstack111llll11_opy_(config, bstack111l111lll1_opy_):
    proxy = bstack111111l1l_opy_(config)
    proxies = {}
    if config.get(bstack1llll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᷘ")) or config.get(bstack1llll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᷙ")):
        if proxy.endswith(bstack1llll1l_opy_ (u"ࠬ࠴ࡰࡢࡥࠪᷚ")):
            proxies = bstack1ll11lll1l_opy_(proxy, bstack111l111lll1_opy_)
        else:
            proxies = {
                bstack1llll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᷛ"): proxy
            }
    bstack1lll1l111l_opy_.bstack1lll1ll11_opy_(bstack1llll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧᷜ"), proxies)
    return proxies
def bstack1ll11lll1l_opy_(bstack111l11l11l1_opy_, bstack111l111lll1_opy_):
    proxies = {}
    global bstack111l111ll1l_opy_
    if bstack1llll1l_opy_ (u"ࠨࡒࡄࡇࡤࡖࡒࡐ࡚࡜ࠫᷝ") in globals():
        return bstack111l111ll1l_opy_
    try:
        proxy = bstack111l11l1111_opy_(bstack111l11l11l1_opy_, bstack111l111lll1_opy_)
        if bstack1llll1l_opy_ (u"ࠤࡇࡍࡗࡋࡃࡕࠤᷞ") in proxy:
            proxies = {}
        elif bstack1llll1l_opy_ (u"ࠥࡌ࡙࡚ࡐࠣᷟ") in proxy or bstack1llll1l_opy_ (u"ࠦࡍ࡚ࡔࡑࡕࠥᷠ") in proxy or bstack1llll1l_opy_ (u"࡙ࠧࡏࡄࡍࡖࠦᷡ") in proxy:
            bstack111l111llll_opy_ = proxy.split(bstack1llll1l_opy_ (u"ࠨࠠࠣᷢ"))
            if bstack1llll1l_opy_ (u"ࠢ࠻࠱࠲ࠦᷣ") in bstack1llll1l_opy_ (u"ࠣࠤᷤ").join(bstack111l111llll_opy_[1:]):
                proxies = {
                    bstack1llll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᷥ"): bstack1llll1l_opy_ (u"ࠥࠦᷦ").join(bstack111l111llll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1llll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᷧ"): str(bstack111l111llll_opy_[0]).lower() + bstack1llll1l_opy_ (u"ࠧࡀ࠯࠰ࠤᷨ") + bstack1llll1l_opy_ (u"ࠨࠢᷩ").join(bstack111l111llll_opy_[1:])
                }
        elif bstack1llll1l_opy_ (u"ࠢࡑࡔࡒ࡜࡞ࠨᷪ") in proxy:
            bstack111l111llll_opy_ = proxy.split(bstack1llll1l_opy_ (u"ࠣࠢࠥᷫ"))
            if bstack1llll1l_opy_ (u"ࠤ࠽࠳࠴ࠨᷬ") in bstack1llll1l_opy_ (u"ࠥࠦᷭ").join(bstack111l111llll_opy_[1:]):
                proxies = {
                    bstack1llll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᷮ"): bstack1llll1l_opy_ (u"ࠧࠨᷯ").join(bstack111l111llll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1llll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᷰ"): bstack1llll1l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᷱ") + bstack1llll1l_opy_ (u"ࠣࠤᷲ").join(bstack111l111llll_opy_[1:])
                }
        else:
            proxies = {
                bstack1llll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᷳ"): proxy
            }
    except Exception as e:
        print(bstack1llll1l_opy_ (u"ࠥࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᷴ"), bstack111llll111l_opy_.format(bstack111l11l11l1_opy_, str(e)))
    bstack111l111ll1l_opy_ = proxies
    return proxies