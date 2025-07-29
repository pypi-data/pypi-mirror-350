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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l1lll1ll1_opy_
from browserstack_sdk.bstack1lll1111l_opy_ import bstack1l1l1ll1l_opy_
def _11l111l1lll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l111l1111_opy_:
    def __init__(self, handler):
        self._11l111l1l1l_opy_ = {}
        self._11l1111llll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l1l1ll1l_opy_.version()
        if bstack11l1lll1ll1_opy_(pytest_version, bstack1llll1l_opy_ (u"ࠤ࠻࠲࠶࠴࠱ࠣᱲ")) >= 0:
            self._11l111l1l1l_opy_[bstack1llll1l_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᱳ")] = Module._register_setup_function_fixture
            self._11l111l1l1l_opy_[bstack1llll1l_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᱴ")] = Module._register_setup_module_fixture
            self._11l111l1l1l_opy_[bstack1llll1l_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᱵ")] = Class._register_setup_class_fixture
            self._11l111l1l1l_opy_[bstack1llll1l_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᱶ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11l111ll11l_opy_(bstack1llll1l_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᱷ"))
            Module._register_setup_module_fixture = self.bstack11l111ll11l_opy_(bstack1llll1l_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᱸ"))
            Class._register_setup_class_fixture = self.bstack11l111ll11l_opy_(bstack1llll1l_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᱹ"))
            Class._register_setup_method_fixture = self.bstack11l111ll11l_opy_(bstack1llll1l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᱺ"))
        else:
            self._11l111l1l1l_opy_[bstack1llll1l_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᱻ")] = Module._inject_setup_function_fixture
            self._11l111l1l1l_opy_[bstack1llll1l_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᱼ")] = Module._inject_setup_module_fixture
            self._11l111l1l1l_opy_[bstack1llll1l_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᱽ")] = Class._inject_setup_class_fixture
            self._11l111l1l1l_opy_[bstack1llll1l_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᱾")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11l111ll11l_opy_(bstack1llll1l_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᱿"))
            Module._inject_setup_module_fixture = self.bstack11l111ll11l_opy_(bstack1llll1l_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᲀ"))
            Class._inject_setup_class_fixture = self.bstack11l111ll11l_opy_(bstack1llll1l_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᲁ"))
            Class._inject_setup_method_fixture = self.bstack11l111ll11l_opy_(bstack1llll1l_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᲂ"))
    def bstack11l1111l1ll_opy_(self, bstack11l111l1l11_opy_, hook_type):
        bstack11l1111ll11_opy_ = id(bstack11l111l1l11_opy_.__class__)
        if (bstack11l1111ll11_opy_, hook_type) in self._11l1111llll_opy_:
            return
        meth = getattr(bstack11l111l1l11_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l1111llll_opy_[(bstack11l1111ll11_opy_, hook_type)] = meth
            setattr(bstack11l111l1l11_opy_, hook_type, self.bstack11l1111ll1l_opy_(hook_type, bstack11l1111ll11_opy_))
    def bstack11l1111lll1_opy_(self, instance, bstack11l111ll1l1_opy_):
        if bstack11l111ll1l1_opy_ == bstack1llll1l_opy_ (u"ࠧ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᲃ"):
            self.bstack11l1111l1ll_opy_(instance.obj, bstack1llll1l_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢᲄ"))
            self.bstack11l1111l1ll_opy_(instance.obj, bstack1llll1l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦᲅ"))
        if bstack11l111ll1l1_opy_ == bstack1llll1l_opy_ (u"ࠣ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᲆ"):
            self.bstack11l1111l1ll_opy_(instance.obj, bstack1llll1l_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠣᲇ"))
            self.bstack11l1111l1ll_opy_(instance.obj, bstack1llll1l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠧᲈ"))
        if bstack11l111ll1l1_opy_ == bstack1llll1l_opy_ (u"ࠦࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠦᲉ"):
            self.bstack11l1111l1ll_opy_(instance.obj, bstack1llll1l_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠥᲊ"))
            self.bstack11l1111l1ll_opy_(instance.obj, bstack1llll1l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠢ᲋"))
        if bstack11l111ll1l1_opy_ == bstack1llll1l_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣ᲌"):
            self.bstack11l1111l1ll_opy_(instance.obj, bstack1llll1l_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠢ᲍"))
            self.bstack11l1111l1ll_opy_(instance.obj, bstack1llll1l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠦ᲎"))
    @staticmethod
    def bstack11l111ll111_opy_(hook_type, func, args):
        if hook_type in [bstack1llll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩ᲏"), bstack1llll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭Ა")]:
            _11l111l1lll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l1111ll1l_opy_(self, hook_type, bstack11l1111ll11_opy_):
        def bstack11l111l1ll1_opy_(arg=None):
            self.handler(hook_type, bstack1llll1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬᲑ"))
            result = None
            try:
                bstack11111ll1l1_opy_ = self._11l1111llll_opy_[(bstack11l1111ll11_opy_, hook_type)]
                self.bstack11l111ll111_opy_(hook_type, bstack11111ll1l1_opy_, (arg,))
                result = Result(result=bstack1llll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭Გ"))
            except Exception as e:
                result = Result(result=bstack1llll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᲓ"), exception=e)
                self.handler(hook_type, bstack1llll1l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᲔ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1llll1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᲕ"), result)
        def bstack11l111l11ll_opy_(this, arg=None):
            self.handler(hook_type, bstack1llll1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᲖ"))
            result = None
            exception = None
            try:
                self.bstack11l111ll111_opy_(hook_type, self._11l1111llll_opy_[hook_type], (this, arg))
                result = Result(result=bstack1llll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᲗ"))
            except Exception as e:
                result = Result(result=bstack1llll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᲘ"), exception=e)
                self.handler(hook_type, bstack1llll1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᲙ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1llll1l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭Ლ"), result)
        if hook_type in [bstack1llll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᲛ"), bstack1llll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᲜ")]:
            return bstack11l111l11ll_opy_
        return bstack11l111l1ll1_opy_
    def bstack11l111ll11l_opy_(self, bstack11l111ll1l1_opy_):
        def bstack11l111l111l_opy_(this, *args, **kwargs):
            self.bstack11l1111lll1_opy_(this, bstack11l111ll1l1_opy_)
            self._11l111l1l1l_opy_[bstack11l111ll1l1_opy_](this, *args, **kwargs)
        return bstack11l111l111l_opy_