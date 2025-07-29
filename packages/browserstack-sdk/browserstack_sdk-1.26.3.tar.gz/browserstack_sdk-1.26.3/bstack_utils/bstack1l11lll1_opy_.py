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
class bstack1ll111l11l_opy_:
    def __init__(self, handler):
        self._1111ll1ll1l_opy_ = None
        self.handler = handler
        self._1111ll1l1ll_opy_ = self.bstack1111ll1l1l1_opy_()
        self.patch()
    def patch(self):
        self._1111ll1ll1l_opy_ = self._1111ll1l1ll_opy_.execute
        self._1111ll1l1ll_opy_.execute = self.bstack1111ll1ll11_opy_()
    def bstack1111ll1ll11_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1llll1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢḾ"), driver_command, None, this, args)
            response = self._1111ll1ll1l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1llll1l_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢḿ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1111ll1l1ll_opy_.execute = self._1111ll1ll1l_opy_
    @staticmethod
    def bstack1111ll1l1l1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver