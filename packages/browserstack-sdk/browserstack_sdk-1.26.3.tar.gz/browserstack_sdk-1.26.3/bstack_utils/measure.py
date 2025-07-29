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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1llll11l1l_opy_ import get_logger
from bstack_utils.bstack1l1lll111l_opy_ import bstack1lllll11ll1_opy_
bstack1l1lll111l_opy_ = bstack1lllll11ll1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11lll11ll_opy_: Optional[str] = None):
    bstack1llll1l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡉ࡫ࡣࡰࡴࡤࡸࡴࡸࠠࡵࡱࠣࡰࡴ࡭ࠠࡵࡪࡨࠤࡸࡺࡡࡳࡶࠣࡸ࡮ࡳࡥࠡࡱࡩࠤࡦࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠎࠥࠦࠠࠡࡣ࡯ࡳࡳ࡭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࠤࡳࡧ࡭ࡦࠢࡤࡲࡩࠦࡳࡵࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ᳝")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1l1l11ll_opy_: str = bstack1l1lll111l_opy_.bstack11lll1lll11_opy_(label)
            start_mark: str = label + bstack1llll1l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸ᳞ࠧ")
            end_mark: str = label + bstack1llll1l_opy_ (u"ࠨ࠺ࡦࡰࡧ᳟ࠦ")
            result = None
            try:
                if stage.value == STAGE.bstack1lll11llll_opy_.value:
                    bstack1l1lll111l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1l1lll111l_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11lll11ll_opy_)
                elif stage.value == STAGE.bstack11111l1l1_opy_.value:
                    start_mark: str = bstack1ll1l1l11ll_opy_ + bstack1llll1l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᳠")
                    end_mark: str = bstack1ll1l1l11ll_opy_ + bstack1llll1l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ᳡")
                    bstack1l1lll111l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1l1lll111l_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11lll11ll_opy_)
            except Exception as e:
                bstack1l1lll111l_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11lll11ll_opy_)
            return result
        return wrapper
    return decorator