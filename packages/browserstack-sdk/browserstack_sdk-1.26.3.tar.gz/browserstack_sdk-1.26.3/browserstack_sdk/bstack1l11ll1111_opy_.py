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
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11lll11l1l_opy_():
  def __init__(self, args, logger, bstack1111l1ll1l_opy_, bstack1111ll111l_opy_, bstack1111l1l111_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111l1ll1l_opy_ = bstack1111l1ll1l_opy_
    self.bstack1111ll111l_opy_ = bstack1111ll111l_opy_
    self.bstack1111l1l111_opy_ = bstack1111l1l111_opy_
  def bstack11llll1ll1_opy_(self, bstack1111lll111_opy_, bstack11l1ll11l_opy_, bstack1111l1l11l_opy_=False):
    bstack1ll11ll11_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111l1lll1_opy_ = manager.list()
    bstack1lll1l111l_opy_ = Config.bstack11l11l11l1_opy_()
    if bstack1111l1l11l_opy_:
      for index, platform in enumerate(self.bstack1111l1ll1l_opy_[bstack1llll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬဤ")]):
        if index == 0:
          bstack11l1ll11l_opy_[bstack1llll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ဥ")] = self.args
        bstack1ll11ll11_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111lll111_opy_,
                                                    args=(bstack11l1ll11l_opy_, bstack1111l1lll1_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111l1ll1l_opy_[bstack1llll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧဦ")]):
        bstack1ll11ll11_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111lll111_opy_,
                                                    args=(bstack11l1ll11l_opy_, bstack1111l1lll1_opy_)))
    i = 0
    for t in bstack1ll11ll11_opy_:
      try:
        if bstack1lll1l111l_opy_.get_property(bstack1llll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ဧ")):
          os.environ[bstack1llll1l_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧဨ")] = json.dumps(self.bstack1111l1ll1l_opy_[bstack1llll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪဩ")][i % self.bstack1111l1l111_opy_])
      except Exception as e:
        self.logger.debug(bstack1llll1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶ࠾ࠥࢁࡽࠣဪ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1ll11ll11_opy_:
      t.join()
    return list(bstack1111l1lll1_opy_)