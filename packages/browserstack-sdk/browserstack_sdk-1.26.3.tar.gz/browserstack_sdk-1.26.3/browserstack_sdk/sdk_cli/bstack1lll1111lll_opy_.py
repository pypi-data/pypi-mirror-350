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
from browserstack_sdk.sdk_cli.bstack1ll1llll111_opy_ import bstack1lll1l1llll_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll111_opy_ import (
    bstack11111l1l1l_opy_,
    bstack1llllll1l1l_opy_,
    bstack1111111ll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1lllll1ll1l_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1llll111_opy_ import bstack1lll1l1llll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1lll111ll11_opy_(bstack1lll1l1llll_opy_):
    bstack1ll1l1l1111_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1lllll1ll1l_opy_.bstack1ll1l1l1l1l_opy_((bstack11111l1l1l_opy_.bstack111111llll_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1ll11l11l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11l11l11_opy_(
        self,
        f: bstack1lllll1ll1l_opy_,
        driver: object,
        exec: Tuple[bstack1111111ll1_opy_, str],
        bstack11111l1lll_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll11l1l111_opy_(hub_url):
            if not bstack1lll111ll11_opy_.bstack1ll1l1l1111_opy_:
                self.logger.warning(bstack1llll1l_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࠢࡶࡩࡱ࡬࠭ࡩࡧࡤࡰࠥ࡬࡬ࡰࡹࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡ࡫ࡱࡪࡷࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦᆟ") + str(hub_url) + bstack1llll1l_opy_ (u"ࠦࠧᆠ"))
                bstack1lll111ll11_opy_.bstack1ll1l1l1111_opy_ = True
            return
        bstack1ll1l11l11l_opy_ = f.bstack1ll1l111l1l_opy_(*args)
        bstack1ll11l11lll_opy_ = f.bstack1ll11l11l1l_opy_(*args)
        if bstack1ll1l11l11l_opy_ and bstack1ll1l11l11l_opy_.lower() == bstack1llll1l_opy_ (u"ࠧ࡬ࡩ࡯ࡦࡨࡰࡪࡳࡥ࡯ࡶࠥᆡ") and bstack1ll11l11lll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll11l11lll_opy_.get(bstack1llll1l_opy_ (u"ࠨࡵࡴ࡫ࡱ࡫ࠧᆢ"), None), bstack1ll11l11lll_opy_.get(bstack1llll1l_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᆣ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1llll1l_opy_ (u"ࠣࡽࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥࡾ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠤࡴࡸࠠࡢࡴࡪࡷ࠳ࡻࡳࡪࡰࡪࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡵࡲࠡࡣࡵ࡫ࡸ࠴ࡶࡢ࡮ࡸࡩࡂࠨᆤ") + str(locator_value) + bstack1llll1l_opy_ (u"ࠤࠥᆥ"))
                return
            def bstack1llllll11ll_opy_(driver, bstack1ll11l1l1l1_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll11l1l1l1_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll11l111l1_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1llll1l_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࠨᆦ") + str(locator_value) + bstack1llll1l_opy_ (u"ࠦࠧᆧ"))
                    else:
                        self.logger.warning(bstack1llll1l_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸ࠳࡮ࡰ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠽ࠣᆨ") + str(response) + bstack1llll1l_opy_ (u"ࠨࠢᆩ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll11l1l1ll_opy_(
                        driver, bstack1ll11l1l1l1_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1llllll11ll_opy_.__name__ = bstack1ll1l11l11l_opy_
            return bstack1llllll11ll_opy_
    def __1ll11l1l1ll_opy_(
        self,
        driver,
        bstack1ll11l1l1l1_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll11l111l1_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1llll1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡷࡶ࡮࡭ࡧࡦࡴࡨࡨ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࠢᆪ") + str(locator_value) + bstack1llll1l_opy_ (u"ࠣࠤᆫ"))
                bstack1ll11l11ll1_opy_ = self.bstack1ll11l1l11l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1llll1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡩࡧࡤࡰ࡮ࡴࡧࡠࡴࡨࡷࡺࡲࡴ࠾ࠤᆬ") + str(bstack1ll11l11ll1_opy_) + bstack1llll1l_opy_ (u"ࠥࠦᆭ"))
                if bstack1ll11l11ll1_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1llll1l_opy_ (u"ࠦࡺࡹࡩ࡯ࡩࠥᆮ"): bstack1ll11l11ll1_opy_.locator_type,
                            bstack1llll1l_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᆯ"): bstack1ll11l11ll1_opy_.locator_value,
                        }
                    )
                    return bstack1ll11l1l1l1_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1llll1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡉࡠࡆࡈࡆ࡚ࡍࠢᆰ"), False):
                    self.logger.info(bstack1ll1ll1ll1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠯ࡰ࡭ࡸࡹࡩ࡯ࡩ࠽ࠤࡸࡲࡥࡦࡲࠫ࠷࠵࠯ࠠ࡭ࡧࡷࡸ࡮ࡴࡧࠡࡻࡲࡹࠥ࡯࡮ࡴࡲࡨࡧࡹࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࠠ࡭ࡱࡪࡷࠧᆱ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1llll1l_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯ࡱࡳ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࡀࠦᆲ") + str(response) + bstack1llll1l_opy_ (u"ࠤࠥᆳ"))
        except Exception as err:
            self.logger.warning(bstack1llll1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠿ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢᆴ") + str(err) + bstack1llll1l_opy_ (u"ࠦࠧᆵ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll11l1111l_opy_, stage=STAGE.bstack11111l1l1_opy_)
    def bstack1ll11l111l1_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1llll1l_opy_ (u"ࠧ࠶ࠢᆶ"),
    ):
        self.bstack1ll11llllll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1llll1l_opy_ (u"ࠨࠢᆷ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1llll111l1l_opy_.AISelfHealStep(req)
            self.logger.info(bstack1llll1l_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᆸ") + str(r) + bstack1llll1l_opy_ (u"ࠣࠤᆹ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1llll1l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᆺ") + str(e) + bstack1llll1l_opy_ (u"ࠥࠦᆻ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11l111ll_opy_, stage=STAGE.bstack11111l1l1_opy_)
    def bstack1ll11l1l11l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1llll1l_opy_ (u"ࠦ࠵ࠨᆼ")):
        self.bstack1ll11llllll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1llll111l1l_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1llll1l_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᆽ") + str(r) + bstack1llll1l_opy_ (u"ࠨࠢᆾ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1llll1l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᆿ") + str(e) + bstack1llll1l_opy_ (u"ࠣࠤᇀ"))
            traceback.print_exc()
            raise e