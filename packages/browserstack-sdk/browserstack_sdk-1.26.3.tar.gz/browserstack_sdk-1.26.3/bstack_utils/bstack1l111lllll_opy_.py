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
import threading
import logging
import bstack_utils.accessibility as bstack11l1lll1_opy_
from bstack_utils.helper import bstack11l11111_opy_
logger = logging.getLogger(__name__)
def bstack111llllll_opy_(bstack11ll1ll111_opy_):
  return True if bstack11ll1ll111_opy_ in threading.current_thread().__dict__.keys() else False
def bstack111l1ll1l_opy_(context, *args):
    tags = getattr(args[0], bstack1llll1l_opy_ (u"ࠫࡹࡧࡧࡴࠩᛧ"), [])
    bstack1l1ll1l111_opy_ = bstack11l1lll1_opy_.bstack1ll1l11l1l_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l1ll1l111_opy_
    try:
      bstack111lll11_opy_ = threading.current_thread().bstackSessionDriver if bstack111llllll_opy_(bstack1llll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫᛨ")) else context.browser
      if bstack111lll11_opy_ and bstack111lll11_opy_.session_id and bstack1l1ll1l111_opy_ and bstack11l11111_opy_(
              threading.current_thread(), bstack1llll1l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᛩ"), None):
          threading.current_thread().isA11yTest = bstack11l1lll1_opy_.bstack11l11ll1l1_opy_(bstack111lll11_opy_, bstack1l1ll1l111_opy_)
    except Exception as e:
       logger.debug(bstack1llll1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡤ࠵࠶ࡿࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧ࠽ࠤࢀࢃࠧᛪ").format(str(e)))
def bstack11l11ll11_opy_(bstack111lll11_opy_):
    if bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ᛫"), None) and bstack11l11111_opy_(
      threading.current_thread(), bstack1llll1l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᛬"), None) and not bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠪࡥ࠶࠷ࡹࡠࡵࡷࡳࡵ࠭᛭"), False):
      threading.current_thread().a11y_stop = True
      bstack11l1lll1_opy_.bstack11l1111ll_opy_(bstack111lll11_opy_, name=bstack1llll1l_opy_ (u"ࠦࠧᛮ"), path=bstack1llll1l_opy_ (u"ࠧࠨᛯ"))