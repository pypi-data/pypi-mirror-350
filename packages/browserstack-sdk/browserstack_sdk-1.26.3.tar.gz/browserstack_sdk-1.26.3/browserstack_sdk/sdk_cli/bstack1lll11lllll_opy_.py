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
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll1llll111_opy_ import bstack1lll1l1llll_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll111_opy_ import (
    bstack11111l1l1l_opy_,
    bstack1llllll1l1l_opy_,
    bstack1111111ll1_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1llll111l11_opy_ import bstack1llll11llll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11ll111ll_opy_
from bstack_utils.helper import bstack1ll111l111l_opy_
import threading
import os
import urllib.parse
class bstack1lll11ll11l_opy_(bstack1lll1l1llll_opy_):
    def __init__(self, bstack1ll1ll1llll_opy_):
        super().__init__()
        bstack1llll11llll_opy_.bstack1ll1l1l1l1l_opy_((bstack11111l1l1l_opy_.bstack11111ll111_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l1lll1l1_opy_)
        bstack1llll11llll_opy_.bstack1ll1l1l1l1l_opy_((bstack11111l1l1l_opy_.bstack11111ll111_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l1lllll1_opy_)
        bstack1llll11llll_opy_.bstack1ll1l1l1l1l_opy_((bstack11111l1l1l_opy_.bstack111111l1l1_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l1ll1l11_opy_)
        bstack1llll11llll_opy_.bstack1ll1l1l1l1l_opy_((bstack11111l1l1l_opy_.bstack111111llll_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l1llllll_opy_)
        bstack1llll11llll_opy_.bstack1ll1l1l1l1l_opy_((bstack11111l1l1l_opy_.bstack11111ll111_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l1ll111l_opy_)
        bstack1llll11llll_opy_.bstack1ll1l1l1l1l_opy_((bstack11111l1l1l_opy_.QUIT, bstack1llllll1l1l_opy_.PRE), self.on_close)
        self.bstack1ll1ll1llll_opy_ = bstack1ll1ll1llll_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1lll1l1_opy_(
        self,
        f: bstack1llll11llll_opy_,
        bstack1l1l1llll11_opy_: object,
        exec: Tuple[bstack1111111ll1_opy_, str],
        bstack11111l1lll_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1llll1l_opy_ (u"ࠧࡲࡡࡶࡰࡦ࡬ࠧብ"):
            return
        if not bstack1ll111l111l_opy_():
            self.logger.debug(bstack1llll1l_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡲࡡࡶࡰࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥቦ"))
            return
        def wrapped(bstack1l1l1llll11_opy_, launch, *args, **kwargs):
            response = self.bstack1l1l1ll1l1l_opy_(f.platform_index, instance.ref(), json.dumps({bstack1llll1l_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ቧ"): True}).encode(bstack1llll1l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢቨ")))
            if response is not None and response.capabilities:
                if not bstack1ll111l111l_opy_():
                    browser = launch(bstack1l1l1llll11_opy_)
                    return browser
                bstack1l1l1l1llll_opy_ = json.loads(response.capabilities.decode(bstack1llll1l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣቩ")))
                if not bstack1l1l1l1llll_opy_: # empty caps bstack1l1l1lll111_opy_ bstack1l1l1ll1lll_opy_ bstack1l1l1llll1l_opy_ bstack1lll111lll1_opy_ or error in processing
                    return
                bstack1l1l1ll11l1_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l1l1llll_opy_))
                f.bstack111111111l_opy_(instance, bstack1llll11llll_opy_.bstack1l1ll11111l_opy_, bstack1l1l1ll11l1_opy_)
                f.bstack111111111l_opy_(instance, bstack1llll11llll_opy_.bstack1l1ll111111_opy_, bstack1l1l1l1llll_opy_)
                browser = bstack1l1l1llll11_opy_.connect(bstack1l1l1ll11l1_opy_)
                return browser
        return wrapped
    def bstack1l1l1ll1l11_opy_(
        self,
        f: bstack1llll11llll_opy_,
        Connection: object,
        exec: Tuple[bstack1111111ll1_opy_, str],
        bstack11111l1lll_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1llll1l_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧቪ"):
            self.logger.debug(bstack1llll1l_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥቫ"))
            return
        if not bstack1ll111l111l_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1llll1l_opy_ (u"ࠬࡶࡡࡳࡣࡰࡷࠬቬ"), {}).get(bstack1llll1l_opy_ (u"࠭ࡢࡴࡒࡤࡶࡦࡳࡳࠨቭ")):
                    bstack1l1l1ll1111_opy_ = args[0][bstack1llll1l_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢቮ")][bstack1llll1l_opy_ (u"ࠣࡤࡶࡔࡦࡸࡡ࡮ࡵࠥቯ")]
                    session_id = bstack1l1l1ll1111_opy_.get(bstack1llll1l_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧተ"))
                    f.bstack111111111l_opy_(instance, bstack1llll11llll_opy_.bstack1l1l1lll11l_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1llll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࠨቱ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1l1ll111l_opy_(
        self,
        f: bstack1llll11llll_opy_,
        bstack1l1l1llll11_opy_: object,
        exec: Tuple[bstack1111111ll1_opy_, str],
        bstack11111l1lll_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1llll1l_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧቲ"):
            return
        if not bstack1ll111l111l_opy_():
            self.logger.debug(bstack1llll1l_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡨࡵ࡮࡯ࡧࡦࡸࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥታ"))
            return
        def wrapped(bstack1l1l1llll11_opy_, connect, *args, **kwargs):
            response = self.bstack1l1l1ll1l1l_opy_(f.platform_index, instance.ref(), json.dumps({bstack1llll1l_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬቴ"): True}).encode(bstack1llll1l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨት")))
            if response is not None and response.capabilities:
                bstack1l1l1l1llll_opy_ = json.loads(response.capabilities.decode(bstack1llll1l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢቶ")))
                if not bstack1l1l1l1llll_opy_:
                    return
                bstack1l1l1ll11l1_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l1l1llll_opy_))
                if bstack1l1l1l1llll_opy_.get(bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨቷ")):
                    browser = bstack1l1l1llll11_opy_.bstack1l1l1ll11ll_opy_(bstack1l1l1ll11l1_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1l1ll11l1_opy_
                    return connect(bstack1l1l1llll11_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1l1lllll1_opy_(
        self,
        f: bstack1llll11llll_opy_,
        bstack1ll111ll11l_opy_: object,
        exec: Tuple[bstack1111111ll1_opy_, str],
        bstack11111l1lll_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1llll1l_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧቸ"):
            return
        if not bstack1ll111l111l_opy_():
            self.logger.debug(bstack1llll1l_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡲࡪࡽ࡟ࡱࡣࡪࡩࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥቹ"))
            return
        def wrapped(bstack1ll111ll11l_opy_, bstack1l1l1ll1ll1_opy_, *args, **kwargs):
            contexts = bstack1ll111ll11l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack1llll1l_opy_ (u"ࠧࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠥቺ") in page.url:
                                    return page
                    else:
                        return bstack1l1l1ll1ll1_opy_(bstack1ll111ll11l_opy_)
        return wrapped
    def bstack1l1l1ll1l1l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1llll1l_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡹࡨࡦࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦቻ") + str(req) + bstack1llll1l_opy_ (u"ࠢࠣቼ"))
        try:
            r = self.bstack1llll111l1l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1llll1l_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦች") + str(r.success) + bstack1llll1l_opy_ (u"ࠤࠥቾ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1llll1l_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣቿ") + str(e) + bstack1llll1l_opy_ (u"ࠦࠧኀ"))
            traceback.print_exc()
            raise e
    def bstack1l1l1llllll_opy_(
        self,
        f: bstack1llll11llll_opy_,
        Connection: object,
        exec: Tuple[bstack1111111ll1_opy_, str],
        bstack11111l1lll_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1llll1l_opy_ (u"ࠧࡥࡳࡦࡰࡧࡣࡲ࡫ࡳࡴࡣࡪࡩࡤࡺ࡯ࡠࡵࡨࡶࡻ࡫ࡲࠣኁ"):
            return
        if not bstack1ll111l111l_opy_():
            return
        def wrapped(Connection, bstack1l1l1lll1ll_opy_, *args, **kwargs):
            return bstack1l1l1lll1ll_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1llll11llll_opy_,
        bstack1l1l1llll11_opy_: object,
        exec: Tuple[bstack1111111ll1_opy_, str],
        bstack11111l1lll_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1llll1l_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧኂ"):
            return
        if not bstack1ll111l111l_opy_():
            self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦࡣ࡭ࡱࡶࡩࠥࡳࡥࡵࡪࡲࡨ࠱ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥኃ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped