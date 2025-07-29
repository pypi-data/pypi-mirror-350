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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l11lll1l1_opy_, bstack1lll1ll11l_opy_, bstack11l11111_opy_, bstack11ll11lll1_opy_, \
    bstack11l1l11111l_opy_
from bstack_utils.measure import measure
def bstack11ll111111_opy_(bstack1111ll1l11l_opy_):
    for driver in bstack1111ll1l11l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1111l1l1l_opy_, stage=STAGE.bstack11111l1l1_opy_)
def bstack1ll111l11_opy_(driver, status, reason=bstack1llll1l_opy_ (u"ࠩࠪṀ")):
    bstack1lll1l111l_opy_ = Config.bstack11l11l11l1_opy_()
    if bstack1lll1l111l_opy_.bstack1111l1ll11_opy_():
        return
    bstack1l1ll1ll_opy_ = bstack11llll11l_opy_(bstack1llll1l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ṁ"), bstack1llll1l_opy_ (u"ࠫࠬṂ"), status, reason, bstack1llll1l_opy_ (u"ࠬ࠭ṃ"), bstack1llll1l_opy_ (u"࠭ࠧṄ"))
    driver.execute_script(bstack1l1ll1ll_opy_)
@measure(event_name=EVENTS.bstack1111l1l1l_opy_, stage=STAGE.bstack11111l1l1_opy_)
def bstack11l111l11_opy_(page, status, reason=bstack1llll1l_opy_ (u"ࠧࠨṅ")):
    try:
        if page is None:
            return
        bstack1lll1l111l_opy_ = Config.bstack11l11l11l1_opy_()
        if bstack1lll1l111l_opy_.bstack1111l1ll11_opy_():
            return
        bstack1l1ll1ll_opy_ = bstack11llll11l_opy_(bstack1llll1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫṆ"), bstack1llll1l_opy_ (u"ࠩࠪṇ"), status, reason, bstack1llll1l_opy_ (u"ࠪࠫṈ"), bstack1llll1l_opy_ (u"ࠫࠬṉ"))
        page.evaluate(bstack1llll1l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨṊ"), bstack1l1ll1ll_opy_)
    except Exception as e:
        print(bstack1llll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦṋ"), e)
def bstack11llll11l_opy_(type, name, status, reason, bstack11l1l1ll1l_opy_, bstack11l1llllll_opy_):
    bstack1lll11111_opy_ = {
        bstack1llll1l_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧṌ"): type,
        bstack1llll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫṍ"): {}
    }
    if type == bstack1llll1l_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫṎ"):
        bstack1lll11111_opy_[bstack1llll1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ṏ")][bstack1llll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪṐ")] = bstack11l1l1ll1l_opy_
        bstack1lll11111_opy_[bstack1llll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨṑ")][bstack1llll1l_opy_ (u"࠭ࡤࡢࡶࡤࠫṒ")] = json.dumps(str(bstack11l1llllll_opy_))
    if type == bstack1llll1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨṓ"):
        bstack1lll11111_opy_[bstack1llll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫṔ")][bstack1llll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧṕ")] = name
    if type == bstack1llll1l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭Ṗ"):
        bstack1lll11111_opy_[bstack1llll1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧṗ")][bstack1llll1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬṘ")] = status
        if status == bstack1llll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ṙ") and str(reason) != bstack1llll1l_opy_ (u"ࠢࠣṚ"):
            bstack1lll11111_opy_[bstack1llll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫṛ")][bstack1llll1l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩṜ")] = json.dumps(str(reason))
    bstack1l1l1l11_opy_ = bstack1llll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨṝ").format(json.dumps(bstack1lll11111_opy_))
    return bstack1l1l1l11_opy_
def bstack1ll11ll1ll_opy_(url, config, logger, bstack1ll11111ll_opy_=False):
    hostname = bstack1lll1ll11l_opy_(url)
    is_private = bstack11ll11lll1_opy_(hostname)
    try:
        if is_private or bstack1ll11111ll_opy_:
            file_path = bstack11l11lll1l1_opy_(bstack1llll1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫṞ"), bstack1llll1l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫṟ"), logger)
            if os.environ.get(bstack1llll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫṠ")) and eval(
                    os.environ.get(bstack1llll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬṡ"))):
                return
            if (bstack1llll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬṢ") in config and not config[bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ṣ")]):
                os.environ[bstack1llll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨṤ")] = str(True)
                bstack1111ll11ll1_opy_ = {bstack1llll1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ṥ"): hostname}
                bstack11l1l11111l_opy_(bstack1llll1l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫṦ"), bstack1llll1l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫṧ"), bstack1111ll11ll1_opy_, logger)
    except Exception as e:
        pass
def bstack111lllll1_opy_(caps, bstack1111ll11lll_opy_):
    if bstack1llll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨṨ") in caps:
        caps[bstack1llll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩṩ")][bstack1llll1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨṪ")] = True
        if bstack1111ll11lll_opy_:
            caps[bstack1llll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫṫ")][bstack1llll1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭Ṭ")] = bstack1111ll11lll_opy_
    else:
        caps[bstack1llll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪṭ")] = True
        if bstack1111ll11lll_opy_:
            caps[bstack1llll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧṮ")] = bstack1111ll11lll_opy_
def bstack1111lllllll_opy_(bstack111l111lll_opy_):
    bstack1111ll1l111_opy_ = bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫṯ"), bstack1llll1l_opy_ (u"ࠨࠩṰ"))
    if bstack1111ll1l111_opy_ == bstack1llll1l_opy_ (u"ࠩࠪṱ") or bstack1111ll1l111_opy_ == bstack1llll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫṲ"):
        threading.current_thread().testStatus = bstack111l111lll_opy_
    else:
        if bstack111l111lll_opy_ == bstack1llll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫṳ"):
            threading.current_thread().testStatus = bstack111l111lll_opy_