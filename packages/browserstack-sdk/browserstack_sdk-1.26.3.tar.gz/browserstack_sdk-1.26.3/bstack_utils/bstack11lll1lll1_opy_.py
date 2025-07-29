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
import logging
import datetime
import threading
from bstack_utils.helper import bstack11llll1111l_opy_, bstack1llllll111_opy_, get_host_info, bstack11l1llll111_opy_, \
 bstack1l111ll11_opy_, bstack11l11111_opy_, bstack111l1l1111_opy_, bstack11l11l1ll11_opy_, bstack1l1ll1l1l_opy_
import bstack_utils.accessibility as bstack11l1lll1_opy_
from bstack_utils.bstack11l11111l1_opy_ import bstack1l11l111ll_opy_
from bstack_utils.percy import bstack111111111_opy_
from bstack_utils.config import Config
bstack1lll1l111l_opy_ = Config.bstack11l11l11l1_opy_()
logger = logging.getLogger(__name__)
percy = bstack111111111_opy_()
@bstack111l1l1111_opy_(class_method=False)
def bstack1111l11111l_opy_(bs_config, bstack1ll1llll_opy_):
  try:
    data = {
        bstack1llll1l_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭ᾰ"): bstack1llll1l_opy_ (u"ࠧ࡫ࡵࡲࡲࠬᾱ"),
        bstack1llll1l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧᾲ"): bs_config.get(bstack1llll1l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᾳ"), bstack1llll1l_opy_ (u"ࠪࠫᾴ")),
        bstack1llll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᾵"): bs_config.get(bstack1llll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᾶ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1llll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᾷ"): bs_config.get(bstack1llll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᾸ")),
        bstack1llll1l_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭Ᾱ"): bs_config.get(bstack1llll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᾺ"), bstack1llll1l_opy_ (u"ࠪࠫΆ")),
        bstack1llll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᾼ"): bstack1l1ll1l1l_opy_(),
        bstack1llll1l_opy_ (u"ࠬࡺࡡࡨࡵࠪ᾽"): bstack11l1llll111_opy_(bs_config),
        bstack1llll1l_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩι"): get_host_info(),
        bstack1llll1l_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨ᾿"): bstack1llllll111_opy_(),
        bstack1llll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ῀"): os.environ.get(bstack1llll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ῁")),
        bstack1llll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨῂ"): os.environ.get(bstack1llll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩῃ"), False),
        bstack1llll1l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧῄ"): bstack11llll1111l_opy_(),
        bstack1llll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭῅"): bstack11111ll1ll1_opy_(bs_config),
        bstack1llll1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡨࡪࡺࡡࡪ࡮ࡶࠫῆ"): bstack11111ll1l11_opy_(bstack1ll1llll_opy_),
        bstack1llll1l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ῇ"): bstack11111l1ll11_opy_(bs_config, bstack1ll1llll_opy_.get(bstack1llll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪῈ"), bstack1llll1l_opy_ (u"ࠪࠫΈ"))),
        bstack1llll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ὴ"): bstack1l111ll11_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1llll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡥࡾࡲ࡯ࡢࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨΉ").format(str(error)))
    return None
def bstack11111ll1l11_opy_(framework):
  return {
    bstack1llll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ῌ"): framework.get(bstack1llll1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨ῍"), bstack1llll1l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ῎")),
    bstack1llll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ῏"): framework.get(bstack1llll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧῐ")),
    bstack1llll1l_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨῑ"): framework.get(bstack1llll1l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪῒ")),
    bstack1llll1l_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨΐ"): bstack1llll1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ῔"),
    bstack1llll1l_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ῕"): framework.get(bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩῖ"))
  }
def bstack1l1ll1l1l1_opy_(bs_config, framework):
  bstack1llllll1l_opy_ = False
  bstack1llll11l1_opy_ = False
  bstack11111lll111_opy_ = False
  if bstack1llll1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧῗ") in bs_config:
    bstack11111lll111_opy_ = True
  elif bstack1llll1l_opy_ (u"ࠫࡦࡶࡰࠨῘ") in bs_config:
    bstack1llllll1l_opy_ = True
  else:
    bstack1llll11l1_opy_ = True
  bstack11l1l1llll_opy_ = {
    bstack1llll1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬῙ"): bstack1l11l111ll_opy_.bstack11111ll11ll_opy_(bs_config, framework),
    bstack1llll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ὶ"): bstack11l1lll1_opy_.bstack1lllll1111_opy_(bs_config),
    bstack1llll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭Ί"): bs_config.get(bstack1llll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ῜"), False),
    bstack1llll1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ῝"): bstack1llll11l1_opy_,
    bstack1llll1l_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ῞"): bstack1llllll1l_opy_,
    bstack1llll1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ῟"): bstack11111lll111_opy_
  }
  return bstack11l1l1llll_opy_
@bstack111l1l1111_opy_(class_method=False)
def bstack11111ll1ll1_opy_(bs_config):
  try:
    bstack11111l1lll1_opy_ = json.loads(os.getenv(bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ῠ"), bstack1llll1l_opy_ (u"࠭ࡻࡾࠩῡ")))
    bstack11111l1lll1_opy_ = bstack11111ll1lll_opy_(bs_config, bstack11111l1lll1_opy_)
    return {
        bstack1llll1l_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩῢ"): bstack11111l1lll1_opy_
    }
  except Exception as error:
    logger.error(bstack1llll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢΰ").format(str(error)))
    return {}
def bstack11111ll1lll_opy_(bs_config, bstack11111l1lll1_opy_):
  if ((bstack1llll1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ῤ") in bs_config or not bstack1l111ll11_opy_(bs_config)) and bstack11l1lll1_opy_.bstack1lllll1111_opy_(bs_config)):
    bstack11111l1lll1_opy_[bstack1llll1l_opy_ (u"ࠥ࡭ࡳࡩ࡬ࡶࡦࡨࡉࡳࡩ࡯ࡥࡧࡧࡉࡽࡺࡥ࡯ࡵ࡬ࡳࡳࠨῥ")] = True
  return bstack11111l1lll1_opy_
def bstack11111llllll_opy_(array, bstack11111l1llll_opy_, bstack11111ll11l1_opy_):
  result = {}
  for o in array:
    key = o[bstack11111l1llll_opy_]
    result[key] = o[bstack11111ll11l1_opy_]
  return result
def bstack11111lll1ll_opy_(bstack111lll1l_opy_=bstack1llll1l_opy_ (u"ࠫࠬῦ")):
  bstack11111ll1111_opy_ = bstack11l1lll1_opy_.on()
  bstack11111l1ll1l_opy_ = bstack1l11l111ll_opy_.on()
  bstack11111ll1l1l_opy_ = percy.bstack1lllllll1l_opy_()
  if bstack11111ll1l1l_opy_ and not bstack11111l1ll1l_opy_ and not bstack11111ll1111_opy_:
    return bstack111lll1l_opy_ not in [bstack1llll1l_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩῧ"), bstack1llll1l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪῨ")]
  elif bstack11111ll1111_opy_ and not bstack11111l1ll1l_opy_:
    return bstack111lll1l_opy_ not in [bstack1llll1l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨῩ"), bstack1llll1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪῪ"), bstack1llll1l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭Ύ")]
  return bstack11111ll1111_opy_ or bstack11111l1ll1l_opy_ or bstack11111ll1l1l_opy_
@bstack111l1l1111_opy_(class_method=False)
def bstack1111l11l111_opy_(bstack111lll1l_opy_, test=None):
  bstack11111ll111l_opy_ = bstack11l1lll1_opy_.on()
  if not bstack11111ll111l_opy_ or bstack111lll1l_opy_ not in [bstack1llll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬῬ")] or test == None:
    return None
  return {
    bstack1llll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ῭"): bstack11111ll111l_opy_ and bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ΅"), None) == True and bstack11l1lll1_opy_.bstack1ll1l11l1l_opy_(test[bstack1llll1l_opy_ (u"࠭ࡴࡢࡩࡶࠫ`")])
  }
def bstack11111l1ll11_opy_(bs_config, framework):
  bstack1llllll1l_opy_ = False
  bstack1llll11l1_opy_ = False
  bstack11111lll111_opy_ = False
  if bstack1llll1l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ῰") in bs_config:
    bstack11111lll111_opy_ = True
  elif bstack1llll1l_opy_ (u"ࠨࡣࡳࡴࠬ῱") in bs_config:
    bstack1llllll1l_opy_ = True
  else:
    bstack1llll11l1_opy_ = True
  bstack11l1l1llll_opy_ = {
    bstack1llll1l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩῲ"): bstack1l11l111ll_opy_.bstack11111ll11ll_opy_(bs_config, framework),
    bstack1llll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪῳ"): bstack11l1lll1_opy_.bstack111l1lll1_opy_(bs_config),
    bstack1llll1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪῴ"): bs_config.get(bstack1llll1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ῵"), False),
    bstack1llll1l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨῶ"): bstack1llll11l1_opy_,
    bstack1llll1l_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ῷ"): bstack1llllll1l_opy_,
    bstack1llll1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬῸ"): bstack11111lll111_opy_
  }
  return bstack11l1l1llll_opy_