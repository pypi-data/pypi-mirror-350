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
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack1l1l111ll_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack11l1lll11_opy_:
    pass
class bstack1ll111111_opy_:
    bstack1l1l111l1l_opy_ = bstack1llll1l_opy_ (u"ࠧࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠣᄀ")
    CONNECT = bstack1llll1l_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺࠢᄁ")
    bstack1lll11l111_opy_ = bstack1llll1l_opy_ (u"ࠢࡴࡪࡸࡸࡩࡵࡷ࡯ࠤᄂ")
    CONFIG = bstack1llll1l_opy_ (u"ࠣࡥࡲࡲ࡫࡯ࡧࠣᄃ")
    bstack1ll1ll11lll_opy_ = bstack1llll1l_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡸࠨᄄ")
    bstack1l1l1llll_opy_ = bstack1llll1l_opy_ (u"ࠥࡩࡽ࡯ࡴࠣᄅ")
class bstack1ll1ll1l111_opy_:
    bstack1ll1ll11ll1_opy_ = bstack1llll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡷࡹࡧࡲࡵࡧࡧࠦᄆ")
    FINISHED = bstack1llll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᄇ")
class bstack1ll1ll1l1l1_opy_:
    bstack1ll1ll11ll1_opy_ = bstack1llll1l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡵࡷࡥࡷࡺࡥࡥࠤᄈ")
    FINISHED = bstack1llll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᄉ")
class bstack1ll1ll1ll11_opy_:
    bstack1ll1ll11ll1_opy_ = bstack1llll1l_opy_ (u"ࠣࡪࡲࡳࡰࡥࡲࡶࡰࡢࡷࡹࡧࡲࡵࡧࡧࠦᄊ")
    FINISHED = bstack1llll1l_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᄋ")
class bstack1ll1ll11l1l_opy_:
    bstack1ll1ll1l1ll_opy_ = bstack1llll1l_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡥࡵࡩࡦࡺࡥࡥࠤᄌ")
class bstack1ll1ll1l11l_opy_:
    _1ll1lllllll_opy_ = None
    def __new__(cls):
        if not cls._1ll1lllllll_opy_:
            cls._1ll1lllllll_opy_ = super(bstack1ll1ll1l11l_opy_, cls).__new__(cls)
        return cls._1ll1lllllll_opy_
    def __init__(self):
        self._hooks = defaultdict(lambda: defaultdict(list))
        self._lock = Lock()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def clear(self):
        with self._lock:
            self._hooks = defaultdict(list)
    def register(self, event_name, callback):
        with self._lock:
            if not callable(callback):
                raise ValueError(bstack1llll1l_opy_ (u"ࠦࡈࡧ࡬࡭ࡤࡤࡧࡰࠦ࡭ࡶࡵࡷࠤࡧ࡫ࠠࡤࡣ࡯ࡰࡦࡨ࡬ࡦࠢࡩࡳࡷࠦࠢᄍ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack1llll1l_opy_ (u"ࠧࡘࡥࡨ࡫ࡶࡸࡪࡸࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠨࠢࡺ࡭ࡹ࡮ࠠࡱ࡫ࡧࠤࠧᄎ") + str(pid) + bstack1llll1l_opy_ (u"ࠨࠢᄏ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack1llll1l_opy_ (u"ࠢࡏࡱࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࡸࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࠢࠪࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠩࠣࡻ࡮ࡺࡨࠡࡲ࡬ࡨࠥࠨᄐ") + str(pid) + bstack1llll1l_opy_ (u"ࠣࠤᄑ"))
                return
            self.logger.debug(bstack1llll1l_opy_ (u"ࠤࡌࡲࡻࡵ࡫ࡪࡰࡪࠤࢀࡲࡥ࡯ࠪࡦࡥࡱࡲࡢࡢࡥ࡮ࡷ࠮ࢃࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࠦࠧࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂ࠭ࠠࡸ࡫ࡷ࡬ࠥࡶࡩࡥࠢࠥᄒ") + str(pid) + bstack1llll1l_opy_ (u"ࠥࠦᄓ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack1llll1l_opy_ (u"ࠦࡎࡴࡶࡰ࡭ࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࠣࠫࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠪࠤࡼ࡯ࡴࡩࠢࡳ࡭ࡩࠦࠢᄔ") + str(pid) + bstack1llll1l_opy_ (u"ࠧࠨᄕ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack1llll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࡷࡪࡶ࡫ࠤࡵ࡯ࡤࠡࡽࡳ࡭ࡩࢃ࠺ࠡࠤᄖ") + str(e) + bstack1llll1l_opy_ (u"ࠢࠣᄗ"))
                    traceback.print_exc()
bstack1ll1ll1ll_opy_ = bstack1ll1ll1l11l_opy_()