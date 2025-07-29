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
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111l1111l_opy_ import bstack11111llll1_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll11l_opy_ import bstack1llllll1lll_opy_, bstack11111lll1l_opy_
class bstack1llll1l1lll_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1llll1l_opy_ (u"ࠤࡗࡩࡸࡺࡈࡰࡱ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧᔥ").format(self.name)
class bstack1ll1llll1ll_opy_(Enum):
    NONE = 0
    BEFORE_ALL = 1
    LOG = 2
    SETUP_FIXTURE = 3
    INIT_TEST = 4
    BEFORE_EACH = 5
    AFTER_EACH = 6
    TEST = 7
    STEP = 8
    LOG_REPORT = 9
    AFTER_ALL = 10
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack1llll1l_opy_ (u"ࠥࡘࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦᔦ").format(self.name)
class bstack1llll111111_opy_(bstack1llllll1lll_opy_):
    bstack1ll11lll11l_opy_: List[str]
    bstack1l111l1l111_opy_: Dict[str, str]
    state: bstack1ll1llll1ll_opy_
    bstack1llllll1ll1_opy_: datetime
    bstack1lllllll1l1_opy_: datetime
    def __init__(
        self,
        context: bstack11111lll1l_opy_,
        bstack1ll11lll11l_opy_: List[str],
        bstack1l111l1l111_opy_: Dict[str, str],
        state=bstack1ll1llll1ll_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll11lll11l_opy_ = bstack1ll11lll11l_opy_
        self.bstack1l111l1l111_opy_ = bstack1l111l1l111_opy_
        self.state = state
        self.bstack1llllll1ll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lllllll1l1_opy_ = datetime.now(tz=timezone.utc)
    def bstack111111111l_opy_(self, bstack1lllllll1ll_opy_: bstack1ll1llll1ll_opy_):
        bstack11111111l1_opy_ = bstack1ll1llll1ll_opy_(bstack1lllllll1ll_opy_).name
        if not bstack11111111l1_opy_:
            return False
        if bstack1lllllll1ll_opy_ == self.state:
            return False
        self.state = bstack1lllllll1ll_opy_
        self.bstack1lllllll1l1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l111l11l1l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll1lll1lll_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1llll1l11_opy_: int = None
    bstack1l1llll1ll1_opy_: str = None
    bstack11ll11l_opy_: str = None
    bstack11l1l111_opy_: str = None
    bstack1ll11111111_opy_: str = None
    bstack1l1111ll11l_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll11lll1ll_opy_ = bstack1llll1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠢᔧ")
    bstack1l111l1111l_opy_ = bstack1llll1l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡭ࡩࠨᔨ")
    bstack1ll1l11lll1_opy_ = bstack1llll1l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠤᔩ")
    bstack1l111l1llll_opy_ = bstack1llll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡢࡴࡦࡺࡨࠣᔪ")
    bstack1l1111ll1ll_opy_ = bstack1llll1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡴࡢࡩࡶࠦᔫ")
    bstack1l1l1l1ll1l_opy_ = bstack1llll1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᔬ")
    bstack1l1lll11l1l_opy_ = bstack1llll1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡨࡷࡺࡲࡴࡠࡣࡷࠦᔭ")
    bstack1l1ll11llll_opy_ = bstack1llll1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᔮ")
    bstack1l1lll1111l_opy_ = bstack1llll1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡩࡳࡪࡥࡥࡡࡤࡸࠧᔯ")
    bstack1l11l111l1l_opy_ = bstack1llll1l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᔰ")
    bstack1ll1ll1111l_opy_ = bstack1llll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࠨᔱ")
    bstack1l1llll1l1l_opy_ = bstack1llll1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠥᔲ")
    bstack1l11l1ll11l_opy_ = bstack1llll1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡤࡱࡧࡩࠧᔳ")
    bstack1l1ll11lll1_opy_ = bstack1llll1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠧᔴ")
    bstack1ll11l1ll11_opy_ = bstack1llll1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࠧᔵ")
    bstack1l1l1l11111_opy_ = bstack1llll1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡦ࡯࡬ࡶࡴࡨࠦᔶ")
    bstack1l111l111ll_opy_ = bstack1llll1l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠥᔷ")
    bstack1l11ll11l1l_opy_ = bstack1llll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡲ࡯ࡨࡵࠥᔸ")
    bstack1l111l1lll1_opy_ = bstack1llll1l_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡭ࡦࡶࡤࠦᔹ")
    bstack1l1111l1lll_opy_ = bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡴࡥࡲࡴࡪࡹࠧᔺ")
    bstack1l11lll1lll_opy_ = bstack1llll1l_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦᔻ")
    bstack1l111lll111_opy_ = bstack1llll1l_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᔼ")
    bstack1l111l11111_opy_ = bstack1llll1l_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡪࡴࡤࡦࡦࡢࡥࡹࠨᔽ")
    bstack1l11l1l1l11_opy_ = bstack1llll1l_opy_ (u"ࠨࡨࡰࡱ࡮ࡣ࡮ࡪࠢᔾ")
    bstack1l11ll11l11_opy_ = bstack1llll1l_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡸࡥࡴࡷ࡯ࡸࠧᔿ")
    bstack1l111l11lll_opy_ = bstack1llll1l_opy_ (u"ࠣࡪࡲࡳࡰࡥ࡬ࡰࡩࡶࠦᕀ")
    bstack1l111llll1l_opy_ = bstack1llll1l_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠧᕁ")
    bstack1l111llllll_opy_ = bstack1llll1l_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᕂ")
    bstack1l11ll111l1_opy_ = bstack1llll1l_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᕃ")
    bstack1l1111lll1l_opy_ = bstack1llll1l_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨᕄ")
    bstack1l11l11ll1l_opy_ = bstack1llll1l_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢᕅ")
    bstack1ll11111l1l_opy_ = bstack1llll1l_opy_ (u"ࠢࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠤᕆ")
    bstack1l1lll1l1ll_opy_ = bstack1llll1l_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡌࡐࡉࠥᕇ")
    bstack1l1llll1lll_opy_ = bstack1llll1l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᕈ")
    bstack1llllllll1l_opy_: Dict[str, bstack1llll111111_opy_] = dict()
    bstack1l11111l1l1_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll11lll11l_opy_: List[str]
    bstack1l111l1l111_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll11lll11l_opy_: List[str],
        bstack1l111l1l111_opy_: Dict[str, str],
        bstack1111l1111l_opy_: bstack11111llll1_opy_
    ):
        self.bstack1ll11lll11l_opy_ = bstack1ll11lll11l_opy_
        self.bstack1l111l1l111_opy_ = bstack1l111l1l111_opy_
        self.bstack1111l1111l_opy_ = bstack1111l1111l_opy_
    def track_event(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1ll1llll1ll_opy_,
        test_hook_state: bstack1llll1l1lll_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1llll1l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡥࡷ࡭ࡳ࠾ࡽࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࢃࠢᕉ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l11l1111l1_opy_(
        self,
        instance: bstack1llll111111_opy_,
        bstack11111l1lll_opy_: Tuple[bstack1ll1llll1ll_opy_, bstack1llll1l1lll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11lll11ll_opy_ = TestFramework.bstack1l11ll1ll1l_opy_(bstack11111l1lll_opy_)
        if not bstack1l11lll11ll_opy_ in TestFramework.bstack1l11111l1l1_opy_:
            return
        self.logger.debug(bstack1llll1l_opy_ (u"ࠦ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡻࡾࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࡷࠧᕊ").format(len(TestFramework.bstack1l11111l1l1_opy_[bstack1l11lll11ll_opy_])))
        for callback in TestFramework.bstack1l11111l1l1_opy_[bstack1l11lll11ll_opy_]:
            try:
                callback(self, instance, bstack11111l1lll_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1llll1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠧᕋ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1llllll11_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1lll1llll_opy_(self, instance, bstack11111l1lll_opy_):
        return
    @abc.abstractmethod
    def bstack1ll1111l111_opy_(self, instance, bstack11111l1lll_opy_):
        return
    @staticmethod
    def bstack111111l11l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1llllll1lll_opy_.create_context(target)
        instance = TestFramework.bstack1llllllll1l_opy_.get(ctx.id, None)
        if instance and instance.bstack1llllllllll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1ll1ll11l_opy_(reverse=True) -> List[bstack1llll111111_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1llllllll1l_opy_.values(),
            ),
            key=lambda t: t.bstack1llllll1ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llllll11l1_opy_(ctx: bstack11111lll1l_opy_, reverse=True) -> List[bstack1llll111111_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1llllllll1l_opy_.values(),
            ),
            key=lambda t: t.bstack1llllll1ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack111111ll1l_opy_(instance: bstack1llll111111_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lllllllll1_opy_(instance: bstack1llll111111_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack111111111l_opy_(instance: bstack1llll111111_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1llll1l_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥᕌ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l11111l_opy_(instance: bstack1llll111111_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1llll1l_opy_ (u"ࠢࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡳࡺࡲࡪࡧࡶࡁࢀࢃࠢᕍ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l111111lll_opy_(instance: bstack1ll1llll1ll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1llll1l_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡫ࡦࡻࡀࡿࢂࠦࡶࡢ࡮ࡸࡩࡂࢁࡽࠣᕎ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack111111l11l_opy_(target, strict)
        return TestFramework.bstack1lllllllll1_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack111111l11l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l111l1ll1l_opy_(instance: bstack1llll111111_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l11l1l111l_opy_(instance: bstack1llll111111_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11ll1ll1l_opy_(bstack11111l1lll_opy_: Tuple[bstack1ll1llll1ll_opy_, bstack1llll1l1lll_opy_]):
        return bstack1llll1l_opy_ (u"ࠤ࠽ࠦᕏ").join((bstack1ll1llll1ll_opy_(bstack11111l1lll_opy_[0]).name, bstack1llll1l1lll_opy_(bstack11111l1lll_opy_[1]).name))
    @staticmethod
    def bstack1ll1l1l1l1l_opy_(bstack11111l1lll_opy_: Tuple[bstack1ll1llll1ll_opy_, bstack1llll1l1lll_opy_], callback: Callable):
        bstack1l11lll11ll_opy_ = TestFramework.bstack1l11ll1ll1l_opy_(bstack11111l1lll_opy_)
        TestFramework.logger.debug(bstack1llll1l_opy_ (u"ࠥࡷࡪࡺ࡟ࡩࡱࡲ࡯ࡤࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡪࡲࡳࡰࡥࡲࡦࡩ࡬ࡷࡹࡸࡹࡠ࡭ࡨࡽࡂࢁࡽࠣᕐ").format(bstack1l11lll11ll_opy_))
        if not bstack1l11lll11ll_opy_ in TestFramework.bstack1l11111l1l1_opy_:
            TestFramework.bstack1l11111l1l1_opy_[bstack1l11lll11ll_opy_] = []
        TestFramework.bstack1l11111l1l1_opy_[bstack1l11lll11ll_opy_].append(callback)
    @staticmethod
    def bstack1l1ll1lll1l_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1llll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡶ࡬ࡲࡸࠨᕑ"):
            return klass.__qualname__
        return module + bstack1llll1l_opy_ (u"ࠧ࠴ࠢᕒ") + klass.__qualname__
    @staticmethod
    def bstack1l1lll1l11l_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}