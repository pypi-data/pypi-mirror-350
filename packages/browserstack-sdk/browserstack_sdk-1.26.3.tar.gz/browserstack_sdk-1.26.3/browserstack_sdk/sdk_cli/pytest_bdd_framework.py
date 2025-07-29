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
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lllllll11l_opy_ import bstack1llllll1lll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll111lll1_opy_ import bstack1l111ll11ll_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll1llll1ll_opy_,
    bstack1llll111111_opy_,
    bstack1llll1l1lll_opy_,
    bstack1l111l11l1l_opy_,
    bstack1ll1lll1lll_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1lll1l111_opy_
from bstack_utils.bstack1l1lll111l_opy_ import bstack1lllll11ll1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1lllll11l1l_opy_ import bstack1lll111llll_opy_
from browserstack_sdk.sdk_cli.bstack1111l1111l_opy_ import bstack11111llll1_opy_
bstack1l1llll1111_opy_ = bstack1l1lll1l111_opy_()
bstack1l1lll111ll_opy_ = bstack1llll1l_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤ᎝")
bstack1l11l1l1lll_opy_ = bstack1llll1l_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨ᎞")
bstack1l111l1ll11_opy_ = bstack1llll1l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥ᎟")
bstack1l11ll11111_opy_ = 1.0
_1l1lllll1ll_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l111lll1l1_opy_ = bstack1llll1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᎠ")
    bstack1l11l1lll1l_opy_ = bstack1llll1l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࠦᎡ")
    bstack1l1111lllll_opy_ = bstack1llll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᎢ")
    bstack1l1111llll1_opy_ = bstack1llll1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࠥᎣ")
    bstack1l11l1l1l1l_opy_ = bstack1llll1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᎤ")
    bstack1l11l1l1111_opy_: bool
    bstack1111l1111l_opy_: bstack11111llll1_opy_  = None
    bstack1l1111ll111_opy_ = [
        bstack1ll1llll1ll_opy_.BEFORE_ALL,
        bstack1ll1llll1ll_opy_.AFTER_ALL,
        bstack1ll1llll1ll_opy_.BEFORE_EACH,
        bstack1ll1llll1ll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111l1l111_opy_: Dict[str, str],
        bstack1ll11lll11l_opy_: List[str]=[bstack1llll1l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᎥ")],
        bstack1111l1111l_opy_: bstack11111llll1_opy_ = None,
        bstack1llll111l1l_opy_=None
    ):
        super().__init__(bstack1ll11lll11l_opy_, bstack1l111l1l111_opy_, bstack1111l1111l_opy_)
        self.bstack1l11l1l1111_opy_ = any(bstack1llll1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᎦ") in item.lower() for item in bstack1ll11lll11l_opy_)
        self.bstack1llll111l1l_opy_ = bstack1llll111l1l_opy_
    def track_event(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1ll1llll1ll_opy_,
        test_hook_state: bstack1llll1l1lll_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll1llll1ll_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l1111ll111_opy_:
            bstack1l111ll11ll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll1llll1ll_opy_.NONE:
            self.logger.warning(bstack1llll1l_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࠨᎧ") + str(test_hook_state) + bstack1llll1l_opy_ (u"ࠨࠢᎨ"))
            return
        if not self.bstack1l11l1l1111_opy_:
            self.logger.warning(bstack1llll1l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠽ࠣᎩ") + str(str(self.bstack1ll11lll11l_opy_)) + bstack1llll1l_opy_ (u"ࠣࠤᎪ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1llll1l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᎫ") + str(kwargs) + bstack1llll1l_opy_ (u"ࠥࠦᎬ"))
            return
        instance = self.__1l111lllll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡦࡸࡧࡴ࠿ࠥᎭ") + str(args) + bstack1llll1l_opy_ (u"ࠧࠨᎮ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l1111ll111_opy_ and test_hook_state == bstack1llll1l1lll_opy_.PRE:
                bstack1ll1l1l11ll_opy_ = bstack1lllll11ll1_opy_.bstack1ll1ll11l11_opy_(EVENTS.bstack11l1lll11l_opy_.value)
                name = str(EVENTS.bstack11l1lll11l_opy_.name)+bstack1llll1l_opy_ (u"ࠨ࠺ࠣᎯ")+str(test_framework_state.name)
                TestFramework.bstack1l111l1ll1l_opy_(instance, name, bstack1ll1l1l11ll_opy_)
        except Exception as e:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴࠣࡴࡷ࡫࠺ࠡࡽࢀࠦᎰ").format(e))
        try:
            if test_framework_state == bstack1ll1llll1ll_opy_.TEST:
                if not TestFramework.bstack111111ll1l_opy_(instance, TestFramework.bstack1l111l1111l_opy_) and test_hook_state == bstack1llll1l1lll_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l111ll1lll_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1llll1l_opy_ (u"ࠣ࡮ࡲࡥࡩ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᎱ") + str(test_hook_state) + bstack1llll1l_opy_ (u"ࠤࠥᎲ"))
                if test_hook_state == bstack1llll1l1lll_opy_.PRE and not TestFramework.bstack111111ll1l_opy_(instance, TestFramework.bstack1l1ll11llll_opy_):
                    TestFramework.bstack111111111l_opy_(instance, TestFramework.bstack1l1ll11llll_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11l1lll11_opy_(instance, args)
                    self.logger.debug(bstack1llll1l_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲ࡹࡴࡢࡴࡷࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᎳ") + str(test_hook_state) + bstack1llll1l_opy_ (u"ࠦࠧᎴ"))
                elif test_hook_state == bstack1llll1l1lll_opy_.POST and not TestFramework.bstack111111ll1l_opy_(instance, TestFramework.bstack1l1lll1111l_opy_):
                    TestFramework.bstack111111111l_opy_(instance, TestFramework.bstack1l1lll1111l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1llll1l_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡦࡰࡧࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᎵ") + str(test_hook_state) + bstack1llll1l_opy_ (u"ࠨࠢᎶ"))
            elif test_framework_state == bstack1ll1llll1ll_opy_.STEP:
                if test_hook_state == bstack1llll1l1lll_opy_.PRE:
                    PytestBDDFramework.__1l11l11lll1_opy_(instance, args)
                elif test_hook_state == bstack1llll1l1lll_opy_.POST:
                    PytestBDDFramework.__1l11l111ll1_opy_(instance, args)
            elif test_framework_state == bstack1ll1llll1ll_opy_.LOG and test_hook_state == bstack1llll1l1lll_opy_.POST:
                PytestBDDFramework.__1l11l1ll111_opy_(instance, *args)
            elif test_framework_state == bstack1ll1llll1ll_opy_.LOG_REPORT and test_hook_state == bstack1llll1l1lll_opy_.POST:
                self.__1l11l1l1ll1_opy_(instance, *args)
                self.__1l11ll1l111_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l1111ll111_opy_:
                self.__1l111ll11l1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᎷ") + str(instance.ref()) + bstack1llll1l_opy_ (u"ࠣࠤᎸ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11l1111l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l1111ll111_opy_ and test_hook_state == bstack1llll1l1lll_opy_.POST:
                name = str(EVENTS.bstack11l1lll11l_opy_.name)+bstack1llll1l_opy_ (u"ࠤ࠽ࠦᎹ")+str(test_framework_state.name)
                bstack1ll1l1l11ll_opy_ = TestFramework.bstack1l11l1l111l_opy_(instance, name)
                bstack1lllll11ll1_opy_.end(EVENTS.bstack11l1lll11l_opy_.value, bstack1ll1l1l11ll_opy_+bstack1llll1l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᎺ"), bstack1ll1l1l11ll_opy_+bstack1llll1l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᎻ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᎼ").format(e))
    def bstack1l1llllll11_opy_(self):
        return self.bstack1l11l1l1111_opy_
    def __1l111ll1111_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1llll1l_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᎽ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1lll1l11l_opy_(rep, [bstack1llll1l_opy_ (u"ࠢࡸࡪࡨࡲࠧᎾ"), bstack1llll1l_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᎿ"), bstack1llll1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᏀ"), bstack1llll1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᏁ"), bstack1llll1l_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠧᏂ"), bstack1llll1l_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᏃ")])
        return None
    def __1l11l1l1ll1_opy_(self, instance: bstack1llll111111_opy_, *args):
        result = self.__1l111ll1111_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111l11l11_opy_ = None
        if result.get(bstack1llll1l_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᏄ"), None) == bstack1llll1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᏅ") and len(args) > 1 and getattr(args[1], bstack1llll1l_opy_ (u"ࠣࡧࡻࡧ࡮ࡴࡦࡰࠤᏆ"), None) is not None:
            failure = [{bstack1llll1l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᏇ"): [args[1].excinfo.exconly(), result.get(bstack1llll1l_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᏈ"), None)]}]
            bstack1111l11l11_opy_ = bstack1llll1l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᏉ") if bstack1llll1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᏊ") in getattr(args[1].excinfo, bstack1llll1l_opy_ (u"ࠨࡴࡺࡲࡨࡲࡦࡳࡥࠣᏋ"), bstack1llll1l_opy_ (u"ࠢࠣᏌ")) else bstack1llll1l_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᏍ")
        bstack1l111l11l11_opy_ = result.get(bstack1llll1l_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᏎ"), TestFramework.bstack1l1111lll1l_opy_)
        if bstack1l111l11l11_opy_ != TestFramework.bstack1l1111lll1l_opy_:
            TestFramework.bstack111111111l_opy_(instance, TestFramework.bstack1l1lll11l1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11l11111l_opy_(instance, {
            TestFramework.bstack1l1l1l11111_opy_: failure,
            TestFramework.bstack1l111l111ll_opy_: bstack1111l11l11_opy_,
            TestFramework.bstack1l1l1l1ll1l_opy_: bstack1l111l11l11_opy_,
        })
    def __1l111lllll1_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1ll1llll1ll_opy_,
        test_hook_state: bstack1llll1l1lll_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll1llll1ll_opy_.SETUP_FIXTURE:
            instance = self.__1l111ll1ll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11l1lllll_opy_ bstack1l11ll111ll_opy_ this to be bstack1llll1l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᏏ")
            if test_framework_state == bstack1ll1llll1ll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11l1ll1l1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll1llll1ll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1llll1l_opy_ (u"ࠦࡳࡵࡤࡦࠤᏐ"), None), bstack1llll1l_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᏑ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1llll1l_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᏒ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1llll1l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᏓ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack111111l11l_opy_(target) if target else None
        return instance
    def __1l111ll11l1_opy_(
        self,
        instance: bstack1llll111111_opy_,
        test_framework_state: bstack1ll1llll1ll_opy_,
        test_hook_state: bstack1llll1l1lll_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11l11l111_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, PytestBDDFramework.bstack1l11l1lll1l_opy_, {})
        if not key in bstack1l11l11l111_opy_:
            bstack1l11l11l111_opy_[key] = []
        bstack1l11l11l1ll_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, PytestBDDFramework.bstack1l1111lllll_opy_, {})
        if not key in bstack1l11l11l1ll_opy_:
            bstack1l11l11l1ll_opy_[key] = []
        bstack1l111ll1l1l_opy_ = {
            PytestBDDFramework.bstack1l11l1lll1l_opy_: bstack1l11l11l111_opy_,
            PytestBDDFramework.bstack1l1111lllll_opy_: bstack1l11l11l1ll_opy_,
        }
        if test_hook_state == bstack1llll1l1lll_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1llll1l_opy_ (u"ࠣ࡭ࡨࡽࠧᏔ"): key,
                TestFramework.bstack1l11l1l1l11_opy_: uuid4().__str__(),
                TestFramework.bstack1l11ll11l11_opy_: TestFramework.bstack1l11l11ll1l_opy_,
                TestFramework.bstack1l111lll111_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l111l11lll_opy_: [],
                TestFramework.bstack1l111llll1l_opy_: hook_name,
                TestFramework.bstack1l11ll111l1_opy_: bstack1lll111llll_opy_.bstack1l11l111111_opy_()
            }
            bstack1l11l11l111_opy_[key].append(hook)
            bstack1l111ll1l1l_opy_[PytestBDDFramework.bstack1l1111llll1_opy_] = key
        elif test_hook_state == bstack1llll1l1lll_opy_.POST:
            bstack1l1111lll11_opy_ = bstack1l11l11l111_opy_.get(key, [])
            hook = bstack1l1111lll11_opy_.pop() if bstack1l1111lll11_opy_ else None
            if hook:
                result = self.__1l111ll1111_opy_(*args)
                if result:
                    bstack1l111l111l1_opy_ = result.get(bstack1llll1l_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᏕ"), TestFramework.bstack1l11l11ll1l_opy_)
                    if bstack1l111l111l1_opy_ != TestFramework.bstack1l11l11ll1l_opy_:
                        hook[TestFramework.bstack1l11ll11l11_opy_] = bstack1l111l111l1_opy_
                hook[TestFramework.bstack1l111l11111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11ll111l1_opy_] = bstack1lll111llll_opy_.bstack1l11l111111_opy_()
                self.bstack1l11l11llll_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111llllll_opy_, [])
                self.bstack1l1ll1lllll_opy_(instance, logs)
                bstack1l11l11l1ll_opy_[key].append(hook)
                bstack1l111ll1l1l_opy_[PytestBDDFramework.bstack1l11l1l1l1l_opy_] = key
        TestFramework.bstack1l11l11111l_opy_(instance, bstack1l111ll1l1l_opy_)
        self.logger.debug(bstack1llll1l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡫ࡳࡴࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾ࡯ࡪࡿࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࡂࢁࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࢃࠠࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤ࠾ࠤᏖ") + str(bstack1l11l11l1ll_opy_) + bstack1llll1l_opy_ (u"ࠦࠧᏗ"))
    def __1l111ll1ll1_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1ll1llll1ll_opy_,
        test_hook_state: bstack1llll1l1lll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1lll1l11l_opy_(args[0], [bstack1llll1l_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᏘ"), bstack1llll1l_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢᏙ"), bstack1llll1l_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢᏚ"), bstack1llll1l_opy_ (u"ࠣ࡫ࡧࡷࠧᏛ"), bstack1llll1l_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦᏜ"), bstack1llll1l_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᏝ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1llll1l_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᏞ")) else fixturedef.get(bstack1llll1l_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᏟ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1llll1l_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦᏠ")) else None
        node = request.node if hasattr(request, bstack1llll1l_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᏡ")) else None
        target = request.node.nodeid if hasattr(node, bstack1llll1l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᏢ")) else None
        baseid = fixturedef.get(bstack1llll1l_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᏣ"), None) or bstack1llll1l_opy_ (u"ࠥࠦᏤ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1llll1l_opy_ (u"ࠦࡤࡶࡹࡧࡷࡱࡧ࡮ࡺࡥ࡮ࠤᏥ")):
            target = PytestBDDFramework.__1l111l1l1l1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1llll1l_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᏦ")) else None
            if target and not TestFramework.bstack111111l11l_opy_(target):
                self.__1l11l1ll1l1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1llll1l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡰࡲࡨࡪࡃࡻ࡯ࡱࡧࡩࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᏧ") + str(test_hook_state) + bstack1llll1l_opy_ (u"ࠢࠣᏨ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1llll1l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࡃࡻࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᏩ") + str(target) + bstack1llll1l_opy_ (u"ࠤࠥᏪ"))
            return None
        instance = TestFramework.bstack111111l11l_opy_(target)
        if not instance:
            self.logger.warning(bstack1llll1l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡥࡥࡸ࡫ࡩࡥ࠿ࡾࡦࡦࡹࡥࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᏫ") + str(target) + bstack1llll1l_opy_ (u"ࠦࠧᏬ"))
            return None
        bstack1l11l1l11ll_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, PytestBDDFramework.bstack1l111lll1l1_opy_, {})
        if os.getenv(bstack1llll1l_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡋࡏࡘࡕࡗࡕࡉࡘࠨᏭ"), bstack1llll1l_opy_ (u"ࠨ࠱ࠣᏮ")) == bstack1llll1l_opy_ (u"ࠢ࠲ࠤᏯ"):
            bstack1l11l1ll1ll_opy_ = bstack1llll1l_opy_ (u"ࠣ࠼ࠥᏰ").join((scope, fixturename))
            bstack1l111llll11_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11ll11lll_opy_ = {
                bstack1llll1l_opy_ (u"ࠤ࡮ࡩࡾࠨᏱ"): bstack1l11l1ll1ll_opy_,
                bstack1llll1l_opy_ (u"ࠥࡸࡦ࡭ࡳࠣᏲ"): PytestBDDFramework.__1l1111ll1l1_opy_(request.node, scenario),
                bstack1llll1l_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࠧᏳ"): fixturedef,
                bstack1llll1l_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᏴ"): scope,
                bstack1llll1l_opy_ (u"ࠨࡴࡺࡲࡨࠦᏵ"): None,
            }
            try:
                if test_hook_state == bstack1llll1l1lll_opy_.POST and callable(getattr(args[-1], bstack1llll1l_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦ᏶"), None)):
                    bstack1l11ll11lll_opy_[bstack1llll1l_opy_ (u"ࠣࡶࡼࡴࡪࠨ᏷")] = TestFramework.bstack1l1ll1lll1l_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1llll1l1lll_opy_.PRE:
                bstack1l11ll11lll_opy_[bstack1llll1l_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᏸ")] = uuid4().__str__()
                bstack1l11ll11lll_opy_[PytestBDDFramework.bstack1l111lll111_opy_] = bstack1l111llll11_opy_
            elif test_hook_state == bstack1llll1l1lll_opy_.POST:
                bstack1l11ll11lll_opy_[PytestBDDFramework.bstack1l111l11111_opy_] = bstack1l111llll11_opy_
            if bstack1l11l1ll1ll_opy_ in bstack1l11l1l11ll_opy_:
                bstack1l11l1l11ll_opy_[bstack1l11l1ll1ll_opy_].update(bstack1l11ll11lll_opy_)
                self.logger.debug(bstack1llll1l_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࠦᏹ") + str(bstack1l11l1l11ll_opy_[bstack1l11l1ll1ll_opy_]) + bstack1llll1l_opy_ (u"ࠦࠧᏺ"))
            else:
                bstack1l11l1l11ll_opy_[bstack1l11l1ll1ll_opy_] = bstack1l11ll11lll_opy_
                self.logger.debug(bstack1llll1l_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࡿࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࢀࠤࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࠣᏻ") + str(len(bstack1l11l1l11ll_opy_)) + bstack1llll1l_opy_ (u"ࠨࠢᏼ"))
        TestFramework.bstack111111111l_opy_(instance, PytestBDDFramework.bstack1l111lll1l1_opy_, bstack1l11l1l11ll_opy_)
        self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࡽ࡯ࡩࡳ࠮ࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠫࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᏽ") + str(instance.ref()) + bstack1llll1l_opy_ (u"ࠣࠤ᏾"))
        return instance
    def __1l11l1ll1l1_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1ll1llll1ll_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1llllll1lll_opy_.create_context(target)
        ob = bstack1llll111111_opy_(ctx, self.bstack1ll11lll11l_opy_, self.bstack1l111l1l111_opy_, test_framework_state)
        TestFramework.bstack1l11l11111l_opy_(ob, {
            TestFramework.bstack1ll1ll1111l_opy_: context.test_framework_name,
            TestFramework.bstack1l1llll1l1l_opy_: context.test_framework_version,
            TestFramework.bstack1l11ll11l1l_opy_: [],
            PytestBDDFramework.bstack1l111lll1l1_opy_: {},
            PytestBDDFramework.bstack1l1111lllll_opy_: {},
            PytestBDDFramework.bstack1l11l1lll1l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack111111111l_opy_(ob, TestFramework.bstack1l11l111l1l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack111111111l_opy_(ob, TestFramework.bstack1ll11l1ll11_opy_, context.platform_index)
        TestFramework.bstack1llllllll1l_opy_[ctx.id] = ob
        self.logger.debug(bstack1llll1l_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡧࡹࡾ࠮ࡪࡦࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤ᏿") + str(TestFramework.bstack1llllllll1l_opy_.keys()) + bstack1llll1l_opy_ (u"ࠥࠦ᐀"))
        return ob
    @staticmethod
    def __1l11l1lll11_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1llll1l_opy_ (u"ࠫ࡮ࡪࠧᐁ"): id(step),
                bstack1llll1l_opy_ (u"ࠬࡺࡥࡹࡶࠪᐂ"): step.name,
                bstack1llll1l_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧᐃ"): step.keyword,
            })
        meta = {
            bstack1llll1l_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨᐄ"): {
                bstack1llll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᐅ"): feature.name,
                bstack1llll1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧᐆ"): feature.filename,
                bstack1llll1l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᐇ"): feature.description
            },
            bstack1llll1l_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ᐈ"): {
                bstack1llll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᐉ"): scenario.name
            },
            bstack1llll1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᐊ"): steps,
            bstack1llll1l_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩᐋ"): PytestBDDFramework.__1l11ll11ll1_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l111l1lll1_opy_: meta
            }
        )
    def bstack1l11l11llll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1llll1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡸ࡭ࡱࡪ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᐌ")
        global _1l1lllll1ll_opy_
        platform_index = os.environ[bstack1llll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᐍ")]
        bstack1l1lll1ll11_opy_ = os.path.join(bstack1l1llll1111_opy_, (bstack1l1lll111ll_opy_ + str(platform_index)), bstack1l11l1l1lll_opy_)
        if not os.path.exists(bstack1l1lll1ll11_opy_) or not os.path.isdir(bstack1l1lll1ll11_opy_):
            return
        logs = hook.get(bstack1llll1l_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᐎ"), [])
        with os.scandir(bstack1l1lll1ll11_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1lllll1ll_opy_:
                    self.logger.info(bstack1llll1l_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᐏ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1llll1l_opy_ (u"ࠧࠨᐐ")
                    log_entry = bstack1ll1lll1lll_opy_(
                        kind=bstack1llll1l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᐑ"),
                        message=bstack1llll1l_opy_ (u"ࠢࠣᐒ"),
                        level=bstack1llll1l_opy_ (u"ࠣࠤᐓ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1llll1l11_opy_=entry.stat().st_size,
                        bstack1l1llll1ll1_opy_=bstack1llll1l_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᐔ"),
                        bstack11ll11l_opy_=os.path.abspath(entry.path),
                        bstack1l1111ll11l_opy_=hook.get(TestFramework.bstack1l11l1l1l11_opy_)
                    )
                    logs.append(log_entry)
                    _1l1lllll1ll_opy_.add(abs_path)
        platform_index = os.environ[bstack1llll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᐕ")]
        bstack1l111lll11l_opy_ = os.path.join(bstack1l1llll1111_opy_, (bstack1l1lll111ll_opy_ + str(platform_index)), bstack1l11l1l1lll_opy_, bstack1l111l1ll11_opy_)
        if not os.path.exists(bstack1l111lll11l_opy_) or not os.path.isdir(bstack1l111lll11l_opy_):
            self.logger.info(bstack1llll1l_opy_ (u"ࠦࡓࡵࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࠦࡡࡵ࠼ࠣࡿࢂࠨᐖ").format(bstack1l111lll11l_opy_))
        else:
            self.logger.info(bstack1llll1l_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡦࡳࡱࡰࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦᐗ").format(bstack1l111lll11l_opy_))
            with os.scandir(bstack1l111lll11l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1lllll1ll_opy_:
                        self.logger.info(bstack1llll1l_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᐘ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1llll1l_opy_ (u"ࠢࠣᐙ")
                        log_entry = bstack1ll1lll1lll_opy_(
                            kind=bstack1llll1l_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᐚ"),
                            message=bstack1llll1l_opy_ (u"ࠤࠥᐛ"),
                            level=bstack1llll1l_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᐜ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1llll1l11_opy_=entry.stat().st_size,
                            bstack1l1llll1ll1_opy_=bstack1llll1l_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᐝ"),
                            bstack11ll11l_opy_=os.path.abspath(entry.path),
                            bstack1ll11111111_opy_=hook.get(TestFramework.bstack1l11l1l1l11_opy_)
                        )
                        logs.append(log_entry)
                        _1l1lllll1ll_opy_.add(abs_path)
        hook[bstack1llll1l_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᐞ")] = logs
    def bstack1l1ll1lllll_opy_(
        self,
        bstack1l1llll11ll_opy_: bstack1llll111111_opy_,
        entries: List[bstack1ll1lll1lll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1llll1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥᐟ"))
        req.platform_index = TestFramework.bstack1lllllllll1_opy_(bstack1l1llll11ll_opy_, TestFramework.bstack1ll11l1ll11_opy_)
        req.execution_context.hash = str(bstack1l1llll11ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1llll11ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1llll11ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lllllllll1_opy_(bstack1l1llll11ll_opy_, TestFramework.bstack1ll1ll1111l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lllllllll1_opy_(bstack1l1llll11ll_opy_, TestFramework.bstack1l1llll1l1l_opy_)
            log_entry.uuid = entry.bstack1l1111ll11l_opy_
            log_entry.test_framework_state = bstack1l1llll11ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1llll1l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᐠ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1llll1l_opy_ (u"ࠣࠤᐡ")
            if entry.kind == bstack1llll1l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᐢ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1llll1l11_opy_
                log_entry.file_path = entry.bstack11ll11l_opy_
        def bstack1l1ll1l11l1_opy_():
            bstack1l11l1lll_opy_ = datetime.now()
            try:
                self.bstack1llll111l1l_opy_.LogCreatedEvent(req)
                bstack1l1llll11ll_opy_.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᐣ"), datetime.now() - bstack1l11l1lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1llll1l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡼࡿࠥᐤ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l1111l_opy_.enqueue(bstack1l1ll1l11l1_opy_)
    def __1l11ll1l111_opy_(self, instance) -> None:
        bstack1llll1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡏࡳࡦࡪࡳࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧࠠࡥ࡫ࡦࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡡ࡯ࡦࠣࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡷࡹࡧࡴࡦࠢࡸࡷ࡮ࡴࡧࠡࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᐥ")
        bstack1l111ll1l1l_opy_ = {bstack1llll1l_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᐦ"): bstack1lll111llll_opy_.bstack1l11l111111_opy_()}
        TestFramework.bstack1l11l11111l_opy_(instance, bstack1l111ll1l1l_opy_)
    @staticmethod
    def __1l11l11lll1_opy_(instance, args):
        request, bstack1l111l11ll1_opy_ = args
        bstack1l11l11l1l1_opy_ = id(bstack1l111l11ll1_opy_)
        bstack1l111lll1ll_opy_ = instance.data[TestFramework.bstack1l111l1lll1_opy_]
        step = next(filter(lambda st: st[bstack1llll1l_opy_ (u"ࠧࡪࡦࠪᐧ")] == bstack1l11l11l1l1_opy_, bstack1l111lll1ll_opy_[bstack1llll1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐨ")]), None)
        step.update({
            bstack1llll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᐩ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l111lll1ll_opy_[bstack1llll1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᐪ")]) if st[bstack1llll1l_opy_ (u"ࠫ࡮ࡪࠧᐫ")] == step[bstack1llll1l_opy_ (u"ࠬ࡯ࡤࠨᐬ")]), None)
        if index is not None:
            bstack1l111lll1ll_opy_[bstack1llll1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᐭ")][index] = step
        instance.data[TestFramework.bstack1l111l1lll1_opy_] = bstack1l111lll1ll_opy_
    @staticmethod
    def __1l11l111ll1_opy_(instance, args):
        bstack1llll1l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡮ࡥ࡯ࠢ࡯ࡩࡳࠦࡡࡳࡩࡶࠤ࡮ࡹࠠ࠳࠮ࠣ࡭ࡹࠦࡳࡪࡩࡱ࡭࡫࡯ࡥࡴࠢࡷ࡬ࡪࡸࡥࠡ࡫ࡶࠤࡳࡵࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡣࡵ࡫ࡸࠦࡡࡳࡧࠣ࠱ࠥࡡࡲࡦࡳࡸࡩࡸࡺࠬࠡࡵࡷࡩࡵࡣࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡩࠤࡦࡸࡧࡴࠢࡤࡶࡪࠦ࠳ࠡࡶ࡫ࡩࡳࠦࡴࡩࡧࠣࡰࡦࡹࡴࠡࡸࡤࡰࡺ࡫ࠠࡪࡵࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᐮ")
        bstack1l11l1l11l1_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l111l11ll1_opy_ = args[1]
        bstack1l11l11l1l1_opy_ = id(bstack1l111l11ll1_opy_)
        bstack1l111lll1ll_opy_ = instance.data[TestFramework.bstack1l111l1lll1_opy_]
        step = None
        if bstack1l11l11l1l1_opy_ is not None and bstack1l111lll1ll_opy_.get(bstack1llll1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐯ")):
            step = next(filter(lambda st: st[bstack1llll1l_opy_ (u"ࠩ࡬ࡨࠬᐰ")] == bstack1l11l11l1l1_opy_, bstack1l111lll1ll_opy_[bstack1llll1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᐱ")]), None)
            step.update({
                bstack1llll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᐲ"): bstack1l11l1l11l1_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1llll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᐳ"): bstack1llll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᐴ"),
                bstack1llll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᐵ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1llll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᐶ"): bstack1llll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᐷ"),
                })
        index = next((i for i, st in enumerate(bstack1l111lll1ll_opy_[bstack1llll1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᐸ")]) if st[bstack1llll1l_opy_ (u"ࠫ࡮ࡪࠧᐹ")] == step[bstack1llll1l_opy_ (u"ࠬ࡯ࡤࠨᐺ")]), None)
        if index is not None:
            bstack1l111lll1ll_opy_[bstack1llll1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᐻ")][index] = step
        instance.data[TestFramework.bstack1l111l1lll1_opy_] = bstack1l111lll1ll_opy_
    @staticmethod
    def __1l11ll11ll1_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1llll1l_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᐼ")):
                examples = list(node.callspec.params[bstack1llll1l_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧᐽ")].values())
            return examples
        except:
            return []
    def bstack1l1lll1llll_opy_(self, instance: bstack1llll111111_opy_, bstack11111l1lll_opy_: Tuple[bstack1ll1llll1ll_opy_, bstack1llll1l1lll_opy_]):
        bstack1l11l11ll11_opy_ = (
            PytestBDDFramework.bstack1l1111llll1_opy_
            if bstack11111l1lll_opy_[1] == bstack1llll1l1lll_opy_.PRE
            else PytestBDDFramework.bstack1l11l1l1l1l_opy_
        )
        hook = PytestBDDFramework.bstack1l111l1l11l_opy_(instance, bstack1l11l11ll11_opy_)
        entries = hook.get(TestFramework.bstack1l111l11lll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_, []))
        return entries
    def bstack1ll1111l111_opy_(self, instance: bstack1llll111111_opy_, bstack11111l1lll_opy_: Tuple[bstack1ll1llll1ll_opy_, bstack1llll1l1lll_opy_]):
        bstack1l11l11ll11_opy_ = (
            PytestBDDFramework.bstack1l1111llll1_opy_
            if bstack11111l1lll_opy_[1] == bstack1llll1l1lll_opy_.PRE
            else PytestBDDFramework.bstack1l11l1l1l1l_opy_
        )
        PytestBDDFramework.bstack1l11l1llll1_opy_(instance, bstack1l11l11ll11_opy_)
        TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_, []).clear()
    @staticmethod
    def bstack1l111l1l11l_opy_(instance: bstack1llll111111_opy_, bstack1l11l11ll11_opy_: str):
        bstack1l111ll111l_opy_ = (
            PytestBDDFramework.bstack1l1111lllll_opy_
            if bstack1l11l11ll11_opy_ == PytestBDDFramework.bstack1l11l1l1l1l_opy_
            else PytestBDDFramework.bstack1l11l1lll1l_opy_
        )
        bstack1l11l111l11_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, bstack1l11l11ll11_opy_, None)
        bstack1l11ll1l11l_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, bstack1l111ll111l_opy_, None) if bstack1l11l111l11_opy_ else None
        return (
            bstack1l11ll1l11l_opy_[bstack1l11l111l11_opy_][-1]
            if isinstance(bstack1l11ll1l11l_opy_, dict) and len(bstack1l11ll1l11l_opy_.get(bstack1l11l111l11_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l11l1llll1_opy_(instance: bstack1llll111111_opy_, bstack1l11l11ll11_opy_: str):
        hook = PytestBDDFramework.bstack1l111l1l11l_opy_(instance, bstack1l11l11ll11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l111l11lll_opy_, []).clear()
    @staticmethod
    def __1l11l1ll111_opy_(instance: bstack1llll111111_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1llll1l_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡥࡲࡶࡩࡹࠢᐾ"), None)):
            return
        if os.getenv(bstack1llll1l_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡏࡓࡌ࡙ࠢᐿ"), bstack1llll1l_opy_ (u"ࠦ࠶ࠨᑀ")) != bstack1llll1l_opy_ (u"ࠧ࠷ࠢᑁ"):
            PytestBDDFramework.logger.warning(bstack1llll1l_opy_ (u"ࠨࡩࡨࡰࡲࡶ࡮ࡴࡧࠡࡥࡤࡴࡱࡵࡧࠣᑂ"))
            return
        bstack1l11l11l11l_opy_ = {
            bstack1llll1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᑃ"): (PytestBDDFramework.bstack1l1111llll1_opy_, PytestBDDFramework.bstack1l11l1lll1l_opy_),
            bstack1llll1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᑄ"): (PytestBDDFramework.bstack1l11l1l1l1l_opy_, PytestBDDFramework.bstack1l1111lllll_opy_),
        }
        for when in (bstack1llll1l_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᑅ"), bstack1llll1l_opy_ (u"ࠥࡧࡦࡲ࡬ࠣᑆ"), bstack1llll1l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᑇ")):
            bstack1l111l1l1ll_opy_ = args[1].get_records(when)
            if not bstack1l111l1l1ll_opy_:
                continue
            records = [
                bstack1ll1lll1lll_opy_(
                    kind=TestFramework.bstack1l1lll1l1ll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1llll1l_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠣᑈ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1llll1l_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪࠢᑉ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111l1l1ll_opy_
                if isinstance(getattr(r, bstack1llll1l_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᑊ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l111ll1l11_opy_, bstack1l111ll111l_opy_ = bstack1l11l11l11l_opy_.get(when, (None, None))
            bstack1l11ll1111l_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, bstack1l111ll1l11_opy_, None) if bstack1l111ll1l11_opy_ else None
            bstack1l11ll1l11l_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, bstack1l111ll111l_opy_, None) if bstack1l11ll1111l_opy_ else None
            if isinstance(bstack1l11ll1l11l_opy_, dict) and len(bstack1l11ll1l11l_opy_.get(bstack1l11ll1111l_opy_, [])) > 0:
                hook = bstack1l11ll1l11l_opy_[bstack1l11ll1111l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l111l11lll_opy_ in hook:
                    hook[TestFramework.bstack1l111l11lll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l111ll1lll_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1l111llll1_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l11l1111ll_opy_(request.node, scenario)
        bstack1l11l111lll_opy_ = feature.filename
        if not bstack1l111llll1_opy_ or not test_name or not bstack1l11l111lll_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll11lll1ll_opy_: uuid4().__str__(),
            TestFramework.bstack1l111l1111l_opy_: bstack1l111llll1_opy_,
            TestFramework.bstack1ll1l11lll1_opy_: test_name,
            TestFramework.bstack1l1ll11lll1_opy_: bstack1l111llll1_opy_,
            TestFramework.bstack1l111l1llll_opy_: bstack1l11l111lll_opy_,
            TestFramework.bstack1l1111ll1ll_opy_: PytestBDDFramework.__1l1111ll1l1_opy_(feature, scenario),
            TestFramework.bstack1l11l1ll11l_opy_: code,
            TestFramework.bstack1l1l1l1ll1l_opy_: TestFramework.bstack1l1111lll1l_opy_,
            TestFramework.bstack1l11lll1lll_opy_: test_name
        }
    @staticmethod
    def __1l11l1111ll_opy_(node, scenario):
        if hasattr(node, bstack1llll1l_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᑋ")):
            parts = node.nodeid.rsplit(bstack1llll1l_opy_ (u"ࠤ࡞ࠦᑌ"))
            params = parts[-1]
            return bstack1llll1l_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥᑍ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l1111ll1l1_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1llll1l_opy_ (u"ࠫࡹࡧࡧࡴࠩᑎ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1llll1l_opy_ (u"ࠬࡺࡡࡨࡵࠪᑏ")) else [])
    @staticmethod
    def __1l111l1l1l1_opy_(location):
        return bstack1llll1l_opy_ (u"ࠨ࠺࠻ࠤᑐ").join(filter(lambda x: isinstance(x, str), location))