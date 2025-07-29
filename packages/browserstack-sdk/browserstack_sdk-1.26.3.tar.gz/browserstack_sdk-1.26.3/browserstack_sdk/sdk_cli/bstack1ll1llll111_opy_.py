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
import abc
from browserstack_sdk.sdk_cli.bstack1111l1111l_opy_ import bstack11111llll1_opy_
class bstack1lll1l1llll_opy_(abc.ABC):
    bin_session_id: str
    bstack1111l1111l_opy_: bstack11111llll1_opy_
    def __init__(self):
        self.bstack1llll111l1l_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111l1111l_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1lll1llll11_opy_(self):
        return (self.bstack1llll111l1l_opy_ != None and self.bin_session_id != None and self.bstack1111l1111l_opy_ != None)
    def configure(self, bstack1llll111l1l_opy_, config, bin_session_id: str, bstack1111l1111l_opy_: bstack11111llll1_opy_):
        self.bstack1llll111l1l_opy_ = bstack1llll111l1l_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111l1111l_opy_ = bstack1111l1111l_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1llll1l_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࡨࠥࡳ࡯ࡥࡷ࡯ࡩࠥࢁࡳࡦ࡮ࡩ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥ࠮ࡠࡡࡱࡥࡲ࡫࡟ࡠࡿ࠽ࠤࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨᇁ") + str(self.bin_session_id) + bstack1llll1l_opy_ (u"ࠥࠦᇂ"))
    def bstack1ll11llllll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1llll1l_opy_ (u"ࠦࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡩࡡ࡯ࡰࡲࡸࠥࡨࡥࠡࡐࡲࡲࡪࠨᇃ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False