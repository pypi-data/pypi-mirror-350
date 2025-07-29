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
from bstack_utils.bstack1l1lll111l_opy_ import bstack1lllll11ll1_opy_
from bstack_utils.constants import EVENTS
class bstack1lllll1ll1l_opy_(bstack11111lll11_opy_):
    bstack1l11ll1ll11_opy_ = bstack1llll1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᓬ")
    NAME = bstack1llll1l_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᓭ")
    bstack1l1ll11111l_opy_ = bstack1llll1l_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࠦᓮ")
    bstack1l1l1lll11l_opy_ = bstack1llll1l_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᓯ")
    bstack1l11111ll11_opy_ = bstack1llll1l_opy_ (u"ࠧ࡯࡮ࡱࡷࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᓰ")
    bstack1l1ll111111_opy_ = bstack1llll1l_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᓱ")
    bstack1l11lll1ll1_opy_ = bstack1llll1l_opy_ (u"ࠢࡪࡵࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡫ࡹࡧࠨᓲ")
    bstack1l1111l111l_opy_ = bstack1llll1l_opy_ (u"ࠣࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᓳ")
    bstack1l11111lll1_opy_ = bstack1llll1l_opy_ (u"ࠤࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᓴ")
    bstack1ll11l1ll11_opy_ = bstack1llll1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠦᓵ")
    bstack1l1l111l11l_opy_ = bstack1llll1l_opy_ (u"ࠦࡳ࡫ࡷࡴࡧࡶࡷ࡮ࡵ࡮ࠣᓶ")
    bstack1l1111l1111_opy_ = bstack1llll1l_opy_ (u"ࠧ࡭ࡥࡵࠤᓷ")
    bstack1l1lllll111_opy_ = bstack1llll1l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᓸ")
    bstack1l11lll1111_opy_ = bstack1llll1l_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥᓹ")
    bstack1l11ll1lll1_opy_ = bstack1llll1l_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤᓺ")
    bstack1l11111llll_opy_ = bstack1llll1l_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᓻ")
    bstack1l11111l1l1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l11lll11_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1llll11l111_opy_: Any
    bstack1l11lll111l_opy_: Dict
    def __init__(
        self,
        bstack1l1l11lll11_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1llll11l111_opy_: Dict[str, Any],
        methods=[bstack1llll1l_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧᓼ"), bstack1llll1l_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᓽ"), bstack1llll1l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᓾ"), bstack1llll1l_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᓿ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1l11lll11_opy_ = bstack1l1l11lll11_opy_
        self.platform_index = platform_index
        self.bstack11111l111l_opy_(methods)
        self.bstack1llll11l111_opy_ = bstack1llll11l111_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack11111lll11_opy_.get_data(bstack1lllll1ll1l_opy_.bstack1l1l1lll11l_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack11111lll11_opy_.get_data(bstack1lllll1ll1l_opy_.bstack1l1ll11111l_opy_, target, strict)
    @staticmethod
    def bstack1l11111l1ll_opy_(target: object, strict=True):
        return bstack11111lll11_opy_.get_data(bstack1lllll1ll1l_opy_.bstack1l11111ll11_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack11111lll11_opy_.get_data(bstack1lllll1ll1l_opy_.bstack1l1ll111111_opy_, target, strict)
    @staticmethod
    def bstack1ll111ll111_opy_(instance: bstack1111111ll1_opy_) -> bool:
        return bstack11111lll11_opy_.bstack1lllllllll1_opy_(instance, bstack1lllll1ll1l_opy_.bstack1l11lll1ll1_opy_, False)
    @staticmethod
    def bstack1ll11ll11l1_opy_(instance: bstack1111111ll1_opy_, default_value=None):
        return bstack11111lll11_opy_.bstack1lllllllll1_opy_(instance, bstack1lllll1ll1l_opy_.bstack1l1ll11111l_opy_, default_value)
    @staticmethod
    def bstack1ll1l11ll11_opy_(instance: bstack1111111ll1_opy_, default_value=None):
        return bstack11111lll11_opy_.bstack1lllllllll1_opy_(instance, bstack1lllll1ll1l_opy_.bstack1l1ll111111_opy_, default_value)
    @staticmethod
    def bstack1ll11l1l111_opy_(hub_url: str, bstack1l11111l11l_opy_=bstack1llll1l_opy_ (u"ࠢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦᔀ")):
        try:
            bstack1l11111l111_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l11111l111_opy_.endswith(bstack1l11111l11l_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1l1ll1ll_opy_(method_name: str):
        return method_name == bstack1llll1l_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᔁ")
    @staticmethod
    def bstack1ll1l111111_opy_(method_name: str, *args):
        return (
            bstack1lllll1ll1l_opy_.bstack1ll1l1ll1ll_opy_(method_name)
            and bstack1lllll1ll1l_opy_.bstack1l1l11ll11l_opy_(*args) == bstack1lllll1ll1l_opy_.bstack1l1l111l11l_opy_
        )
    @staticmethod
    def bstack1ll1l11llll_opy_(method_name: str, *args):
        if not bstack1lllll1ll1l_opy_.bstack1ll1l1ll1ll_opy_(method_name):
            return False
        if not bstack1lllll1ll1l_opy_.bstack1l11lll1111_opy_ in bstack1lllll1ll1l_opy_.bstack1l1l11ll11l_opy_(*args):
            return False
        bstack1ll11l11lll_opy_ = bstack1lllll1ll1l_opy_.bstack1ll11l11l1l_opy_(*args)
        return bstack1ll11l11lll_opy_ and bstack1llll1l_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᔂ") in bstack1ll11l11lll_opy_ and bstack1llll1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᔃ") in bstack1ll11l11lll_opy_[bstack1llll1l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᔄ")]
    @staticmethod
    def bstack1ll1l1ll1l1_opy_(method_name: str, *args):
        if not bstack1lllll1ll1l_opy_.bstack1ll1l1ll1ll_opy_(method_name):
            return False
        if not bstack1lllll1ll1l_opy_.bstack1l11lll1111_opy_ in bstack1lllll1ll1l_opy_.bstack1l1l11ll11l_opy_(*args):
            return False
        bstack1ll11l11lll_opy_ = bstack1lllll1ll1l_opy_.bstack1ll11l11l1l_opy_(*args)
        return (
            bstack1ll11l11lll_opy_
            and bstack1llll1l_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᔅ") in bstack1ll11l11lll_opy_
            and bstack1llll1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡧࡷ࡯ࡰࡵࠤᔆ") in bstack1ll11l11lll_opy_[bstack1llll1l_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᔇ")]
        )
    @staticmethod
    def bstack1l1l11ll11l_opy_(*args):
        return str(bstack1lllll1ll1l_opy_.bstack1ll1l111l1l_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1l111l1l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11l11l1l_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack11l1lll111_opy_(driver):
        command_executor = getattr(driver, bstack1llll1l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᔈ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1llll1l_opy_ (u"ࠤࡢࡹࡷࡲࠢᔉ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1llll1l_opy_ (u"ࠥࡣࡨࡲࡩࡦࡰࡷࡣࡨࡵ࡮ࡧ࡫ࡪࠦᔊ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1llll1l_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡣࡸ࡫ࡲࡷࡧࡵࡣࡦࡪࡤࡳࠤᔋ"), None)
        return hub_url
    def bstack1l1l111111l_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1llll1l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᔌ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1llll1l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᔍ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1llll1l_opy_ (u"ࠢࡠࡷࡵࡰࠧᔎ")):
                setattr(command_executor, bstack1llll1l_opy_ (u"ࠣࡡࡸࡶࡱࠨᔏ"), hub_url)
                result = True
        if result:
            self.bstack1l1l11lll11_opy_ = hub_url
            bstack1lllll1ll1l_opy_.bstack111111111l_opy_(instance, bstack1lllll1ll1l_opy_.bstack1l1ll11111l_opy_, hub_url)
            bstack1lllll1ll1l_opy_.bstack111111111l_opy_(
                instance, bstack1lllll1ll1l_opy_.bstack1l11lll1ll1_opy_, bstack1lllll1ll1l_opy_.bstack1ll11l1l111_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11ll1ll1l_opy_(bstack11111l1lll_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_]):
        return bstack1llll1l_opy_ (u"ࠤ࠽ࠦᔐ").join((bstack11111l1l1l_opy_(bstack11111l1lll_opy_[0]).name, bstack1llllll1l1l_opy_(bstack11111l1lll_opy_[1]).name))
    @staticmethod
    def bstack1ll1l1l1l1l_opy_(bstack11111l1lll_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_], callback: Callable):
        bstack1l11lll11ll_opy_ = bstack1lllll1ll1l_opy_.bstack1l11ll1ll1l_opy_(bstack11111l1lll_opy_)
        if not bstack1l11lll11ll_opy_ in bstack1lllll1ll1l_opy_.bstack1l11111l1l1_opy_:
            bstack1lllll1ll1l_opy_.bstack1l11111l1l1_opy_[bstack1l11lll11ll_opy_] = []
        bstack1lllll1ll1l_opy_.bstack1l11111l1l1_opy_[bstack1l11lll11ll_opy_].append(callback)
    def bstack11111l1l11_opy_(self, instance: bstack1111111ll1_opy_, method_name: str, bstack111111l1ll_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1llll1l_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᔑ")):
            return
        cmd = args[0] if method_name == bstack1llll1l_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᔒ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l11111ll1l_opy_ = bstack1llll1l_opy_ (u"ࠧࡀࠢᔓ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠢᔔ") + bstack1l11111ll1l_opy_, bstack111111l1ll_opy_)
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
        bstack1l11lll11ll_opy_ = bstack1lllll1ll1l_opy_.bstack1l11ll1ll1l_opy_(bstack11111l1lll_opy_)
        self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡰࡰࡢ࡬ࡴࡵ࡫࠻ࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᔕ") + str(kwargs) + bstack1llll1l_opy_ (u"ࠣࠤᔖ"))
        if bstack11111l11ll_opy_ == bstack11111l1l1l_opy_.QUIT:
            if bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.PRE:
                bstack1ll1l1l11ll_opy_ = bstack1lllll11ll1_opy_.bstack1ll1ll11l11_opy_(EVENTS.bstack11ll1l1l1l_opy_.value)
                bstack11111lll11_opy_.bstack111111111l_opy_(instance, EVENTS.bstack11ll1l1l1l_opy_.value, bstack1ll1l1l11ll_opy_)
                self.logger.debug(bstack1llll1l_opy_ (u"ࠤ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠨᔗ").format(instance, method_name, bstack11111l11ll_opy_, bstack1l11ll1llll_opy_))
        if bstack11111l11ll_opy_ == bstack11111l1l1l_opy_.bstack11111ll111_opy_:
            if bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.POST and not bstack1lllll1ll1l_opy_.bstack1l1l1lll11l_opy_ in instance.data:
                session_id = getattr(target, bstack1llll1l_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᔘ"), None)
                if session_id:
                    instance.data[bstack1lllll1ll1l_opy_.bstack1l1l1lll11l_opy_] = session_id
        elif (
            bstack11111l11ll_opy_ == bstack11111l1l1l_opy_.bstack111111llll_opy_
            and bstack1lllll1ll1l_opy_.bstack1l1l11ll11l_opy_(*args) == bstack1lllll1ll1l_opy_.bstack1l1l111l11l_opy_
        ):
            if bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.PRE:
                hub_url = bstack1lllll1ll1l_opy_.bstack11l1lll111_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1lllll1ll1l_opy_.bstack1l1ll11111l_opy_: hub_url,
                            bstack1lllll1ll1l_opy_.bstack1l11lll1ll1_opy_: bstack1lllll1ll1l_opy_.bstack1ll11l1l111_opy_(hub_url),
                            bstack1lllll1ll1l_opy_.bstack1ll11l1ll11_opy_: int(
                                os.environ.get(bstack1llll1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦᔙ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll11l11lll_opy_ = bstack1lllll1ll1l_opy_.bstack1ll11l11l1l_opy_(*args)
                bstack1l11111l1ll_opy_ = bstack1ll11l11lll_opy_.get(bstack1llll1l_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᔚ"), None) if bstack1ll11l11lll_opy_ else None
                if isinstance(bstack1l11111l1ll_opy_, dict):
                    instance.data[bstack1lllll1ll1l_opy_.bstack1l11111ll11_opy_] = copy.deepcopy(bstack1l11111l1ll_opy_)
                    instance.data[bstack1lllll1ll1l_opy_.bstack1l1ll111111_opy_] = bstack1l11111l1ll_opy_
            elif bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1llll1l_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᔛ"), dict()).get(bstack1llll1l_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡊࡦࠥᔜ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1lllll1ll1l_opy_.bstack1l1l1lll11l_opy_: framework_session_id,
                                bstack1lllll1ll1l_opy_.bstack1l1111l111l_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack11111l11ll_opy_ == bstack11111l1l1l_opy_.bstack111111llll_opy_
            and bstack1lllll1ll1l_opy_.bstack1l1l11ll11l_opy_(*args) == bstack1lllll1ll1l_opy_.bstack1l11111llll_opy_
            and bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.POST
        ):
            instance.data[bstack1lllll1ll1l_opy_.bstack1l11111lll1_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11lll11ll_opy_ in bstack1lllll1ll1l_opy_.bstack1l11111l1l1_opy_:
            bstack1l11ll1l1l1_opy_ = None
            for callback in bstack1lllll1ll1l_opy_.bstack1l11111l1l1_opy_[bstack1l11lll11ll_opy_]:
                try:
                    bstack1l11lll11l1_opy_ = callback(self, target, exec, bstack11111l1lll_opy_, result, *args, **kwargs)
                    if bstack1l11ll1l1l1_opy_ == None:
                        bstack1l11ll1l1l1_opy_ = bstack1l11lll11l1_opy_
                except Exception as e:
                    self.logger.error(bstack1llll1l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨᔝ") + str(e) + bstack1llll1l_opy_ (u"ࠤࠥᔞ"))
                    traceback.print_exc()
            if bstack11111l11ll_opy_ == bstack11111l1l1l_opy_.QUIT:
                if bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.POST:
                    bstack1ll1l1l11ll_opy_ = bstack11111lll11_opy_.bstack1lllllllll1_opy_(instance, EVENTS.bstack11ll1l1l1l_opy_.value)
                    if bstack1ll1l1l11ll_opy_!=None:
                        bstack1lllll11ll1_opy_.end(EVENTS.bstack11ll1l1l1l_opy_.value, bstack1ll1l1l11ll_opy_+bstack1llll1l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᔟ"), bstack1ll1l1l11ll_opy_+bstack1llll1l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᔠ"), True, None)
            if bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.PRE and callable(bstack1l11ll1l1l1_opy_):
                return bstack1l11ll1l1l1_opy_
            elif bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.POST and bstack1l11ll1l1l1_opy_:
                return bstack1l11ll1l1l1_opy_
    def bstack111111l111_opy_(
        self, method_name, previous_state: bstack11111l1l1l_opy_, *args, **kwargs
    ) -> bstack11111l1l1l_opy_:
        if method_name == bstack1llll1l_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᔡ") or method_name == bstack1llll1l_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᔢ"):
            return bstack11111l1l1l_opy_.bstack11111ll111_opy_
        if method_name == bstack1llll1l_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᔣ"):
            return bstack11111l1l1l_opy_.QUIT
        if method_name == bstack1llll1l_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᔤ"):
            if previous_state != bstack11111l1l1l_opy_.NONE:
                bstack1ll1l11l11l_opy_ = bstack1lllll1ll1l_opy_.bstack1l1l11ll11l_opy_(*args)
                if bstack1ll1l11l11l_opy_ == bstack1lllll1ll1l_opy_.bstack1l1l111l11l_opy_:
                    return bstack11111l1l1l_opy_.bstack11111ll111_opy_
            return bstack11111l1l1l_opy_.bstack111111llll_opy_
        return bstack11111l1l1l_opy_.NONE