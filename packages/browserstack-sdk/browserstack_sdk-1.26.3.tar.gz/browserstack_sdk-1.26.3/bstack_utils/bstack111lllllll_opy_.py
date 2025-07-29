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
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11lll11lll1_opy_, bstack11lll1llll1_opy_, bstack11lll1l1l1_opy_, bstack111l1l1111_opy_, bstack11l1ll11l1l_opy_, bstack11l1l1l1ll1_opy_, bstack11l11l1ll11_opy_, bstack1l1ll1l1l_opy_, bstack11l11111_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1111lllll1l_opy_ import bstack1111lll1l11_opy_
import bstack_utils.bstack11lll1lll1_opy_ as bstack1lll11ll_opy_
from bstack_utils.bstack11l11111l1_opy_ import bstack1l11l111ll_opy_
import bstack_utils.accessibility as bstack11l1lll1_opy_
from bstack_utils.bstack1ll11l111l_opy_ import bstack1ll11l111l_opy_
from bstack_utils.bstack111lll1ll1_opy_ import bstack111ll1ll11_opy_
bstack1111l11l1l1_opy_ = bstack1llll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬẳ")
logger = logging.getLogger(__name__)
class bstack1llllll1ll_opy_:
    bstack1111lllll1l_opy_ = None
    bs_config = None
    bstack1ll1llll_opy_ = None
    @classmethod
    @bstack111l1l1111_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11ll11ll1ll_opy_, stage=STAGE.bstack11111l1l1_opy_)
    def launch(cls, bs_config, bstack1ll1llll_opy_):
        cls.bs_config = bs_config
        cls.bstack1ll1llll_opy_ = bstack1ll1llll_opy_
        try:
            cls.bstack1111l11ll1l_opy_()
            bstack11llll11lll_opy_ = bstack11lll11lll1_opy_(bs_config)
            bstack11lll1111ll_opy_ = bstack11lll1llll1_opy_(bs_config)
            data = bstack1lll11ll_opy_.bstack1111l11111l_opy_(bs_config, bstack1ll1llll_opy_)
            config = {
                bstack1llll1l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫẴ"): (bstack11llll11lll_opy_, bstack11lll1111ll_opy_),
                bstack1llll1l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨẵ"): cls.default_headers()
            }
            response = bstack11lll1l1l1_opy_(bstack1llll1l_opy_ (u"ࠨࡒࡒࡗ࡙࠭Ặ"), cls.request_url(bstack1llll1l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠳࠱ࡥࡹ࡮ࡲࡤࡴࠩặ")), data, config)
            if response.status_code != 200:
                bstack1lll111l1l_opy_ = response.json()
                if bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫẸ")] == False:
                    cls.bstack1111l1111l1_opy_(bstack1lll111l1l_opy_)
                    return
                cls.bstack11111lll11l_opy_(bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫẹ")])
                cls.bstack1111l1111ll_opy_(bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬẺ")])
                return None
            bstack1111l1l111l_opy_ = cls.bstack1111l111111_opy_(response)
            return bstack1111l1l111l_opy_, response.json()
        except Exception as error:
            logger.error(bstack1llll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡽࢀࠦẻ").format(str(error)))
            return None
    @classmethod
    @bstack111l1l1111_opy_(class_method=True)
    def stop(cls, bstack1111l111ll1_opy_=None):
        if not bstack1l11l111ll_opy_.on() and not bstack11l1lll1_opy_.on():
            return
        if os.environ.get(bstack1llll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫẼ")) == bstack1llll1l_opy_ (u"ࠣࡰࡸࡰࡱࠨẽ") or os.environ.get(bstack1llll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧẾ")) == bstack1llll1l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣế"):
            logger.error(bstack1llll1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧỀ"))
            return {
                bstack1llll1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬề"): bstack1llll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬỂ"),
                bstack1llll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨể"): bstack1llll1l_opy_ (u"ࠨࡖࡲ࡯ࡪࡴ࠯ࡣࡷ࡬ࡰࡩࡏࡄࠡ࡫ࡶࠤࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠬࠡࡤࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡰ࡭࡬࡮ࡴࠡࡪࡤࡺࡪࠦࡦࡢ࡫࡯ࡩࡩ࠭Ễ")
            }
        try:
            cls.bstack1111lllll1l_opy_.shutdown()
            data = {
                bstack1llll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧễ"): bstack1l1ll1l1l_opy_()
            }
            if not bstack1111l111ll1_opy_ is None:
                data[bstack1llll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡳࡥࡵࡣࡧࡥࡹࡧࠧỆ")] = [{
                    bstack1llll1l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫệ"): bstack1llll1l_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦࠪỈ"),
                    bstack1llll1l_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭ỉ"): bstack1111l111ll1_opy_
                }]
            config = {
                bstack1llll1l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨỊ"): cls.default_headers()
            }
            bstack11l111llll1_opy_ = bstack1llll1l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸࡺ࡯ࡱࠩị").format(os.environ[bstack1llll1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢỌ")])
            bstack1111l1l1111_opy_ = cls.request_url(bstack11l111llll1_opy_)
            response = bstack11lll1l1l1_opy_(bstack1llll1l_opy_ (u"ࠪࡔ࡚࡚ࠧọ"), bstack1111l1l1111_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1llll1l_opy_ (u"ࠦࡘࡺ࡯ࡱࠢࡵࡩࡶࡻࡥࡴࡶࠣࡲࡴࡺࠠࡰ࡭ࠥỎ"))
        except Exception as error:
            logger.error(bstack1llll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀ࠺ࠡࠤỏ") + str(error))
            return {
                bstack1llll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭Ố"): bstack1llll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ố"),
                bstack1llll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩỒ"): str(error)
            }
    @classmethod
    @bstack111l1l1111_opy_(class_method=True)
    def bstack1111l111111_opy_(cls, response):
        bstack1lll111l1l_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1111l1l111l_opy_ = {}
        if bstack1lll111l1l_opy_.get(bstack1llll1l_opy_ (u"ࠩ࡭ࡻࡹ࠭ồ")) is None:
            os.environ[bstack1llll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧỔ")] = bstack1llll1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩổ")
        else:
            os.environ[bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩỖ")] = bstack1lll111l1l_opy_.get(bstack1llll1l_opy_ (u"࠭ࡪࡸࡶࠪỗ"), bstack1llll1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬỘ"))
        os.environ[bstack1llll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ộ")] = bstack1lll111l1l_opy_.get(bstack1llll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫỚ"), bstack1llll1l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨớ"))
        logger.info(bstack1llll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡪࡸࡦࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࠩỜ") + os.getenv(bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪờ")));
        if bstack1l11l111ll_opy_.bstack11111llll11_opy_(cls.bs_config, cls.bstack1ll1llll_opy_.get(bstack1llll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧỞ"), bstack1llll1l_opy_ (u"ࠧࠨở"))) is True:
            bstack1111lll111l_opy_, build_hashed_id, bstack1111l11llll_opy_ = cls.bstack11111lllll1_opy_(bstack1lll111l1l_opy_)
            if bstack1111lll111l_opy_ != None and build_hashed_id != None:
                bstack1111l1l111l_opy_[bstack1llll1l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨỠ")] = {
                    bstack1llll1l_opy_ (u"ࠩ࡭ࡻࡹࡥࡴࡰ࡭ࡨࡲࠬỡ"): bstack1111lll111l_opy_,
                    bstack1llll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬỢ"): build_hashed_id,
                    bstack1llll1l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨợ"): bstack1111l11llll_opy_
                }
            else:
                bstack1111l1l111l_opy_[bstack1llll1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬỤ")] = {}
        else:
            bstack1111l1l111l_opy_[bstack1llll1l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ụ")] = {}
        bstack1111l11ll11_opy_, build_hashed_id = cls.bstack1111l1l11ll_opy_(bstack1lll111l1l_opy_)
        if bstack1111l11ll11_opy_ != None and build_hashed_id != None:
            bstack1111l1l111l_opy_[bstack1llll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧỦ")] = {
                bstack1llll1l_opy_ (u"ࠨࡣࡸࡸ࡭ࡥࡴࡰ࡭ࡨࡲࠬủ"): bstack1111l11ll11_opy_,
                bstack1llll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫỨ"): build_hashed_id,
            }
        else:
            bstack1111l1l111l_opy_[bstack1llll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪứ")] = {}
        if bstack1111l1l111l_opy_[bstack1llll1l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫỪ")].get(bstack1llll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧừ")) != None or bstack1111l1l111l_opy_[bstack1llll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ử")].get(bstack1llll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩử")) != None:
            cls.bstack1111l111lll_opy_(bstack1lll111l1l_opy_.get(bstack1llll1l_opy_ (u"ࠨ࡬ࡺࡸࠬỮ")), bstack1lll111l1l_opy_.get(bstack1llll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫữ")))
        return bstack1111l1l111l_opy_
    @classmethod
    def bstack11111lllll1_opy_(cls, bstack1lll111l1l_opy_):
        if bstack1lll111l1l_opy_.get(bstack1llll1l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪỰ")) == None:
            cls.bstack11111lll11l_opy_()
            return [None, None, None]
        if bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫự")][bstack1llll1l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭Ỳ")] != True:
            cls.bstack11111lll11l_opy_(bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ỳ")])
            return [None, None, None]
        logger.debug(bstack1llll1l_opy_ (u"ࠧࡕࡧࡶࡸࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫỴ"))
        os.environ[bstack1llll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧỵ")] = bstack1llll1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧỶ")
        if bstack1lll111l1l_opy_.get(bstack1llll1l_opy_ (u"ࠪ࡮ࡼࡺࠧỷ")):
            os.environ[bstack1llll1l_opy_ (u"ࠫࡈࡘࡅࡅࡇࡑࡘࡎࡇࡌࡔࡡࡉࡓࡗࡥࡃࡓࡃࡖࡌࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨỸ")] = json.dumps({
                bstack1llll1l_opy_ (u"ࠬࡻࡳࡦࡴࡱࡥࡲ࡫ࠧỹ"): bstack11lll11lll1_opy_(cls.bs_config),
                bstack1llll1l_opy_ (u"࠭ࡰࡢࡵࡶࡻࡴࡸࡤࠨỺ"): bstack11lll1llll1_opy_(cls.bs_config)
            })
        if bstack1lll111l1l_opy_.get(bstack1llll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩỻ")):
            os.environ[bstack1llll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧỼ")] = bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫỽ")]
        if bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪỾ")].get(bstack1llll1l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬỿ"), {}).get(bstack1llll1l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩἀ")):
            os.environ[bstack1llll1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧἁ")] = str(bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧἂ")][bstack1llll1l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩἃ")][bstack1llll1l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ἄ")])
        else:
            os.environ[bstack1llll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫἅ")] = bstack1llll1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤἆ")
        return [bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"ࠬࡰࡷࡵࠩἇ")], bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨἈ")], os.environ[bstack1llll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨἉ")]]
    @classmethod
    def bstack1111l1l11ll_opy_(cls, bstack1lll111l1l_opy_):
        if bstack1lll111l1l_opy_.get(bstack1llll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨἊ")) == None:
            cls.bstack1111l1111ll_opy_()
            return [None, None]
        if bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩἋ")][bstack1llll1l_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫἌ")] != True:
            cls.bstack1111l1111ll_opy_(bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫἍ")])
            return [None, None]
        if bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬἎ")].get(bstack1llll1l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧἏ")):
            logger.debug(bstack1llll1l_opy_ (u"ࠧࡕࡧࡶࡸࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫἐ"))
            parsed = json.loads(os.getenv(bstack1llll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩἑ"), bstack1llll1l_opy_ (u"ࠩࡾࢁࠬἒ")))
            capabilities = bstack1lll11ll_opy_.bstack11111llllll_opy_(bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪἓ")][bstack1llll1l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬἔ")][bstack1llll1l_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫἕ")], bstack1llll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ἖"), bstack1llll1l_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭἗"))
            bstack1111l11ll11_opy_ = capabilities[bstack1llll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭Ἐ")]
            os.environ[bstack1llll1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧἙ")] = bstack1111l11ll11_opy_
            if bstack1llll1l_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧἚ") in bstack1lll111l1l_opy_ and bstack1lll111l1l_opy_.get(bstack1llll1l_opy_ (u"ࠦࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠥἛ")) is None:
                parsed[bstack1llll1l_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ἔ")] = capabilities[bstack1llll1l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧἝ")]
            os.environ[bstack1llll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ἞")] = json.dumps(parsed)
            scripts = bstack1lll11ll_opy_.bstack11111llllll_opy_(bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ἟")][bstack1llll1l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪἠ")][bstack1llll1l_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫἡ")], bstack1llll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩἢ"), bstack1llll1l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࠭ἣ"))
            bstack1ll11l111l_opy_.bstack1l111lll1l_opy_(scripts)
            commands = bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ἤ")][bstack1llll1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨἥ")][bstack1llll1l_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠩἦ")].get(bstack1llll1l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫἧ"))
            bstack1ll11l111l_opy_.bstack11llll1l11l_opy_(commands)
            bstack11lll1l11l1_opy_ = capabilities.get(bstack1llll1l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨἨ"))
            bstack1ll11l111l_opy_.bstack11ll1llll11_opy_(bstack11lll1l11l1_opy_)
            bstack1ll11l111l_opy_.store()
        return [bstack1111l11ll11_opy_, bstack1lll111l1l_opy_[bstack1llll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭Ἡ")]]
    @classmethod
    def bstack11111lll11l_opy_(cls, response=None):
        os.environ[bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪἪ")] = bstack1llll1l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫἫ")
        os.environ[bstack1llll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫἬ")] = bstack1llll1l_opy_ (u"ࠨࡰࡸࡰࡱ࠭Ἥ")
        os.environ[bstack1llll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨἮ")] = bstack1llll1l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩἯ")
        os.environ[bstack1llll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪἰ")] = bstack1llll1l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥἱ")
        os.environ[bstack1llll1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧἲ")] = bstack1llll1l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧἳ")
        cls.bstack1111l1111l1_opy_(response, bstack1llll1l_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣἴ"))
        return [None, None, None]
    @classmethod
    def bstack1111l1111ll_opy_(cls, response=None):
        os.environ[bstack1llll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧἵ")] = bstack1llll1l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨἶ")
        os.environ[bstack1llll1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩἷ")] = bstack1llll1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪἸ")
        os.environ[bstack1llll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪἹ")] = bstack1llll1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬἺ")
        cls.bstack1111l1111l1_opy_(response, bstack1llll1l_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣἻ"))
        return [None, None, None]
    @classmethod
    def bstack1111l111lll_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1llll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ἴ")] = jwt
        os.environ[bstack1llll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨἽ")] = build_hashed_id
    @classmethod
    def bstack1111l1111l1_opy_(cls, response=None, product=bstack1llll1l_opy_ (u"ࠦࠧἾ")):
        if response == None or response.get(bstack1llll1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬἿ")) == None:
            logger.error(product + bstack1llll1l_opy_ (u"ࠨࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠣὀ"))
            return
        for error in response[bstack1llll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧὁ")]:
            bstack11l1l11l111_opy_ = error[bstack1llll1l_opy_ (u"ࠨ࡭ࡨࡽࠬὂ")]
            error_message = error[bstack1llll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪὃ")]
            if error_message:
                if bstack11l1l11l111_opy_ == bstack1llll1l_opy_ (u"ࠥࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠤὄ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1llll1l_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࠧὅ") + product + bstack1llll1l_opy_ (u"ࠧࠦࡦࡢ࡫࡯ࡩࡩࠦࡤࡶࡧࠣࡸࡴࠦࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥ὆"))
    @classmethod
    def bstack1111l11ll1l_opy_(cls):
        if cls.bstack1111lllll1l_opy_ is not None:
            return
        cls.bstack1111lllll1l_opy_ = bstack1111lll1l11_opy_(cls.bstack1111l11l11l_opy_)
        cls.bstack1111lllll1l_opy_.start()
    @classmethod
    def bstack111ll1l111_opy_(cls):
        if cls.bstack1111lllll1l_opy_ is None:
            return
        cls.bstack1111lllll1l_opy_.shutdown()
    @classmethod
    @bstack111l1l1111_opy_(class_method=True)
    def bstack1111l11l11l_opy_(cls, bstack111l1ll111_opy_, event_url=bstack1llll1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬ὇")):
        config = {
            bstack1llll1l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨὈ"): cls.default_headers()
        }
        logger.debug(bstack1llll1l_opy_ (u"ࠣࡲࡲࡷࡹࡥࡤࡢࡶࡤ࠾࡙ࠥࡥ࡯ࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡹࡵࠠࡵࡧࡶࡸ࡭ࡻࡢࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࡷࠥࢁࡽࠣὉ").format(bstack1llll1l_opy_ (u"ࠩ࠯ࠤࠬὊ").join([event[bstack1llll1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧὋ")] for event in bstack111l1ll111_opy_])))
        response = bstack11lll1l1l1_opy_(bstack1llll1l_opy_ (u"ࠫࡕࡕࡓࡕࠩὌ"), cls.request_url(event_url), bstack111l1ll111_opy_, config)
        bstack11lll111lll_opy_ = response.json()
    @classmethod
    def bstack1l1ll11111_opy_(cls, bstack111l1ll111_opy_, event_url=bstack1llll1l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫὍ")):
        logger.debug(bstack1llll1l_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡥࡩࡪࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨ὎").format(bstack111l1ll111_opy_[bstack1llll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ὏")]))
        if not bstack1lll11ll_opy_.bstack11111lll1ll_opy_(bstack111l1ll111_opy_[bstack1llll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬὐ")]):
            logger.debug(bstack1llll1l_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡎࡰࡶࠣࡥࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢὑ").format(bstack111l1ll111_opy_[bstack1llll1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧὒ")]))
            return
        bstack11l1l1llll_opy_ = bstack1lll11ll_opy_.bstack1111l11l111_opy_(bstack111l1ll111_opy_[bstack1llll1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨὓ")], bstack111l1ll111_opy_.get(bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧὔ")))
        if bstack11l1l1llll_opy_ != None:
            if bstack111l1ll111_opy_.get(bstack1llll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨὕ")) != None:
                bstack111l1ll111_opy_[bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩὖ")][bstack1llll1l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ὗ")] = bstack11l1l1llll_opy_
            else:
                bstack111l1ll111_opy_[bstack1llll1l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ὘")] = bstack11l1l1llll_opy_
        if event_url == bstack1llll1l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩὙ"):
            cls.bstack1111l11ll1l_opy_()
            logger.debug(bstack1llll1l_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡃࡧࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢ὚").format(bstack111l1ll111_opy_[bstack1llll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩὛ")]))
            cls.bstack1111lllll1l_opy_.add(bstack111l1ll111_opy_)
        elif event_url == bstack1llll1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ὜"):
            cls.bstack1111l11l11l_opy_([bstack111l1ll111_opy_], event_url)
    @classmethod
    @bstack111l1l1111_opy_(class_method=True)
    def bstack111l1l11l_opy_(cls, logs):
        bstack1111l11l1ll_opy_ = []
        for log in logs:
            bstack11111llll1l_opy_ = {
                bstack1llll1l_opy_ (u"ࠧ࡬࡫ࡱࡨࠬὝ"): bstack1llll1l_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡌࡐࡉࠪ὞"),
                bstack1llll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨὟ"): log[bstack1llll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩὠ")],
                bstack1llll1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧὡ"): log[bstack1llll1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨὢ")],
                bstack1llll1l_opy_ (u"࠭ࡨࡵࡶࡳࡣࡷ࡫ࡳࡱࡱࡱࡷࡪ࠭ὣ"): {},
                bstack1llll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨὤ"): log[bstack1llll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩὥ")],
            }
            if bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩὦ") in log:
                bstack11111llll1l_opy_[bstack1llll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪὧ")] = log[bstack1llll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫὨ")]
            elif bstack1llll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬὩ") in log:
                bstack11111llll1l_opy_[bstack1llll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ὢ")] = log[bstack1llll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧὫ")]
            bstack1111l11l1ll_opy_.append(bstack11111llll1l_opy_)
        cls.bstack1l1ll11111_opy_({
            bstack1llll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬὬ"): bstack1llll1l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭Ὥ"),
            bstack1llll1l_opy_ (u"ࠪࡰࡴ࡭ࡳࠨὮ"): bstack1111l11l1ll_opy_
        })
    @classmethod
    @bstack111l1l1111_opy_(class_method=True)
    def bstack1111l111l1l_opy_(cls, steps):
        bstack1111l111l11_opy_ = []
        for step in steps:
            bstack11111lll1l1_opy_ = {
                bstack1llll1l_opy_ (u"ࠫࡰ࡯࡮ࡥࠩὯ"): bstack1llll1l_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨὰ"),
                bstack1llll1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬά"): step[bstack1llll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ὲ")],
                bstack1llll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫέ"): step[bstack1llll1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬὴ")],
                bstack1llll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫή"): step[bstack1llll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬὶ")],
                bstack1llll1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧί"): step[bstack1llll1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨὸ")]
            }
            if bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧό") in step:
                bstack11111lll1l1_opy_[bstack1llll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨὺ")] = step[bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩύ")]
            elif bstack1llll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪὼ") in step:
                bstack11111lll1l1_opy_[bstack1llll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫώ")] = step[bstack1llll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ὾")]
            bstack1111l111l11_opy_.append(bstack11111lll1l1_opy_)
        cls.bstack1l1ll11111_opy_({
            bstack1llll1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ὿"): bstack1llll1l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᾀ"),
            bstack1llll1l_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ᾁ"): bstack1111l111l11_opy_
        })
    @classmethod
    @bstack111l1l1111_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1lll11l11_opy_, stage=STAGE.bstack11111l1l1_opy_)
    def bstack111l1ll11_opy_(cls, screenshot):
        cls.bstack1l1ll11111_opy_({
            bstack1llll1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᾂ"): bstack1llll1l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᾃ"),
            bstack1llll1l_opy_ (u"ࠫࡱࡵࡧࡴࠩᾄ"): [{
                bstack1llll1l_opy_ (u"ࠬࡱࡩ࡯ࡦࠪᾅ"): bstack1llll1l_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨᾆ"),
                bstack1llll1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᾇ"): datetime.datetime.utcnow().isoformat() + bstack1llll1l_opy_ (u"ࠨ࡜ࠪᾈ"),
                bstack1llll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᾉ"): screenshot[bstack1llll1l_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩᾊ")],
                bstack1llll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᾋ"): screenshot[bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᾌ")]
            }]
        }, event_url=bstack1llll1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᾍ"))
    @classmethod
    @bstack111l1l1111_opy_(class_method=True)
    def bstack11ll1l11l1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l1ll11111_opy_({
            bstack1llll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᾎ"): bstack1llll1l_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬᾏ"),
            bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᾐ"): {
                bstack1llll1l_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᾑ"): cls.current_test_uuid(),
                bstack1llll1l_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥᾒ"): cls.bstack11l1111111_opy_(driver)
            }
        })
    @classmethod
    def bstack111ll1lll1_opy_(cls, event: str, bstack111l1ll111_opy_: bstack111ll1ll11_opy_):
        bstack111l11l11l_opy_ = {
            bstack1llll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᾓ"): event,
            bstack111l1ll111_opy_.bstack111ll1111l_opy_(): bstack111l1ll111_opy_.bstack111l1l1lll_opy_(event)
        }
        cls.bstack1l1ll11111_opy_(bstack111l11l11l_opy_)
        result = getattr(bstack111l1ll111_opy_, bstack1llll1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᾔ"), None)
        if event == bstack1llll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᾕ"):
            threading.current_thread().bstackTestMeta = {bstack1llll1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᾖ"): bstack1llll1l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᾗ")}
        elif event == bstack1llll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᾘ"):
            threading.current_thread().bstackTestMeta = {bstack1llll1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᾙ"): getattr(result, bstack1llll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᾚ"), bstack1llll1l_opy_ (u"࠭ࠧᾛ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1llll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᾜ"), None) is None or os.environ[bstack1llll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᾝ")] == bstack1llll1l_opy_ (u"ࠤࡱࡹࡱࡲࠢᾞ")) and (os.environ.get(bstack1llll1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᾟ"), None) is None or os.environ[bstack1llll1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᾠ")] == bstack1llll1l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᾡ")):
            return False
        return True
    @staticmethod
    def bstack1111l11lll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1llllll1ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1llll1l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬᾢ"): bstack1llll1l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪᾣ"),
            bstack1llll1l_opy_ (u"ࠨ࡚࠰ࡆࡘ࡚ࡁࡄࡍ࠰ࡘࡊ࡙ࡔࡐࡒࡖࠫᾤ"): bstack1llll1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᾥ")
        }
        if os.environ.get(bstack1llll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᾦ"), None):
            headers[bstack1llll1l_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫᾧ")] = bstack1llll1l_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨᾨ").format(os.environ[bstack1llll1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠥᾩ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1llll1l_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ᾪ").format(bstack1111l11l1l1_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1llll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᾫ"), None)
    @staticmethod
    def bstack11l1111111_opy_(driver):
        return {
            bstack11l1ll11l1l_opy_(): bstack11l1l1l1ll1_opy_(driver)
        }
    @staticmethod
    def bstack1111l1l11l1_opy_(exception_info, report):
        return [{bstack1llll1l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᾬ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111l11l11_opy_(typename):
        if bstack1llll1l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᾭ") in typename:
            return bstack1llll1l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᾮ")
        return bstack1llll1l_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᾯ")