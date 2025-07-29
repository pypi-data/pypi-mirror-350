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
from browserstack_sdk.bstack1lll1111l_opy_ import bstack1l1l1ll1l_opy_
from browserstack_sdk.bstack111l1ll1l1_opy_ import RobotHandler
def bstack11ll1111l1_opy_(framework):
    if framework.lower() == bstack1llll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᨰ"):
        return bstack1l1l1ll1l_opy_.version()
    elif framework.lower() == bstack1llll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬᨱ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1llll1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧᨲ"):
        import behave
        return behave.__version__
    else:
        return bstack1llll1l_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩᨳ")
def bstack1ll111l1ll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1llll1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᨴ"))
        framework_version.append(importlib.metadata.version(bstack1llll1l_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᨵ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1llll1l_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᨶ"))
        framework_version.append(importlib.metadata.version(bstack1llll1l_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᨷ")))
    except:
        pass
    return {
        bstack1llll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᨸ"): bstack1llll1l_opy_ (u"ࠧࡠࠩᨹ").join(framework_name),
        bstack1llll1l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩᨺ"): bstack1llll1l_opy_ (u"ࠩࡢࠫᨻ").join(framework_version)
    }