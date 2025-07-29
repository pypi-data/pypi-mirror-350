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
bstack111lll1ll11_opy_ = {bstack1llll1l_opy_ (u"ࠫࡷ࡫ࡴࡳࡻࡗࡩࡸࡺࡳࡐࡰࡉࡥ࡮ࡲࡵࡳࡧࠪᴪ")}
class bstack11ll1lllll_opy_:
    @staticmethod
    def bstack11ll11l1ll_opy_(config: dict) -> bool:
        bstack111lll1ll1l_opy_ = config.get(bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᴫ"), {}).get(bstack1llll1l_opy_ (u"࠭ࡲࡦࡶࡵࡽ࡙࡫ࡳࡵࡵࡒࡲࡋࡧࡩ࡭ࡷࡵࡩࠬᴬ"), {})
        return bstack111lll1ll1l_opy_.get(bstack1llll1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨᴭ"), False)
    @staticmethod
    def bstack11l1ll1l1_opy_(config: dict) -> int:
        bstack111lll1ll1l_opy_ = config.get(bstack1llll1l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬᴮ"), {}).get(bstack1llll1l_opy_ (u"ࠩࡵࡩࡹࡸࡹࡕࡧࡶࡸࡸࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠨᴯ"), {})
        retries = 0
        if bstack11ll1lllll_opy_.bstack11ll11l1ll_opy_(config):
            retries = bstack111lll1ll1l_opy_.get(bstack1llll1l_opy_ (u"ࠪࡱࡦࡾࡒࡦࡶࡵ࡭ࡪࡹࠧᴰ"), 1)
        return retries
    @staticmethod
    def bstack1ll11ll1_opy_(config: dict) -> dict:
        bstack111lll1lll1_opy_ = config.get(bstack1llll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨᴱ"), {})
        return {
            key: value for key, value in bstack111lll1lll1_opy_.items() if key in bstack111lll1ll11_opy_
        }