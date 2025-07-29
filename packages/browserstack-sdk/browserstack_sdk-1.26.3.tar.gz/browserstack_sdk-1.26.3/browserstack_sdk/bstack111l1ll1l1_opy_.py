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
class RobotHandler():
    def __init__(self, args, logger, bstack1111l1ll1l_opy_, bstack1111ll111l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111l1ll1l_opy_ = bstack1111l1ll1l_opy_
        self.bstack1111ll111l_opy_ = bstack1111ll111l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l1ll1ll_opy_(bstack1111l11lll_opy_):
        bstack1111l11l1l_opy_ = []
        if bstack1111l11lll_opy_:
            tokens = str(os.path.basename(bstack1111l11lll_opy_)).split(bstack1llll1l_opy_ (u"ࠤࡢࠦါ"))
            camelcase_name = bstack1llll1l_opy_ (u"ࠥࠤࠧာ").join(t.title() for t in tokens)
            suite_name, bstack1111l11ll1_opy_ = os.path.splitext(camelcase_name)
            bstack1111l11l1l_opy_.append(suite_name)
        return bstack1111l11l1l_opy_
    @staticmethod
    def bstack1111l11l11_opy_(typename):
        if bstack1llll1l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢိ") in typename:
            return bstack1llll1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨီ")
        return bstack1llll1l_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢု")