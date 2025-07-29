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
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1111l1111l_opy_ import bstack11111llll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll111_opy_ import bstack1lll1l1llll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll11l11_opy_ import bstack1lll11llll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111lll_opy_ import bstack1lll111ll11_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l11ll_opy_ import bstack1llll1lll11_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1111l_opy_ import bstack1llll1l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1111_opy_ import bstack1ll1lll1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import bstack1lll11ll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1lll_opy_ import bstack1lllll11111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll111_opy_ import bstack1lll111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1ll_opy_ import bstack1ll1ll1ll_opy_, bstack1ll111111_opy_, bstack11l1lll11_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import bstack1llll1l1111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1lllll1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll111_opy_ import bstack11111lll11_opy_
from browserstack_sdk.sdk_cli.bstack1llll111l11_opy_ import bstack1llll11llll_opy_
from bstack_utils.helper import Notset, bstack1lllll1l111_opy_, get_cli_dir, bstack1lll11lll11_opy_, bstack11l111l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1lllll11l1l_opy_ import bstack1lll111llll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll111lll1_opy_ import bstack1lllll11l1_opy_
from bstack_utils.helper import Notset, bstack1lllll1l111_opy_, get_cli_dir, bstack1lll11lll11_opy_, bstack11l111l1_opy_, bstack11lll1l1l1_opy_, bstack1ll1l1l11_opy_, bstack1ll1l1l1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1llll1ll_opy_, bstack1llll111111_opy_, bstack1llll1l1lll_opy_, bstack1ll1lll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll111_opy_ import bstack1111111ll1_opy_, bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1llll11l1l_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11l11l1lll_opy_, bstack111ll11ll_opy_
logger = bstack1llll11l1l_opy_.get_logger(__name__, bstack1llll11l1l_opy_.bstack1lll1llllll_opy_())
def bstack1lll1l1l1l1_opy_(bs_config):
    bstack1ll1ll1lll1_opy_ = None
    bstack1llll1ll11l_opy_ = None
    try:
        bstack1llll1ll11l_opy_ = get_cli_dir()
        bstack1ll1ll1lll1_opy_ = bstack1lll11lll11_opy_(bstack1llll1ll11l_opy_)
        bstack1lll1l11111_opy_ = bstack1lllll1l111_opy_(bstack1ll1ll1lll1_opy_, bstack1llll1ll11l_opy_, bs_config)
        bstack1ll1ll1lll1_opy_ = bstack1lll1l11111_opy_ if bstack1lll1l11111_opy_ else bstack1ll1ll1lll1_opy_
        if not bstack1ll1ll1lll1_opy_:
            raise ValueError(bstack1llll1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠥ၄"))
    except Exception as ex:
        logger.debug(bstack1llll1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡸ࡭࡫ࠠ࡭ࡣࡷࡩࡸࡺࠠࡣ࡫ࡱࡥࡷࡿࠠࡼࡿࠥ၅").format(ex))
        bstack1ll1ll1lll1_opy_ = os.environ.get(bstack1llll1l_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠦ၆"))
        if bstack1ll1ll1lll1_opy_:
            logger.debug(bstack1llll1l_opy_ (u"ࠤࡉࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠡࡶࡲࠤࡘࡊࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡓࡅ࡙ࡎࠠࡧࡴࡲࡱࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠽ࠤࠧ၇") + str(bstack1ll1ll1lll1_opy_) + bstack1llll1l_opy_ (u"ࠥࠦ၈"))
        else:
            logger.debug(bstack1llll1l_opy_ (u"ࠦࡓࡵࠠࡷࡣ࡯࡭ࡩࠦࡓࡅࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡕࡇࡔࡉࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵ࠽ࠣࡷࡪࡺࡵࡱࠢࡰࡥࡾࠦࡢࡦࠢ࡬ࡲࡨࡵ࡭ࡱ࡮ࡨࡸࡪ࠴ࠢ၉"))
    return bstack1ll1ll1lll1_opy_, bstack1llll1ll11l_opy_
bstack1ll1lllll11_opy_ = bstack1llll1l_opy_ (u"ࠧ࠿࠹࠺࠻ࠥ၊")
bstack1lll1lll1l1_opy_ = bstack1llll1l_opy_ (u"ࠨࡲࡦࡣࡧࡽࠧ။")
bstack1lll11ll111_opy_ = bstack1llll1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦ၌")
bstack1lll11l1ll1_opy_ = bstack1llll1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡎࡌࡗ࡙ࡋࡎࡠࡃࡇࡈࡗࠨ၍")
bstack1111l111l_opy_ = bstack1llll1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠧ၎")
bstack1lll1ll111l_opy_ = re.compile(bstack1llll1l_opy_ (u"ࡵࠦ࠭ࡅࡩࠪ࠰࠭ࠬࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡿࡆࡘ࠯࠮ࠫࠤ၏"))
bstack1lll11l1l1l_opy_ = bstack1llll1l_opy_ (u"ࠦࡩ࡫ࡶࡦ࡮ࡲࡴࡲ࡫࡮ࡵࠤၐ")
bstack1lll11ll1ll_opy_ = [
    bstack1ll111111_opy_.bstack1l1l111l1l_opy_,
    bstack1ll111111_opy_.CONNECT,
    bstack1ll111111_opy_.bstack1lll11l111_opy_,
]
class SDKCLI:
    _1ll1lllllll_opy_ = None
    process: Union[None, Any]
    bstack1lllll1lll1_opy_: bool
    bstack1lllll1l1l1_opy_: bool
    bstack1ll1lll11ll_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1lll1l1ll11_opy_: Union[None, grpc.Channel]
    bstack1llll1llll1_opy_: str
    test_framework: TestFramework
    bstack1lllllll111_opy_: bstack11111lll11_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1llll11ll11_opy_: bstack1lll111l1ll_opy_
    accessibility: bstack1lll11llll1_opy_
    bstack1ll111lll1_opy_: bstack1lllll11l1_opy_
    ai: bstack1lll111ll11_opy_
    bstack1lll1l111ll_opy_: bstack1llll1lll11_opy_
    bstack1lll1ll11l1_opy_: List[bstack1lll1l1llll_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1lll11l1l11_opy_: Any
    bstack1lll1l11l1l_opy_: Dict[str, timedelta]
    bstack1lll1l1ll1l_opy_: str
    bstack1111l1111l_opy_: bstack11111llll1_opy_
    def __new__(cls):
        if not cls._1ll1lllllll_opy_:
            cls._1ll1lllllll_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll1lllllll_opy_
    def __init__(self):
        self.process = None
        self.bstack1lllll1lll1_opy_ = False
        self.bstack1lll1l1ll11_opy_ = None
        self.bstack1llll111l1l_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1lll11l1ll1_opy_, None)
        self.bstack1lll1lll11l_opy_ = os.environ.get(bstack1lll11ll111_opy_, bstack1llll1l_opy_ (u"ࠧࠨၑ")) == bstack1llll1l_opy_ (u"ࠨࠢၒ")
        self.bstack1lllll1l1l1_opy_ = False
        self.bstack1ll1lll11ll_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1lll11l1l11_opy_ = None
        self.test_framework = None
        self.bstack1lllllll111_opy_ = None
        self.bstack1llll1llll1_opy_=bstack1llll1l_opy_ (u"ࠢࠣၓ")
        self.session_framework = None
        self.logger = bstack1llll11l1l_opy_.get_logger(self.__class__.__name__, bstack1llll11l1l_opy_.bstack1lll1llllll_opy_())
        self.bstack1lll1l11l1l_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1111l1111l_opy_ = bstack11111llll1_opy_()
        self.bstack1lll11111ll_opy_ = None
        self.bstack1ll1ll1llll_opy_ = None
        self.bstack1llll11ll11_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1lll1ll11l1_opy_ = []
    def bstack1l111ll11_opy_(self):
        return os.environ.get(bstack1111l111l_opy_).lower().__eq__(bstack1llll1l_opy_ (u"ࠣࡶࡵࡹࡪࠨၔ"))
    def is_enabled(self, config):
        if bstack1llll1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ၕ") in config and str(config[bstack1llll1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧၖ")]).lower() != bstack1llll1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪၗ"):
            return False
        bstack1llll1lllll_opy_ = [bstack1llll1l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧၘ"), bstack1llll1l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥၙ")]
        bstack1lll1ll1ll1_opy_ = config.get(bstack1llll1l_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥၚ")) in bstack1llll1lllll_opy_ or os.environ.get(bstack1llll1l_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩၛ")) in bstack1llll1lllll_opy_
        os.environ[bstack1llll1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧၜ")] = str(bstack1lll1ll1ll1_opy_) # bstack1llll1l1l11_opy_ bstack1lll1ll11ll_opy_ VAR to bstack1lll11111l1_opy_ is binary running
        return bstack1lll1ll1ll1_opy_
    def bstack1llll11111_opy_(self):
        for event in bstack1lll11ll1ll_opy_:
            bstack1ll1ll1ll_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1ll1ll1ll_opy_.logger.debug(bstack1llll1l_opy_ (u"ࠥࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠢࡀࡂࠥࢁࡡࡳࡩࡶࢁࠥࠨၝ") + str(kwargs) + bstack1llll1l_opy_ (u"ࠦࠧၞ"))
            )
        bstack1ll1ll1ll_opy_.register(bstack1ll111111_opy_.bstack1l1l111l1l_opy_, self.__1lll111111l_opy_)
        bstack1ll1ll1ll_opy_.register(bstack1ll111111_opy_.CONNECT, self.__1lll1l1l11l_opy_)
        bstack1ll1ll1ll_opy_.register(bstack1ll111111_opy_.bstack1lll11l111_opy_, self.__1lll1lll1ll_opy_)
        bstack1ll1ll1ll_opy_.register(bstack1ll111111_opy_.bstack1l1l1llll_opy_, self.__1lllll11lll_opy_)
    def bstack11l111l1l_opy_(self):
        return not self.bstack1lll1lll11l_opy_ and os.environ.get(bstack1lll11ll111_opy_, bstack1llll1l_opy_ (u"ࠧࠨၟ")) != bstack1llll1l_opy_ (u"ࠨࠢၠ")
    def is_running(self):
        if self.bstack1lll1lll11l_opy_:
            return self.bstack1lllll1lll1_opy_
        else:
            return bool(self.bstack1lll1l1ll11_opy_)
    def bstack1lll11ll1l1_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1lll1ll11l1_opy_) and cli.is_running()
    def __1llll111ll1_opy_(self, bstack1lll11l1111_opy_=10):
        if self.bstack1llll111l1l_opy_:
            return
        bstack1l11l1lll_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1lll11l1ll1_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1llll1l_opy_ (u"ࠢ࡜ࠤၡ") + str(id(self)) + bstack1llll1l_opy_ (u"ࠣ࡟ࠣࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡳ࡭ࠢၢ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1llll1l_opy_ (u"ࠤࡪࡶࡵࡩ࠮ࡦࡰࡤࡦࡱ࡫࡟ࡩࡶࡷࡴࡤࡶࡲࡰࡺࡼࠦၣ"), 0), (bstack1llll1l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠯ࡧࡱࡥࡧࡲࡥࡠࡪࡷࡸࡵࡹ࡟ࡱࡴࡲࡼࡾࠨၤ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1lll11l1111_opy_)
        self.bstack1lll1l1ll11_opy_ = channel
        self.bstack1llll111l1l_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1lll1l1ll11_opy_)
        self.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡦࡳࡳࡴࡥࡤࡶࠥၥ"), datetime.now() - bstack1l11l1lll_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1lll11l1ll1_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1llll1l_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪ࠺ࠡ࡫ࡶࡣࡨ࡮ࡩ࡭ࡦࡢࡴࡷࡵࡣࡦࡵࡶࡁࠧၦ") + str(self.bstack11l111l1l_opy_()) + bstack1llll1l_opy_ (u"ࠨࠢၧ"))
    def __1lll1lll1ll_opy_(self, event_name):
        if self.bstack11l111l1l_opy_():
            self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡵࡷࡳࡵࡶࡩ࡯ࡩࠣࡇࡑࡏࠢၨ"))
        self.__1llll111lll_opy_()
    def __1lllll11lll_opy_(self, event_name, bstack1lll1ll1l11_opy_ = None, bstack1l1ll1llll_opy_=1):
        if bstack1l1ll1llll_opy_ == 1:
            self.logger.error(bstack1llll1l_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠣၩ"))
        bstack1lll11l111l_opy_ = Path(bstack1ll1ll1ll1l_opy_ (u"ࠤࡾࡷࡪࡲࡦ࠯ࡥ࡯࡭ࡤࡪࡩࡳࡿ࠲ࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࡷ࠳ࡰࡳࡰࡰࠥၪ"))
        if self.bstack1llll1ll11l_opy_ and bstack1lll11l111l_opy_.exists():
            with open(bstack1lll11l111l_opy_, bstack1llll1l_opy_ (u"ࠪࡶࠬၫ"), encoding=bstack1llll1l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪၬ")) as fp:
                data = json.load(fp)
                try:
                    bstack11lll1l1l1_opy_(bstack1llll1l_opy_ (u"ࠬࡖࡏࡔࡖࠪၭ"), bstack1ll1l1l11_opy_(bstack1ll11l1l11_opy_), data, {
                        bstack1llll1l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫၮ"): (self.config[bstack1llll1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩၯ")], self.config[bstack1llll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫၰ")])
                    })
                except Exception as e:
                    logger.debug(bstack111ll11ll_opy_.format(str(e)))
            bstack1lll11l111l_opy_.unlink()
        sys.exit(bstack1l1ll1llll_opy_)
    @measure(event_name=EVENTS.bstack1lllll111ll_opy_, stage=STAGE.bstack11111l1l1_opy_)
    def __1lll111111l_opy_(self, event_name: str, data):
        from bstack_utils.bstack1l1lll111l_opy_ import bstack1lllll11ll1_opy_
        self.bstack1llll1llll1_opy_, self.bstack1llll1ll11l_opy_ = bstack1lll1l1l1l1_opy_(data.bs_config)
        os.environ[bstack1llll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠ࡙ࡕࡍ࡙ࡇࡂࡍࡇࡢࡈࡎࡘࠧၱ")] = self.bstack1llll1ll11l_opy_
        if not self.bstack1llll1llll1_opy_ or not self.bstack1llll1ll11l_opy_:
            raise ValueError(bstack1llll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺࠤၲ"))
        if self.bstack11l111l1l_opy_():
            self.__1lll1l1l11l_opy_(event_name, bstack11l1lll11_opy_())
            return
        try:
            bstack1lllll11ll1_opy_.end(EVENTS.bstack111l1ll1_opy_.value, EVENTS.bstack111l1ll1_opy_.value + bstack1llll1l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦၳ"), EVENTS.bstack111l1ll1_opy_.value + bstack1llll1l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥၴ"), status=True, failure=None, test_name=None)
            logger.debug(bstack1llll1l_opy_ (u"ࠨࡃࡰ࡯ࡳࡰࡪࡺࡥࠡࡕࡇࡏ࡙ࠥࡥࡵࡷࡳ࠲ࠧၵ"))
        except Exception as e:
            logger.debug(bstack1llll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡽࢀࠦၶ").format(e))
        start = datetime.now()
        is_started = self.__1lll111l111_opy_()
        self.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠣࡵࡳࡥࡼࡴ࡟ࡵ࡫ࡰࡩࠧၷ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1llll111ll1_opy_()
            self.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࡢࡸ࡮ࡳࡥࠣၸ"), datetime.now() - start)
            start = datetime.now()
            self.__1lllll1ll11_opy_(data)
            self.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣၹ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1lll11lll1l_opy_, stage=STAGE.bstack11111l1l1_opy_)
    def __1lll1l1l11l_opy_(self, event_name: str, data: bstack11l1lll11_opy_):
        if not self.bstack11l111l1l_opy_():
            self.logger.debug(bstack1llll1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱࡱࡲࡪࡩࡴ࠻ࠢࡱࡳࡹࠦࡡࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳࠣၺ"))
            return
        bin_session_id = os.environ.get(bstack1lll11ll111_opy_)
        start = datetime.now()
        self.__1llll111ll1_opy_()
        self.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦၻ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1llll1l_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠢࡷࡳࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡄࡎࡌࠤࠧၼ") + str(bin_session_id) + bstack1llll1l_opy_ (u"ࠢࠣၽ"))
        start = datetime.now()
        self.__1llll1111l1_opy_()
        self.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨၾ"), datetime.now() - start)
    def __1llll1l111l_opy_(self):
        if not self.bstack1llll111l1l_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠤࡦࡥࡳࡴ࡯ࡵࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࠥࡳ࡯ࡥࡷ࡯ࡩࡸࠨၿ"))
            return
        bstack1ll1llllll1_opy_ = {
            bstack1llll1l_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢႀ"): (bstack1lll11ll11l_opy_, bstack1lllll11111_opy_, bstack1llll11llll_opy_),
            bstack1llll1l_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨႁ"): (bstack1llll1l1l1l_opy_, bstack1ll1lll1ll1_opy_, bstack1lllll1ll1l_opy_),
        }
        if not self.bstack1lll11111ll_opy_ and self.session_framework in bstack1ll1llllll1_opy_:
            bstack1lll111l1l1_opy_, bstack1llll1ll111_opy_, bstack1lll1111l11_opy_ = bstack1ll1llllll1_opy_[self.session_framework]
            bstack1llll11111l_opy_ = bstack1llll1ll111_opy_()
            self.bstack1ll1ll1llll_opy_ = bstack1llll11111l_opy_
            self.bstack1lll11111ll_opy_ = bstack1lll1111l11_opy_
            self.bstack1lll1ll11l1_opy_.append(bstack1llll11111l_opy_)
            self.bstack1lll1ll11l1_opy_.append(bstack1lll111l1l1_opy_(self.bstack1ll1ll1llll_opy_))
        if not self.bstack1llll11ll11_opy_ and self.config_observability and self.config_observability.success: # bstack1lll111lll1_opy_
            self.bstack1llll11ll11_opy_ = bstack1lll111l1ll_opy_(self.bstack1lll11111ll_opy_, self.bstack1ll1ll1llll_opy_) # bstack1lll1llll1l_opy_
            self.bstack1lll1ll11l1_opy_.append(self.bstack1llll11ll11_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1lll11llll1_opy_(self.bstack1lll11111ll_opy_, self.bstack1ll1ll1llll_opy_)
            self.bstack1lll1ll11l1_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1llll1l_opy_ (u"ࠧࡹࡥ࡭ࡨࡋࡩࡦࡲࠢႂ"), False) == True:
            self.ai = bstack1lll111ll11_opy_()
            self.bstack1lll1ll11l1_opy_.append(self.ai)
        if not self.percy and self.bstack1lll11l1l11_opy_ and self.bstack1lll11l1l11_opy_.success:
            self.percy = bstack1llll1lll11_opy_(self.bstack1lll11l1l11_opy_)
            self.bstack1lll1ll11l1_opy_.append(self.percy)
        for mod in self.bstack1lll1ll11l1_opy_:
            if not mod.bstack1lll1llll11_opy_():
                mod.configure(self.bstack1llll111l1l_opy_, self.config, self.cli_bin_session_id, self.bstack1111l1111l_opy_)
    def __1lllll1l11l_opy_(self):
        for mod in self.bstack1lll1ll11l1_opy_:
            if mod.bstack1lll1llll11_opy_():
                mod.configure(self.bstack1llll111l1l_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1llll1ll1ll_opy_, stage=STAGE.bstack11111l1l1_opy_)
    def __1lllll1ll11_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1lllll1l1l1_opy_:
            return
        self.__1llll1l1ll1_opy_(data)
        bstack1l11l1lll_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1llll1l_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨႃ")
        req.sdk_language = bstack1llll1l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢႄ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1lll1ll111l_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠣ࡝ࠥႅ") + str(id(self)) + bstack1llll1l_opy_ (u"ࠤࡠࠤࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡸࡺࡡࡳࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣႆ"))
            r = self.bstack1llll111l1l_opy_.StartBinSession(req)
            self.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡷࡥࡷࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧႇ"), datetime.now() - bstack1l11l1lll_opy_)
            os.environ[bstack1lll11ll111_opy_] = r.bin_session_id
            self.__1ll1lll11l1_opy_(r)
            self.__1llll1l111l_opy_()
            self.bstack1111l1111l_opy_.start()
            self.bstack1lllll1l1l1_opy_ = True
            self.logger.debug(bstack1llll1l_opy_ (u"ࠦࡠࠨႈ") + str(id(self)) + bstack1llll1l_opy_ (u"ࠧࡣࠠ࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦࠥႉ"))
        except grpc.bstack1lllll111l1_opy_ as bstack1llll11l11l_opy_:
            self.logger.error(bstack1llll1l_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡺࡩ࡮ࡧࡲࡩࡺࡺ࠭ࡦࡴࡵࡳࡷࡀࠠࠣႊ") + str(bstack1llll11l11l_opy_) + bstack1llll1l_opy_ (u"ࠢࠣႋ"))
            traceback.print_exc()
            raise bstack1llll11l11l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1llll1l_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧႌ") + str(e) + bstack1llll1l_opy_ (u"ࠤႍࠥ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1llll11l1ll_opy_, stage=STAGE.bstack11111l1l1_opy_)
    def __1llll1111l1_opy_(self):
        if not self.bstack11l111l1l_opy_() or not self.cli_bin_session_id or self.bstack1ll1lll11ll_opy_:
            return
        bstack1l11l1lll_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1llll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪႎ"), bstack1llll1l_opy_ (u"ࠫ࠵࠭ႏ")))
        try:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠧࡡࠢ႐") + str(id(self)) + bstack1llll1l_opy_ (u"ࠨ࡝ࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣ႑"))
            r = self.bstack1llll111l1l_opy_.ConnectBinSession(req)
            self.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡩ࡯࡯ࡰࡨࡧࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦ႒"), datetime.now() - bstack1l11l1lll_opy_)
            self.__1ll1lll11l1_opy_(r)
            self.__1llll1l111l_opy_()
            self.bstack1111l1111l_opy_.start()
            self.bstack1ll1lll11ll_opy_ = True
            self.logger.debug(bstack1llll1l_opy_ (u"ࠣ࡝ࠥ႓") + str(id(self)) + bstack1llll1l_opy_ (u"ࠤࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠣ႔"))
        except grpc.bstack1lllll111l1_opy_ as bstack1llll11l11l_opy_:
            self.logger.error(bstack1llll1l_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡷ࡭ࡲ࡫࡯ࡦࡷࡷ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧ႕") + str(bstack1llll11l11l_opy_) + bstack1llll1l_opy_ (u"ࠦࠧ႖"))
            traceback.print_exc()
            raise bstack1llll11l11l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1llll1l_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤ႗") + str(e) + bstack1llll1l_opy_ (u"ࠨࠢ႘"))
            traceback.print_exc()
            raise e
    def __1ll1lll11l1_opy_(self, r):
        self.bstack1llll11ll1l_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1llll1l_opy_ (u"ࠢࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡸ࡫ࡲࡷࡧࡵࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨ႙") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1llll1l_opy_ (u"ࠣࡧࡰࡴࡹࡿࠠࡤࡱࡱࡪ࡮࡭ࠠࡧࡱࡸࡲࡩࠨႚ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1llll1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡦࡴࡦࡽࠥ࡯ࡳࠡࡵࡨࡲࡹࠦ࡯࡯࡮ࡼࠤࡦࡹࠠࡱࡣࡵࡸࠥࡵࡦࠡࡶ࡫ࡩࠥࠨࡃࡰࡰࡱࡩࡨࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰ࠯ࠦࠥࡧ࡮ࡥࠢࡷ࡬࡮ࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢ࡬ࡷࠥࡧ࡬ࡴࡱࠣࡹࡸ࡫ࡤࠡࡤࡼࠤࡘࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫ࡩࡷ࡫ࡦࡰࡴࡨ࠰ࠥࡔ࡯࡯ࡧࠣ࡬ࡦࡴࡤ࡭࡫ࡱ࡫ࠥ࡯ࡳࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦႛ")
        self.bstack1lll11l1l11_opy_ = getattr(r, bstack1llll1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩႜ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1llll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨႝ")] = self.config_testhub.jwt
        os.environ[bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ႞")] = self.config_testhub.build_hashed_id
    def bstack1lll1l11lll_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1lllll1lll1_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1llll1111ll_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1llll1111ll_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1lll1l11lll_opy_(event_name=EVENTS.bstack1lll1l1lll1_opy_, stage=STAGE.bstack11111l1l1_opy_)
    def __1lll111l111_opy_(self, bstack1lll11l1111_opy_=10):
        if self.bstack1lllll1lll1_opy_:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠨࡳࡵࡣࡵࡸ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠣ႟"))
            return True
        self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡴࡶࡤࡶࡹࠨႠ"))
        if os.getenv(bstack1llll1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡊࡔࡖࠣႡ")) == bstack1lll11l1l1l_opy_:
            self.cli_bin_session_id = bstack1lll11l1l1l_opy_
            self.cli_listen_addr = bstack1llll1l_opy_ (u"ࠤࡸࡲ࡮ࡾ࠺࠰ࡶࡰࡴ࠴ࡹࡤ࡬࠯ࡳࡰࡦࡺࡦࡰࡴࡰ࠱ࠪࡹ࠮ࡴࡱࡦ࡯ࠧႢ") % (self.cli_bin_session_id)
            self.bstack1lllll1lll1_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1llll1llll1_opy_, bstack1llll1l_opy_ (u"ࠥࡷࡩࡱࠢႣ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1lll111ll1l_opy_ compat for text=True in bstack1llll1ll1l1_opy_ python
            encoding=bstack1llll1l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥႤ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1lll1111ll1_opy_ = threading.Thread(target=self.__1ll1lll1l11_opy_, args=(bstack1lll11l1111_opy_,))
        bstack1lll1111ll1_opy_.start()
        bstack1lll1111ll1_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡸࡶࡡࡸࡰ࠽ࠤࡷ࡫ࡴࡶࡴࡱࡧࡴࡪࡥ࠾ࡽࡶࡩࡱ࡬࠮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡴࡨࡸࡺࡸ࡮ࡤࡱࡧࡩࢂࠦ࡯ࡶࡶࡀࡿࡸ࡫࡬ࡧ࠰ࡳࡶࡴࡩࡥࡴࡵ࠱ࡷࡹࡪ࡯ࡶࡶ࠱ࡶࡪࡧࡤࠩࠫࢀࠤࡪࡸࡲ࠾ࠤႥ") + str(self.process.stderr.read()) + bstack1llll1l_opy_ (u"ࠨࠢႦ"))
        if not self.bstack1lllll1lll1_opy_:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠢ࡜ࠤႧ") + str(id(self)) + bstack1llll1l_opy_ (u"ࠣ࡟ࠣࡧࡱ࡫ࡡ࡯ࡷࡳࠦႨ"))
            self.__1llll111lll_opy_()
        self.logger.debug(bstack1llll1l_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡲࡵࡳࡨ࡫ࡳࡴࡡࡵࡩࡦࡪࡹ࠻ࠢࠥႩ") + str(self.bstack1lllll1lll1_opy_) + bstack1llll1l_opy_ (u"ࠥࠦႪ"))
        return self.bstack1lllll1lll1_opy_
    def __1ll1lll1l11_opy_(self, bstack1lll1ll1l1l_opy_=10):
        bstack1lll1l1111l_opy_ = time.time()
        while self.process and time.time() - bstack1lll1l1111l_opy_ < bstack1lll1ll1l1l_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1llll1l_opy_ (u"ࠦ࡮ࡪ࠽ࠣႫ") in line:
                    self.cli_bin_session_id = line.split(bstack1llll1l_opy_ (u"ࠧ࡯ࡤ࠾ࠤႬ"))[-1:][0].strip()
                    self.logger.debug(bstack1llll1l_opy_ (u"ࠨࡣ࡭࡫ࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧ࠾ࠧႭ") + str(self.cli_bin_session_id) + bstack1llll1l_opy_ (u"ࠢࠣႮ"))
                    continue
                if bstack1llll1l_opy_ (u"ࠣ࡮࡬ࡷࡹ࡫࡮࠾ࠤႯ") in line:
                    self.cli_listen_addr = line.split(bstack1llll1l_opy_ (u"ࠤ࡯࡭ࡸࡺࡥ࡯࠿ࠥႰ"))[-1:][0].strip()
                    self.logger.debug(bstack1llll1l_opy_ (u"ࠥࡧࡱ࡯࡟࡭࡫ࡶࡸࡪࡴ࡟ࡢࡦࡧࡶ࠿ࠨႱ") + str(self.cli_listen_addr) + bstack1llll1l_opy_ (u"ࠦࠧႲ"))
                    continue
                if bstack1llll1l_opy_ (u"ࠧࡶ࡯ࡳࡶࡀࠦႳ") in line:
                    port = line.split(bstack1llll1l_opy_ (u"ࠨࡰࡰࡴࡷࡁࠧႴ"))[-1:][0].strip()
                    self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡱࡱࡵࡸ࠿ࠨႵ") + str(port) + bstack1llll1l_opy_ (u"ࠣࠤႶ"))
                    continue
                if line.strip() == bstack1lll1lll1l1_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1llll1l_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡋࡒࡣࡘ࡚ࡒࡆࡃࡐࠦႷ"), bstack1llll1l_opy_ (u"ࠥ࠵ࠧႸ")) == bstack1llll1l_opy_ (u"ࠦ࠶ࠨႹ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1lllll1lll1_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1llll1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵ࠾ࠥࠨႺ") + str(e) + bstack1llll1l_opy_ (u"ࠨࠢႻ"))
        return False
    @measure(event_name=EVENTS.bstack1llll11lll1_opy_, stage=STAGE.bstack11111l1l1_opy_)
    def __1llll111lll_opy_(self):
        if self.bstack1lll1l1ll11_opy_:
            self.bstack1111l1111l_opy_.stop()
            start = datetime.now()
            if self.bstack1lll11l1lll_opy_():
                self.cli_bin_session_id = None
                if self.bstack1ll1lll11ll_opy_:
                    self.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠢࡴࡶࡲࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦႼ"), datetime.now() - start)
                else:
                    self.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠣࡵࡷࡳࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧႽ"), datetime.now() - start)
            self.__1lllll1l11l_opy_()
            start = datetime.now()
            self.bstack1lll1l1ll11_opy_.close()
            self.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠤࡧ࡭ࡸࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦႾ"), datetime.now() - start)
            self.bstack1lll1l1ll11_opy_ = None
        if self.process:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠥࡷࡹࡵࡰࠣႿ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠦࡰ࡯࡬࡭ࡡࡷ࡭ࡲ࡫ࠢჀ"), datetime.now() - start)
            self.process = None
            if self.bstack1lll1lll11l_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1l1lllll1_opy_()
                self.logger.info(
                    bstack1llll1l_opy_ (u"ࠧ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠣჁ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1llll1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬჂ")] = self.config_testhub.build_hashed_id
        self.bstack1lllll1lll1_opy_ = False
    def __1llll1l1ll1_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack1llll1l_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤჃ")] = selenium.__version__
            data.frameworks.append(bstack1llll1l_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥჄ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack1llll1l_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨჅ")] = __version__
            data.frameworks.append(bstack1llll1l_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ჆"))
        except:
            pass
    def bstack1llll1lll1l_opy_(self, hub_url: str, platform_index: int, bstack1lllllll1_opy_: Any):
        if self.bstack1lllllll111_opy_:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡵࡨࡸࠥࡻࡰࠣჇ"))
            return
        try:
            bstack1l11l1lll_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1llll1l_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢ჈")
            self.bstack1lllllll111_opy_ = bstack1lllll1ll1l_opy_(
                hub_url,
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1llll11l111_opy_={bstack1llll1l_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥ჉"): bstack1lllllll1_opy_}
            )
            def bstack1llll1l11l1_opy_(self):
                return
            if self.config.get(bstack1llll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠤ჊"), True):
                Service.start = bstack1llll1l11l1_opy_
                Service.stop = bstack1llll1l11l1_opy_
            def get_accessibility_results(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results(driver, framework_name=framework)
            def get_accessibility_results_summary(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results_summary(driver, framework_name=framework)
            def perform_scan(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.perform_scan(driver, method=None, framework_name=framework)
            WebDriver.getAccessibilityResults = get_accessibility_results
            WebDriver.get_accessibility_results = get_accessibility_results
            WebDriver.getAccessibilityResultsSummary = get_accessibility_results_summary
            WebDriver.get_accessibility_results_summary = get_accessibility_results_summary
            WebDriver.upload_attachment = staticmethod(bstack1lllll11l1_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1lll111llll_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤ჋"), datetime.now() - bstack1l11l1lll_opy_)
        except Exception as e:
            self.logger.error(bstack1llll1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࠣ჌") + str(e) + bstack1llll1l_opy_ (u"ࠥࠦჍ"))
    def bstack1lll1111111_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1lll111l_opy_
            self.bstack1lllllll111_opy_ = bstack1llll11llll_opy_(
                platform_index,
                framework_name=bstack1llll1l_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ჎"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack1llll1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠾ࠥࠨ჏") + str(e) + bstack1llll1l_opy_ (u"ࠨࠢა"))
            pass
    def bstack1lll111l11l_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠡࡵࡨࡸࡺࡶࠠࡱࡻࡷࡩࡸࡺ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡶࡩࡹࠦࡵࡱࠤბ"))
            return
        if bstack11l111l1_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1llll1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣგ"): pytest.__version__ }, [bstack1llll1l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨდ")], self.bstack1111l1111l_opy_, self.bstack1llll111l1l_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1llll1l1111_opy_({ bstack1llll1l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥე"): pytest.__version__ }, [bstack1llll1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦვ")], self.bstack1111l1111l_opy_, self.bstack1llll111l1l_opy_)
        except Exception as e:
            self.logger.error(bstack1llll1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡻࡷࡩࡸࡺ࠺ࠡࠤზ") + str(e) + bstack1llll1l_opy_ (u"ࠨࠢთ"))
        self.bstack1ll1lll111l_opy_()
    def bstack1ll1lll111l_opy_(self):
        if not self.bstack1l111ll11_opy_():
            return
        bstack11ll111l1l_opy_ = None
        def bstack11ll11ll_opy_(config, startdir):
            return bstack1llll1l_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧი").format(bstack1llll1l_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢკ"))
        def bstack1lllll111_opy_():
            return
        def bstack1ll111llll_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1llll1l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩლ"):
                return bstack1llll1l_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤმ")
            else:
                return bstack11ll111l1l_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack11ll111l1l_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11ll11ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1lllll111_opy_
            Config.getoption = bstack1ll111llll_opy_
        except Exception as e:
            self.logger.error(bstack1llll1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡷࡧ࡭ࠦࡰࡺࡶࡨࡷࡹࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡨࡲࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠾ࠥࠨნ") + str(e) + bstack1llll1l_opy_ (u"ࠧࠨო"))
    def bstack1ll1lllll1l_opy_(self):
        bstack1lll111l1l_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1lll111l1l_opy_, dict):
            if cli.config_observability:
                bstack1lll111l1l_opy_.update(
                    {bstack1llll1l_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨპ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1llll1l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࡡࡷࡳࡤࡽࡲࡢࡲࠥჟ") in accessibility.get(bstack1llll1l_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤრ"), {}):
                    bstack1llll11l1l1_opy_ = accessibility.get(bstack1llll1l_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥს"))
                    bstack1llll11l1l1_opy_.update({ bstack1llll1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠦტ"): bstack1llll11l1l1_opy_.pop(bstack1llll1l_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸࡥࡴࡰࡡࡺࡶࡦࡶࠢუ")) })
                bstack1lll111l1l_opy_.update({bstack1llll1l_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧფ"): accessibility })
        return bstack1lll111l1l_opy_
    @measure(event_name=EVENTS.bstack1lll1l111l1_opy_, stage=STAGE.bstack11111l1l1_opy_)
    def bstack1lll11l1lll_opy_(self, bstack1lll11l11l1_opy_: str = None, bstack1lll1l11l11_opy_: str = None, bstack1l1ll1llll_opy_: int = None):
        if not self.cli_bin_session_id or not self.bstack1llll111l1l_opy_:
            return
        bstack1l11l1lll_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if bstack1l1ll1llll_opy_:
            req.bstack1l1ll1llll_opy_ = bstack1l1ll1llll_opy_
        if bstack1lll11l11l1_opy_:
            req.bstack1lll11l11l1_opy_ = bstack1lll11l11l1_opy_
        if bstack1lll1l11l11_opy_:
            req.bstack1lll1l11l11_opy_ = bstack1lll1l11l11_opy_
        try:
            r = self.bstack1llll111l1l_opy_.StopBinSession(req)
            SDKCLI.bstack1lll1l11ll1_opy_ = r.bstack1lll1l11ll1_opy_
            SDKCLI.bstack1l1l11lll_opy_ = r.bstack1l1l11lll_opy_
            self.bstack1111lllll_opy_(bstack1llll1l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸࡺ࡯ࡱࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢქ"), datetime.now() - bstack1l11l1lll_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1111lllll_opy_(self, key: str, value: timedelta):
        tag = bstack1llll1l_opy_ (u"ࠢࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹࠢღ") if self.bstack11l111l1l_opy_() else bstack1llll1l_opy_ (u"ࠣ࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹࠢყ")
        self.bstack1lll1l11l1l_opy_[bstack1llll1l_opy_ (u"ࠤ࠽ࠦშ").join([tag + bstack1llll1l_opy_ (u"ࠥ࠱ࠧჩ") + str(id(self)), key])] += value
    def bstack1l1lllll1_opy_(self):
        if not os.getenv(bstack1llll1l_opy_ (u"ࠦࡉࡋࡂࡖࡉࡢࡔࡊࡘࡆࠣც"), bstack1llll1l_opy_ (u"ࠧ࠶ࠢძ")) == bstack1llll1l_opy_ (u"ࠨ࠱ࠣწ"):
            return
        bstack1lll1l1l111_opy_ = dict()
        bstack1llllllll1l_opy_ = []
        if self.test_framework:
            bstack1llllllll1l_opy_.extend(list(self.test_framework.bstack1llllllll1l_opy_.values()))
        if self.bstack1lllllll111_opy_:
            bstack1llllllll1l_opy_.extend(list(self.bstack1lllllll111_opy_.bstack1llllllll1l_opy_.values()))
        for instance in bstack1llllllll1l_opy_:
            if not instance.platform_index in bstack1lll1l1l111_opy_:
                bstack1lll1l1l111_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1lll1l1l111_opy_[instance.platform_index]
            for k, v in instance.bstack1lll1111l1l_opy_().items():
                report[k] += v
                report[k.split(bstack1llll1l_opy_ (u"ࠢ࠻ࠤჭ"))[0]] += v
        bstack1lll1lllll1_opy_ = sorted([(k, v) for k, v in self.bstack1lll1l11l1l_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1ll1lll1l1l_opy_ = 0
        for r in bstack1lll1lllll1_opy_:
            bstack1lll1l1l1ll_opy_ = r[1].total_seconds()
            bstack1ll1lll1l1l_opy_ += bstack1lll1l1l1ll_opy_
            self.logger.debug(bstack1llll1l_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡥ࡯࡭࠿ࢁࡲ࡜࠲ࡠࢁࡂࠨხ") + str(bstack1lll1l1l1ll_opy_) + bstack1llll1l_opy_ (u"ࠤࠥჯ"))
        self.logger.debug(bstack1llll1l_opy_ (u"ࠥ࠱࠲ࠨჰ"))
        bstack1ll1lll1111_opy_ = []
        for platform_index, report in bstack1lll1l1l111_opy_.items():
            bstack1ll1lll1111_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1ll1lll1111_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1l1l1l1l1l_opy_ = set()
        bstack1lll11l11ll_opy_ = 0
        for r in bstack1ll1lll1111_opy_:
            bstack1lll1l1l1ll_opy_ = r[2].total_seconds()
            bstack1lll11l11ll_opy_ += bstack1lll1l1l1ll_opy_
            bstack1l1l1l1l1l_opy_.add(r[0])
            self.logger.debug(bstack1llll1l_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡹ࡫ࡳࡵ࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࠱ࢀࡸ࡛࠱࡟ࢀ࠾ࢀࡸ࡛࠲࡟ࢀࡁࠧჱ") + str(bstack1lll1l1l1ll_opy_) + bstack1llll1l_opy_ (u"ࠧࠨჲ"))
        if self.bstack11l111l1l_opy_():
            self.logger.debug(bstack1llll1l_opy_ (u"ࠨ࠭࠮ࠤჳ"))
            self.logger.debug(bstack1llll1l_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡤ࡮࡬࠾ࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶࡁࢀࡺ࡯ࡵࡣ࡯ࡣࡨࡲࡩࡾࠢࡷࡩࡸࡺ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵ࠰ࡿࡸࡺࡲࠩࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ࠭ࢂࡃࠢჴ") + str(bstack1lll11l11ll_opy_) + bstack1llll1l_opy_ (u"ࠣࠤჵ"))
        else:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷࡂࠨჶ") + str(bstack1ll1lll1l1l_opy_) + bstack1llll1l_opy_ (u"ࠥࠦჷ"))
        self.logger.debug(bstack1llll1l_opy_ (u"ࠦ࠲࠳ࠢჸ"))
    def bstack1llll11ll1l_opy_(self, r):
        if r is not None and getattr(r, bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧ࠭ჹ"), None) and getattr(r.testhub, bstack1llll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ჺ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1llll1l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ჻")))
            for bstack1ll1llll11l_opy_, err in errors.items():
                if err[bstack1llll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ჼ")] == bstack1llll1l_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧჽ"):
                    self.logger.info(err[bstack1llll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫჾ")])
                else:
                    self.logger.error(err[bstack1llll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬჿ")])
    def bstack1ll1ll1l1_opy_(self):
        return SDKCLI.bstack1lll1l11ll1_opy_, SDKCLI.bstack1l1l11lll_opy_
cli = SDKCLI()