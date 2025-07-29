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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111l1ll1l1_opy_ import RobotHandler
from bstack_utils.capture import bstack111lll11ll_opy_
from bstack_utils.bstack111lll1ll1_opy_ import bstack111ll1ll11_opy_, bstack111lllll11_opy_, bstack11l111111l_opy_
from bstack_utils.bstack11l11111l1_opy_ import bstack1l11l111ll_opy_
from bstack_utils.bstack111lllllll_opy_ import bstack1llllll1ll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11l11111_opy_, bstack1l1ll1l1l_opy_, Result, \
    bstack111l1l1111_opy_, bstack111ll11ll1_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1llll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ༲"): [],
        bstack1llll1l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ༳"): [],
        bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ༴"): []
    }
    bstack111ll11l1l_opy_ = []
    bstack111l11ll1l_opy_ = []
    @staticmethod
    def bstack111lll1111_opy_(log):
        if not ((isinstance(log[bstack1llll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦ༵ࠩ")], list) or (isinstance(log[bstack1llll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༶")], dict)) and len(log[bstack1llll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨ༷ࠫ")])>0) or (isinstance(log[bstack1llll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༸")], str) and log[bstack1llll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ༹࠭")].strip())):
            return
        active = bstack1l11l111ll_opy_.bstack111llll1ll_opy_()
        log = {
            bstack1llll1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ༺"): log[bstack1llll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭༻")],
            bstack1llll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ༼"): bstack111ll11ll1_opy_().isoformat() + bstack1llll1l_opy_ (u"ࠩ࡝ࠫ༽"),
            bstack1llll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༾"): log[bstack1llll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༿")],
        }
        if active:
            if active[bstack1llll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪཀ")] == bstack1llll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫཁ"):
                log[bstack1llll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧག")] = active[bstack1llll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨགྷ")]
            elif active[bstack1llll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧང")] == bstack1llll1l_opy_ (u"ࠪࡸࡪࡹࡴࠨཅ"):
                log[bstack1llll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫཆ")] = active[bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬཇ")]
        bstack1llllll1ll_opy_.bstack111l1l11l_opy_([log])
    def __init__(self):
        self.messages = bstack111l1l11l1_opy_()
        self._111ll1ll1l_opy_ = None
        self._111ll11111_opy_ = None
        self._111l1l111l_opy_ = OrderedDict()
        self.bstack11l1111ll1_opy_ = bstack111lll11ll_opy_(self.bstack111lll1111_opy_)
    @bstack111l1l1111_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1111lllll1_opy_()
        if not self._111l1l111l_opy_.get(attrs.get(bstack1llll1l_opy_ (u"࠭ࡩࡥࠩ཈")), None):
            self._111l1l111l_opy_[attrs.get(bstack1llll1l_opy_ (u"ࠧࡪࡦࠪཉ"))] = {}
        bstack111ll111l1_opy_ = bstack11l111111l_opy_(
                bstack111l11lll1_opy_=attrs.get(bstack1llll1l_opy_ (u"ࠨ࡫ࡧࠫཊ")),
                name=name,
                started_at=bstack1l1ll1l1l_opy_(),
                file_path=os.path.relpath(attrs[bstack1llll1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩཋ")], start=os.getcwd()) if attrs.get(bstack1llll1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪཌ")) != bstack1llll1l_opy_ (u"ࠫࠬཌྷ") else bstack1llll1l_opy_ (u"ࠬ࠭ཎ"),
                framework=bstack1llll1l_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬཏ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1llll1l_opy_ (u"ࠧࡪࡦࠪཐ"), None)
        self._111l1l111l_opy_[attrs.get(bstack1llll1l_opy_ (u"ࠨ࡫ࡧࠫད"))][bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬདྷ")] = bstack111ll111l1_opy_
    @bstack111l1l1111_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111ll1l11l_opy_()
        self._111l1lll1l_opy_(messages)
        for bstack111ll1l1l1_opy_ in self.bstack111ll11l1l_opy_:
            bstack111ll1l1l1_opy_[bstack1llll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬན")][bstack1llll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪཔ")].extend(self.store[bstack1llll1l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫཕ")])
            bstack1llllll1ll_opy_.bstack1l1ll11111_opy_(bstack111ll1l1l1_opy_)
        self.bstack111ll11l1l_opy_ = []
        self.store[bstack1llll1l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬབ")] = []
    @bstack111l1l1111_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11l1111ll1_opy_.start()
        if not self._111l1l111l_opy_.get(attrs.get(bstack1llll1l_opy_ (u"ࠧࡪࡦࠪབྷ")), None):
            self._111l1l111l_opy_[attrs.get(bstack1llll1l_opy_ (u"ࠨ࡫ࡧࠫམ"))] = {}
        driver = bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨཙ"), None)
        bstack111lll1ll1_opy_ = bstack11l111111l_opy_(
            bstack111l11lll1_opy_=attrs.get(bstack1llll1l_opy_ (u"ࠪ࡭ࡩ࠭ཚ")),
            name=name,
            started_at=bstack1l1ll1l1l_opy_(),
            file_path=os.path.relpath(attrs[bstack1llll1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫཛ")], start=os.getcwd()),
            scope=RobotHandler.bstack111l1ll1ll_opy_(attrs.get(bstack1llll1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬཛྷ"), None)),
            framework=bstack1llll1l_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬཝ"),
            tags=attrs[bstack1llll1l_opy_ (u"ࠧࡵࡣࡪࡷࠬཞ")],
            hooks=self.store[bstack1llll1l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧཟ")],
            bstack11l1111l11_opy_=bstack1llllll1ll_opy_.bstack11l1111111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1llll1l_opy_ (u"ࠤࡾࢁࠥࡢ࡮ࠡࡽࢀࠦའ").format(bstack1llll1l_opy_ (u"ࠥࠤࠧཡ").join(attrs[bstack1llll1l_opy_ (u"ࠫࡹࡧࡧࡴࠩར")]), name) if attrs[bstack1llll1l_opy_ (u"ࠬࡺࡡࡨࡵࠪལ")] else name
        )
        self._111l1l111l_opy_[attrs.get(bstack1llll1l_opy_ (u"࠭ࡩࡥࠩཤ"))][bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪཥ")] = bstack111lll1ll1_opy_
        threading.current_thread().current_test_uuid = bstack111lll1ll1_opy_.bstack111l1l1ll1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1llll1l_opy_ (u"ࠨ࡫ࡧࠫས"), None)
        self.bstack111ll1lll1_opy_(bstack1llll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪཧ"), bstack111lll1ll1_opy_)
    @bstack111l1l1111_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11l1111ll1_opy_.reset()
        bstack111l111lll_opy_ = bstack111l111111_opy_.get(attrs.get(bstack1llll1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪཨ")), bstack1llll1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬཀྵ"))
        self._111l1l111l_opy_[attrs.get(bstack1llll1l_opy_ (u"ࠬ࡯ࡤࠨཪ"))][bstack1llll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩཫ")].stop(time=bstack1l1ll1l1l_opy_(), duration=int(attrs.get(bstack1llll1l_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬཬ"), bstack1llll1l_opy_ (u"ࠨ࠲ࠪ཭"))), result=Result(result=bstack111l111lll_opy_, exception=attrs.get(bstack1llll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ཮")), bstack111ll1llll_opy_=[attrs.get(bstack1llll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ཯"))]))
        self.bstack111ll1lll1_opy_(bstack1llll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭཰"), self._111l1l111l_opy_[attrs.get(bstack1llll1l_opy_ (u"ࠬ࡯ࡤࠨཱ"))][bstack1llll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢིࠩ")], True)
        self.store[bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶཱིࠫ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack111l1l1111_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1111lllll1_opy_()
        current_test_id = bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦུࠪ"), None)
        bstack111l1l1l1l_opy_ = current_test_id if bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧཱུࠫ"), None) else bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ྲྀ"), None)
        if attrs.get(bstack1llll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩཷ"), bstack1llll1l_opy_ (u"ࠬ࠭ླྀ")).lower() in [bstack1llll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬཹ"), bstack1llll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ེࠩ")]:
            hook_type = bstack111l111ll1_opy_(attrs.get(bstack1llll1l_opy_ (u"ࠨࡶࡼࡴࡪཻ࠭")), bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩོ࠭"), None))
            hook_name = bstack1llll1l_opy_ (u"ࠪࡿࢂཽ࠭").format(attrs.get(bstack1llll1l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫཾ"), bstack1llll1l_opy_ (u"ࠬ࠭ཿ")))
            if hook_type in [bstack1llll1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎྀࠪ"), bstack1llll1l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎཱྀࠪ")]:
                hook_name = bstack1llll1l_opy_ (u"ࠨ࡝ࡾࢁࡢࠦࡻࡾࠩྂ").format(bstack111l1111l1_opy_.get(hook_type), attrs.get(bstack1llll1l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩྃ"), bstack1llll1l_opy_ (u"྄ࠪࠫ")))
            bstack111l1l11ll_opy_ = bstack111lllll11_opy_(
                bstack111l11lll1_opy_=bstack111l1l1l1l_opy_ + bstack1llll1l_opy_ (u"ࠫ࠲࠭྅") + attrs.get(bstack1llll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪ྆"), bstack1llll1l_opy_ (u"࠭ࠧ྇")).lower(),
                name=hook_name,
                started_at=bstack1l1ll1l1l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1llll1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧྈ")), start=os.getcwd()),
                framework=bstack1llll1l_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧྉ"),
                tags=attrs[bstack1llll1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧྊ")],
                scope=RobotHandler.bstack111l1ll1ll_opy_(attrs.get(bstack1llll1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪྋ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111l1l11ll_opy_.bstack111l1l1ll1_opy_()
            threading.current_thread().current_hook_id = bstack111l1l1l1l_opy_ + bstack1llll1l_opy_ (u"ࠫ࠲࠭ྌ") + attrs.get(bstack1llll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪྍ"), bstack1llll1l_opy_ (u"࠭ࠧྎ")).lower()
            self.store[bstack1llll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫྏ")] = [bstack111l1l11ll_opy_.bstack111l1l1ll1_opy_()]
            if bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬྐ"), None):
                self.store[bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ྑ")].append(bstack111l1l11ll_opy_.bstack111l1l1ll1_opy_())
            else:
                self.store[bstack1llll1l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩྒ")].append(bstack111l1l11ll_opy_.bstack111l1l1ll1_opy_())
            if bstack111l1l1l1l_opy_:
                self._111l1l111l_opy_[bstack111l1l1l1l_opy_ + bstack1llll1l_opy_ (u"ࠫ࠲࠭ྒྷ") + attrs.get(bstack1llll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪྔ"), bstack1llll1l_opy_ (u"࠭ࠧྕ")).lower()] = { bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪྖ"): bstack111l1l11ll_opy_ }
            bstack1llllll1ll_opy_.bstack111ll1lll1_opy_(bstack1llll1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩྗ"), bstack111l1l11ll_opy_)
        else:
            bstack111llll111_opy_ = {
                bstack1llll1l_opy_ (u"ࠩ࡬ࡨࠬ྘"): uuid4().__str__(),
                bstack1llll1l_opy_ (u"ࠪࡸࡪࡾࡴࠨྙ"): bstack1llll1l_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪྚ").format(attrs.get(bstack1llll1l_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬྛ")), attrs.get(bstack1llll1l_opy_ (u"࠭ࡡࡳࡩࡶࠫྜ"), bstack1llll1l_opy_ (u"ࠧࠨྜྷ"))) if attrs.get(bstack1llll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ྞ"), []) else attrs.get(bstack1llll1l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩྟ")),
                bstack1llll1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪྠ"): attrs.get(bstack1llll1l_opy_ (u"ࠫࡦࡸࡧࡴࠩྡ"), []),
                bstack1llll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩྡྷ"): bstack1l1ll1l1l_opy_(),
                bstack1llll1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ྣ"): bstack1llll1l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨྤ"),
                bstack1llll1l_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ྥ"): attrs.get(bstack1llll1l_opy_ (u"ࠩࡧࡳࡨ࠭ྦ"), bstack1llll1l_opy_ (u"ࠪࠫྦྷ"))
            }
            if attrs.get(bstack1llll1l_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬྨ"), bstack1llll1l_opy_ (u"ࠬ࠭ྩ")) != bstack1llll1l_opy_ (u"࠭ࠧྪ"):
                bstack111llll111_opy_[bstack1llll1l_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨྫ")] = attrs.get(bstack1llll1l_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩྫྷ"))
            if not self.bstack111l11ll1l_opy_:
                self._111l1l111l_opy_[self._111ll11l11_opy_()][bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬྭ")].add_step(bstack111llll111_opy_)
                threading.current_thread().current_step_uuid = bstack111llll111_opy_[bstack1llll1l_opy_ (u"ࠪ࡭ࡩ࠭ྮ")]
            self.bstack111l11ll1l_opy_.append(bstack111llll111_opy_)
    @bstack111l1l1111_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111ll1l11l_opy_()
        self._111l1lll1l_opy_(messages)
        current_test_id = bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ྯ"), None)
        bstack111l1l1l1l_opy_ = current_test_id if current_test_id else bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨྰ"), None)
        bstack111l11l1l1_opy_ = bstack111l111111_opy_.get(attrs.get(bstack1llll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ྱ")), bstack1llll1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨྲ"))
        bstack111l111l11_opy_ = attrs.get(bstack1llll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩླ"))
        if bstack111l11l1l1_opy_ != bstack1llll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪྴ") and not attrs.get(bstack1llll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྵ")) and self._111ll1ll1l_opy_:
            bstack111l111l11_opy_ = self._111ll1ll1l_opy_
        bstack11l1111l1l_opy_ = Result(result=bstack111l11l1l1_opy_, exception=bstack111l111l11_opy_, bstack111ll1llll_opy_=[bstack111l111l11_opy_])
        if attrs.get(bstack1llll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩྶ"), bstack1llll1l_opy_ (u"ࠬ࠭ྷ")).lower() in [bstack1llll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬྸ"), bstack1llll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩྐྵ")]:
            bstack111l1l1l1l_opy_ = current_test_id if current_test_id else bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫྺ"), None)
            if bstack111l1l1l1l_opy_:
                bstack11l11111ll_opy_ = bstack111l1l1l1l_opy_ + bstack1llll1l_opy_ (u"ࠤ࠰ࠦྻ") + attrs.get(bstack1llll1l_opy_ (u"ࠪࡸࡾࡶࡥࠨྼ"), bstack1llll1l_opy_ (u"ࠫࠬ྽")).lower()
                self._111l1l111l_opy_[bstack11l11111ll_opy_][bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ྾")].stop(time=bstack1l1ll1l1l_opy_(), duration=int(attrs.get(bstack1llll1l_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫ྿"), bstack1llll1l_opy_ (u"ࠧ࠱ࠩ࿀"))), result=bstack11l1111l1l_opy_)
                bstack1llllll1ll_opy_.bstack111ll1lll1_opy_(bstack1llll1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ࿁"), self._111l1l111l_opy_[bstack11l11111ll_opy_][bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ࿂")])
        else:
            bstack111l1l1l1l_opy_ = current_test_id if current_test_id else bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡ࡬ࡨࠬ࿃"), None)
            if bstack111l1l1l1l_opy_ and len(self.bstack111l11ll1l_opy_) == 1:
                current_step_uuid = bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨ࿄"), None)
                self._111l1l111l_opy_[bstack111l1l1l1l_opy_][bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿅")].bstack111llll11l_opy_(current_step_uuid, duration=int(attrs.get(bstack1llll1l_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨ࿆ࠫ"), bstack1llll1l_opy_ (u"ࠧ࠱ࠩ࿇"))), result=bstack11l1111l1l_opy_)
            else:
                self.bstack111ll111ll_opy_(attrs)
            self.bstack111l11ll1l_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1llll1l_opy_ (u"ࠨࡪࡷࡱࡱ࠭࿈"), bstack1llll1l_opy_ (u"ࠩࡱࡳࠬ࿉")) == bstack1llll1l_opy_ (u"ࠪࡽࡪࡹࠧ࿊"):
                return
            self.messages.push(message)
            logs = []
            if bstack1l11l111ll_opy_.bstack111llll1ll_opy_():
                logs.append({
                    bstack1llll1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ࿋"): bstack1l1ll1l1l_opy_(),
                    bstack1llll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿌"): message.get(bstack1llll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ࿍")),
                    bstack1llll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭࿎"): message.get(bstack1llll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ࿏")),
                    **bstack1l11l111ll_opy_.bstack111llll1ll_opy_()
                })
                if len(logs) > 0:
                    bstack1llllll1ll_opy_.bstack111l1l11l_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack1llllll1ll_opy_.bstack111ll1l111_opy_()
    def bstack111ll111ll_opy_(self, bstack111l1ll11l_opy_):
        if not bstack1l11l111ll_opy_.bstack111llll1ll_opy_():
            return
        kwname = bstack1llll1l_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨ࿐").format(bstack111l1ll11l_opy_.get(bstack1llll1l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ࿑")), bstack111l1ll11l_opy_.get(bstack1llll1l_opy_ (u"ࠫࡦࡸࡧࡴࠩ࿒"), bstack1llll1l_opy_ (u"ࠬ࠭࿓"))) if bstack111l1ll11l_opy_.get(bstack1llll1l_opy_ (u"࠭ࡡࡳࡩࡶࠫ࿔"), []) else bstack111l1ll11l_opy_.get(bstack1llll1l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧ࿕"))
        error_message = bstack1llll1l_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠠࡽࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦ࡜ࠣࡽ࠵ࢁࡡࠨࠢ࿖").format(kwname, bstack111l1ll11l_opy_.get(bstack1llll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ࿗")), str(bstack111l1ll11l_opy_.get(bstack1llll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿘"))))
        bstack111l11l1ll_opy_ = bstack1llll1l_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠥ࿙").format(kwname, bstack111l1ll11l_opy_.get(bstack1llll1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ࿚")))
        bstack111ll11lll_opy_ = error_message if bstack111l1ll11l_opy_.get(bstack1llll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ࿛")) else bstack111l11l1ll_opy_
        bstack111l1l1l11_opy_ = {
            bstack1llll1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ࿜"): self.bstack111l11ll1l_opy_[-1].get(bstack1llll1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ࿝"), bstack1l1ll1l1l_opy_()),
            bstack1llll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿞"): bstack111ll11lll_opy_,
            bstack1llll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ࿟"): bstack1llll1l_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ࿠") if bstack111l1ll11l_opy_.get(bstack1llll1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ࿡")) == bstack1llll1l_opy_ (u"࠭ࡆࡂࡋࡏࠫ࿢") else bstack1llll1l_opy_ (u"ࠧࡊࡐࡉࡓࠬ࿣"),
            **bstack1l11l111ll_opy_.bstack111llll1ll_opy_()
        }
        bstack1llllll1ll_opy_.bstack111l1l11l_opy_([bstack111l1l1l11_opy_])
    def _111ll11l11_opy_(self):
        for bstack111l11lll1_opy_ in reversed(self._111l1l111l_opy_):
            bstack111l1llll1_opy_ = bstack111l11lll1_opy_
            data = self._111l1l111l_opy_[bstack111l11lll1_opy_][bstack1llll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ࿤")]
            if isinstance(data, bstack111lllll11_opy_):
                if not bstack1llll1l_opy_ (u"ࠩࡈࡅࡈࡎࠧ࿥") in data.bstack111ll1l1ll_opy_():
                    return bstack111l1llll1_opy_
            else:
                return bstack111l1llll1_opy_
    def _111l1lll1l_opy_(self, messages):
        try:
            bstack111l11llll_opy_ = BuiltIn().get_variable_value(bstack1llll1l_opy_ (u"ࠥࠨࢀࡒࡏࡈࠢࡏࡉ࡛ࡋࡌࡾࠤ࿦")) in (bstack111l1lllll_opy_.DEBUG, bstack111l1lllll_opy_.TRACE)
            for message, bstack111l1111ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1llll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ࿧"))
                level = message.get(bstack1llll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ࿨"))
                if level == bstack111l1lllll_opy_.FAIL:
                    self._111ll1ll1l_opy_ = name or self._111ll1ll1l_opy_
                    self._111ll11111_opy_ = bstack111l1111ll_opy_.get(bstack1llll1l_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢ࿩")) if bstack111l11llll_opy_ and bstack111l1111ll_opy_ else self._111ll11111_opy_
        except:
            pass
    @classmethod
    def bstack111ll1lll1_opy_(self, event: str, bstack111l1ll111_opy_: bstack111ll1ll11_opy_, bstack1111llllll_opy_=False):
        if event == bstack1llll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ࿪"):
            bstack111l1ll111_opy_.set(hooks=self.store[bstack1llll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ࿫")])
        if event == bstack1llll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ࿬"):
            event = bstack1llll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ࿭")
        if bstack1111llllll_opy_:
            bstack111l11l11l_opy_ = {
                bstack1llll1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ࿮"): event,
                bstack111l1ll111_opy_.bstack111ll1111l_opy_(): bstack111l1ll111_opy_.bstack111l1l1lll_opy_(event)
            }
            self.bstack111ll11l1l_opy_.append(bstack111l11l11l_opy_)
        else:
            bstack1llllll1ll_opy_.bstack111ll1lll1_opy_(event, bstack111l1ll111_opy_)
class bstack111l1l11l1_opy_:
    def __init__(self):
        self._111l1lll11_opy_ = []
    def bstack1111lllll1_opy_(self):
        self._111l1lll11_opy_.append([])
    def bstack111ll1l11l_opy_(self):
        return self._111l1lll11_opy_.pop() if self._111l1lll11_opy_ else list()
    def push(self, message):
        self._111l1lll11_opy_[-1].append(message) if self._111l1lll11_opy_ else self._111l1lll11_opy_.append([message])
class bstack111l1lllll_opy_:
    FAIL = bstack1llll1l_opy_ (u"ࠬࡌࡁࡊࡎࠪ࿯")
    ERROR = bstack1llll1l_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬ࿰")
    WARNING = bstack1llll1l_opy_ (u"ࠧࡘࡃࡕࡒࠬ࿱")
    bstack111l11l111_opy_ = bstack1llll1l_opy_ (u"ࠨࡋࡑࡊࡔ࠭࿲")
    DEBUG = bstack1llll1l_opy_ (u"ࠩࡇࡉࡇ࡛ࡇࠨ࿳")
    TRACE = bstack1llll1l_opy_ (u"ࠪࡘࡗࡇࡃࡆࠩ࿴")
    bstack111l11111l_opy_ = [FAIL, ERROR]
def bstack111l111l1l_opy_(bstack111l11ll11_opy_):
    if not bstack111l11ll11_opy_:
        return None
    if bstack111l11ll11_opy_.get(bstack1llll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ࿵"), None):
        return getattr(bstack111l11ll11_opy_[bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿶")], bstack1llll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ࿷"), None)
    return bstack111l11ll11_opy_.get(bstack1llll1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ࿸"), None)
def bstack111l111ll1_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1llll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ࿹"), bstack1llll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ࿺")]:
        return
    if hook_type.lower() == bstack1llll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ࿻"):
        if current_test_uuid is None:
            return bstack1llll1l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨ࿼")
        else:
            return bstack1llll1l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ࿽")
    elif hook_type.lower() == bstack1llll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ࿾"):
        if current_test_uuid is None:
            return bstack1llll1l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ࿿")
        else:
            return bstack1llll1l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬက")