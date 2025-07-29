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
import requests
import logging
import threading
import bstack_utils.constants as bstack11lll111l1l_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11lll1l1l11_opy_ as bstack11lll1111l1_opy_, EVENTS
from bstack_utils.bstack1ll11l111l_opy_ import bstack1ll11l111l_opy_
from bstack_utils.helper import bstack1l1ll1l1l_opy_, bstack111ll11ll1_opy_, bstack1l111ll11_opy_, bstack11lll11lll1_opy_, \
  bstack11lll1llll1_opy_, bstack1llllll111_opy_, get_host_info, bstack11llll1111l_opy_, bstack11lll1l1l1_opy_, bstack111l1l1111_opy_, bstack11lll1l111l_opy_, bstack11lll111111_opy_, bstack11l11111_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1llll11l1l_opy_ import get_logger
from bstack_utils.bstack1l1lll111l_opy_ import bstack1lllll11ll1_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1l1lll111l_opy_ = bstack1lllll11ll1_opy_()
@bstack111l1l1111_opy_(class_method=False)
def _11llll11111_opy_(driver, bstack1111llll11_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1llll1l_opy_ (u"ࠬࡵࡳࡠࡰࡤࡱࡪ࠭ᖊ"): caps.get(bstack1llll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᖋ"), None),
        bstack1llll1l_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫᖌ"): bstack1111llll11_opy_.get(bstack1llll1l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᖍ"), None),
        bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨᖎ"): caps.get(bstack1llll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᖏ"), None),
        bstack1llll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᖐ"): caps.get(bstack1llll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᖑ"), None)
    }
  except Exception as error:
    logger.debug(bstack1llll1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪᖒ") + str(error))
  return response
def on():
    if os.environ.get(bstack1llll1l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᖓ"), None) is None or os.environ[bstack1llll1l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᖔ")] == bstack1llll1l_opy_ (u"ࠤࡱࡹࡱࡲࠢᖕ"):
        return False
    return True
def bstack1lllll1111_opy_(config):
  return config.get(bstack1llll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᖖ"), False) or any([p.get(bstack1llll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᖗ"), False) == True for p in config.get(bstack1llll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᖘ"), [])])
def bstack1ll1111ll_opy_(config, bstack1l111l11l1_opy_):
  try:
    bstack11llll11l11_opy_ = config.get(bstack1llll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᖙ"), False)
    if int(bstack1l111l11l1_opy_) < len(config.get(bstack1llll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᖚ"), [])) and config[bstack1llll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᖛ")][bstack1l111l11l1_opy_]:
      bstack11ll1llll1l_opy_ = config[bstack1llll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᖜ")][bstack1l111l11l1_opy_].get(bstack1llll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᖝ"), None)
    else:
      bstack11ll1llll1l_opy_ = config.get(bstack1llll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᖞ"), None)
    if bstack11ll1llll1l_opy_ != None:
      bstack11llll11l11_opy_ = bstack11ll1llll1l_opy_
    bstack11lll11llll_opy_ = os.getenv(bstack1llll1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᖟ")) is not None and len(os.getenv(bstack1llll1l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᖠ"))) > 0 and os.getenv(bstack1llll1l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᖡ")) != bstack1llll1l_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᖢ")
    return bstack11llll11l11_opy_ and bstack11lll11llll_opy_
  except Exception as error:
    logger.debug(bstack1llll1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡨࡶ࡮࡬ࡹࡪࡰࡪࠤࡹ࡮ࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩᖣ") + str(error))
  return False
def bstack1ll1l11l1l_opy_(test_tags):
  bstack1ll1l1ll11l_opy_ = os.getenv(bstack1llll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᖤ"))
  if bstack1ll1l1ll11l_opy_ is None:
    return True
  bstack1ll1l1ll11l_opy_ = json.loads(bstack1ll1l1ll11l_opy_)
  try:
    include_tags = bstack1ll1l1ll11l_opy_[bstack1llll1l_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᖥ")] if bstack1llll1l_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᖦ") in bstack1ll1l1ll11l_opy_ and isinstance(bstack1ll1l1ll11l_opy_[bstack1llll1l_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᖧ")], list) else []
    exclude_tags = bstack1ll1l1ll11l_opy_[bstack1llll1l_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᖨ")] if bstack1llll1l_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᖩ") in bstack1ll1l1ll11l_opy_ and isinstance(bstack1ll1l1ll11l_opy_[bstack1llll1l_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᖪ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1llll1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥᖫ") + str(error))
  return False
def bstack11llll1l111_opy_(config, bstack11lll1ll1l1_opy_, bstack11lll11ll11_opy_, bstack11ll1llllll_opy_):
  bstack11llll11lll_opy_ = bstack11lll11lll1_opy_(config)
  bstack11lll1111ll_opy_ = bstack11lll1llll1_opy_(config)
  if bstack11llll11lll_opy_ is None or bstack11lll1111ll_opy_ is None:
    logger.error(bstack1llll1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬᖬ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᖭ"), bstack1llll1l_opy_ (u"࠭ࡻࡾࠩᖮ")))
    data = {
        bstack1llll1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᖯ"): config[bstack1llll1l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᖰ")],
        bstack1llll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᖱ"): config.get(bstack1llll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᖲ"), os.path.basename(os.getcwd())),
        bstack1llll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡗ࡭ࡲ࡫ࠧᖳ"): bstack1l1ll1l1l_opy_(),
        bstack1llll1l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᖴ"): config.get(bstack1llll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᖵ"), bstack1llll1l_opy_ (u"ࠧࠨᖶ")),
        bstack1llll1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨᖷ"): {
            bstack1llll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩᖸ"): bstack11lll1ll1l1_opy_,
            bstack1llll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᖹ"): bstack11lll11ll11_opy_,
            bstack1llll1l_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᖺ"): __version__,
            bstack1llll1l_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧᖻ"): bstack1llll1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᖼ"),
            bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᖽ"): bstack1llll1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪᖾ"),
            bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᖿ"): bstack11ll1llllll_opy_
        },
        bstack1llll1l_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬᗀ"): settings,
        bstack1llll1l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡈࡵ࡮ࡵࡴࡲࡰࠬᗁ"): bstack11llll1111l_opy_(),
        bstack1llll1l_opy_ (u"ࠬࡩࡩࡊࡰࡩࡳࠬᗂ"): bstack1llllll111_opy_(),
        bstack1llll1l_opy_ (u"࠭ࡨࡰࡵࡷࡍࡳ࡬࡯ࠨᗃ"): get_host_info(),
        bstack1llll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᗄ"): bstack1l111ll11_opy_(config)
    }
    headers = {
        bstack1llll1l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᗅ"): bstack1llll1l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᗆ"),
    }
    config = {
        bstack1llll1l_opy_ (u"ࠪࡥࡺࡺࡨࠨᗇ"): (bstack11llll11lll_opy_, bstack11lll1111ll_opy_),
        bstack1llll1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᗈ"): headers
    }
    response = bstack11lll1l1l1_opy_(bstack1llll1l_opy_ (u"ࠬࡖࡏࡔࡖࠪᗉ"), bstack11lll1111l1_opy_ + bstack1llll1l_opy_ (u"࠭࠯ࡷ࠴࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠭ᗊ"), data, config)
    bstack11lll111lll_opy_ = response.json()
    if bstack11lll111lll_opy_[bstack1llll1l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᗋ")]:
      parsed = json.loads(os.getenv(bstack1llll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᗌ"), bstack1llll1l_opy_ (u"ࠩࡾࢁࠬᗍ")))
      parsed[bstack1llll1l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᗎ")] = bstack11lll111lll_opy_[bstack1llll1l_opy_ (u"ࠫࡩࡧࡴࡢࠩᗏ")][bstack1llll1l_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᗐ")]
      os.environ[bstack1llll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᗑ")] = json.dumps(parsed)
      bstack1ll11l111l_opy_.bstack1l111lll1l_opy_(bstack11lll111lll_opy_[bstack1llll1l_opy_ (u"ࠧࡥࡣࡷࡥࠬᗒ")][bstack1llll1l_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᗓ")])
      bstack1ll11l111l_opy_.bstack11llll1l11l_opy_(bstack11lll111lll_opy_[bstack1llll1l_opy_ (u"ࠩࡧࡥࡹࡧࠧᗔ")][bstack1llll1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᗕ")])
      bstack1ll11l111l_opy_.store()
      return bstack11lll111lll_opy_[bstack1llll1l_opy_ (u"ࠫࡩࡧࡴࡢࠩᗖ")][bstack1llll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠪᗗ")], bstack11lll111lll_opy_[bstack1llll1l_opy_ (u"࠭ࡤࡢࡶࡤࠫᗘ")][bstack1llll1l_opy_ (u"ࠧࡪࡦࠪᗙ")]
    else:
      logger.error(bstack1llll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠩᗚ") + bstack11lll111lll_opy_[bstack1llll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᗛ")])
      if bstack11lll111lll_opy_[bstack1llll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᗜ")] == bstack1llll1l_opy_ (u"ࠫࡎࡴࡶࡢ࡮࡬ࡨࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡶࡡࡴࡵࡨࡨ࠳࠭ᗝ"):
        for bstack11lll111l11_opy_ in bstack11lll111lll_opy_[bstack1llll1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬᗞ")]:
          logger.error(bstack11lll111l11_opy_[bstack1llll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᗟ")])
      return None, None
  except Exception as error:
    logger.error(bstack1llll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠣᗠ") +  str(error))
    return None, None
def bstack11lll111ll1_opy_():
  if os.getenv(bstack1llll1l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᗡ")) is None:
    return {
        bstack1llll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᗢ"): bstack1llll1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᗣ"),
        bstack1llll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᗤ"): bstack1llll1l_opy_ (u"ࠬࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡨࡢࡦࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠫᗥ")
    }
  data = {bstack1llll1l_opy_ (u"࠭ࡥ࡯ࡦࡗ࡭ࡲ࡫ࠧᗦ"): bstack1l1ll1l1l_opy_()}
  headers = {
      bstack1llll1l_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧᗧ"): bstack1llll1l_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࠩᗨ") + os.getenv(bstack1llll1l_opy_ (u"ࠤࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠢᗩ")),
      bstack1llll1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᗪ"): bstack1llll1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᗫ")
  }
  response = bstack11lll1l1l1_opy_(bstack1llll1l_opy_ (u"ࠬࡖࡕࡕࠩᗬ"), bstack11lll1111l1_opy_ + bstack1llll1l_opy_ (u"࠭࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵ࠲ࡷࡹࡵࡰࠨᗭ"), data, { bstack1llll1l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᗮ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1llll1l_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࠦ࡭ࡢࡴ࡮ࡩࡩࠦࡡࡴࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠥࡧࡴࠡࠤᗯ") + bstack111ll11ll1_opy_().isoformat() + bstack1llll1l_opy_ (u"ࠩ࡝ࠫᗰ"))
      return {bstack1llll1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᗱ"): bstack1llll1l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᗲ"), bstack1llll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᗳ"): bstack1llll1l_opy_ (u"࠭ࠧᗴ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1llll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡧࡴࡳࡰ࡭ࡧࡷ࡭ࡴࡴࠠࡰࡨࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮࠻ࠢࠥᗵ") + str(error))
    return {
        bstack1llll1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᗶ"): bstack1llll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᗷ"),
        bstack1llll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᗸ"): str(error)
    }
def bstack11lll1l11ll_opy_(bstack11lll1ll1ll_opy_):
    return re.match(bstack1llll1l_opy_ (u"ࡶࠬࡤ࡜ࡥ࠭ࠫࡠ࠳ࡢࡤࠬࠫࡂࠨࠬᗹ"), bstack11lll1ll1ll_opy_.strip()) is not None
def bstack11ll1l1ll1_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11lll1lllll_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11lll1lllll_opy_ = desired_capabilities
        else:
          bstack11lll1lllll_opy_ = {}
        bstack11lll1l1ll1_opy_ = (bstack11lll1lllll_opy_.get(bstack1llll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᗺ"), bstack1llll1l_opy_ (u"࠭ࠧᗻ")).lower() or caps.get(bstack1llll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᗼ"), bstack1llll1l_opy_ (u"ࠨࠩᗽ")).lower())
        if bstack11lll1l1ll1_opy_ == bstack1llll1l_opy_ (u"ࠩ࡬ࡳࡸ࠭ᗾ"):
            return True
        if bstack11lll1l1ll1_opy_ == bstack1llll1l_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫᗿ"):
            bstack11llll111ll_opy_ = str(float(caps.get(bstack1llll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᘀ")) or bstack11lll1lllll_opy_.get(bstack1llll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᘁ"), {}).get(bstack1llll1l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᘂ"),bstack1llll1l_opy_ (u"ࠧࠨᘃ"))))
            if bstack11lll1l1ll1_opy_ == bstack1llll1l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࠩᘄ") and int(bstack11llll111ll_opy_.split(bstack1llll1l_opy_ (u"ࠩ࠱ࠫᘅ"))[0]) < float(bstack11lll1ll11l_opy_):
                logger.warning(str(bstack11lll11l1ll_opy_))
                return False
            return True
        bstack1ll11l1lll1_opy_ = caps.get(bstack1llll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᘆ"), {}).get(bstack1llll1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᘇ"), caps.get(bstack1llll1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᘈ"), bstack1llll1l_opy_ (u"࠭ࠧᘉ")))
        if bstack1ll11l1lll1_opy_:
            logger.warning(bstack1llll1l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᘊ"))
            return False
        browser = caps.get(bstack1llll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᘋ"), bstack1llll1l_opy_ (u"ࠩࠪᘌ")).lower() or bstack11lll1lllll_opy_.get(bstack1llll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᘍ"), bstack1llll1l_opy_ (u"ࠫࠬᘎ")).lower()
        if browser != bstack1llll1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᘏ"):
            logger.warning(bstack1llll1l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᘐ"))
            return False
        browser_version = caps.get(bstack1llll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᘑ")) or caps.get(bstack1llll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᘒ")) or bstack11lll1lllll_opy_.get(bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᘓ")) or bstack11lll1lllll_opy_.get(bstack1llll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᘔ"), {}).get(bstack1llll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᘕ")) or bstack11lll1lllll_opy_.get(bstack1llll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᘖ"), {}).get(bstack1llll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᘗ"))
        bstack1ll1l1111ll_opy_ = bstack11lll111l1l_opy_.bstack1ll11lll111_opy_
        bstack11lll1lll1l_opy_ = False
        if config is not None:
          bstack11lll1lll1l_opy_ = bstack1llll1l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᘘ") in config and str(config[bstack1llll1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᘙ")]).lower() != bstack1llll1l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᘚ")
        if os.environ.get(bstack1llll1l_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨᘛ"), bstack1llll1l_opy_ (u"ࠫࠬᘜ")).lower() == bstack1llll1l_opy_ (u"ࠬࡺࡲࡶࡧࠪᘝ") or bstack11lll1lll1l_opy_:
          bstack1ll1l1111ll_opy_ = bstack11lll111l1l_opy_.bstack1ll11llll11_opy_
        if browser_version and browser_version != bstack1llll1l_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ᘞ") and int(browser_version.split(bstack1llll1l_opy_ (u"ࠧ࠯ࠩᘟ"))[0]) <= bstack1ll1l1111ll_opy_:
          logger.warning(bstack1ll1ll1ll1l_opy_ (u"ࠨࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࡾࡱ࡮ࡴ࡟ࡢ࠳࠴ࡽࡤࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࡠࡥ࡫ࡶࡴࡳࡥࡠࡸࡨࡶࡸ࡯࡯࡯ࡿ࠱ࠫᘠ"))
          return False
        if not options:
          bstack1ll1l111lll_opy_ = caps.get(bstack1llll1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᘡ")) or bstack11lll1lllll_opy_.get(bstack1llll1l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᘢ"), {})
          if bstack1llll1l_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᘣ") in bstack1ll1l111lll_opy_.get(bstack1llll1l_opy_ (u"ࠬࡧࡲࡨࡵࠪᘤ"), []):
              logger.warning(bstack1llll1l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᘥ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack1llll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤᘦ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1llll11l1l1_opy_ = config.get(bstack1llll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᘧ"), {})
    bstack1llll11l1l1_opy_[bstack1llll1l_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬᘨ")] = os.getenv(bstack1llll1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᘩ"))
    bstack11lll11ll1l_opy_ = json.loads(os.getenv(bstack1llll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᘪ"), bstack1llll1l_opy_ (u"ࠬࢁࡽࠨᘫ"))).get(bstack1llll1l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᘬ"))
    if not config[bstack1llll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᘭ")].get(bstack1llll1l_opy_ (u"ࠣࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠢᘮ")):
      if bstack1llll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᘯ") in caps:
        caps[bstack1llll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᘰ")][bstack1llll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᘱ")] = bstack1llll11l1l1_opy_
        caps[bstack1llll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᘲ")][bstack1llll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᘳ")][bstack1llll1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᘴ")] = bstack11lll11ll1l_opy_
      else:
        caps[bstack1llll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᘵ")] = bstack1llll11l1l1_opy_
        caps[bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᘶ")][bstack1llll1l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᘷ")] = bstack11lll11ll1l_opy_
  except Exception as error:
    logger.debug(bstack1llll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࠧᘸ") +  str(error))
def bstack11l11ll1l1_opy_(driver, bstack11lll1l1111_opy_):
  try:
    setattr(driver, bstack1llll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬᘹ"), True)
    session = driver.session_id
    if session:
      bstack11llll111l1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11llll111l1_opy_ = False
      bstack11llll111l1_opy_ = url.scheme in [bstack1llll1l_opy_ (u"ࠨࡨࡵࡶࡳࠦᘺ"), bstack1llll1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᘻ")]
      if bstack11llll111l1_opy_:
        if bstack11lll1l1111_opy_:
          logger.info(bstack1llll1l_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱ࠤࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡦࡪ࡭ࡩ࡯ࠢࡰࡳࡲ࡫࡮ࡵࡣࡵ࡭ࡱࡿ࠮ࠣᘼ"))
      return bstack11lll1l1111_opy_
  except Exception as e:
    logger.error(bstack1llll1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧᘽ") + str(e))
    return False
def bstack11l1111ll_opy_(driver, name, path):
  try:
    bstack1ll1l11l111_opy_ = {
        bstack1llll1l_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪᘾ"): threading.current_thread().current_test_uuid,
        bstack1llll1l_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᘿ"): os.environ.get(bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᙀ"), bstack1llll1l_opy_ (u"࠭ࠧᙁ")),
        bstack1llll1l_opy_ (u"ࠧࡵࡪࡍࡻࡹ࡚࡯࡬ࡧࡱࠫᙂ"): os.environ.get(bstack1llll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᙃ"), bstack1llll1l_opy_ (u"ࠩࠪᙄ"))
    }
    bstack1ll1l1l11ll_opy_ = bstack1l1lll111l_opy_.bstack1ll1ll11l11_opy_(EVENTS.bstack11l11ll1l_opy_.value)
    logger.debug(bstack1llll1l_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ᙅ"))
    try:
      if (bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᙆ"), None) and bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᙇ"), None)):
        scripts = {bstack1llll1l_opy_ (u"࠭ࡳࡤࡣࡱࠫᙈ"): bstack1ll11l111l_opy_.perform_scan}
        bstack11lll11111l_opy_ = json.loads(scripts[bstack1llll1l_opy_ (u"ࠢࡴࡥࡤࡲࠧᙉ")].replace(bstack1llll1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᙊ"), bstack1llll1l_opy_ (u"ࠤࠥᙋ")))
        bstack11lll11111l_opy_[bstack1llll1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᙌ")][bstack1llll1l_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫᙍ")] = None
        scripts[bstack1llll1l_opy_ (u"ࠧࡹࡣࡢࡰࠥᙎ")] = bstack1llll1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤᙏ") + json.dumps(bstack11lll11111l_opy_)
        bstack1ll11l111l_opy_.bstack1l111lll1l_opy_(scripts)
        bstack1ll11l111l_opy_.store()
        logger.debug(driver.execute_script(bstack1ll11l111l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1ll11l111l_opy_.perform_scan, {bstack1llll1l_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᙐ"): name}))
      bstack1l1lll111l_opy_.end(EVENTS.bstack11l11ll1l_opy_.value, bstack1ll1l1l11ll_opy_ + bstack1llll1l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᙑ"), bstack1ll1l1l11ll_opy_ + bstack1llll1l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᙒ"), True, None)
    except Exception as error:
      bstack1l1lll111l_opy_.end(EVENTS.bstack11l11ll1l_opy_.value, bstack1ll1l1l11ll_opy_ + bstack1llll1l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᙓ"), bstack1ll1l1l11ll_opy_ + bstack1llll1l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᙔ"), False, str(error))
    bstack1ll1l1l11ll_opy_ = bstack1l1lll111l_opy_.bstack11lll1lll11_opy_(EVENTS.bstack1ll11ll1ll1_opy_.value)
    bstack1l1lll111l_opy_.mark(bstack1ll1l1l11ll_opy_ + bstack1llll1l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᙕ"))
    try:
      if (bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᙖ"), None) and bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᙗ"), None)):
        scripts = {bstack1llll1l_opy_ (u"ࠨࡵࡦࡥࡳ࠭ᙘ"): bstack1ll11l111l_opy_.perform_scan}
        bstack11lll11111l_opy_ = json.loads(scripts[bstack1llll1l_opy_ (u"ࠤࡶࡧࡦࡴࠢᙙ")].replace(bstack1llll1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᙚ"), bstack1llll1l_opy_ (u"ࠦࠧᙛ")))
        bstack11lll11111l_opy_[bstack1llll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᙜ")][bstack1llll1l_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭ᙝ")] = None
        scripts[bstack1llll1l_opy_ (u"ࠢࡴࡥࡤࡲࠧᙞ")] = bstack1llll1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᙟ") + json.dumps(bstack11lll11111l_opy_)
        bstack1ll11l111l_opy_.bstack1l111lll1l_opy_(scripts)
        bstack1ll11l111l_opy_.store()
        logger.debug(driver.execute_script(bstack1ll11l111l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1ll11l111l_opy_.bstack11ll1lllll1_opy_, bstack1ll1l11l111_opy_))
      bstack1l1lll111l_opy_.end(bstack1ll1l1l11ll_opy_, bstack1ll1l1l11ll_opy_ + bstack1llll1l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᙠ"), bstack1ll1l1l11ll_opy_ + bstack1llll1l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᙡ"),True, None)
    except Exception as error:
      bstack1l1lll111l_opy_.end(bstack1ll1l1l11ll_opy_, bstack1ll1l1l11ll_opy_ + bstack1llll1l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᙢ"), bstack1ll1l1l11ll_opy_ + bstack1llll1l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᙣ"),False, str(error))
    logger.info(bstack1llll1l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤᙤ"))
  except Exception as bstack1ll1l1l1l11_opy_:
    logger.error(bstack1llll1l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᙥ") + str(path) + bstack1llll1l_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥᙦ") + str(bstack1ll1l1l1l11_opy_))
def bstack11llll11l1l_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1llll1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣᙧ")) and str(caps.get(bstack1llll1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤᙨ"))).lower() == bstack1llll1l_opy_ (u"ࠦࡦࡴࡤࡳࡱ࡬ࡨࠧᙩ"):
        bstack11llll111ll_opy_ = caps.get(bstack1llll1l_opy_ (u"ࠧࡧࡰࡱ࡫ࡸࡱ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᙪ")) or caps.get(bstack1llll1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᙫ"))
        if bstack11llll111ll_opy_ and int(str(bstack11llll111ll_opy_)) < bstack11lll1ll11l_opy_:
            return False
    return True
def bstack111l1lll1_opy_(config):
  if bstack1llll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᙬ") in config:
        return config[bstack1llll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᙭")]
  for platform in config.get(bstack1llll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᙮"), []):
      if bstack1llll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᙯ") in platform:
          return platform[bstack1llll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᙰ")]
  return None
def bstack1ll1ll111l_opy_(bstack11l1l11l_opy_):
  try:
    browser_name = bstack11l1l11l_opy_[bstack1llll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᙱ")]
    browser_version = bstack11l1l11l_opy_[bstack1llll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᙲ")]
    chrome_options = bstack11l1l11l_opy_[bstack1llll1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࠨᙳ")]
    try:
        bstack11lll11l1l1_opy_ = int(browser_version.split(bstack1llll1l_opy_ (u"ࠨ࠰ࠪᙴ"))[0])
    except ValueError as e:
        logger.error(bstack1llll1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡪࡰࡪࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠨᙵ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1llll1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᙶ")):
        logger.warning(bstack1llll1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᙷ"))
        return False
    if bstack11lll11l1l1_opy_ < bstack11lll111l1l_opy_.bstack1ll11llll11_opy_:
        logger.warning(bstack1ll1ll1ll1l_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡩࡳࡧࡶࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࢁࡃࡐࡐࡖࡘࡆࡔࡔࡔ࠰ࡐࡍࡓࡏࡍࡖࡏࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘ࡛ࡐࡑࡑࡕࡘࡊࡊ࡟ࡄࡊࡕࡓࡒࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࡾࠢࡲࡶࠥ࡮ࡩࡨࡪࡨࡶ࠳࠭ᙸ"))
        return False
    if chrome_options and any(bstack1llll1l_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪᙹ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack1llll1l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤᙺ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1llll1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡷࡳࡴࡴࡸࡴࠡࡨࡲࡶࠥࡲ࡯ࡤࡣ࡯ࠤࡈ࡮ࡲࡰ࡯ࡨ࠾ࠥࠨᙻ") + str(e))
    return False
def bstack1ll1l111l_opy_(bstack1l1l111111_opy_, config):
    try:
      bstack1ll1l1111l1_opy_ = bstack1llll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᙼ") in config and config[bstack1llll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᙽ")] == True
      bstack11lll1lll1l_opy_ = bstack1llll1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᙾ") in config and str(config[bstack1llll1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᙿ")]).lower() != bstack1llll1l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ ")
      if not (bstack1ll1l1111l1_opy_ and (not bstack1l111ll11_opy_(config) or bstack11lll1lll1l_opy_)):
        return bstack1l1l111111_opy_
      bstack11lll1l1l1l_opy_ = bstack1ll11l111l_opy_.bstack11lll1l11l1_opy_
      if bstack11lll1l1l1l_opy_ is None:
        logger.debug(bstack1llll1l_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡤࡪࡵࡳࡲ࡫ࠠࡰࡲࡷ࡭ࡴࡴࡳࠡࡣࡵࡩࠥࡔ࡯࡯ࡧࠥᚁ"))
        return bstack1l1l111111_opy_
      bstack11lll11l111_opy_ = int(str(bstack11lll111111_opy_()).split(bstack1llll1l_opy_ (u"ࠨ࠰ࠪᚂ"))[0])
      logger.debug(bstack1llll1l_opy_ (u"ࠤࡖࡩࡱ࡫࡮ࡪࡷࡰࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡪࡥࡵࡧࡦࡸࡪࡪ࠺ࠡࠤᚃ") + str(bstack11lll11l111_opy_) + bstack1llll1l_opy_ (u"ࠥࠦᚄ"))
      if bstack11lll11l111_opy_ == 3 and isinstance(bstack1l1l111111_opy_, dict) and bstack1llll1l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᚅ") in bstack1l1l111111_opy_ and bstack11lll1l1l1l_opy_ is not None:
        if bstack1llll1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᚆ") not in bstack1l1l111111_opy_[bstack1llll1l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᚇ")]:
          bstack1l1l111111_opy_[bstack1llll1l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᚈ")][bstack1llll1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚉ")] = {}
        if bstack1llll1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᚊ") in bstack11lll1l1l1l_opy_:
          if bstack1llll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᚋ") not in bstack1l1l111111_opy_[bstack1llll1l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᚌ")][bstack1llll1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᚍ")]:
            bstack1l1l111111_opy_[bstack1llll1l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᚎ")][bstack1llll1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᚏ")][bstack1llll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᚐ")] = []
          for arg in bstack11lll1l1l1l_opy_[bstack1llll1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᚑ")]:
            if arg not in bstack1l1l111111_opy_[bstack1llll1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᚒ")][bstack1llll1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᚓ")][bstack1llll1l_opy_ (u"ࠬࡧࡲࡨࡵࠪᚔ")]:
              bstack1l1l111111_opy_[bstack1llll1l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᚕ")][bstack1llll1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᚖ")][bstack1llll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᚗ")].append(arg)
        if bstack1llll1l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᚘ") in bstack11lll1l1l1l_opy_:
          if bstack1llll1l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᚙ") not in bstack1l1l111111_opy_[bstack1llll1l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᚚ")][bstack1llll1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᚛")]:
            bstack1l1l111111_opy_[bstack1llll1l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᚜")][bstack1llll1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᚝")][bstack1llll1l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ᚞")] = []
          for ext in bstack11lll1l1l1l_opy_[bstack1llll1l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭᚟")]:
            if ext not in bstack1l1l111111_opy_[bstack1llll1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᚠ")][bstack1llll1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᚡ")][bstack1llll1l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᚢ")]:
              bstack1l1l111111_opy_[bstack1llll1l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᚣ")][bstack1llll1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᚤ")][bstack1llll1l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᚥ")].append(ext)
        if bstack1llll1l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᚦ") in bstack11lll1l1l1l_opy_:
          if bstack1llll1l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᚧ") not in bstack1l1l111111_opy_[bstack1llll1l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᚨ")][bstack1llll1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᚩ")]:
            bstack1l1l111111_opy_[bstack1llll1l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᚪ")][bstack1llll1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᚫ")][bstack1llll1l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᚬ")] = {}
          bstack11lll1l111l_opy_(bstack1l1l111111_opy_[bstack1llll1l_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᚭ")][bstack1llll1l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᚮ")][bstack1llll1l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᚯ")],
                    bstack11lll1l1l1l_opy_[bstack1llll1l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᚰ")])
        os.environ[bstack1llll1l_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫᚱ")] = bstack1llll1l_opy_ (u"ࠧࡵࡴࡸࡩࠬᚲ")
        return bstack1l1l111111_opy_
      else:
        chrome_options = None
        if isinstance(bstack1l1l111111_opy_, ChromeOptions):
          chrome_options = bstack1l1l111111_opy_
        elif isinstance(bstack1l1l111111_opy_, dict):
          for value in bstack1l1l111111_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1l1l111111_opy_, dict):
            bstack1l1l111111_opy_[bstack1llll1l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩᚳ")] = chrome_options
          else:
            bstack1l1l111111_opy_ = chrome_options
        if bstack11lll1l1l1l_opy_ is not None:
          if bstack1llll1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᚴ") in bstack11lll1l1l1l_opy_:
                bstack11lll11l11l_opy_ = chrome_options.arguments or []
                new_args = bstack11lll1l1l1l_opy_[bstack1llll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᚵ")]
                for arg in new_args:
                    if arg not in bstack11lll11l11l_opy_:
                        chrome_options.add_argument(arg)
          if bstack1llll1l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᚶ") in bstack11lll1l1l1l_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1llll1l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᚷ"), [])
                bstack11llll11ll1_opy_ = bstack11lll1l1l1l_opy_[bstack1llll1l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᚸ")]
                for extension in bstack11llll11ll1_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1llll1l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᚹ") in bstack11lll1l1l1l_opy_:
                bstack11lll1ll111_opy_ = chrome_options.experimental_options.get(bstack1llll1l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᚺ"), {})
                bstack11lll1l1lll_opy_ = bstack11lll1l1l1l_opy_[bstack1llll1l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᚻ")]
                bstack11lll1l111l_opy_(bstack11lll1ll111_opy_, bstack11lll1l1lll_opy_)
                chrome_options.add_experimental_option(bstack1llll1l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᚼ"), bstack11lll1ll111_opy_)
        os.environ[bstack1llll1l_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩᚽ")] = bstack1llll1l_opy_ (u"ࠬࡺࡲࡶࡧࠪᚾ")
        return bstack1l1l111111_opy_
    except Exception as e:
      logger.error(bstack1llll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡦࡪࡤࡪࡰࡪࠤࡳࡵ࡮࠮ࡄࡖࠤ࡮ࡴࡦࡳࡣࠣࡥ࠶࠷ࡹࠡࡥ࡫ࡶࡴࡳࡥࠡࡱࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࠦᚿ") + str(e))
      return bstack1l1l111111_opy_