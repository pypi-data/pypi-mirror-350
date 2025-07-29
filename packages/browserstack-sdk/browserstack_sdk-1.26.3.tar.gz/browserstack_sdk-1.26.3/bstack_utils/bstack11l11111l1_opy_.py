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
import threading
from bstack_utils.helper import bstack111l11ll1_opy_
from bstack_utils.constants import bstack11ll1l111ll_opy_, EVENTS, STAGE
from bstack_utils.bstack1llll11l1l_opy_ import get_logger
logger = get_logger(__name__)
class bstack1l11l111ll_opy_:
    bstack1111lllll1l_opy_ = None
    @classmethod
    def bstack11llll11ll_opy_(cls):
        if cls.on() and os.getenv(bstack1llll1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢΌ")):
            logger.info(
                bstack1llll1l_opy_ (u"࡚ࠪ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭Ὼ").format(os.getenv(bstack1llll1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤΏ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩῼ"), None) is None or os.environ[bstack1llll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ´")] == bstack1llll1l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ῾"):
            return False
        return True
    @classmethod
    def bstack11111ll11ll_opy_(cls, bs_config, framework=bstack1llll1l_opy_ (u"ࠣࠤ῿")):
        bstack11ll1l11ll1_opy_ = False
        for fw in bstack11ll1l111ll_opy_:
            if fw in framework:
                bstack11ll1l11ll1_opy_ = True
        return bstack111l11ll1_opy_(bs_config.get(bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ "), bstack11ll1l11ll1_opy_))
    @classmethod
    def bstack11111l11lll_opy_(cls, framework):
        return framework in bstack11ll1l111ll_opy_
    @classmethod
    def bstack11111llll11_opy_(cls, bs_config, framework):
        return cls.bstack11111ll11ll_opy_(bs_config, framework) is True and cls.bstack11111l11lll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1llll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ "), None)
    @staticmethod
    def bstack111llll1ll_opy_():
        if getattr(threading.current_thread(), bstack1llll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ "), None):
            return {
                bstack1llll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪ "): bstack1llll1l_opy_ (u"࠭ࡴࡦࡵࡷࠫ "),
                bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ "): getattr(threading.current_thread(), bstack1llll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ "), None)
            }
        if getattr(threading.current_thread(), bstack1llll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ "), None):
            return {
                bstack1llll1l_opy_ (u"ࠪࡸࡾࡶࡥࠨ "): bstack1llll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ "),
                bstack1llll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ "): getattr(threading.current_thread(), bstack1llll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ​"), None)
            }
        return None
    @staticmethod
    def bstack11111l1l1ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l11l111ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111l1ll1ll_opy_(test, hook_name=None):
        bstack11111l1l11l_opy_ = test.parent
        if hook_name in [bstack1llll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ‌"), bstack1llll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ‍"), bstack1llll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ‎"), bstack1llll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ‏")]:
            bstack11111l1l11l_opy_ = test
        scope = []
        while bstack11111l1l11l_opy_ is not None:
            scope.append(bstack11111l1l11l_opy_.name)
            bstack11111l1l11l_opy_ = bstack11111l1l11l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack11111l1l111_opy_(hook_type):
        if hook_type == bstack1llll1l_opy_ (u"ࠦࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠤ‐"):
            return bstack1llll1l_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡭ࡵ࡯࡬ࠤ‑")
        elif hook_type == bstack1llll1l_opy_ (u"ࠨࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠥ‒"):
            return bstack1llll1l_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢ࡫ࡳࡴࡱࠢ–")
    @staticmethod
    def bstack11111l1l1l1_opy_(bstack1l111l1l1l_opy_):
        try:
            if not bstack1l11l111ll_opy_.on():
                return bstack1l111l1l1l_opy_
            if os.environ.get(bstack1llll1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࠨ—"), None) == bstack1llll1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ―"):
                tests = os.environ.get(bstack1llll1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠢ‖"), None)
                if tests is None or tests == bstack1llll1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ‗"):
                    return bstack1l111l1l1l_opy_
                bstack1l111l1l1l_opy_ = tests.split(bstack1llll1l_opy_ (u"ࠬ࠲ࠧ‘"))
                return bstack1l111l1l1l_opy_
        except Exception as exc:
            logger.debug(bstack1llll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡥࡳࡷࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠿ࠦࠢ’") + str(str(exc)) + bstack1llll1l_opy_ (u"ࠢࠣ‚"))
        return bstack1l111l1l1l_opy_