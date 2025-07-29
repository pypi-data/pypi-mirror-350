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
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lllllll111_opy_ import (
    bstack11111lll11_opy_,
    bstack1111111ll1_opy_,
    bstack11111l1l1l_opy_,
    bstack1llllll1l1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1llll11llll_opy_(bstack11111lll11_opy_):
    bstack1l11ll1ll11_opy_ = bstack1llll1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦᎃ")
    bstack1l1l1lll11l_opy_ = bstack1llll1l_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᎄ")
    bstack1l1ll11111l_opy_ = bstack1llll1l_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲࠢᎅ")
    bstack1l1ll111111_opy_ = bstack1llll1l_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᎆ")
    bstack1l11lll1111_opy_ = bstack1llll1l_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࠦᎇ")
    bstack1l11ll1lll1_opy_ = bstack1llll1l_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࡦࡹࡹ࡯ࡥࠥᎈ")
    NAME = bstack1llll1l_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᎉ")
    bstack1l11ll1l1ll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1llll11l111_opy_: Any
    bstack1l11lll111l_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1llll1l_opy_ (u"ࠦࡱࡧࡵ࡯ࡥ࡫ࠦᎊ"), bstack1llll1l_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨᎋ"), bstack1llll1l_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣᎌ"), bstack1llll1l_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨᎍ"), bstack1llll1l_opy_ (u"ࠣࡦ࡬ࡷࡵࡧࡴࡤࡪࠥᎎ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack11111l111l_opy_(methods)
    def bstack11111l1l11_opy_(self, instance: bstack1111111ll1_opy_, method_name: str, bstack111111l1ll_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1111111l1l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1111111ll1_opy_, str],
        bstack11111l1lll_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack11111l11ll_opy_, bstack1l11ll1llll_opy_ = bstack11111l1lll_opy_
        bstack1l11lll11ll_opy_ = bstack1llll11llll_opy_.bstack1l11ll1ll1l_opy_(bstack11111l1lll_opy_)
        if bstack1l11lll11ll_opy_ in bstack1llll11llll_opy_.bstack1l11ll1l1ll_opy_:
            bstack1l11ll1l1l1_opy_ = None
            for callback in bstack1llll11llll_opy_.bstack1l11ll1l1ll_opy_[bstack1l11lll11ll_opy_]:
                try:
                    bstack1l11lll11l1_opy_ = callback(self, target, exec, bstack11111l1lll_opy_, result, *args, **kwargs)
                    if bstack1l11ll1l1l1_opy_ == None:
                        bstack1l11ll1l1l1_opy_ = bstack1l11lll11l1_opy_
                except Exception as e:
                    self.logger.error(bstack1llll1l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࠢᎏ") + str(e) + bstack1llll1l_opy_ (u"ࠥࠦ᎐"))
                    traceback.print_exc()
            if bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.PRE and callable(bstack1l11ll1l1l1_opy_):
                return bstack1l11ll1l1l1_opy_
            elif bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.POST and bstack1l11ll1l1l1_opy_:
                return bstack1l11ll1l1l1_opy_
    def bstack111111l111_opy_(
        self, method_name, previous_state: bstack11111l1l1l_opy_, *args, **kwargs
    ) -> bstack11111l1l1l_opy_:
        if method_name == bstack1llll1l_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࠫ᎑") or method_name == bstack1llll1l_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹ࠭᎒") or method_name == bstack1llll1l_opy_ (u"࠭࡮ࡦࡹࡢࡴࡦ࡭ࡥࠨ᎓"):
            return bstack11111l1l1l_opy_.bstack11111ll111_opy_
        if method_name == bstack1llll1l_opy_ (u"ࠧࡥ࡫ࡶࡴࡦࡺࡣࡩࠩ᎔"):
            return bstack11111l1l1l_opy_.bstack111111l1l1_opy_
        if method_name == bstack1llll1l_opy_ (u"ࠨࡥ࡯ࡳࡸ࡫ࠧ᎕"):
            return bstack11111l1l1l_opy_.QUIT
        return bstack11111l1l1l_opy_.NONE
    @staticmethod
    def bstack1l11ll1ll1l_opy_(bstack11111l1lll_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_]):
        return bstack1llll1l_opy_ (u"ࠤ࠽ࠦ᎖").join((bstack11111l1l1l_opy_(bstack11111l1lll_opy_[0]).name, bstack1llllll1l1l_opy_(bstack11111l1lll_opy_[1]).name))
    @staticmethod
    def bstack1ll1l1l1l1l_opy_(bstack11111l1lll_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_], callback: Callable):
        bstack1l11lll11ll_opy_ = bstack1llll11llll_opy_.bstack1l11ll1ll1l_opy_(bstack11111l1lll_opy_)
        if not bstack1l11lll11ll_opy_ in bstack1llll11llll_opy_.bstack1l11ll1l1ll_opy_:
            bstack1llll11llll_opy_.bstack1l11ll1l1ll_opy_[bstack1l11lll11ll_opy_] = []
        bstack1llll11llll_opy_.bstack1l11ll1l1ll_opy_[bstack1l11lll11ll_opy_].append(callback)
    @staticmethod
    def bstack1ll1l1ll1ll_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll1l111111_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1l11ll11_opy_(instance: bstack1111111ll1_opy_, default_value=None):
        return bstack11111lll11_opy_.bstack1lllllllll1_opy_(instance, bstack1llll11llll_opy_.bstack1l1ll111111_opy_, default_value)
    @staticmethod
    def bstack1ll111ll111_opy_(instance: bstack1111111ll1_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll11ll11l1_opy_(instance: bstack1111111ll1_opy_, default_value=None):
        return bstack11111lll11_opy_.bstack1lllllllll1_opy_(instance, bstack1llll11llll_opy_.bstack1l1ll11111l_opy_, default_value)
    @staticmethod
    def bstack1ll1l111l1l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l11llll_opy_(method_name: str, *args):
        if not bstack1llll11llll_opy_.bstack1ll1l1ll1ll_opy_(method_name):
            return False
        if not bstack1llll11llll_opy_.bstack1l11lll1111_opy_ in bstack1llll11llll_opy_.bstack1l1l11ll11l_opy_(*args):
            return False
        bstack1ll11l11lll_opy_ = bstack1llll11llll_opy_.bstack1ll11l11l1l_opy_(*args)
        return bstack1ll11l11lll_opy_ and bstack1llll1l_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥ᎗") in bstack1ll11l11lll_opy_ and bstack1llll1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧ᎘") in bstack1ll11l11lll_opy_[bstack1llll1l_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ᎙")]
    @staticmethod
    def bstack1ll1l1ll1l1_opy_(method_name: str, *args):
        if not bstack1llll11llll_opy_.bstack1ll1l1ll1ll_opy_(method_name):
            return False
        if not bstack1llll11llll_opy_.bstack1l11lll1111_opy_ in bstack1llll11llll_opy_.bstack1l1l11ll11l_opy_(*args):
            return False
        bstack1ll11l11lll_opy_ = bstack1llll11llll_opy_.bstack1ll11l11l1l_opy_(*args)
        return (
            bstack1ll11l11lll_opy_
            and bstack1llll1l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨ᎚") in bstack1ll11l11lll_opy_
            and bstack1llll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡨࡸࡩࡱࡶࠥ᎛") in bstack1ll11l11lll_opy_[bstack1llll1l_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣ᎜")]
        )
    @staticmethod
    def bstack1l1l11ll11l_opy_(*args):
        return str(bstack1llll11llll_opy_.bstack1ll1l111l1l_opy_(*args)).lower()