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
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll1llll1ll_opy_,
    bstack1llll111111_opy_,
    bstack1llll1l1lll_opy_,
    bstack1l111l11l1l_opy_,
    bstack1ll1lll1lll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1lll1l111_opy_
from bstack_utils.bstack1l1lll111l_opy_ import bstack1lllll11ll1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1111l1111l_opy_ import bstack11111llll1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lllll11l1l_opy_ import bstack1lll111llll_opy_
from bstack_utils.bstack11l11111l1_opy_ import bstack1l11l111ll_opy_
bstack1l1llll1111_opy_ = bstack1l1lll1l111_opy_()
bstack1l11ll11111_opy_ = 1.0
bstack1l1lll111ll_opy_ = bstack1llll1l_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᑑ")
bstack1l1111l1l1l_opy_ = bstack1llll1l_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᑒ")
bstack1l1111l11ll_opy_ = bstack1llll1l_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᑓ")
bstack1l1111l11l1_opy_ = bstack1llll1l_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨᑔ")
bstack1l1111l1ll1_opy_ = bstack1llll1l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥᑕ")
_1l1lllll1ll_opy_ = set()
class bstack1llll1l1111_opy_(TestFramework):
    bstack1l111lll1l1_opy_ = bstack1llll1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᑖ")
    bstack1l11l1lll1l_opy_ = bstack1llll1l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࠦᑗ")
    bstack1l1111lllll_opy_ = bstack1llll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᑘ")
    bstack1l1111llll1_opy_ = bstack1llll1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࠥᑙ")
    bstack1l11l1l1l1l_opy_ = bstack1llll1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᑚ")
    bstack1l11l1l1111_opy_: bool
    bstack1111l1111l_opy_: bstack11111llll1_opy_  = None
    bstack1llll111l1l_opy_ = None
    bstack1l1111ll111_opy_ = [
        bstack1ll1llll1ll_opy_.BEFORE_ALL,
        bstack1ll1llll1ll_opy_.AFTER_ALL,
        bstack1ll1llll1ll_opy_.BEFORE_EACH,
        bstack1ll1llll1ll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111l1l111_opy_: Dict[str, str],
        bstack1ll11lll11l_opy_: List[str]=[bstack1llll1l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᑛ")],
        bstack1111l1111l_opy_: bstack11111llll1_opy_=None,
        bstack1llll111l1l_opy_=None
    ):
        super().__init__(bstack1ll11lll11l_opy_, bstack1l111l1l111_opy_, bstack1111l1111l_opy_)
        self.bstack1l11l1l1111_opy_ = any(bstack1llll1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᑜ") in item.lower() for item in bstack1ll11lll11l_opy_)
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
        if test_framework_state == bstack1ll1llll1ll_opy_.TEST or test_framework_state in bstack1llll1l1111_opy_.bstack1l1111ll111_opy_:
            bstack1l111ll11ll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll1llll1ll_opy_.NONE:
            self.logger.warning(bstack1llll1l_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࠨᑝ") + str(test_hook_state) + bstack1llll1l_opy_ (u"ࠨࠢᑞ"))
            return
        if not self.bstack1l11l1l1111_opy_:
            self.logger.warning(bstack1llll1l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠽ࠣᑟ") + str(str(self.bstack1ll11lll11l_opy_)) + bstack1llll1l_opy_ (u"ࠣࠤᑠ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1llll1l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᑡ") + str(kwargs) + bstack1llll1l_opy_ (u"ࠥࠦᑢ"))
            return
        instance = self.__1l111lllll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡦࡸࡧࡴ࠿ࠥᑣ") + str(args) + bstack1llll1l_opy_ (u"ࠧࠨᑤ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1llll1l1111_opy_.bstack1l1111ll111_opy_ and test_hook_state == bstack1llll1l1lll_opy_.PRE:
                bstack1ll1l1l11ll_opy_ = bstack1lllll11ll1_opy_.bstack1ll1ll11l11_opy_(EVENTS.bstack11l1lll11l_opy_.value)
                name = str(EVENTS.bstack11l1lll11l_opy_.name)+bstack1llll1l_opy_ (u"ࠨ࠺ࠣᑥ")+str(test_framework_state.name)
                TestFramework.bstack1l111l1ll1l_opy_(instance, name, bstack1ll1l1l11ll_opy_)
        except Exception as e:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴࠣࡴࡷ࡫࠺ࠡࡽࢀࠦᑦ").format(e))
        try:
            if not TestFramework.bstack111111ll1l_opy_(instance, TestFramework.bstack1l111l1111l_opy_) and test_hook_state == bstack1llll1l1lll_opy_.PRE:
                test = bstack1llll1l1111_opy_.__1l111ll1lll_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1llll1l_opy_ (u"ࠣ࡮ࡲࡥࡩ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᑧ") + str(test_hook_state) + bstack1llll1l_opy_ (u"ࠤࠥᑨ"))
            if test_framework_state == bstack1ll1llll1ll_opy_.TEST:
                if test_hook_state == bstack1llll1l1lll_opy_.PRE and not TestFramework.bstack111111ll1l_opy_(instance, TestFramework.bstack1l1ll11llll_opy_):
                    TestFramework.bstack111111111l_opy_(instance, TestFramework.bstack1l1ll11llll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1llll1l_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲ࡹࡴࡢࡴࡷࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᑩ") + str(test_hook_state) + bstack1llll1l_opy_ (u"ࠦࠧᑪ"))
                elif test_hook_state == bstack1llll1l1lll_opy_.POST and not TestFramework.bstack111111ll1l_opy_(instance, TestFramework.bstack1l1lll1111l_opy_):
                    TestFramework.bstack111111111l_opy_(instance, TestFramework.bstack1l1lll1111l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1llll1l_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡦࡰࡧࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᑫ") + str(test_hook_state) + bstack1llll1l_opy_ (u"ࠨࠢᑬ"))
            elif test_framework_state == bstack1ll1llll1ll_opy_.LOG and test_hook_state == bstack1llll1l1lll_opy_.POST:
                bstack1llll1l1111_opy_.__1l11l1ll111_opy_(instance, *args)
            elif test_framework_state == bstack1ll1llll1ll_opy_.LOG_REPORT and test_hook_state == bstack1llll1l1lll_opy_.POST:
                self.__1l11l1l1ll1_opy_(instance, *args)
                self.__1l11ll1l111_opy_(instance)
            elif test_framework_state in bstack1llll1l1111_opy_.bstack1l1111ll111_opy_:
                self.__1l111ll11l1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᑭ") + str(instance.ref()) + bstack1llll1l_opy_ (u"ࠣࠤᑮ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11l1111l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1llll1l1111_opy_.bstack1l1111ll111_opy_ and test_hook_state == bstack1llll1l1lll_opy_.POST:
                name = str(EVENTS.bstack11l1lll11l_opy_.name)+bstack1llll1l_opy_ (u"ࠤ࠽ࠦᑯ")+str(test_framework_state.name)
                bstack1ll1l1l11ll_opy_ = TestFramework.bstack1l11l1l111l_opy_(instance, name)
                bstack1lllll11ll1_opy_.end(EVENTS.bstack11l1lll11l_opy_.value, bstack1ll1l1l11ll_opy_+bstack1llll1l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᑰ"), bstack1ll1l1l11ll_opy_+bstack1llll1l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᑱ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᑲ").format(e))
    def bstack1l1llllll11_opy_(self):
        return self.bstack1l11l1l1111_opy_
    def __1l111ll1111_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1llll1l_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᑳ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1lll1l11l_opy_(rep, [bstack1llll1l_opy_ (u"ࠢࡸࡪࡨࡲࠧᑴ"), bstack1llll1l_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᑵ"), bstack1llll1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᑶ"), bstack1llll1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᑷ"), bstack1llll1l_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠧᑸ"), bstack1llll1l_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᑹ")])
        return None
    def __1l11l1l1ll1_opy_(self, instance: bstack1llll111111_opy_, *args):
        result = self.__1l111ll1111_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111l11l11_opy_ = None
        if result.get(bstack1llll1l_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᑺ"), None) == bstack1llll1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᑻ") and len(args) > 1 and getattr(args[1], bstack1llll1l_opy_ (u"ࠣࡧࡻࡧ࡮ࡴࡦࡰࠤᑼ"), None) is not None:
            failure = [{bstack1llll1l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᑽ"): [args[1].excinfo.exconly(), result.get(bstack1llll1l_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᑾ"), None)]}]
            bstack1111l11l11_opy_ = bstack1llll1l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᑿ") if bstack1llll1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᒀ") in getattr(args[1].excinfo, bstack1llll1l_opy_ (u"ࠨࡴࡺࡲࡨࡲࡦࡳࡥࠣᒁ"), bstack1llll1l_opy_ (u"ࠢࠣᒂ")) else bstack1llll1l_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᒃ")
        bstack1l111l11l11_opy_ = result.get(bstack1llll1l_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᒄ"), TestFramework.bstack1l1111lll1l_opy_)
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
            target = None # bstack1l11l1lllll_opy_ bstack1l11ll111ll_opy_ this to be bstack1llll1l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᒅ")
            if test_framework_state == bstack1ll1llll1ll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11l1ll1l1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll1llll1ll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1llll1l_opy_ (u"ࠦࡳࡵࡤࡦࠤᒆ"), None), bstack1llll1l_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᒇ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1llll1l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᒈ"), None):
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
        bstack1l11l11l111_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, bstack1llll1l1111_opy_.bstack1l11l1lll1l_opy_, {})
        if not key in bstack1l11l11l111_opy_:
            bstack1l11l11l111_opy_[key] = []
        bstack1l11l11l1ll_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, bstack1llll1l1111_opy_.bstack1l1111lllll_opy_, {})
        if not key in bstack1l11l11l1ll_opy_:
            bstack1l11l11l1ll_opy_[key] = []
        bstack1l111ll1l1l_opy_ = {
            bstack1llll1l1111_opy_.bstack1l11l1lll1l_opy_: bstack1l11l11l111_opy_,
            bstack1llll1l1111_opy_.bstack1l1111lllll_opy_: bstack1l11l11l1ll_opy_,
        }
        if test_hook_state == bstack1llll1l1lll_opy_.PRE:
            hook = {
                bstack1llll1l_opy_ (u"ࠢ࡬ࡧࡼࠦᒉ"): key,
                TestFramework.bstack1l11l1l1l11_opy_: uuid4().__str__(),
                TestFramework.bstack1l11ll11l11_opy_: TestFramework.bstack1l11l11ll1l_opy_,
                TestFramework.bstack1l111lll111_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l111l11lll_opy_: [],
                TestFramework.bstack1l111llll1l_opy_: args[1] if len(args) > 1 else bstack1llll1l_opy_ (u"ࠨࠩᒊ"),
                TestFramework.bstack1l11ll111l1_opy_: bstack1lll111llll_opy_.bstack1l11l111111_opy_()
            }
            bstack1l11l11l111_opy_[key].append(hook)
            bstack1l111ll1l1l_opy_[bstack1llll1l1111_opy_.bstack1l1111llll1_opy_] = key
        elif test_hook_state == bstack1llll1l1lll_opy_.POST:
            bstack1l1111lll11_opy_ = bstack1l11l11l111_opy_.get(key, [])
            hook = bstack1l1111lll11_opy_.pop() if bstack1l1111lll11_opy_ else None
            if hook:
                result = self.__1l111ll1111_opy_(*args)
                if result:
                    bstack1l111l111l1_opy_ = result.get(bstack1llll1l_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᒋ"), TestFramework.bstack1l11l11ll1l_opy_)
                    if bstack1l111l111l1_opy_ != TestFramework.bstack1l11l11ll1l_opy_:
                        hook[TestFramework.bstack1l11ll11l11_opy_] = bstack1l111l111l1_opy_
                hook[TestFramework.bstack1l111l11111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11ll111l1_opy_]= bstack1lll111llll_opy_.bstack1l11l111111_opy_()
                self.bstack1l11l11llll_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111llllll_opy_, [])
                if logs: self.bstack1l1ll1lllll_opy_(instance, logs)
                bstack1l11l11l1ll_opy_[key].append(hook)
                bstack1l111ll1l1l_opy_[bstack1llll1l1111_opy_.bstack1l11l1l1l1l_opy_] = key
        TestFramework.bstack1l11l11111l_opy_(instance, bstack1l111ll1l1l_opy_)
        self.logger.debug(bstack1llll1l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡫ࡳࡴࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾ࡯ࡪࡿࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࡂࢁࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࢃࠠࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤ࠾ࠤᒌ") + str(bstack1l11l11l1ll_opy_) + bstack1llll1l_opy_ (u"ࠦࠧᒍ"))
    def __1l111ll1ll1_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1ll1llll1ll_opy_,
        test_hook_state: bstack1llll1l1lll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1lll1l11l_opy_(args[0], [bstack1llll1l_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᒎ"), bstack1llll1l_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢᒏ"), bstack1llll1l_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢᒐ"), bstack1llll1l_opy_ (u"ࠣ࡫ࡧࡷࠧᒑ"), bstack1llll1l_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦᒒ"), bstack1llll1l_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᒓ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1llll1l_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᒔ")) else fixturedef.get(bstack1llll1l_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᒕ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1llll1l_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦᒖ")) else None
        node = request.node if hasattr(request, bstack1llll1l_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᒗ")) else None
        target = request.node.nodeid if hasattr(node, bstack1llll1l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᒘ")) else None
        baseid = fixturedef.get(bstack1llll1l_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᒙ"), None) or bstack1llll1l_opy_ (u"ࠥࠦᒚ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1llll1l_opy_ (u"ࠦࡤࡶࡹࡧࡷࡱࡧ࡮ࡺࡥ࡮ࠤᒛ")):
            target = bstack1llll1l1111_opy_.__1l111l1l1l1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1llll1l_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᒜ")) else None
            if target and not TestFramework.bstack111111l11l_opy_(target):
                self.__1l11l1ll1l1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1llll1l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡰࡲࡨࡪࡃࡻ࡯ࡱࡧࡩࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᒝ") + str(test_hook_state) + bstack1llll1l_opy_ (u"ࠢࠣᒞ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1llll1l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࡃࡻࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᒟ") + str(target) + bstack1llll1l_opy_ (u"ࠤࠥᒠ"))
            return None
        instance = TestFramework.bstack111111l11l_opy_(target)
        if not instance:
            self.logger.warning(bstack1llll1l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡥࡥࡸ࡫ࡩࡥ࠿ࡾࡦࡦࡹࡥࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᒡ") + str(target) + bstack1llll1l_opy_ (u"ࠦࠧᒢ"))
            return None
        bstack1l11l1l11ll_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, bstack1llll1l1111_opy_.bstack1l111lll1l1_opy_, {})
        if os.getenv(bstack1llll1l_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡋࡏࡘࡕࡗࡕࡉࡘࠨᒣ"), bstack1llll1l_opy_ (u"ࠨ࠱ࠣᒤ")) == bstack1llll1l_opy_ (u"ࠢ࠲ࠤᒥ"):
            bstack1l11l1ll1ll_opy_ = bstack1llll1l_opy_ (u"ࠣ࠼ࠥᒦ").join((scope, fixturename))
            bstack1l111llll11_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11ll11lll_opy_ = {
                bstack1llll1l_opy_ (u"ࠤ࡮ࡩࡾࠨᒧ"): bstack1l11l1ll1ll_opy_,
                bstack1llll1l_opy_ (u"ࠥࡸࡦ࡭ࡳࠣᒨ"): bstack1llll1l1111_opy_.__1l1111ll1l1_opy_(request.node),
                bstack1llll1l_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࠧᒩ"): fixturedef,
                bstack1llll1l_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᒪ"): scope,
                bstack1llll1l_opy_ (u"ࠨࡴࡺࡲࡨࠦᒫ"): None,
            }
            try:
                if test_hook_state == bstack1llll1l1lll_opy_.POST and callable(getattr(args[-1], bstack1llll1l_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᒬ"), None)):
                    bstack1l11ll11lll_opy_[bstack1llll1l_opy_ (u"ࠣࡶࡼࡴࡪࠨᒭ")] = TestFramework.bstack1l1ll1lll1l_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1llll1l1lll_opy_.PRE:
                bstack1l11ll11lll_opy_[bstack1llll1l_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᒮ")] = uuid4().__str__()
                bstack1l11ll11lll_opy_[bstack1llll1l1111_opy_.bstack1l111lll111_opy_] = bstack1l111llll11_opy_
            elif test_hook_state == bstack1llll1l1lll_opy_.POST:
                bstack1l11ll11lll_opy_[bstack1llll1l1111_opy_.bstack1l111l11111_opy_] = bstack1l111llll11_opy_
            if bstack1l11l1ll1ll_opy_ in bstack1l11l1l11ll_opy_:
                bstack1l11l1l11ll_opy_[bstack1l11l1ll1ll_opy_].update(bstack1l11ll11lll_opy_)
                self.logger.debug(bstack1llll1l_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࠦᒯ") + str(bstack1l11l1l11ll_opy_[bstack1l11l1ll1ll_opy_]) + bstack1llll1l_opy_ (u"ࠦࠧᒰ"))
            else:
                bstack1l11l1l11ll_opy_[bstack1l11l1ll1ll_opy_] = bstack1l11ll11lll_opy_
                self.logger.debug(bstack1llll1l_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࡿࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࢀࠤࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࠣᒱ") + str(len(bstack1l11l1l11ll_opy_)) + bstack1llll1l_opy_ (u"ࠨࠢᒲ"))
        TestFramework.bstack111111111l_opy_(instance, bstack1llll1l1111_opy_.bstack1l111lll1l1_opy_, bstack1l11l1l11ll_opy_)
        self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࡽ࡯ࡩࡳ࠮ࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠫࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᒳ") + str(instance.ref()) + bstack1llll1l_opy_ (u"ࠣࠤᒴ"))
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
            bstack1llll1l1111_opy_.bstack1l111lll1l1_opy_: {},
            bstack1llll1l1111_opy_.bstack1l1111lllll_opy_: {},
            bstack1llll1l1111_opy_.bstack1l11l1lll1l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack111111111l_opy_(ob, TestFramework.bstack1l11l111l1l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack111111111l_opy_(ob, TestFramework.bstack1ll11l1ll11_opy_, context.platform_index)
        TestFramework.bstack1llllllll1l_opy_[ctx.id] = ob
        self.logger.debug(bstack1llll1l_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡧࡹࡾ࠮ࡪࡦࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤᒵ") + str(TestFramework.bstack1llllllll1l_opy_.keys()) + bstack1llll1l_opy_ (u"ࠥࠦᒶ"))
        return ob
    def bstack1l1lll1llll_opy_(self, instance: bstack1llll111111_opy_, bstack11111l1lll_opy_: Tuple[bstack1ll1llll1ll_opy_, bstack1llll1l1lll_opy_]):
        bstack1l11l11ll11_opy_ = (
            bstack1llll1l1111_opy_.bstack1l1111llll1_opy_
            if bstack11111l1lll_opy_[1] == bstack1llll1l1lll_opy_.PRE
            else bstack1llll1l1111_opy_.bstack1l11l1l1l1l_opy_
        )
        hook = bstack1llll1l1111_opy_.bstack1l111l1l11l_opy_(instance, bstack1l11l11ll11_opy_)
        entries = hook.get(TestFramework.bstack1l111l11lll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_, []))
        return entries
    def bstack1ll1111l111_opy_(self, instance: bstack1llll111111_opy_, bstack11111l1lll_opy_: Tuple[bstack1ll1llll1ll_opy_, bstack1llll1l1lll_opy_]):
        bstack1l11l11ll11_opy_ = (
            bstack1llll1l1111_opy_.bstack1l1111llll1_opy_
            if bstack11111l1lll_opy_[1] == bstack1llll1l1lll_opy_.PRE
            else bstack1llll1l1111_opy_.bstack1l11l1l1l1l_opy_
        )
        bstack1llll1l1111_opy_.bstack1l11l1llll1_opy_(instance, bstack1l11l11ll11_opy_)
        TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_, []).clear()
    def bstack1l11l11llll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1llll1l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡸࡴࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡅ࡫ࡩࡨࡱࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡮ࡴࡳࡪࡦࡨࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡋࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠯ࠤࡷ࡫ࡰ࡭ࡣࡦࡩࡸࠦࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨࠠࡪࡰࠣ࡭ࡹࡹࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡎ࡬ࠠࡢࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸ࡭࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡱࡦࡺࡣࡩࡧࡶࠤࡦࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࠡࡪࡲࡳࡰ࠳࡬ࡦࡸࡨࡰࠥ࡬ࡩ࡭ࡧ࠯ࠤ࡮ࡺࠠࡤࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࠥࡽࡩࡵࡪࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡥࡧࡷࡥ࡮ࡲࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡔ࡫ࡰ࡭ࡱࡧࡲ࡭ࡻ࠯ࠤ࡮ࡺࠠࡱࡴࡲࡧࡪࡹࡳࡦࡵࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡲ࡯ࡤࡣࡷࡩࡩࠦࡩ࡯ࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡧࡿࠠࡳࡧࡳࡰࡦࡩࡩ࡯ࡩࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡘ࡭࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࡶࠤࡦࡸࡥࠡࡣࡧࡨࡪࡪࠠࡵࡱࠣࡸ࡭࡫ࠠࡩࡱࡲ࡯ࠬࡹࠠࠣ࡮ࡲ࡫ࡸࠨࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬࠼ࠣࡘ࡭࡫ࠠࡦࡸࡨࡲࡹࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹࠠࡢࡰࡧࠤ࡭ࡵ࡯࡬ࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩ࡚ࠥࡥࡴࡶࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡻࡩ࡭ࡦࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᒷ")
        global _1l1lllll1ll_opy_
        platform_index = os.environ[bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᒸ")]
        bstack1l1lll1ll11_opy_ = os.path.join(bstack1l1llll1111_opy_, (bstack1l1lll111ll_opy_ + str(platform_index)), bstack1l1111l11l1_opy_)
        if not os.path.exists(bstack1l1lll1ll11_opy_) or not os.path.isdir(bstack1l1lll1ll11_opy_):
            self.logger.debug(bstack1llll1l_opy_ (u"ࠨࡄࡪࡴࡨࡧࡹࡵࡲࡺࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶࡶࠤࡹࡵࠠࡱࡴࡲࡧࡪࡹࡳࠡࡽࢀࠦᒹ").format(bstack1l1lll1ll11_opy_))
            return
        logs = hook.get(bstack1llll1l_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᒺ"), [])
        with os.scandir(bstack1l1lll1ll11_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1lllll1ll_opy_:
                    self.logger.info(bstack1llll1l_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᒻ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1llll1l_opy_ (u"ࠤࠥᒼ")
                    log_entry = bstack1ll1lll1lll_opy_(
                        kind=bstack1llll1l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᒽ"),
                        message=bstack1llll1l_opy_ (u"ࠦࠧᒾ"),
                        level=bstack1llll1l_opy_ (u"ࠧࠨᒿ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1llll1l11_opy_=entry.stat().st_size,
                        bstack1l1llll1ll1_opy_=bstack1llll1l_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᓀ"),
                        bstack11ll11l_opy_=os.path.abspath(entry.path),
                        bstack1l1111ll11l_opy_=hook.get(TestFramework.bstack1l11l1l1l11_opy_)
                    )
                    logs.append(log_entry)
                    _1l1lllll1ll_opy_.add(abs_path)
        platform_index = os.environ[bstack1llll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᓁ")]
        bstack1l111lll11l_opy_ = os.path.join(bstack1l1llll1111_opy_, (bstack1l1lll111ll_opy_ + str(platform_index)), bstack1l1111l11l1_opy_, bstack1l1111l1ll1_opy_)
        if not os.path.exists(bstack1l111lll11l_opy_) or not os.path.isdir(bstack1l111lll11l_opy_):
            self.logger.info(bstack1llll1l_opy_ (u"ࠣࡐࡲࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣࡥࡹࡀࠠࡼࡿࠥᓂ").format(bstack1l111lll11l_opy_))
        else:
            self.logger.info(bstack1llll1l_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡪࡷࡵ࡭ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᓃ").format(bstack1l111lll11l_opy_))
            with os.scandir(bstack1l111lll11l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1lllll1ll_opy_:
                        self.logger.info(bstack1llll1l_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᓄ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1llll1l_opy_ (u"ࠦࠧᓅ")
                        log_entry = bstack1ll1lll1lll_opy_(
                            kind=bstack1llll1l_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᓆ"),
                            message=bstack1llll1l_opy_ (u"ࠨࠢᓇ"),
                            level=bstack1llll1l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᓈ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1llll1l11_opy_=entry.stat().st_size,
                            bstack1l1llll1ll1_opy_=bstack1llll1l_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᓉ"),
                            bstack11ll11l_opy_=os.path.abspath(entry.path),
                            bstack1ll11111111_opy_=hook.get(TestFramework.bstack1l11l1l1l11_opy_)
                        )
                        logs.append(log_entry)
                        _1l1lllll1ll_opy_.add(abs_path)
        hook[bstack1llll1l_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᓊ")] = logs
    def bstack1l1ll1lllll_opy_(
        self,
        bstack1l1llll11ll_opy_: bstack1llll111111_opy_,
        entries: List[bstack1ll1lll1lll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1llll1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢᓋ"))
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
            log_entry.message = entry.message.encode(bstack1llll1l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᓌ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1llll1l_opy_ (u"ࠧࠨᓍ")
            if entry.kind == bstack1llll1l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᓎ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1llll1l11_opy_
                log_entry.file_path = entry.bstack11ll11l_opy_
        def bstack1l1ll1l11l1_opy_():
            bstack1l11l1lll_opy_ = datetime.now()
            try:
                self.bstack1llll111l1l_opy_.LogCreatedEvent(req)
                bstack1l1llll11ll_opy_.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦᓏ"), datetime.now() - bstack1l11l1lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1llll1l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࢀࢃࠢᓐ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l1111l_opy_.enqueue(bstack1l1ll1l11l1_opy_)
    def __1l11ll1l111_opy_(self, instance) -> None:
        bstack1llll1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡌࡰࡣࡧࡷࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࠤࡩ࡯ࡣࡵࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡨࡵࡳࡲࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡥࡳࡪࠠࡶࡲࡧࡥࡹ࡫ࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡴࡶࡤࡸࡪࠦࡵࡴ࡫ࡱ࡫ࠥࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᓑ")
        bstack1l111ll1l1l_opy_ = {bstack1llll1l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧᓒ"): bstack1lll111llll_opy_.bstack1l11l111111_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l11l11111l_opy_(instance, bstack1l111ll1l1l_opy_)
    @staticmethod
    def bstack1l111l1l11l_opy_(instance: bstack1llll111111_opy_, bstack1l11l11ll11_opy_: str):
        bstack1l111ll111l_opy_ = (
            bstack1llll1l1111_opy_.bstack1l1111lllll_opy_
            if bstack1l11l11ll11_opy_ == bstack1llll1l1111_opy_.bstack1l11l1l1l1l_opy_
            else bstack1llll1l1111_opy_.bstack1l11l1lll1l_opy_
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
        hook = bstack1llll1l1111_opy_.bstack1l111l1l11l_opy_(instance, bstack1l11l11ll11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l111l11lll_opy_, []).clear()
    @staticmethod
    def __1l11l1ll111_opy_(instance: bstack1llll111111_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1llll1l_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡧࡴࡸࡤࡴࠤᓓ"), None)):
            return
        if os.getenv(bstack1llll1l_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡑࡕࡇࡔࠤᓔ"), bstack1llll1l_opy_ (u"ࠨ࠱ࠣᓕ")) != bstack1llll1l_opy_ (u"ࠢ࠲ࠤᓖ"):
            bstack1llll1l1111_opy_.logger.warning(bstack1llll1l_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡩ࡯ࡩࠣࡧࡦࡶ࡬ࡰࡩࠥᓗ"))
            return
        bstack1l11l11l11l_opy_ = {
            bstack1llll1l_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᓘ"): (bstack1llll1l1111_opy_.bstack1l1111llll1_opy_, bstack1llll1l1111_opy_.bstack1l11l1lll1l_opy_),
            bstack1llll1l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᓙ"): (bstack1llll1l1111_opy_.bstack1l11l1l1l1l_opy_, bstack1llll1l1111_opy_.bstack1l1111lllll_opy_),
        }
        for when in (bstack1llll1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᓚ"), bstack1llll1l_opy_ (u"ࠧࡩࡡ࡭࡮ࠥᓛ"), bstack1llll1l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᓜ")):
            bstack1l111l1l1ll_opy_ = args[1].get_records(when)
            if not bstack1l111l1l1ll_opy_:
                continue
            records = [
                bstack1ll1lll1lll_opy_(
                    kind=TestFramework.bstack1l1lll1l1ll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1llll1l_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠥᓝ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1llll1l_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࠤᓞ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111l1l1ll_opy_
                if isinstance(getattr(r, bstack1llll1l_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᓟ"), None), str) and r.message.strip()
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
    def __1l111ll1lll_opy_(test) -> Dict[str, Any]:
        bstack1l111llll1_opy_ = bstack1llll1l1111_opy_.__1l111l1l1l1_opy_(test.location) if hasattr(test, bstack1llll1l_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᓠ")) else getattr(test, bstack1llll1l_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᓡ"), None)
        test_name = test.name if hasattr(test, bstack1llll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᓢ")) else None
        bstack1l11l111lll_opy_ = test.fspath.strpath if hasattr(test, bstack1llll1l_opy_ (u"ࠨࡦࡴࡲࡤࡸ࡭ࠨᓣ")) and test.fspath else None
        if not bstack1l111llll1_opy_ or not test_name or not bstack1l11l111lll_opy_:
            return None
        code = None
        if hasattr(test, bstack1llll1l_opy_ (u"ࠢࡰࡤ࡭ࠦᓤ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l1111l1l11_opy_ = []
        try:
            bstack1l1111l1l11_opy_ = bstack1l11l111ll_opy_.bstack111l1ll1ll_opy_(test)
        except:
            bstack1llll1l1111_opy_.logger.warning(bstack1llll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡷࡩࡸࡺࠠࡴࡥࡲࡴࡪࡹࠬࠡࡶࡨࡷࡹࠦࡳࡤࡱࡳࡩࡸࠦࡷࡪ࡮࡯ࠤࡧ࡫ࠠࡳࡧࡶࡳࡱࡼࡥࡥࠢ࡬ࡲࠥࡉࡌࡊࠤᓥ"))
        return {
            TestFramework.bstack1ll11lll1ll_opy_: uuid4().__str__(),
            TestFramework.bstack1l111l1111l_opy_: bstack1l111llll1_opy_,
            TestFramework.bstack1ll1l11lll1_opy_: test_name,
            TestFramework.bstack1l1ll11lll1_opy_: getattr(test, bstack1llll1l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᓦ"), None),
            TestFramework.bstack1l111l1llll_opy_: bstack1l11l111lll_opy_,
            TestFramework.bstack1l1111ll1ll_opy_: bstack1llll1l1111_opy_.__1l1111ll1l1_opy_(test),
            TestFramework.bstack1l11l1ll11l_opy_: code,
            TestFramework.bstack1l1l1l1ll1l_opy_: TestFramework.bstack1l1111lll1l_opy_,
            TestFramework.bstack1l11lll1lll_opy_: bstack1l111llll1_opy_,
            TestFramework.bstack1l1111l1lll_opy_: bstack1l1111l1l11_opy_
        }
    @staticmethod
    def __1l1111ll1l1_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1llll1l_opy_ (u"ࠥࡳࡼࡴ࡟࡮ࡣࡵ࡯ࡪࡸࡳࠣᓧ"), [])
            markers.extend([getattr(m, bstack1llll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᓨ"), None) for m in own_markers if getattr(m, bstack1llll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᓩ"), None)])
            current = getattr(current, bstack1llll1l_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨᓪ"), None)
        return markers
    @staticmethod
    def __1l111l1l1l1_opy_(location):
        return bstack1llll1l_opy_ (u"ࠢ࠻࠼ࠥᓫ").join(filter(lambda x: isinstance(x, str), location))