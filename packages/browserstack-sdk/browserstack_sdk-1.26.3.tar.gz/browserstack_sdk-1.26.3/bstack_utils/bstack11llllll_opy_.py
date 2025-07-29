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
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll1ll1l11_opy_ import bstack11ll1ll11l1_opy_
from bstack_utils.constants import *
import json
class bstack1l1llll11l_opy_:
    def __init__(self, bstack11l1l111_opy_, bstack11ll1ll1l1l_opy_):
        self.bstack11l1l111_opy_ = bstack11l1l111_opy_
        self.bstack11ll1ll1l1l_opy_ = bstack11ll1ll1l1l_opy_
        self.bstack11ll1ll11ll_opy_ = None
    def __call__(self):
        bstack11ll1ll111l_opy_ = {}
        while True:
            self.bstack11ll1ll11ll_opy_ = bstack11ll1ll111l_opy_.get(
                bstack1llll1l_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩᛝ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll1ll1111_opy_ = self.bstack11ll1ll11ll_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll1ll1111_opy_ > 0:
                sleep(bstack11ll1ll1111_opy_ / 1000)
            params = {
                bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᛞ"): self.bstack11l1l111_opy_,
                bstack1llll1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᛟ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11ll1ll1lll_opy_ = bstack1llll1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᛠ") + bstack11ll1ll1ll1_opy_ + bstack1llll1l_opy_ (u"ࠧ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࠤᛡ")
            if self.bstack11ll1ll1l1l_opy_.lower() == bstack1llll1l_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࡹࠢᛢ"):
                bstack11ll1ll111l_opy_ = bstack11ll1ll11l1_opy_.results(bstack11ll1ll1lll_opy_, params)
            else:
                bstack11ll1ll111l_opy_ = bstack11ll1ll11l1_opy_.bstack11ll1l1llll_opy_(bstack11ll1ll1lll_opy_, params)
            if str(bstack11ll1ll111l_opy_.get(bstack1llll1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᛣ"), bstack1llll1l_opy_ (u"ࠨ࠴࠳࠴ࠬᛤ"))) != bstack1llll1l_opy_ (u"ࠩ࠷࠴࠹࠭ᛥ"):
                break
        return bstack11ll1ll111l_opy_.get(bstack1llll1l_opy_ (u"ࠪࡨࡦࡺࡡࠨᛦ"), bstack11ll1ll111l_opy_)