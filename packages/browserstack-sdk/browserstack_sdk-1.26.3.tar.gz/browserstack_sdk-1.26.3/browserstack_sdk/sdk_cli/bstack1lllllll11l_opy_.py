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
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack11111lll1l_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1llllll1lll_opy_:
    bstack1l111111ll1_opy_ = bstack1llll1l_opy_ (u"ࠨࡢࡦࡰࡦ࡬ࡲࡧࡲ࡬ࠤᕓ")
    context: bstack11111lll1l_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack11111lll1l_opy_):
        self.context = context
        self.data = dict({bstack1llllll1lll_opy_.bstack1l111111ll1_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1llll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᕔ"), bstack1llll1l_opy_ (u"ࠨ࠲ࠪᕕ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1llllllllll_opy_(self, target: object):
        return bstack1llllll1lll_opy_.create_context(target) == self.context
    def bstack1ll111ll1l1_opy_(self, context: bstack11111lll1l_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1111lllll_opy_(self, key: str, value: timedelta):
        self.data[bstack1llllll1lll_opy_.bstack1l111111ll1_opy_][key] += value
    def bstack1lll1111l1l_opy_(self) -> dict:
        return self.data[bstack1llllll1lll_opy_.bstack1l111111ll1_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack11111lll1l_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )