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
import json
from bstack_utils.bstack1llll11l1l_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll1lll111_opy_(object):
  bstack1l1111l11_opy_ = os.path.join(os.path.expanduser(bstack1llll1l_opy_ (u"ࠧࡿࠩᛀ")), bstack1llll1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᛁ"))
  bstack11ll1lll1ll_opy_ = os.path.join(bstack1l1111l11_opy_, bstack1llll1l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶ࠲࡯ࡹ࡯࡯ࠩᛂ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1l1l1ll11l_opy_ = None
  bstack11l111ll_opy_ = None
  bstack11ll1lllll1_opy_ = None
  bstack11lll1l11l1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1llll1l_opy_ (u"ࠪ࡭ࡳࡹࡴࡢࡰࡦࡩࠬᛃ")):
      cls.instance = super(bstack11ll1lll111_opy_, cls).__new__(cls)
      cls.instance.bstack11ll1lll11l_opy_()
    return cls.instance
  def bstack11ll1lll11l_opy_(self):
    try:
      with open(self.bstack11ll1lll1ll_opy_, bstack1llll1l_opy_ (u"ࠫࡷ࠭ᛄ")) as bstack11l1ll11l1_opy_:
        bstack11ll1lll1l1_opy_ = bstack11l1ll11l1_opy_.read()
        data = json.loads(bstack11ll1lll1l1_opy_)
        if bstack1llll1l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᛅ") in data:
          self.bstack11llll1l11l_opy_(data[bstack1llll1l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᛆ")])
        if bstack1llll1l_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᛇ") in data:
          self.bstack1l111lll1l_opy_(data[bstack1llll1l_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᛈ")])
        if bstack1llll1l_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᛉ") in data:
          self.bstack11ll1llll11_opy_(data[bstack1llll1l_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᛊ")])
    except:
      pass
  def bstack11ll1llll11_opy_(self, bstack11lll1l11l1_opy_):
    if bstack11lll1l11l1_opy_ != None:
      self.bstack11lll1l11l1_opy_ = bstack11lll1l11l1_opy_
  def bstack1l111lll1l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1llll1l_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᛋ"),bstack1llll1l_opy_ (u"ࠬ࠭ᛌ"))
      self.bstack1l1l1ll11l_opy_ = scripts.get(bstack1llll1l_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᛍ"),bstack1llll1l_opy_ (u"ࠧࠨᛎ"))
      self.bstack11l111ll_opy_ = scripts.get(bstack1llll1l_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬᛏ"),bstack1llll1l_opy_ (u"ࠩࠪᛐ"))
      self.bstack11ll1lllll1_opy_ = scripts.get(bstack1llll1l_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨᛑ"),bstack1llll1l_opy_ (u"ࠫࠬᛒ"))
  def bstack11llll1l11l_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll1lll1ll_opy_, bstack1llll1l_opy_ (u"ࠬࡽࠧᛓ")) as file:
        json.dump({
          bstack1llll1l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣᛔ"): self.commands_to_wrap,
          bstack1llll1l_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣᛕ"): {
            bstack1llll1l_opy_ (u"ࠣࡵࡦࡥࡳࠨᛖ"): self.perform_scan,
            bstack1llll1l_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨᛗ"): self.bstack1l1l1ll11l_opy_,
            bstack1llll1l_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢᛘ"): self.bstack11l111ll_opy_,
            bstack1llll1l_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤᛙ"): self.bstack11ll1lllll1_opy_
          },
          bstack1llll1l_opy_ (u"ࠧࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠤᛚ"): self.bstack11lll1l11l1_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1llll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠺ࠡࡽࢀࠦᛛ").format(e))
      pass
  def bstack111lll11l_opy_(self, bstack1ll1l11l11l_opy_):
    try:
      return any(command.get(bstack1llll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᛜ")) == bstack1ll1l11l11l_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack1ll11l111l_opy_ = bstack11ll1lll111_opy_()