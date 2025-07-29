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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1ll1l1l11_opy_, bstack11lll1l1l1_opy_
from bstack_utils.measure import measure
class bstack111111111_opy_:
  working_dir = os.getcwd()
  bstack1lll1llll1_opy_ = False
  config = {}
  bstack11l1lll1lll_opy_ = bstack1llll1l_opy_ (u"ࠬ࠭ᴲ")
  binary_path = bstack1llll1l_opy_ (u"࠭ࠧᴳ")
  bstack111ll111l11_opy_ = bstack1llll1l_opy_ (u"ࠧࠨᴴ")
  bstack11llll11l1_opy_ = False
  bstack111lll1l1ll_opy_ = None
  bstack111lll11lll_opy_ = {}
  bstack111l1ll1l1l_opy_ = 300
  bstack111ll1l11l1_opy_ = False
  logger = None
  bstack111ll1l1l11_opy_ = False
  bstack1l11llllll_opy_ = False
  percy_build_id = None
  bstack111ll11l1l1_opy_ = bstack1llll1l_opy_ (u"ࠨࠩᴵ")
  bstack111ll11lll1_opy_ = {
    bstack1llll1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᴶ") : 1,
    bstack1llll1l_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫᴷ") : 2,
    bstack1llll1l_opy_ (u"ࠫࡪࡪࡧࡦࠩᴸ") : 3,
    bstack1llll1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬᴹ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111lll11ll1_opy_(self):
    bstack111ll11llll_opy_ = bstack1llll1l_opy_ (u"࠭ࠧᴺ")
    bstack111lll11l1l_opy_ = sys.platform
    bstack111l1lll111_opy_ = bstack1llll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᴻ")
    if re.match(bstack1llll1l_opy_ (u"ࠣࡦࡤࡶࡼ࡯࡮ࡽ࡯ࡤࡧࠥࡵࡳࠣᴼ"), bstack111lll11l1l_opy_) != None:
      bstack111ll11llll_opy_ = bstack11ll1111lll_opy_ + bstack1llll1l_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡲࡷࡽ࠴ࡺࡪࡲࠥᴽ")
      self.bstack111ll11l1l1_opy_ = bstack1llll1l_opy_ (u"ࠪࡱࡦࡩࠧᴾ")
    elif re.match(bstack1llll1l_opy_ (u"ࠦࡲࡹࡷࡪࡰࡿࡱࡸࡿࡳࡽ࡯࡬ࡲ࡬ࡽࡼࡤࡻࡪࡻ࡮ࡴࡼࡣࡥࡦࡻ࡮ࡴࡼࡸ࡫ࡱࡧࡪࢂࡥ࡮ࡥࡿࡻ࡮ࡴ࠳࠳ࠤᴿ"), bstack111lll11l1l_opy_) != None:
      bstack111ll11llll_opy_ = bstack11ll1111lll_opy_ + bstack1llll1l_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡽࡩ࡯࠰ࡽ࡭ࡵࠨᵀ")
      bstack111l1lll111_opy_ = bstack1llll1l_opy_ (u"ࠨࡰࡦࡴࡦࡽ࠳࡫ࡸࡦࠤᵁ")
      self.bstack111ll11l1l1_opy_ = bstack1llll1l_opy_ (u"ࠧࡸ࡫ࡱࠫᵂ")
    else:
      bstack111ll11llll_opy_ = bstack11ll1111lll_opy_ + bstack1llll1l_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮࡮࡬ࡲࡺࡾ࠮ࡻ࡫ࡳࠦᵃ")
      self.bstack111ll11l1l1_opy_ = bstack1llll1l_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨᵄ")
    return bstack111ll11llll_opy_, bstack111l1lll111_opy_
  def bstack111l1llll1l_opy_(self):
    try:
      bstack111l1l1ll1l_opy_ = [os.path.join(expanduser(bstack1llll1l_opy_ (u"ࠥࢂࠧᵅ")), bstack1llll1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᵆ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111l1l1ll1l_opy_:
        if(self.bstack111ll1l1ll1_opy_(path)):
          return path
      raise bstack1llll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤᵇ")
    except Exception as e:
      self.logger.error(bstack1llll1l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡶࡥࡳࡥࡼࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࠱ࠥࢁࡽࠣᵈ").format(e))
  def bstack111ll1l1ll1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111ll1ll11l_opy_(self, bstack111l1l1llll_opy_):
    return os.path.join(bstack111l1l1llll_opy_, self.bstack11l1lll1lll_opy_ + bstack1llll1l_opy_ (u"ࠢ࠯ࡧࡷࡥ࡬ࠨᵉ"))
  def bstack111l1l1l1ll_opy_(self, bstack111l1l1llll_opy_, bstack111ll1111ll_opy_):
    if not bstack111ll1111ll_opy_: return
    try:
      bstack111l1ll1l11_opy_ = self.bstack111ll1ll11l_opy_(bstack111l1l1llll_opy_)
      with open(bstack111l1ll1l11_opy_, bstack1llll1l_opy_ (u"ࠣࡹࠥᵊ")) as f:
        f.write(bstack111ll1111ll_opy_)
        self.logger.debug(bstack1llll1l_opy_ (u"ࠤࡖࡥࡻ࡫ࡤࠡࡰࡨࡻࠥࡋࡔࡢࡩࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠨᵋ"))
    except Exception as e:
      self.logger.error(bstack1llll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡢࡸࡨࠤࡹ࡮ࡥࠡࡧࡷࡥ࡬࠲ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᵌ").format(e))
  def bstack111ll1lll1l_opy_(self, bstack111l1l1llll_opy_):
    try:
      bstack111l1ll1l11_opy_ = self.bstack111ll1ll11l_opy_(bstack111l1l1llll_opy_)
      if os.path.exists(bstack111l1ll1l11_opy_):
        with open(bstack111l1ll1l11_opy_, bstack1llll1l_opy_ (u"ࠦࡷࠨᵍ")) as f:
          bstack111ll1111ll_opy_ = f.read().strip()
          return bstack111ll1111ll_opy_ if bstack111ll1111ll_opy_ else None
    except Exception as e:
      self.logger.error(bstack1llll1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡅࡕࡣࡪ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᵎ").format(e))
  def bstack111l1lll11l_opy_(self, bstack111l1l1llll_opy_, bstack111ll11llll_opy_):
    bstack111l1ll1lll_opy_ = self.bstack111ll1lll1l_opy_(bstack111l1l1llll_opy_)
    if bstack111l1ll1lll_opy_:
      try:
        bstack111lll1l11l_opy_ = self.bstack111ll1l11ll_opy_(bstack111l1ll1lll_opy_, bstack111ll11llll_opy_)
        if not bstack111lll1l11l_opy_:
          self.logger.debug(bstack1llll1l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯ࡳࠡࡷࡳࠤࡹࡵࠠࡥࡣࡷࡩࠥ࠮ࡅࡕࡣࡪࠤࡺࡴࡣࡩࡣࡱ࡫ࡪࡪࠩࠣᵏ"))
          return True
        self.logger.debug(bstack1llll1l_opy_ (u"ࠢࡏࡧࡺࠤࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡺࡪࡸࡳࡪࡱࡱࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡵࡱࡦࡤࡸࡪࠨᵐ"))
        return False
      except Exception as e:
        self.logger.warn(bstack1llll1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡨ࡮ࡥࡤ࡭ࠣࡪࡴࡸࠠࡣ࡫ࡱࡥࡷࡿࠠࡶࡲࡧࡥࡹ࡫ࡳ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡦ࡮ࡴࡡࡳࡻ࠽ࠤࢀࢃࠢᵑ").format(e))
    return False
  def bstack111ll1l11ll_opy_(self, bstack111l1ll1lll_opy_, bstack111ll11llll_opy_):
    try:
      headers = {
        bstack1llll1l_opy_ (u"ࠤࡌࡪ࠲ࡔ࡯࡯ࡧ࠰ࡑࡦࡺࡣࡩࠤᵒ"): bstack111l1ll1lll_opy_
      }
      response = bstack11lll1l1l1_opy_(bstack1llll1l_opy_ (u"ࠪࡋࡊ࡚ࠧᵓ"), bstack111ll11llll_opy_, {}, {bstack1llll1l_opy_ (u"ࠦ࡭࡫ࡡࡥࡧࡵࡷࠧᵔ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1llll1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡦࡰࡴࠣࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡸࡴࡩࡧࡴࡦࡵ࠽ࠤࢀࢃࠢᵕ").format(e))
  @measure(event_name=EVENTS.bstack11ll1l111l1_opy_, stage=STAGE.bstack11111l1l1_opy_)
  def bstack111lll1l111_opy_(self, bstack111ll11llll_opy_, bstack111l1lll111_opy_):
    try:
      bstack111lll111l1_opy_ = self.bstack111l1llll1l_opy_()
      bstack111ll111ll1_opy_ = os.path.join(bstack111lll111l1_opy_, bstack1llll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࢀࡩࡱࠩᵖ"))
      bstack111lll111ll_opy_ = os.path.join(bstack111lll111l1_opy_, bstack111l1lll111_opy_)
      if self.bstack111l1lll11l_opy_(bstack111lll111l1_opy_, bstack111ll11llll_opy_): # if bstack111l1lllll1_opy_, bstack1l1l1lll111_opy_ bstack111ll1111ll_opy_ is bstack111ll11l111_opy_ to bstack11l1ll1l111_opy_ version available (response 304)
        if os.path.exists(bstack111lll111ll_opy_):
          self.logger.info(bstack1llll1l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤᵗ").format(bstack111lll111ll_opy_))
          return bstack111lll111ll_opy_
        if os.path.exists(bstack111ll111ll1_opy_):
          self.logger.info(bstack1llll1l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡻ࡫ࡳࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡹࡳࢀࡩࡱࡲ࡬ࡲ࡬ࠨᵘ").format(bstack111ll111ll1_opy_))
          return self.bstack111ll11l11l_opy_(bstack111ll111ll1_opy_, bstack111l1lll111_opy_)
      self.logger.info(bstack1llll1l_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰࠤࢀࢃࠢᵙ").format(bstack111ll11llll_opy_))
      response = bstack11lll1l1l1_opy_(bstack1llll1l_opy_ (u"ࠪࡋࡊ࡚ࠧᵚ"), bstack111ll11llll_opy_, {}, {})
      if response.status_code == 200:
        bstack111ll1l111l_opy_ = response.headers.get(bstack1llll1l_opy_ (u"ࠦࡊ࡚ࡡࡨࠤᵛ"), bstack1llll1l_opy_ (u"ࠧࠨᵜ"))
        if bstack111ll1l111l_opy_:
          self.bstack111l1l1l1ll_opy_(bstack111lll111l1_opy_, bstack111ll1l111l_opy_)
        with open(bstack111ll111ll1_opy_, bstack1llll1l_opy_ (u"࠭ࡷࡣࠩᵝ")) as file:
          file.write(response.content)
        self.logger.info(bstack1llll1l_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡥࡳࡪࠠࡴࡣࡹࡩࡩࠦࡡࡵࠢࡾࢁࠧᵞ").format(bstack111ll111ll1_opy_))
        return self.bstack111ll11l11l_opy_(bstack111ll111ll1_opy_, bstack111l1lll111_opy_)
      else:
        raise(bstack1llll1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡴࡩࡧࠣࡪ࡮ࡲࡥ࠯ࠢࡖࡸࡦࡺࡵࡴࠢࡦࡳࡩ࡫࠺ࠡࡽࢀࠦᵟ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1llll1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࡀࠠࡼࡿࠥᵠ").format(e))
  def bstack111l1l1lll1_opy_(self, bstack111ll11llll_opy_, bstack111l1lll111_opy_):
    try:
      retry = 2
      bstack111lll111ll_opy_ = None
      bstack111l1ll11l1_opy_ = False
      while retry > 0:
        bstack111lll111ll_opy_ = self.bstack111lll1l111_opy_(bstack111ll11llll_opy_, bstack111l1lll111_opy_)
        bstack111l1ll11l1_opy_ = self.bstack111l1lll1l1_opy_(bstack111ll11llll_opy_, bstack111l1lll111_opy_, bstack111lll111ll_opy_)
        if bstack111l1ll11l1_opy_:
          break
        retry -= 1
      return bstack111lll111ll_opy_, bstack111l1ll11l1_opy_
    except Exception as e:
      self.logger.error(bstack1llll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡶࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡳࡥࡹ࡮ࠢᵡ").format(e))
    return bstack111lll111ll_opy_, False
  def bstack111l1lll1l1_opy_(self, bstack111ll11llll_opy_, bstack111l1lll111_opy_, bstack111lll111ll_opy_, bstack111ll1ll1ll_opy_ = 0):
    if bstack111ll1ll1ll_opy_ > 1:
      return False
    if bstack111lll111ll_opy_ == None or os.path.exists(bstack111lll111ll_opy_) == False:
      self.logger.warn(bstack1llll1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡸࡥࡵࡴࡼ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤᵢ"))
      return False
    bstack111l1ll1ll1_opy_ = bstack1llll1l_opy_ (u"ࡷࠨ࡞࠯ࠬࡃࡴࡪࡸࡣࡺ࠱ࡦࡰ࡮ࠦ࡜ࡥ࠭࡟࠲ࡡࡪࠫ࡝࠰࡟ࡨ࠰ࠨᵣ")
    command = bstack1llll1l_opy_ (u"࠭ࡻࡾࠢ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬᵤ").format(bstack111lll111ll_opy_)
    bstack111ll11ll11_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111l1ll1ll1_opy_, bstack111ll11ll11_opy_) != None:
      return True
    else:
      self.logger.error(bstack1llll1l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡤࡪࡨࡧࡰࠦࡦࡢ࡫࡯ࡩࡩࠨᵥ"))
      return False
  def bstack111ll11l11l_opy_(self, bstack111ll111ll1_opy_, bstack111l1lll111_opy_):
    try:
      working_dir = os.path.dirname(bstack111ll111ll1_opy_)
      shutil.unpack_archive(bstack111ll111ll1_opy_, working_dir)
      bstack111lll111ll_opy_ = os.path.join(working_dir, bstack111l1lll111_opy_)
      os.chmod(bstack111lll111ll_opy_, 0o755)
      return bstack111lll111ll_opy_
    except Exception as e:
      self.logger.error(bstack1llll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡺࡴࡺࡪࡲࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤᵦ"))
  def bstack111lll11111_opy_(self):
    try:
      bstack111l1ll111l_opy_ = self.config.get(bstack1llll1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᵧ"))
      bstack111lll11111_opy_ = bstack111l1ll111l_opy_ or (bstack111l1ll111l_opy_ is None and self.bstack1lll1llll1_opy_)
      if not bstack111lll11111_opy_ or self.config.get(bstack1llll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᵨ"), None) not in bstack11ll1l11l11_opy_:
        return False
      self.bstack11llll11l1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1llll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᵩ").format(e))
  def bstack111l1ll1111_opy_(self):
    try:
      bstack111l1ll1111_opy_ = self.percy_capture_mode
      return bstack111l1ll1111_opy_
    except Exception as e:
      self.logger.error(bstack1llll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠠࡤࡣࡳࡸࡺࡸࡥࠡ࡯ࡲࡨࡪ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᵪ").format(e))
  def init(self, bstack1lll1llll1_opy_, config, logger):
    self.bstack1lll1llll1_opy_ = bstack1lll1llll1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111lll11111_opy_():
      return
    self.bstack111lll11lll_opy_ = config.get(bstack1llll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬᵫ"), {})
    self.percy_capture_mode = config.get(bstack1llll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᵬ"))
    try:
      bstack111ll11llll_opy_, bstack111l1lll111_opy_ = self.bstack111lll11ll1_opy_()
      self.bstack11l1lll1lll_opy_ = bstack111l1lll111_opy_
      bstack111lll111ll_opy_, bstack111l1ll11l1_opy_ = self.bstack111l1l1lll1_opy_(bstack111ll11llll_opy_, bstack111l1lll111_opy_)
      if bstack111l1ll11l1_opy_:
        self.binary_path = bstack111lll111ll_opy_
        thread = Thread(target=self.bstack111ll1lll11_opy_)
        thread.start()
      else:
        self.bstack111ll1l1l11_opy_ = True
        self.logger.error(bstack1llll1l_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡳࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦࡦࡰࡷࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤ࡚ࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡐࡦࡴࡦࡽࠧᵭ").format(bstack111lll111ll_opy_))
    except Exception as e:
      self.logger.error(bstack1llll1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᵮ").format(e))
  def bstack111ll11111l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1llll1l_opy_ (u"ࠪࡰࡴ࡭ࠧᵯ"), bstack1llll1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡰࡴ࡭ࠧᵰ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1llll1l_opy_ (u"ࠧࡖࡵࡴࡪ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡲ࡯ࡨࡵࠣࡥࡹࠦࡻࡾࠤᵱ").format(logfile))
      self.bstack111ll111l11_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1llll1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࠦࡰࡦࡴࡦࡽࠥࡲ࡯ࡨࠢࡳࡥࡹ࡮ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᵲ").format(e))
  @measure(event_name=EVENTS.bstack11ll111l111_opy_, stage=STAGE.bstack11111l1l1_opy_)
  def bstack111ll1lll11_opy_(self):
    bstack111ll11l1ll_opy_ = self.bstack111ll1l1l1l_opy_()
    if bstack111ll11l1ll_opy_ == None:
      self.bstack111ll1l1l11_opy_ = True
      self.logger.error(bstack1llll1l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠥᵳ"))
      return False
    command_args = [bstack1llll1l_opy_ (u"ࠣࡣࡳࡴ࠿࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠤᵴ") if self.bstack1lll1llll1_opy_ else bstack1llll1l_opy_ (u"ࠩࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹ࠭ᵵ")]
    bstack11l111111ll_opy_ = self.bstack111ll1l1111_opy_()
    if bstack11l111111ll_opy_ != None:
      command_args.append(bstack1llll1l_opy_ (u"ࠥ࠱ࡨࠦࡻࡾࠤᵶ").format(bstack11l111111ll_opy_))
    env = os.environ.copy()
    env[bstack1llll1l_opy_ (u"ࠦࡕࡋࡒࡄ࡛ࡢࡘࡔࡑࡅࡏࠤᵷ")] = bstack111ll11l1ll_opy_
    env[bstack1llll1l_opy_ (u"࡚ࠧࡈࡠࡄࡘࡍࡑࡊ࡟ࡖࡗࡌࡈࠧᵸ")] = os.environ.get(bstack1llll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᵹ"), bstack1llll1l_opy_ (u"ࠧࠨᵺ"))
    bstack111ll1l1lll_opy_ = [self.binary_path]
    self.bstack111ll11111l_opy_()
    self.bstack111lll1l1ll_opy_ = self.bstack111l1ll11ll_opy_(bstack111ll1l1lll_opy_ + command_args, env)
    self.logger.debug(bstack1llll1l_opy_ (u"ࠣࡕࡷࡥࡷࡺࡩ࡯ࡩࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠤᵻ"))
    bstack111ll1ll1ll_opy_ = 0
    while self.bstack111lll1l1ll_opy_.poll() == None:
      bstack111l1llllll_opy_ = self.bstack111l1llll11_opy_()
      if bstack111l1llllll_opy_:
        self.logger.debug(bstack1llll1l_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠧᵼ"))
        self.bstack111ll1l11l1_opy_ = True
        return True
      bstack111ll1ll1ll_opy_ += 1
      self.logger.debug(bstack1llll1l_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡕࡩࡹࡸࡹࠡ࠯ࠣࡿࢂࠨᵽ").format(bstack111ll1ll1ll_opy_))
      time.sleep(2)
    self.logger.error(bstack1llll1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡌࡡࡪ࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࢀࢃࠠࡢࡶࡷࡩࡲࡶࡴࡴࠤᵾ").format(bstack111ll1ll1ll_opy_))
    self.bstack111ll1l1l11_opy_ = True
    return False
  def bstack111l1llll11_opy_(self, bstack111ll1ll1ll_opy_ = 0):
    if bstack111ll1ll1ll_opy_ > 10:
      return False
    try:
      bstack111ll1ll111_opy_ = os.environ.get(bstack1llll1l_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡘࡋࡒࡗࡇࡕࡣࡆࡊࡄࡓࡇࡖࡗࠬᵿ"), bstack1llll1l_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵ࠼࠸࠷࠸࠾ࠧᶀ"))
      bstack111lll1l1l1_opy_ = bstack111ll1ll111_opy_ + bstack11ll11lll1l_opy_
      response = requests.get(bstack111lll1l1l1_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1llll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࠭ᶁ"), {}).get(bstack1llll1l_opy_ (u"ࠨ࡫ࡧࠫᶂ"), None)
      return True
    except:
      self.logger.debug(bstack1llll1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣࡻ࡭࡯࡬ࡦࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡨࡦࡣ࡯ࡸ࡭ࠦࡣࡩࡧࡦ࡯ࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᶃ"))
      return False
  def bstack111ll1l1l1l_opy_(self):
    bstack111ll1ll1l1_opy_ = bstack1llll1l_opy_ (u"ࠪࡥࡵࡶࠧᶄ") if self.bstack1lll1llll1_opy_ else bstack1llll1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᶅ")
    bstack111ll111lll_opy_ = bstack1llll1l_opy_ (u"ࠧࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤࠣᶆ") if self.config.get(bstack1llll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᶇ")) is None else True
    bstack11l111llll1_opy_ = bstack1llll1l_opy_ (u"ࠢࡢࡲ࡬࠳ࡦࡶࡰࡠࡲࡨࡶࡨࡿ࠯ࡨࡧࡷࡣࡵࡸ࡯࡫ࡧࡦࡸࡤࡺ࡯࡬ࡧࡱࡃࡳࡧ࡭ࡦ࠿ࡾࢁࠫࡺࡹࡱࡧࡀࡿࢂࠬࡰࡦࡴࡦࡽࡂࢁࡽࠣᶈ").format(self.config[bstack1llll1l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᶉ")], bstack111ll1ll1l1_opy_, bstack111ll111lll_opy_)
    if self.percy_capture_mode:
      bstack11l111llll1_opy_ += bstack1llll1l_opy_ (u"ࠤࠩࡴࡪࡸࡣࡺࡡࡦࡥࡵࡺࡵࡳࡧࡢࡱࡴࡪࡥ࠾ࡽࢀࠦᶊ").format(self.percy_capture_mode)
    uri = bstack1ll1l1l11_opy_(bstack11l111llll1_opy_)
    try:
      response = bstack11lll1l1l1_opy_(bstack1llll1l_opy_ (u"ࠪࡋࡊ࡚ࠧᶋ"), uri, {}, {bstack1llll1l_opy_ (u"ࠫࡦࡻࡴࡩࠩᶌ"): (self.config[bstack1llll1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᶍ")], self.config[bstack1llll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᶎ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11llll11l1_opy_ = data.get(bstack1llll1l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᶏ"))
        self.percy_capture_mode = data.get(bstack1llll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿ࡟ࡤࡣࡳࡸࡺࡸࡥࡠ࡯ࡲࡨࡪ࠭ᶐ"))
        os.environ[bstack1llll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧᶑ")] = str(self.bstack11llll11l1_opy_)
        os.environ[bstack1llll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧᶒ")] = str(self.percy_capture_mode)
        if bstack111ll111lll_opy_ == bstack1llll1l_opy_ (u"ࠦࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠢᶓ") and str(self.bstack11llll11l1_opy_).lower() == bstack1llll1l_opy_ (u"ࠧࡺࡲࡶࡧࠥᶔ"):
          self.bstack1l11llllll_opy_ = True
        if bstack1llll1l_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧᶕ") in data:
          return data[bstack1llll1l_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨᶖ")]
        else:
          raise bstack1llll1l_opy_ (u"ࠨࡖࡲ࡯ࡪࡴࠠࡏࡱࡷࠤࡋࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽࠨᶗ").format(data)
      else:
        raise bstack1llll1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡵ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡹࡴࡢࡶࡸࡷࠥ࠳ࠠࡼࡿ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡂࡰࡦࡼࠤ࠲ࠦࡻࡾࠤᶘ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1llll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡴࡷࡵࡪࡦࡥࡷࠦᶙ").format(e))
  def bstack111ll1l1111_opy_(self):
    bstack111l1l1l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1llll1l_opy_ (u"ࠦࡵ࡫ࡲࡤࡻࡆࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠢᶚ"))
    try:
      if bstack1llll1l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ᶛ") not in self.bstack111lll11lll_opy_:
        self.bstack111lll11lll_opy_[bstack1llll1l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᶜ")] = 2
      with open(bstack111l1l1l1l1_opy_, bstack1llll1l_opy_ (u"ࠧࡸࠩᶝ")) as fp:
        json.dump(self.bstack111lll11lll_opy_, fp)
      return bstack111l1l1l1l1_opy_
    except Exception as e:
      self.logger.error(bstack1llll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡨࡸࡥࡢࡶࡨࠤࡵ࡫ࡲࡤࡻࠣࡧࡴࡴࡦ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᶞ").format(e))
  def bstack111l1ll11ll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111ll11l1l1_opy_ == bstack1llll1l_opy_ (u"ࠩࡺ࡭ࡳ࠭ᶟ"):
        bstack111lll1111l_opy_ = [bstack1llll1l_opy_ (u"ࠪࡧࡲࡪ࠮ࡦࡺࡨࠫᶠ"), bstack1llll1l_opy_ (u"ࠫ࠴ࡩࠧᶡ")]
        cmd = bstack111lll1111l_opy_ + cmd
      cmd = bstack1llll1l_opy_ (u"ࠬࠦࠧᶢ").join(cmd)
      self.logger.debug(bstack1llll1l_opy_ (u"ࠨࡒࡶࡰࡱ࡭ࡳ࡭ࠠࡼࡿࠥᶣ").format(cmd))
      with open(self.bstack111ll111l11_opy_, bstack1llll1l_opy_ (u"ࠢࡢࠤᶤ")) as bstack111ll111l1l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111ll111l1l_opy_, text=True, stderr=bstack111ll111l1l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111ll1l1l11_opy_ = True
      self.logger.error(bstack1llll1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠢࡺ࡭ࡹ࡮ࠠࡤ࡯ࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᶥ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111ll1l11l1_opy_:
        self.logger.info(bstack1llll1l_opy_ (u"ࠤࡖࡸࡴࡶࡰࡪࡰࡪࠤࡕ࡫ࡲࡤࡻࠥᶦ"))
        cmd = [self.binary_path, bstack1llll1l_opy_ (u"ࠥࡩࡽ࡫ࡣ࠻ࡵࡷࡳࡵࠨᶧ")]
        self.bstack111l1ll11ll_opy_(cmd)
        self.bstack111ll1l11l1_opy_ = False
    except Exception as e:
      self.logger.error(bstack1llll1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡲࡴࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᶨ").format(cmd, e))
  def bstack1ll11l11l_opy_(self):
    if not self.bstack11llll11l1_opy_:
      return
    try:
      bstack111l1l1ll11_opy_ = 0
      while not self.bstack111ll1l11l1_opy_ and bstack111l1l1ll11_opy_ < self.bstack111l1ll1l1l_opy_:
        if self.bstack111ll1l1l11_opy_:
          self.logger.info(bstack1llll1l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡪࡦ࡯࡬ࡦࡦࠥᶩ"))
          return
        time.sleep(1)
        bstack111l1l1ll11_opy_ += 1
      os.environ[bstack1llll1l_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤࡈࡅࡔࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࠬᶪ")] = str(self.bstack111ll1111l1_opy_())
      self.logger.info(bstack1llll1l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠣᶫ"))
    except Exception as e:
      self.logger.error(bstack1llll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᶬ").format(e))
  def bstack111ll1111l1_opy_(self):
    if self.bstack1lll1llll1_opy_:
      return
    try:
      bstack111l1lll1ll_opy_ = [platform[bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᶭ")].lower() for platform in self.config.get(bstack1llll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᶮ"), [])]
      bstack111ll11ll1l_opy_ = sys.maxsize
      bstack111ll111111_opy_ = bstack1llll1l_opy_ (u"ࠫࠬᶯ")
      for browser in bstack111l1lll1ll_opy_:
        if browser in self.bstack111ll11lll1_opy_:
          bstack111ll1llll1_opy_ = self.bstack111ll11lll1_opy_[browser]
        if bstack111ll1llll1_opy_ < bstack111ll11ll1l_opy_:
          bstack111ll11ll1l_opy_ = bstack111ll1llll1_opy_
          bstack111ll111111_opy_ = browser
      return bstack111ll111111_opy_
    except Exception as e:
      self.logger.error(bstack1llll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡢࡦࡵࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᶰ").format(e))
  @classmethod
  def bstack1lllllll1l_opy_(self):
    return os.getenv(bstack1llll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࠫᶱ"), bstack1llll1l_opy_ (u"ࠧࡇࡣ࡯ࡷࡪ࠭ᶲ")).lower()
  @classmethod
  def bstack1l11l11l_opy_(self):
    return os.getenv(bstack1llll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬᶳ"), bstack1llll1l_opy_ (u"ࠩࠪᶴ"))
  @classmethod
  def bstack1l1ll111lll_opy_(cls, value):
    cls.bstack1l11llllll_opy_ = value
  @classmethod
  def bstack111ll1lllll_opy_(cls):
    return cls.bstack1l11llllll_opy_
  @classmethod
  def bstack1l1ll1111ll_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack111lll11l11_opy_(cls):
    return cls.percy_build_id