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
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lllllll111_opy_ import (
    bstack11111l1l1l_opy_,
    bstack1llllll1l1l_opy_,
    bstack11111lll11_opy_,
    bstack1111111ll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1lllll1ll1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1llll1ll_opy_, bstack1llll1l1lll_opy_, bstack1llll111111_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1llll111_opy_ import bstack1lll1l1llll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1111_opy_ import bstack1ll1lll1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1lll_opy_ import bstack1lllll11111_opy_
from browserstack_sdk.sdk_cli.bstack1llll111l11_opy_ import bstack1llll11llll_opy_
from bstack_utils.helper import bstack1ll1ll11111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1l1lll111l_opy_ import bstack1lllll11ll1_opy_
import grpc
import traceback
import json
class bstack1lll11llll1_opy_(bstack1lll1l1llll_opy_):
    bstack1ll1l1l1111_opy_ = False
    bstack1ll11ll111l_opy_ = bstack1llll1l_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࠨᄘ")
    bstack1ll11l1ll1l_opy_ = bstack1llll1l_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦ࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶࠧᄙ")
    bstack1ll1l111ll1_opy_ = bstack1llll1l_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢ࡭ࡳ࡯ࡴࠣᄚ")
    bstack1ll1l1l111l_opy_ = bstack1llll1l_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣ࡮ࡹ࡟ࡴࡥࡤࡲࡳ࡯࡮ࡨࠤᄛ")
    bstack1ll1l1ll111_opy_ = bstack1llll1l_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶࡤ࡮ࡡࡴࡡࡸࡶࡱࠨᄜ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1lll11111ll_opy_, bstack1ll1ll1llll_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        if not self.is_enabled():
            return
        self.bstack1ll1l1l1ll1_opy_ = bstack1ll1ll1llll_opy_
        bstack1lll11111ll_opy_.bstack1ll1l1l1l1l_opy_((bstack11111l1l1l_opy_.bstack111111llll_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1ll11lll1l1_opy_)
        TestFramework.bstack1ll1l1l1l1l_opy_((bstack1ll1llll1ll_opy_.TEST, bstack1llll1l1lll_opy_.PRE), self.bstack1ll11ll1111_opy_)
        TestFramework.bstack1ll1l1l1l1l_opy_((bstack1ll1llll1ll_opy_.TEST, bstack1llll1l1lll_opy_.POST), self.bstack1ll1l1l11l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11ll1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111111_opy_,
        bstack11111l1lll_opy_: Tuple[bstack1ll1llll1ll_opy_, bstack1llll1l1lll_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll11llll1l_opy_(instance, args)
        test_framework = f.bstack1lllllllll1_opy_(instance, TestFramework.bstack1ll1ll1111l_opy_)
        if bstack1llll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᄝ") in instance.bstack1ll11lll11l_opy_:
            platform_index = f.bstack1lllllllll1_opy_(instance, TestFramework.bstack1ll11l1ll11_opy_)
            self.accessibility = self.bstack1ll1l1111l1_opy_(tags, self.config[bstack1llll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᄞ")][platform_index])
        else:
            capabilities = self.bstack1ll1l1l1ll1_opy_.bstack1ll11ll1l1l_opy_(f, instance, bstack11111l1lll_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1llll1l_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᄟ") + str(kwargs) + bstack1llll1l_opy_ (u"ࠤࠥᄠ"))
                return
            self.accessibility = self.bstack1ll1l1111l1_opy_(tags, capabilities)
        if self.bstack1ll1l1l1ll1_opy_.pages and self.bstack1ll1l1l1ll1_opy_.pages.values():
            bstack1ll11ll11ll_opy_ = list(self.bstack1ll1l1l1ll1_opy_.pages.values())
            if bstack1ll11ll11ll_opy_ and isinstance(bstack1ll11ll11ll_opy_[0], (list, tuple)) and bstack1ll11ll11ll_opy_[0]:
                bstack1ll1l1lll1l_opy_ = bstack1ll11ll11ll_opy_[0][0]
                if callable(bstack1ll1l1lll1l_opy_):
                    page = bstack1ll1l1lll1l_opy_()
                    def bstack1l1l1ll11l_opy_():
                        self.get_accessibility_results(page, bstack1llll1l_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᄡ"))
                    def bstack1ll1l11l1ll_opy_():
                        self.get_accessibility_results_summary(page, bstack1llll1l_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᄢ"))
                    setattr(page, bstack1llll1l_opy_ (u"ࠧ࡭ࡥࡵࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡓࡧࡶࡹࡱࡺࡳࠣᄣ"), bstack1l1l1ll11l_opy_)
                    setattr(page, bstack1llll1l_opy_ (u"ࠨࡧࡦࡶࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡔࡨࡷࡺࡲࡴࡔࡷࡰࡱࡦࡸࡹࠣᄤ"), bstack1ll1l11l1ll_opy_)
        self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡴࡪࡲࡹࡱࡪࠠࡳࡷࡱࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡻࡧ࡬ࡶࡧࡀࠦᄥ") + str(self.accessibility) + bstack1llll1l_opy_ (u"ࠣࠤᄦ"))
    def bstack1ll11lll1l1_opy_(
        self,
        f: bstack1lllll1ll1l_opy_,
        driver: object,
        exec: Tuple[bstack1111111ll1_opy_, str],
        bstack11111l1lll_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1l11l1lll_opy_ = datetime.now()
            self.bstack1ll11ll1lll_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡪࡰ࡬ࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡩ࡯࡯ࡨ࡬࡫ࠧᄧ"), datetime.now() - bstack1l11l1lll_opy_)
            if (
                not f.bstack1ll1l1ll1ll_opy_(method_name)
                or f.bstack1ll1l11llll_opy_(method_name, *args)
                or f.bstack1ll1l1ll1l1_opy_(method_name, *args)
            ):
                return
            if not f.bstack1lllllllll1_opy_(instance, bstack1lll11llll1_opy_.bstack1ll1l111ll1_opy_, False):
                if not bstack1lll11llll1_opy_.bstack1ll1l1l1111_opy_:
                    self.logger.warning(bstack1llll1l_opy_ (u"ࠥ࡟ࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨᄨ") + str(f.platform_index) + bstack1llll1l_opy_ (u"ࠦࡢࠦࡡ࠲࠳ࡼࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣ࡬ࡦࡼࡥࠡࡰࡲࡸࠥࡨࡥࡦࡰࠣࡷࡪࡺࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡶࡩࡸࡹࡩࡰࡰࠥᄩ"))
                    bstack1lll11llll1_opy_.bstack1ll1l1l1111_opy_ = True
                return
            bstack1ll1l11l1l1_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll1l11l1l1_opy_:
                platform_index = f.bstack1lllllllll1_opy_(instance, bstack1lllll1ll1l_opy_.bstack1ll11l1ll11_opy_, 0)
                self.logger.debug(bstack1llll1l_opy_ (u"ࠧࡴ࡯ࠡࡣ࠴࠵ࡾࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࢁࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᄪ") + str(f.framework_name) + bstack1llll1l_opy_ (u"ࠨࠢᄫ"))
                return
            bstack1ll1l11l11l_opy_ = f.bstack1ll1l111l1l_opy_(*args)
            if not bstack1ll1l11l11l_opy_:
                self.logger.debug(bstack1llll1l_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫ࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࠤᄬ") + str(method_name) + bstack1llll1l_opy_ (u"ࠣࠤᄭ"))
                return
            bstack1ll11l1llll_opy_ = f.bstack1lllllllll1_opy_(instance, bstack1lll11llll1_opy_.bstack1ll1l1ll111_opy_, False)
            if bstack1ll1l11l11l_opy_ == bstack1llll1l_opy_ (u"ࠤࡪࡩࡹࠨᄮ") and not bstack1ll11l1llll_opy_:
                f.bstack111111111l_opy_(instance, bstack1lll11llll1_opy_.bstack1ll1l1ll111_opy_, True)
                bstack1ll11l1llll_opy_ = True
            if not bstack1ll11l1llll_opy_:
                self.logger.debug(bstack1llll1l_opy_ (u"ࠥࡲࡴࠦࡕࡓࡎࠣࡰࡴࡧࡤࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥ࠾ࠤᄯ") + str(bstack1ll1l11l11l_opy_) + bstack1llll1l_opy_ (u"ࠦࠧᄰ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1ll1l11l11l_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstack1llll1l_opy_ (u"ࠧࡴ࡯ࠡࡣ࠴࠵ࡾࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦ࠿ࠥᄱ") + str(bstack1ll1l11l11l_opy_) + bstack1llll1l_opy_ (u"ࠨࠢᄲ"))
                return
            self.logger.info(bstack1llll1l_opy_ (u"ࠢࡳࡷࡱࡲ࡮ࡴࡧࠡࡽ࡯ࡩࡳ࠮ࡳࡤࡴ࡬ࡴࡹࡹ࡟ࡵࡱࡢࡶࡺࡴࠩࡾࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥ࠾ࠤᄳ") + str(bstack1ll1l11l11l_opy_) + bstack1llll1l_opy_ (u"ࠣࠤᄴ"))
            scripts = [(s, bstack1ll1l11l1l1_opy_[s]) for s in scripts_to_run if s in bstack1ll1l11l1l1_opy_]
            for script_name, bstack1ll1ll111l1_opy_ in scripts:
                try:
                    bstack1l11l1lll_opy_ = datetime.now()
                    if script_name == bstack1llll1l_opy_ (u"ࠤࡶࡧࡦࡴࠢᄵ"):
                        result = self.perform_scan(driver, method=bstack1ll1l11l11l_opy_, framework_name=f.framework_name)
                    instance.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࠤᄶ") + script_name, datetime.now() - bstack1l11l1lll_opy_)
                    if isinstance(result, dict) and not result.get(bstack1llll1l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᄷ"), True):
                        self.logger.warning(bstack1llll1l_opy_ (u"ࠧࡹ࡫ࡪࡲࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡲࡦ࡯ࡤ࡭ࡳ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵࡵ࠽ࠤࠧᄸ") + str(result) + bstack1llll1l_opy_ (u"ࠨࠢᄹ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1llll1l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵ࠿ࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾࠢࡨࡶࡷࡵࡲ࠾ࠤᄺ") + str(e) + bstack1llll1l_opy_ (u"ࠣࠤᄻ"))
        except Exception as e:
            self.logger.error(bstack1llll1l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡥࡳࡴࡲࡶࡂࠨᄼ") + str(e) + bstack1llll1l_opy_ (u"ࠥࠦᄽ"))
    def bstack1ll1l1l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111111_opy_,
        bstack11111l1lll_opy_: Tuple[bstack1ll1llll1ll_opy_, bstack1llll1l1lll_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll11llll1l_opy_(instance, args)
        capabilities = self.bstack1ll1l1l1ll1_opy_.bstack1ll11ll1l1l_opy_(f, instance, bstack11111l1lll_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll1l1111l1_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠣᄾ"))
            return
        driver = self.bstack1ll1l1l1ll1_opy_.bstack1ll1l1l1lll_opy_(f, instance, bstack11111l1lll_opy_, *args, **kwargs)
        test_name = f.bstack1lllllllll1_opy_(instance, TestFramework.bstack1ll1l11lll1_opy_)
        if not test_name:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥᄿ"))
            return
        test_uuid = f.bstack1lllllllll1_opy_(instance, TestFramework.bstack1ll11lll1ll_opy_)
        if not test_uuid:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡵࡶ࡫ࡧࠦᅀ"))
            return
        if isinstance(self.bstack1ll1l1l1ll1_opy_, bstack1lllll11111_opy_):
            framework_name = bstack1llll1l_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᅁ")
        else:
            framework_name = bstack1llll1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪᅂ")
        self.bstack11l1111ll_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll1l1l11ll_opy_ = bstack1lllll11ll1_opy_.bstack1ll1ll11l11_opy_(EVENTS.bstack11l11ll1l_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࠥᅃ"))
            return
        bstack1l11l1lll_opy_ = datetime.now()
        bstack1ll1ll111l1_opy_ = self.scripts.get(framework_name, {}).get(bstack1llll1l_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᅄ"), None)
        if not bstack1ll1ll111l1_opy_:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡳࡤࡣࡱࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᅅ") + str(framework_name) + bstack1llll1l_opy_ (u"ࠧࠦࠢᅆ"))
            return
        instance = bstack11111lll11_opy_.bstack111111l11l_opy_(driver)
        if instance:
            if not bstack11111lll11_opy_.bstack1lllllllll1_opy_(instance, bstack1lll11llll1_opy_.bstack1ll1l1l111l_opy_, False):
                bstack11111lll11_opy_.bstack111111111l_opy_(instance, bstack1lll11llll1_opy_.bstack1ll1l1l111l_opy_, True)
            else:
                self.logger.info(bstack1llll1l_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡪࡰࠣࡴࡷࡵࡧࡳࡧࡶࡷࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡰࡩࡹ࡮࡯ࡥ࠿ࠥᅇ") + str(method) + bstack1llll1l_opy_ (u"ࠢࠣᅈ"))
                return
        self.logger.info(bstack1llll1l_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡂࠨᅉ") + str(method) + bstack1llll1l_opy_ (u"ࠤࠥᅊ"))
        if framework_name == bstack1llll1l_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᅋ"):
            result = self.bstack1ll1l1l1ll1_opy_.bstack1ll11lllll1_opy_(driver, bstack1ll1ll111l1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1ll111l1_opy_, {bstack1llll1l_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᅌ"): method if method else bstack1llll1l_opy_ (u"ࠧࠨᅍ")})
        bstack1lllll11ll1_opy_.end(EVENTS.bstack11l11ll1l_opy_.value, bstack1ll1l1l11ll_opy_+bstack1llll1l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᅎ"), bstack1ll1l1l11ll_opy_+bstack1llll1l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᅏ"), True, None, command=method)
        if instance:
            bstack11111lll11_opy_.bstack111111111l_opy_(instance, bstack1lll11llll1_opy_.bstack1ll1l1l111l_opy_, False)
            instance.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲࠧᅐ"), datetime.now() - bstack1l11l1lll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l111l11_opy_, stage=STAGE.bstack11111l1l1_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠦᅑ"))
            return
        bstack1ll1ll111l1_opy_ = self.scripts.get(framework_name, {}).get(bstack1llll1l_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢᅒ"), None)
        if not bstack1ll1ll111l1_opy_:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᅓ") + str(framework_name) + bstack1llll1l_opy_ (u"ࠧࠨᅔ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l11l1lll_opy_ = datetime.now()
        if framework_name == bstack1llll1l_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᅕ"):
            result = self.bstack1ll1l1l1ll1_opy_.bstack1ll11lllll1_opy_(driver, bstack1ll1ll111l1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1ll111l1_opy_)
        instance = bstack11111lll11_opy_.bstack111111l11l_opy_(driver)
        if instance:
            instance.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࠥᅖ"), datetime.now() - bstack1l11l1lll_opy_)
        return result
    @measure(event_name=EVENTS.bstack11llll1l1_opy_, stage=STAGE.bstack11111l1l1_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠦᅗ"))
            return
        bstack1ll1ll111l1_opy_ = self.scripts.get(framework_name, {}).get(bstack1llll1l_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨᅘ"), None)
        if not bstack1ll1ll111l1_opy_:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᅙ") + str(framework_name) + bstack1llll1l_opy_ (u"ࠦࠧᅚ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l11l1lll_opy_ = datetime.now()
        if framework_name == bstack1llll1l_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᅛ"):
            result = self.bstack1ll1l1l1ll1_opy_.bstack1ll11lllll1_opy_(driver, bstack1ll1ll111l1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1ll111l1_opy_)
        instance = bstack11111lll11_opy_.bstack111111l11l_opy_(driver)
        if instance:
            instance.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻࠥᅜ"), datetime.now() - bstack1l11l1lll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1ll111ll_opy_, stage=STAGE.bstack11111l1l1_opy_)
    def bstack1ll1l1ll11l_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll11llllll_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1llll111l1l_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᅝ") + str(r) + bstack1llll1l_opy_ (u"ࠣࠤᅞ"))
            else:
                self.bstack1ll11ll1l11_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1llll1l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᅟ") + str(e) + bstack1llll1l_opy_ (u"ࠥࠦᅠ"))
            traceback.print_exc()
            raise e
    def bstack1ll11ll1l11_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠦࡱࡵࡡࡥࡡࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦᅡ"))
            return False
        if result.accessibility.options:
            options = result.accessibility.options
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll1l1lllll_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll11ll111l_opy_ and command.module == self.bstack1ll11l1ll1l_opy_:
                        if command.method and not command.method in bstack1ll1l1lllll_opy_:
                            bstack1ll1l1lllll_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll1l1lllll_opy_[command.method]:
                            bstack1ll1l1lllll_opy_[command.method][command.name] = list()
                        bstack1ll1l1lllll_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll1l1lllll_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll11ll1lll_opy_(
        self,
        f: bstack1lllll1ll1l_opy_,
        exec: Tuple[bstack1111111ll1_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll1l1l1ll1_opy_, bstack1lllll11111_opy_) and method_name != bstack1llll1l_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹ࠭ᅢ"):
            return
        if bstack11111lll11_opy_.bstack111111ll1l_opy_(instance, bstack1lll11llll1_opy_.bstack1ll1l111ll1_opy_):
            return
        if f.bstack1ll1l111111_opy_(method_name, *args):
            bstack1ll1l1lll11_opy_ = False
            desired_capabilities = f.bstack1ll1l11ll11_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll11ll11l1_opy_(instance)
                platform_index = f.bstack1lllllllll1_opy_(instance, bstack1lllll1ll1l_opy_.bstack1ll11l1ll11_opy_, 0)
                bstack1ll1l111l11_opy_ = datetime.now()
                r = self.bstack1ll1l1ll11l_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡨࡵ࡮ࡧ࡫ࡪࠦᅣ"), datetime.now() - bstack1ll1l111l11_opy_)
                bstack1ll1l1lll11_opy_ = r.success
            else:
                self.logger.error(bstack1llll1l_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡦࡨࡷ࡮ࡸࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠾ࠤᅤ") + str(desired_capabilities) + bstack1llll1l_opy_ (u"ࠣࠤᅥ"))
            f.bstack111111111l_opy_(instance, bstack1lll11llll1_opy_.bstack1ll1l111ll1_opy_, bstack1ll1l1lll11_opy_)
    def bstack1ll1l11l1l_opy_(self, test_tags):
        bstack1ll1l1ll11l_opy_ = self.config.get(bstack1llll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᅦ"))
        if not bstack1ll1l1ll11l_opy_:
            return True
        try:
            include_tags = bstack1ll1l1ll11l_opy_[bstack1llll1l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᅧ")] if bstack1llll1l_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᅨ") in bstack1ll1l1ll11l_opy_ and isinstance(bstack1ll1l1ll11l_opy_[bstack1llll1l_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᅩ")], list) else []
            exclude_tags = bstack1ll1l1ll11l_opy_[bstack1llll1l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᅪ")] if bstack1llll1l_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᅫ") in bstack1ll1l1ll11l_opy_ and isinstance(bstack1ll1l1ll11l_opy_[bstack1llll1l_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᅬ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤᅭ") + str(error))
        return False
    def bstack11ll1l1ll1_opy_(self, caps):
        try:
            bstack1ll11l1lll1_opy_ = caps.get(bstack1llll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᅮ"), {}).get(bstack1llll1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᅯ"), caps.get(bstack1llll1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᅰ"), bstack1llll1l_opy_ (u"࠭ࠧᅱ")))
            if bstack1ll11l1lll1_opy_:
                self.logger.warning(bstack1llll1l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᅲ"))
                return False
            browser = caps.get(bstack1llll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᅳ"), bstack1llll1l_opy_ (u"ࠩࠪᅴ")).lower()
            if browser != bstack1llll1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᅵ"):
                self.logger.warning(bstack1llll1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᅶ"))
                return False
            bstack1ll1l1111ll_opy_ = bstack1ll11lll111_opy_
            if not self.config.get(bstack1llll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᅷ")) or self.config.get(bstack1llll1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪᅸ")):
                bstack1ll1l1111ll_opy_ = bstack1ll11llll11_opy_
            browser_version = caps.get(bstack1llll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᅹ"))
            if not browser_version:
                browser_version = caps.get(bstack1llll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᅺ"), {}).get(bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᅻ"), bstack1llll1l_opy_ (u"ࠪࠫᅼ"))
            if browser_version and browser_version != bstack1llll1l_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫᅽ") and int(browser_version.split(bstack1llll1l_opy_ (u"ࠬ࠴ࠧᅾ"))[0]) <= bstack1ll1l1111ll_opy_:
                self.logger.warning(bstack1llll1l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠࠣᅿ") + str(bstack1ll1l1111ll_opy_) + bstack1llll1l_opy_ (u"ࠢ࠯ࠤᆀ"))
                return False
            bstack1ll1l111lll_opy_ = caps.get(bstack1llll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᆁ"), {}).get(bstack1llll1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᆂ"))
            if not bstack1ll1l111lll_opy_:
                bstack1ll1l111lll_opy_ = caps.get(bstack1llll1l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᆃ"), {})
            if bstack1ll1l111lll_opy_ and bstack1llll1l_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᆄ") in bstack1ll1l111lll_opy_.get(bstack1llll1l_opy_ (u"ࠬࡧࡲࡨࡵࠪᆅ"), []):
                self.logger.warning(bstack1llll1l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᆆ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤᆇ") + str(error))
            return False
    def bstack1ll1l11ll1l_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1ll1l11l111_opy_ = {
            bstack1llll1l_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨᆈ"): test_uuid,
        }
        bstack1ll1l1llll1_opy_ = {}
        if result.success:
            bstack1ll1l1llll1_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll1ll11111_opy_(bstack1ll1l11l111_opy_, bstack1ll1l1llll1_opy_)
    def bstack11l1111ll_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll1l1l11ll_opy_ = None
        try:
            self.bstack1ll11llllll_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1llll1l_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤᆉ")
            req.script_name = bstack1llll1l_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣᆊ")
            r = self.bstack1llll111l1l_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1llll1l_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡤࡳ࡫ࡹࡩࡷࠦࡥࡹࡧࡦࡹࡹ࡫ࠠࡱࡣࡵࡥࡲࡹࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᆋ") + str(r.error) + bstack1llll1l_opy_ (u"ࠧࠨᆌ"))
            else:
                bstack1ll1l11l111_opy_ = self.bstack1ll1l11ll1l_opy_(test_uuid, r)
                bstack1ll1ll111l1_opy_ = r.script
            self.logger.debug(bstack1llll1l_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡤࡺ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩᆍ") + str(bstack1ll1l11l111_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll1ll111l1_opy_:
                self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᆎ") + str(framework_name) + bstack1llll1l_opy_ (u"ࠣࠢࠥᆏ"))
                return
            bstack1ll1l1l11ll_opy_ = bstack1lllll11ll1_opy_.bstack1ll1ll11l11_opy_(EVENTS.bstack1ll11ll1ll1_opy_.value)
            self.bstack1ll1l11111l_opy_(driver, bstack1ll1ll111l1_opy_, bstack1ll1l11l111_opy_, framework_name)
            self.logger.info(bstack1llll1l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧᆐ"))
            bstack1lllll11ll1_opy_.end(EVENTS.bstack1ll11ll1ll1_opy_.value, bstack1ll1l1l11ll_opy_+bstack1llll1l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᆑ"), bstack1ll1l1l11ll_opy_+bstack1llll1l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᆒ"), True, None, command=bstack1llll1l_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᆓ"),test_name=name)
        except Exception as bstack1ll1l1l1l11_opy_:
            self.logger.error(bstack1llll1l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣᆔ") + bstack1llll1l_opy_ (u"ࠢࡴࡶࡵࠬࡵࡧࡴࡩࠫࠥᆕ") + bstack1llll1l_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥᆖ") + str(bstack1ll1l1l1l11_opy_))
            bstack1lllll11ll1_opy_.end(EVENTS.bstack1ll11ll1ll1_opy_.value, bstack1ll1l1l11ll_opy_+bstack1llll1l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᆗ"), bstack1ll1l1l11ll_opy_+bstack1llll1l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᆘ"), False, bstack1ll1l1l1l11_opy_, command=bstack1llll1l_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩᆙ"),test_name=name)
    def bstack1ll1l11111l_opy_(self, driver, bstack1ll1ll111l1_opy_, bstack1ll1l11l111_opy_, framework_name):
        if framework_name == bstack1llll1l_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᆚ"):
            self.bstack1ll1l1l1ll1_opy_.bstack1ll11lllll1_opy_(driver, bstack1ll1ll111l1_opy_, bstack1ll1l11l111_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll1ll111l1_opy_, bstack1ll1l11l111_opy_))
    def _1ll11llll1l_opy_(self, instance: bstack1llll111111_opy_, args: Tuple) -> list:
        bstack1llll1l_opy_ (u"ࠨࠢࠣࡇࡻࡸࡷࡧࡣࡵࠢࡷࡥ࡬ࡹࠠࡣࡣࡶࡩࡩࠦ࡯࡯ࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࠣࠤࠥᆛ")
        if bstack1llll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᆜ") in instance.bstack1ll11lll11l_opy_:
            return args[2].tags if hasattr(args[2], bstack1llll1l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᆝ")) else []
        if hasattr(args[0], bstack1llll1l_opy_ (u"ࠩࡲࡻࡳࡥ࡭ࡢࡴ࡮ࡩࡷࡹࠧᆞ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll1l1111l1_opy_(self, tags, capabilities):
        return self.bstack1ll1l11l1l_opy_(tags) and self.bstack11ll1l1ll1_opy_(capabilities)