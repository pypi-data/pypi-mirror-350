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
import builtins
import logging
class bstack111lll11ll_opy_:
    def __init__(self, handler):
        self._11ll1l1l11l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11ll1l1l1l1_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1llll1l_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᛰ"), bstack1llll1l_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭ᛱ"), bstack1llll1l_opy_ (u"ࠨࡹࡤࡶࡳ࡯࡮ࡨࠩᛲ"), bstack1llll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᛳ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11ll1l1ll11_opy_
        self._11ll1l1ll1l_opy_()
    def _11ll1l1ll11_opy_(self, *args, **kwargs):
        self._11ll1l1l11l_opy_(*args, **kwargs)
        message = bstack1llll1l_opy_ (u"ࠪࠤࠬᛴ").join(map(str, args)) + bstack1llll1l_opy_ (u"ࠫࡡࡴࠧᛵ")
        self._log_message(bstack1llll1l_opy_ (u"ࠬࡏࡎࡇࡑࠪᛶ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1llll1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᛷ"): level, bstack1llll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᛸ"): msg})
    def _11ll1l1ll1l_opy_(self):
        for level, bstack11ll1l1lll1_opy_ in self._11ll1l1l1l1_opy_.items():
            setattr(logging, level, self._11ll1l1l1ll_opy_(level, bstack11ll1l1lll1_opy_))
    def _11ll1l1l1ll_opy_(self, level, bstack11ll1l1lll1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11ll1l1lll1_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11ll1l1l11l_opy_
        for level, bstack11ll1l1lll1_opy_ in self._11ll1l1l1l1_opy_.items():
            setattr(logging, level, bstack11ll1l1lll1_opy_)