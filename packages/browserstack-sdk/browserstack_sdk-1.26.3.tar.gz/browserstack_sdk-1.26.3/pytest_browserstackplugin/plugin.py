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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1l1lll111l_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack111111lll_opy_, bstack1l1l1l11ll_opy_, update, bstack1lllllll1_opy_,
                                       bstack11ll11ll_opy_, bstack1lllll111_opy_, bstack1ll11l111_opy_, bstack1l1l111l1_opy_,
                                       bstack1l1l1l1ll_opy_, bstack1l1111l11l_opy_, bstack1lll111l1_opy_, bstack11lll11l1_opy_,
                                       bstack1l11111111_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1ll11l1l_opy_)
from browserstack_sdk.bstack1lll1111l_opy_ import bstack1l1l1ll1l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1llll11l1l_opy_
from bstack_utils.capture import bstack111lll11ll_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack11l11l1l_opy_, bstack1ll11lll_opy_, bstack1l11ll111l_opy_, \
    bstack111l11ll_opy_
from bstack_utils.helper import bstack11l11111_opy_, bstack11l1ll11l11_opy_, bstack111ll11ll1_opy_, bstack11llll1111_opy_, bstack1ll111l111l_opy_, bstack1l1ll1l1l_opy_, \
    bstack11l11ll1l1l_opy_, \
    bstack11l1lll1l1l_opy_, bstack1lll11ll1_opy_, bstack11l1lll111_opy_, bstack11l11l11l1l_opy_, bstack11l111l1_opy_, Notset, \
    bstack1ll1lll1ll_opy_, bstack11l11ll1lll_opy_, bstack11l1llll1ll_opy_, Result, bstack11l1l11l1ll_opy_, bstack11l1ll111l1_opy_, bstack111l1l1111_opy_, \
    bstack1l11lll11l_opy_, bstack1ll1l1l11l_opy_, bstack111l11ll1_opy_, bstack11l1ll1l1ll_opy_
from bstack_utils.bstack11l111l11l1_opy_ import bstack11l111l1111_opy_
from bstack_utils.messages import bstack1l1l1l11l1_opy_, bstack1l1l11l1l1_opy_, bstack11ll111ll_opy_, bstack1ll1lll11_opy_, bstack11111l1ll_opy_, \
    bstack1ll11l11ll_opy_, bstack1llllllll1_opy_, bstack1lll1ll1ll_opy_, bstack11ll1llll1_opy_, bstack111l1111l_opy_, \
    bstack111l11111_opy_, bstack11lll1l11_opy_
from bstack_utils.proxy import bstack111111l1l_opy_, bstack1ll11lll1l_opy_
from bstack_utils.bstack1ll1lll1_opy_ import bstack111l111l1ll_opy_, bstack111l11111l1_opy_, bstack111l111111l_opy_, bstack111l111l11l_opy_, \
    bstack111l1111ll1_opy_, bstack111l11111ll_opy_, bstack111l111l111_opy_, bstack1llllll11l_opy_, bstack111l1111lll_opy_
from bstack_utils.bstack1l11lll1_opy_ import bstack1ll111l11l_opy_
from bstack_utils.bstack11l111ll1l_opy_ import bstack11llll11l_opy_, bstack1ll11ll1ll_opy_, bstack111lllll1_opy_, \
    bstack1ll111l11_opy_, bstack11l111l11_opy_
from bstack_utils.bstack111lll1ll1_opy_ import bstack11l111111l_opy_
from bstack_utils.bstack11l11111l1_opy_ import bstack1l11l111ll_opy_
import bstack_utils.accessibility as bstack11l1lll1_opy_
from bstack_utils.bstack111lllllll_opy_ import bstack1llllll1ll_opy_
from bstack_utils.bstack1ll11l111l_opy_ import bstack1ll11l111l_opy_
from browserstack_sdk.__init__ import bstack1l111111ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll111_opy_ import bstack1lll111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1ll_opy_ import bstack1ll1ll1ll_opy_, bstack1ll111111_opy_, bstack11l1lll11_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l111l11l1l_opy_, bstack1ll1llll1ll_opy_, bstack1llll1l1lll_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1ll1ll1ll_opy_ import bstack1ll1ll1ll_opy_, bstack1ll111111_opy_, bstack11l1lll11_opy_
bstack1l11l1ll_opy_ = None
bstack11ll11ll1_opy_ = None
bstack11l1lll1l1_opy_ = None
bstack11l1lll1ll_opy_ = None
bstack1l111ll1l_opy_ = None
bstack11l1ll1ll1_opy_ = None
bstack1l1l11ll1l_opy_ = None
bstack1lll1lll1_opy_ = None
bstack1l1l1l111l_opy_ = None
bstack1l11ll1l1_opy_ = None
bstack11ll111l1l_opy_ = None
bstack11ll1l11l_opy_ = None
bstack1ll111ll1_opy_ = None
bstack1l11l11l11_opy_ = bstack1llll1l_opy_ (u"ࠨࠩ‛")
CONFIG = {}
bstack11lll111l1_opy_ = False
bstack1llllll1l1_opy_ = bstack1llll1l_opy_ (u"ࠩࠪ“")
bstack1l111l1lll_opy_ = bstack1llll1l_opy_ (u"ࠪࠫ”")
bstack1l111ll1ll_opy_ = False
bstack1l1llllll1_opy_ = []
bstack111l11l1_opy_ = bstack11l11l1l_opy_
bstack111111ll11l_opy_ = bstack1llll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ„")
bstack11ll1111_opy_ = {}
bstack1l1111ll1_opy_ = None
bstack11l1l1l111_opy_ = False
logger = bstack1llll11l1l_opy_.get_logger(__name__, bstack111l11l1_opy_)
store = {
    bstack1llll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ‟"): []
}
bstack111111l1l11_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111l1l111l_opy_ = {}
current_test_uuid = None
cli_context = bstack1l111l11l1l_opy_(
    test_framework_name=bstack11ll1llll_opy_[bstack1llll1l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪ†")] if bstack11l111l1_opy_() else bstack11ll1llll_opy_[bstack1llll1l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚ࠧ‡")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack11lll1l1ll_opy_(page, bstack11llllll11_opy_):
    try:
        page.evaluate(bstack1llll1l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ•"),
                      bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭‣") + json.dumps(
                          bstack11llllll11_opy_) + bstack1llll1l_opy_ (u"ࠥࢁࢂࠨ․"))
    except Exception as e:
        print(bstack1llll1l_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤ‥"), e)
def bstack111ll1ll1_opy_(page, message, level):
    try:
        page.evaluate(bstack1llll1l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ…"), bstack1llll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ‧") + json.dumps(
            message) + bstack1llll1l_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪ ") + json.dumps(level) + bstack1llll1l_opy_ (u"ࠨࡿࢀࠫ "))
    except Exception as e:
        print(bstack1llll1l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧ‪"), e)
def pytest_configure(config):
    global bstack1llllll1l1_opy_
    global CONFIG
    bstack1lll1l111l_opy_ = Config.bstack11l11l11l1_opy_()
    config.args = bstack1l11l111ll_opy_.bstack11111l1l1l1_opy_(config.args)
    bstack1lll1l111l_opy_.bstack1lll111lll_opy_(bstack111l11ll1_opy_(config.getoption(bstack1llll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ‫"))))
    try:
        bstack1llll11l1l_opy_.bstack11l11111l11_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1ll1ll1ll_opy_.invoke(bstack1ll111111_opy_.CONNECT, bstack11l1lll11_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1llll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ‬"), bstack1llll1l_opy_ (u"ࠬ࠶ࠧ‭")))
        config = json.loads(os.environ.get(bstack1llll1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠧ‮"), bstack1llll1l_opy_ (u"ࠢࡼࡿࠥ ")))
        cli.bstack1llll1lll1l_opy_(bstack11l1lll111_opy_(bstack1llllll1l1_opy_, CONFIG), cli_context.platform_index, bstack1lllllll1_opy_)
    if cli.bstack1lll11ll1l1_opy_(bstack1lll111l1ll_opy_):
        cli.bstack1lll111l11l_opy_()
        logger.debug(bstack1llll1l_opy_ (u"ࠣࡅࡏࡍࠥ࡯ࡳࠡࡣࡦࡸ࡮ࡼࡥࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢ‰") + str(cli_context.platform_index) + bstack1llll1l_opy_ (u"ࠤࠥ‱"))
        cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.BEFORE_ALL, bstack1llll1l1lll_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1llll1l_opy_ (u"ࠥࡻ࡭࡫࡮ࠣ′"), None)
    if cli.is_running() and when == bstack1llll1l_opy_ (u"ࠦࡨࡧ࡬࡭ࠤ″"):
        cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.LOG_REPORT, bstack1llll1l1lll_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack1llll1l_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦ‴"):
            cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.BEFORE_EACH, bstack1llll1l1lll_opy_.POST, item, call, outcome)
        elif when == bstack1llll1l_opy_ (u"ࠨࡣࡢ࡮࡯ࠦ‵"):
            cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.LOG_REPORT, bstack1llll1l1lll_opy_.POST, item, call, outcome)
        elif when == bstack1llll1l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤ‶"):
            cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.AFTER_EACH, bstack1llll1l1lll_opy_.POST, item, call, outcome)
        return # skip all existing bstack111111ll1l1_opy_
    skipSessionName = item.config.getoption(bstack1llll1l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ‷"))
    plugins = item.config.getoption(bstack1llll1l_opy_ (u"ࠤࡳࡰࡺ࡭ࡩ࡯ࡵࠥ‸"))
    report = outcome.get_result()
    bstack111111l111l_opy_(item, call, report)
    if bstack1llll1l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠣ‹") not in plugins or bstack11l111l1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1llll1l_opy_ (u"ࠦࡤࡪࡲࡪࡸࡨࡶࠧ›"), None)
    page = getattr(item, bstack1llll1l_opy_ (u"ࠧࡥࡰࡢࡩࡨࠦ※"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack111111llll1_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack111111lll1l_opy_(item, report, summary, skipSessionName)
def bstack111111llll1_opy_(item, report, summary, skipSessionName):
    if report.when == bstack1llll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ‼") and report.skipped:
        bstack111l1111lll_opy_(report)
    if report.when in [bstack1llll1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨ‽"), bstack1llll1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥ‾")]:
        return
    if not bstack1ll111l111l_opy_():
        return
    try:
        if (str(skipSessionName).lower() != bstack1llll1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ‿") and not cli.is_running()):
            item._driver.execute_script(
                bstack1llll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨ⁀") + json.dumps(
                    report.nodeid) + bstack1llll1l_opy_ (u"ࠫࢂࢃࠧ⁁"))
        os.environ[bstack1llll1l_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ⁂")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1llll1l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥ࠻ࠢࡾ࠴ࢂࠨ⁃").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1llll1l_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ⁄")))
    bstack1ll111l1_opy_ = bstack1llll1l_opy_ (u"ࠣࠤ⁅")
    bstack111l1111lll_opy_(report)
    if not passed:
        try:
            bstack1ll111l1_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1llll1l_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤ⁆").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll111l1_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1llll1l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧ⁇")))
        bstack1ll111l1_opy_ = bstack1llll1l_opy_ (u"ࠦࠧ⁈")
        if not passed:
            try:
                bstack1ll111l1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1llll1l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧ⁉").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll111l1_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1llll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪ⁊")
                    + json.dumps(bstack1llll1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠡࠣ⁋"))
                    + bstack1llll1l_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦ⁌")
                )
            else:
                item._driver.execute_script(
                    bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧ⁍")
                    + json.dumps(str(bstack1ll111l1_opy_))
                    + bstack1llll1l_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨ⁎")
                )
        except Exception as e:
            summary.append(bstack1llll1l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡤࡲࡳࡵࡴࡢࡶࡨ࠾ࠥࢁ࠰ࡾࠤ⁏").format(e))
def bstack1111111lll1_opy_(test_name, error_message):
    try:
        bstack1111111llll_opy_ = []
        bstack1l111l11l1_opy_ = os.environ.get(bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⁐"), bstack1llll1l_opy_ (u"࠭࠰ࠨ⁑"))
        bstack11111111l_opy_ = {bstack1llll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⁒"): test_name, bstack1llll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ⁓"): error_message, bstack1llll1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ⁔"): bstack1l111l11l1_opy_}
        bstack1111111ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1llll1l_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ⁕"))
        if os.path.exists(bstack1111111ll1l_opy_):
            with open(bstack1111111ll1l_opy_) as f:
                bstack1111111llll_opy_ = json.load(f)
        bstack1111111llll_opy_.append(bstack11111111l_opy_)
        with open(bstack1111111ll1l_opy_, bstack1llll1l_opy_ (u"ࠫࡼ࠭⁖")) as f:
            json.dump(bstack1111111llll_opy_, f)
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡧࡵࡷ࡮ࡹࡴࡪࡰࡪࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡲࡼࡸࡪࡹࡴࠡࡧࡵࡶࡴࡸࡳ࠻ࠢࠪ⁗") + str(e))
def bstack111111lll1l_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack1llll1l_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧ⁘"), bstack1llll1l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤ⁙")]:
        return
    if (str(skipSessionName).lower() != bstack1llll1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭⁚")):
        bstack11lll1l1ll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1llll1l_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ⁛")))
    bstack1ll111l1_opy_ = bstack1llll1l_opy_ (u"ࠥࠦ⁜")
    bstack111l1111lll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1ll111l1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1llll1l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦ⁝").format(e)
                )
        try:
            if passed:
                bstack11l111l11_opy_(getattr(item, bstack1llll1l_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫ⁞"), None), bstack1llll1l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ "))
            else:
                error_message = bstack1llll1l_opy_ (u"ࠧࠨ⁠")
                if bstack1ll111l1_opy_:
                    bstack111ll1ll1_opy_(item._page, str(bstack1ll111l1_opy_), bstack1llll1l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ⁡"))
                    bstack11l111l11_opy_(getattr(item, bstack1llll1l_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ⁢"), None), bstack1llll1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ⁣"), str(bstack1ll111l1_opy_))
                    error_message = str(bstack1ll111l1_opy_)
                else:
                    bstack11l111l11_opy_(getattr(item, bstack1llll1l_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪ⁤"), None), bstack1llll1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ⁥"))
                bstack1111111lll1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1llll1l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻ࠱ࡿࠥ⁦").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1llll1l_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ⁧"), default=bstack1llll1l_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢ⁨"), help=bstack1llll1l_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣ⁩"))
    parser.addoption(bstack1llll1l_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ⁪"), default=bstack1llll1l_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥ⁫"), help=bstack1llll1l_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦ⁬"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1llll1l_opy_ (u"ࠨ࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠣ⁭"), action=bstack1llll1l_opy_ (u"ࠢࡴࡶࡲࡶࡪࠨ⁮"), default=bstack1llll1l_opy_ (u"ࠣࡥ࡫ࡶࡴࡳࡥࠣ⁯"),
                         help=bstack1llll1l_opy_ (u"ࠤࡇࡶ࡮ࡼࡥࡳࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳࠣ⁰"))
def bstack111lll1111_opy_(log):
    if not (log[bstack1llll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫⁱ")] and log[bstack1llll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⁲")].strip()):
        return
    active = bstack111llll1ll_opy_()
    log = {
        bstack1llll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⁳"): log[bstack1llll1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⁴")],
        bstack1llll1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⁵"): bstack111ll11ll1_opy_().isoformat() + bstack1llll1l_opy_ (u"ࠨ࡜ࠪ⁶"),
        bstack1llll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⁷"): log[bstack1llll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⁸")],
    }
    if active:
        if active[bstack1llll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩ⁹")] == bstack1llll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⁺"):
            log[bstack1llll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⁻")] = active[bstack1llll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⁼")]
        elif active[bstack1llll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭⁽")] == bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺࠧ⁾"):
            log[bstack1llll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪⁿ")] = active[bstack1llll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ₀")]
    bstack1llllll1ll_opy_.bstack111l1l11l_opy_([log])
def bstack111llll1ll_opy_():
    if len(store[bstack1llll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ₁")]) > 0 and store[bstack1llll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ₂")][-1]:
        return {
            bstack1llll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬ₃"): bstack1llll1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭₄"),
            bstack1llll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ₅"): store[bstack1llll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ₆")][-1]
        }
    if store.get(bstack1llll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ₇"), None):
        return {
            bstack1llll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪ₈"): bstack1llll1l_opy_ (u"࠭ࡴࡦࡵࡷࠫ₉"),
            bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ₊"): store[bstack1llll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ₋")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.INIT_TEST, bstack1llll1l1lll_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.INIT_TEST, bstack1llll1l1lll_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.TEST, bstack1llll1l1lll_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1111111ll11_opy_ = True
        bstack1l1ll1l111_opy_ = bstack11l1lll1_opy_.bstack1ll1l11l1l_opy_(bstack11l1lll1l1l_opy_(item.own_markers))
        if not cli.bstack1lll11ll1l1_opy_(bstack1lll111l1ll_opy_):
            item._a11y_test_case = bstack1l1ll1l111_opy_
            if bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ₌"), None):
                driver = getattr(item, bstack1llll1l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ₍"), None)
                item._a11y_started = bstack11l1lll1_opy_.bstack11l11ll1l1_opy_(driver, bstack1l1ll1l111_opy_)
        if not bstack1llllll1ll_opy_.on() or bstack111111ll11l_opy_ != bstack1llll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ₎"):
            return
        global current_test_uuid #, bstack11l1111ll1_opy_
        bstack111l11ll11_opy_ = {
            bstack1llll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪ₏"): uuid4().__str__(),
            bstack1llll1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪₐ"): bstack111ll11ll1_opy_().isoformat() + bstack1llll1l_opy_ (u"࡛ࠧࠩₑ")
        }
        current_test_uuid = bstack111l11ll11_opy_[bstack1llll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ₒ")]
        store[bstack1llll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ₓ")] = bstack111l11ll11_opy_[bstack1llll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨₔ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l1l111l_opy_[item.nodeid] = {**_111l1l111l_opy_[item.nodeid], **bstack111l11ll11_opy_}
        bstack1111111l1l1_opy_(item, _111l1l111l_opy_[item.nodeid], bstack1llll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬₕ"))
    except Exception as err:
        print(bstack1llll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡩࡡ࡭࡮࠽ࠤࢀࢃࠧₖ"), str(err))
def pytest_runtest_setup(item):
    store[bstack1llll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪₗ")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.BEFORE_EACH, bstack1llll1l1lll_opy_.PRE, item, bstack1llll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ₘ"))
        return # skip all existing bstack111111ll1l1_opy_
    global bstack111111l1l11_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l11l11l1l_opy_():
        atexit.register(bstack11ll111111_opy_)
        if not bstack111111l1l11_opy_:
            try:
                bstack11111l11l11_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1ll1l1ll_opy_():
                    bstack11111l11l11_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack11111l11l11_opy_:
                    signal.signal(s, bstack1111111l11l_opy_)
                bstack111111l1l11_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1llll1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪ࡭ࡩࡴࡶࡨࡶࠥࡹࡩࡨࡰࡤࡰࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡹ࠺ࠡࠤₙ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111l111l1ll_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1llll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩₚ")
    try:
        if not bstack1llllll1ll_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l11ll11_opy_ = {
            bstack1llll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨₛ"): uuid,
            bstack1llll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨₜ"): bstack111ll11ll1_opy_().isoformat() + bstack1llll1l_opy_ (u"ࠬࡠࠧ₝"),
            bstack1llll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫ₞"): bstack1llll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ₟"),
            bstack1llll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ₠"): bstack1llll1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ₡"),
            bstack1llll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭₢"): bstack1llll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ₣")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1llll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ₤")] = item
        store[bstack1llll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ₥")] = [uuid]
        if not _111l1l111l_opy_.get(item.nodeid, None):
            _111l1l111l_opy_[item.nodeid] = {bstack1llll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭₦"): [], bstack1llll1l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ₧"): []}
        _111l1l111l_opy_[item.nodeid][bstack1llll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ₨")].append(bstack111l11ll11_opy_[bstack1llll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ₩")])
        _111l1l111l_opy_[item.nodeid + bstack1llll1l_opy_ (u"ࠫ࠲ࡹࡥࡵࡷࡳࠫ₪")] = bstack111l11ll11_opy_
        bstack11111l1111l_opy_(item, bstack111l11ll11_opy_, bstack1llll1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭₫"))
    except Exception as err:
        print(bstack1llll1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩ€"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.TEST, bstack1llll1l1lll_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.AFTER_EACH, bstack1llll1l1lll_opy_.PRE, item, bstack1llll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ₭"))
        return # skip all existing bstack111111ll1l1_opy_
    try:
        global bstack11ll1111_opy_
        bstack1l111l11l1_opy_ = 0
        if bstack1l111ll1ll_opy_ is True:
            bstack1l111l11l1_opy_ = int(os.environ.get(bstack1llll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ₮")))
        if bstack111111111_opy_.bstack1lllllll1l_opy_() == bstack1llll1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ₯"):
            if bstack111111111_opy_.bstack1l11l11l_opy_() == bstack1llll1l_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ₰"):
                bstack111111l1ll1_opy_ = bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ₱"), None)
                bstack1l11l1l1l_opy_ = bstack111111l1ll1_opy_ + bstack1llll1l_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣ₲")
                driver = getattr(item, bstack1llll1l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ₳"), None)
                bstack1l111lll_opy_ = getattr(item, bstack1llll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ₴"), None)
                bstack11l111lll1_opy_ = getattr(item, bstack1llll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭₵"), None)
                PercySDK.screenshot(driver, bstack1l11l1l1l_opy_, bstack1l111lll_opy_=bstack1l111lll_opy_, bstack11l111lll1_opy_=bstack11l111lll1_opy_, bstack11l1ll1lll_opy_=bstack1l111l11l1_opy_)
        if not cli.bstack1lll11ll1l1_opy_(bstack1lll111l1ll_opy_):
            if getattr(item, bstack1llll1l_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡥࡷࡺࡥࡥࠩ₶"), False):
                bstack1l1l1ll1l_opy_.bstack1l111l1l_opy_(getattr(item, bstack1llll1l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ₷"), None), bstack11ll1111_opy_, logger, item)
        if not bstack1llllll1ll_opy_.on():
            return
        bstack111l11ll11_opy_ = {
            bstack1llll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ₸"): uuid4().__str__(),
            bstack1llll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ₹"): bstack111ll11ll1_opy_().isoformat() + bstack1llll1l_opy_ (u"࡚࠭ࠨ₺"),
            bstack1llll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬ₻"): bstack1llll1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭₼"),
            bstack1llll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ₽"): bstack1llll1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ₾"),
            bstack1llll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ₿"): bstack1llll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ⃀")
        }
        _111l1l111l_opy_[item.nodeid + bstack1llll1l_opy_ (u"࠭࠭ࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ⃁")] = bstack111l11ll11_opy_
        bstack11111l1111l_opy_(item, bstack111l11ll11_opy_, bstack1llll1l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⃂"))
    except Exception as err:
        print(bstack1llll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰ࠽ࠤࢀࢃࠧ⃃"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack111l111l11l_opy_(fixturedef.argname):
        store[bstack1llll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨ⃄")] = request.node
    elif bstack111l1111ll1_opy_(fixturedef.argname):
        store[bstack1llll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨ⃅")] = request.node
    if not bstack1llllll1ll_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.SETUP_FIXTURE, bstack1llll1l1lll_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.SETUP_FIXTURE, bstack1llll1l1lll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack111111ll1l1_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.SETUP_FIXTURE, bstack1llll1l1lll_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.SETUP_FIXTURE, bstack1llll1l1lll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack111111ll1l1_opy_
    try:
        fixture = {
            bstack1llll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⃆"): fixturedef.argname,
            bstack1llll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⃇"): bstack11l11ll1l1l_opy_(outcome),
            bstack1llll1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ⃈"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1llll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⃉")]
        if not _111l1l111l_opy_.get(current_test_item.nodeid, None):
            _111l1l111l_opy_[current_test_item.nodeid] = {bstack1llll1l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ⃊"): []}
        _111l1l111l_opy_[current_test_item.nodeid][bstack1llll1l_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ⃋")].append(fixture)
    except Exception as err:
        logger.debug(bstack1llll1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭⃌"), str(err))
if bstack11l111l1_opy_() and bstack1llllll1ll_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.STEP, bstack1llll1l1lll_opy_.PRE, request, step)
            return
        try:
            _111l1l111l_opy_[request.node.nodeid][bstack1llll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⃍")].bstack1l1llll111_opy_(id(step))
        except Exception as err:
            print(bstack1llll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࡀࠠࡼࡿࠪ⃎"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.STEP, bstack1llll1l1lll_opy_.POST, request, step, exception)
            return
        try:
            _111l1l111l_opy_[request.node.nodeid][bstack1llll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⃏")].bstack111llll11l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1llll1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫ⃐"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.STEP, bstack1llll1l1lll_opy_.POST, request, step)
            return
        try:
            bstack111lll1ll1_opy_: bstack11l111111l_opy_ = _111l1l111l_opy_[request.node.nodeid][bstack1llll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⃑")]
            bstack111lll1ll1_opy_.bstack111llll11l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1llll1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ⃒࠭"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack111111ll11l_opy_
        try:
            if not bstack1llllll1ll_opy_.on() or bstack111111ll11l_opy_ != bstack1llll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪ⃓ࠧ"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.TEST, bstack1llll1l1lll_opy_.PRE, request, feature, scenario)
                return
            driver = bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ⃔"), None)
            if not _111l1l111l_opy_.get(request.node.nodeid, None):
                _111l1l111l_opy_[request.node.nodeid] = {}
            bstack111lll1ll1_opy_ = bstack11l111111l_opy_.bstack1111l1ll1ll_opy_(
                scenario, feature, request.node,
                name=bstack111l11111ll_opy_(request.node, scenario),
                started_at=bstack1l1ll1l1l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1llll1l_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧ⃕"),
                tags=bstack111l111l111_opy_(feature, scenario),
                bstack11l1111l11_opy_=bstack1llllll1ll_opy_.bstack11l1111111_opy_(driver) if driver and driver.session_id else {}
            )
            _111l1l111l_opy_[request.node.nodeid][bstack1llll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⃖")] = bstack111lll1ll1_opy_
            bstack111111l1l1l_opy_(bstack111lll1ll1_opy_.uuid)
            bstack1llllll1ll_opy_.bstack111ll1lll1_opy_(bstack1llll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⃗"), bstack111lll1ll1_opy_)
        except Exception as err:
            print(bstack1llll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿ⃘ࠪ"), str(err))
def bstack11111l11111_opy_(bstack111lll1lll_opy_):
    if bstack111lll1lll_opy_ in store[bstack1llll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ⃙࠭")]:
        store[bstack1llll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪ⃚ࠧ")].remove(bstack111lll1lll_opy_)
def bstack111111l1l1l_opy_(test_uuid):
    store[bstack1llll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⃛")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1llllll1ll_opy_.bstack1111l11lll1_opy_
def bstack111111l111l_opy_(item, call, report):
    logger.debug(bstack1llll1l_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡷࡺࠧ⃜"))
    global bstack111111ll11l_opy_
    bstack11l11l1ll_opy_ = bstack1l1ll1l1l_opy_()
    if hasattr(report, bstack1llll1l_opy_ (u"࠭ࡳࡵࡱࡳࠫ⃝")):
        bstack11l11l1ll_opy_ = bstack11l1l11l1ll_opy_(report.stop)
    elif hasattr(report, bstack1llll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࠭⃞")):
        bstack11l11l1ll_opy_ = bstack11l1l11l1ll_opy_(report.start)
    try:
        if getattr(report, bstack1llll1l_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭⃟"), bstack1llll1l_opy_ (u"ࠩࠪ⃠")) == bstack1llll1l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⃡"):
            logger.debug(bstack1llll1l_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡸࡪࠦ࠭ࠡࡽࢀ࠰ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࠯ࠣࡿࢂ࠭⃢").format(getattr(report, bstack1llll1l_opy_ (u"ࠬࡽࡨࡦࡰࠪ⃣"), bstack1llll1l_opy_ (u"࠭ࠧ⃤")).__str__(), bstack111111ll11l_opy_))
            if bstack111111ll11l_opy_ == bstack1llll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ⃥ࠧ"):
                _111l1l111l_opy_[item.nodeid][bstack1llll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ⃦࠭")] = bstack11l11l1ll_opy_
                bstack1111111l1l1_opy_(item, _111l1l111l_opy_[item.nodeid], bstack1llll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⃧"), report, call)
                store[bstack1llll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪ⃨ࠧ")] = None
            elif bstack111111ll11l_opy_ == bstack1llll1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣ⃩"):
                bstack111lll1ll1_opy_ = _111l1l111l_opy_[item.nodeid][bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⃪")]
                bstack111lll1ll1_opy_.set(hooks=_111l1l111l_opy_[item.nodeid].get(bstack1llll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷ⃫ࠬ"), []))
                exception, bstack111ll1llll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111ll1llll_opy_ = [call.excinfo.exconly(), getattr(report, bstack1llll1l_opy_ (u"ࠧ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹ⃬࠭"), bstack1llll1l_opy_ (u"ࠨ⃭ࠩ"))]
                bstack111lll1ll1_opy_.stop(time=bstack11l11l1ll_opy_, result=Result(result=getattr(report, bstack1llll1l_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧ⃮ࠪ"), bstack1llll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦ⃯ࠪ")), exception=exception, bstack111ll1llll_opy_=bstack111ll1llll_opy_))
                bstack1llllll1ll_opy_.bstack111ll1lll1_opy_(bstack1llll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⃰"), _111l1l111l_opy_[item.nodeid][bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⃱")])
        elif getattr(report, bstack1llll1l_opy_ (u"࠭ࡷࡩࡧࡱࠫ⃲"), bstack1llll1l_opy_ (u"ࠧࠨ⃳")) in [bstack1llll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⃴"), bstack1llll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ⃵")]:
            logger.debug(bstack1llll1l_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡷࡩࠥ࠳ࠠࡼࡿ࠯ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࠮ࠢࡾࢁࠬ⃶").format(getattr(report, bstack1llll1l_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⃷"), bstack1llll1l_opy_ (u"ࠬ࠭⃸")).__str__(), bstack111111ll11l_opy_))
            bstack11l11111ll_opy_ = item.nodeid + bstack1llll1l_opy_ (u"࠭࠭ࠨ⃹") + getattr(report, bstack1llll1l_opy_ (u"ࠧࡸࡪࡨࡲࠬ⃺"), bstack1llll1l_opy_ (u"ࠨࠩ⃻"))
            if getattr(report, bstack1llll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⃼"), False):
                hook_type = bstack1llll1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ⃽") if getattr(report, bstack1llll1l_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⃾"), bstack1llll1l_opy_ (u"ࠬ࠭⃿")) == bstack1llll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ℀") else bstack1llll1l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ℁")
                _111l1l111l_opy_[bstack11l11111ll_opy_] = {
                    bstack1llll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ℂ"): uuid4().__str__(),
                    bstack1llll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭℃"): bstack11l11l1ll_opy_,
                    bstack1llll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭℄"): hook_type
                }
            _111l1l111l_opy_[bstack11l11111ll_opy_][bstack1llll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ℅")] = bstack11l11l1ll_opy_
            bstack11111l11111_opy_(_111l1l111l_opy_[bstack11l11111ll_opy_][bstack1llll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪ℆")])
            bstack11111l1111l_opy_(item, _111l1l111l_opy_[bstack11l11111ll_opy_], bstack1llll1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨℇ"), report, call)
            if getattr(report, bstack1llll1l_opy_ (u"ࠧࡸࡪࡨࡲࠬ℈"), bstack1llll1l_opy_ (u"ࠨࠩ℉")) == bstack1llll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨℊ"):
                if getattr(report, bstack1llll1l_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫℋ"), bstack1llll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫℌ")) == bstack1llll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬℍ"):
                    bstack111l11ll11_opy_ = {
                        bstack1llll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫℎ"): uuid4().__str__(),
                        bstack1llll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫℏ"): bstack1l1ll1l1l_opy_(),
                        bstack1llll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ℐ"): bstack1l1ll1l1l_opy_()
                    }
                    _111l1l111l_opy_[item.nodeid] = {**_111l1l111l_opy_[item.nodeid], **bstack111l11ll11_opy_}
                    bstack1111111l1l1_opy_(item, _111l1l111l_opy_[item.nodeid], bstack1llll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪℑ"))
                    bstack1111111l1l1_opy_(item, _111l1l111l_opy_[item.nodeid], bstack1llll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬℒ"), report, call)
    except Exception as err:
        print(bstack1llll1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡻࡾࠩℓ"), str(err))
def bstack111111ll1ll_opy_(test, bstack111l11ll11_opy_, result=None, call=None, bstack111lll1l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111lll1ll1_opy_ = {
        bstack1llll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪ℔"): bstack111l11ll11_opy_[bstack1llll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫℕ")],
        bstack1llll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬ№"): bstack1llll1l_opy_ (u"ࠨࡶࡨࡷࡹ࠭℗"),
        bstack1llll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ℘"): test.name,
        bstack1llll1l_opy_ (u"ࠪࡦࡴࡪࡹࠨℙ"): {
            bstack1llll1l_opy_ (u"ࠫࡱࡧ࡮ࡨࠩℚ"): bstack1llll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬℛ"),
            bstack1llll1l_opy_ (u"࠭ࡣࡰࡦࡨࠫℜ"): inspect.getsource(test.obj)
        },
        bstack1llll1l_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫℝ"): test.name,
        bstack1llll1l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧ℞"): test.name,
        bstack1llll1l_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ℟"): bstack1l11l111ll_opy_.bstack111l1ll1ll_opy_(test),
        bstack1llll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭℠"): file_path,
        bstack1llll1l_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭℡"): file_path,
        bstack1llll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ™"): bstack1llll1l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ℣"),
        bstack1llll1l_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬℤ"): file_path,
        bstack1llll1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ℥"): bstack111l11ll11_opy_[bstack1llll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭Ω")],
        bstack1llll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭℧"): bstack1llll1l_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫℨ"),
        bstack1llll1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨ℩"): {
            bstack1llll1l_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪK"): test.nodeid
        },
        bstack1llll1l_opy_ (u"ࠧࡵࡣࡪࡷࠬÅ"): bstack11l1lll1l1l_opy_(test.own_markers)
    }
    if bstack111lll1l_opy_ in [bstack1llll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩℬ"), bstack1llll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫℭ")]:
        bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"ࠪࡱࡪࡺࡡࠨ℮")] = {
            bstack1llll1l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ℯ"): bstack111l11ll11_opy_.get(bstack1llll1l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧℰ"), [])
        }
    if bstack111lll1l_opy_ == bstack1llll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧℱ"):
        bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧℲ")] = bstack1llll1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩℳ")
        bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨℴ")] = bstack111l11ll11_opy_[bstack1llll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩℵ")]
        bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩℶ")] = bstack111l11ll11_opy_[bstack1llll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪℷ")]
    if result:
        bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ℸ")] = result.outcome
        bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨℹ")] = result.duration * 1000
        bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭℺")] = bstack111l11ll11_opy_[bstack1llll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ℻")]
        if result.failed:
            bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩℼ")] = bstack1llllll1ll_opy_.bstack1111l11l11_opy_(call.excinfo.typename)
            bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬℽ")] = bstack1llllll1ll_opy_.bstack1111l1l11l1_opy_(call.excinfo, result)
        bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫℾ")] = bstack111l11ll11_opy_[bstack1llll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬℿ")]
    if outcome:
        bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⅀")] = bstack11l11ll1l1l_opy_(outcome)
        bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⅁")] = 0
        bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⅂")] = bstack111l11ll11_opy_[bstack1llll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⅃")]
        if bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⅄")] == bstack1llll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬⅅ"):
            bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬⅆ")] = bstack1llll1l_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨⅇ")  # bstack111111l1111_opy_
            bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩⅈ")] = [{bstack1llll1l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬⅉ"): [bstack1llll1l_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧ⅊")]}]
        bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⅋")] = bstack111l11ll11_opy_[bstack1llll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⅌")]
    return bstack111lll1ll1_opy_
def bstack111111l1lll_opy_(test, bstack111l1l11ll_opy_, bstack111lll1l_opy_, result, call, outcome, bstack111111lll11_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l1l11ll_opy_[bstack1llll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⅍")]
    hook_name = bstack111l1l11ll_opy_[bstack1llll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪⅎ")]
    hook_data = {
        bstack1llll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⅏"): bstack111l1l11ll_opy_[bstack1llll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⅐")],
        bstack1llll1l_opy_ (u"ࠪࡸࡾࡶࡥࠨ⅑"): bstack1llll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⅒"),
        bstack1llll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⅓"): bstack1llll1l_opy_ (u"࠭ࡻࡾࠩ⅔").format(bstack111l11111l1_opy_(hook_name)),
        bstack1llll1l_opy_ (u"ࠧࡣࡱࡧࡽࠬ⅕"): {
            bstack1llll1l_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭⅖"): bstack1llll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ⅗"),
            bstack1llll1l_opy_ (u"ࠪࡧࡴࡪࡥࠨ⅘"): None
        },
        bstack1llll1l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪ⅙"): test.name,
        bstack1llll1l_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ⅚"): bstack1l11l111ll_opy_.bstack111l1ll1ll_opy_(test, hook_name),
        bstack1llll1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ⅛"): file_path,
        bstack1llll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ⅜"): file_path,
        bstack1llll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⅝"): bstack1llll1l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⅞"),
        bstack1llll1l_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ⅟"): file_path,
        bstack1llll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨⅠ"): bstack111l1l11ll_opy_[bstack1llll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩⅡ")],
        bstack1llll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩⅢ"): bstack1llll1l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩⅣ") if bstack111111ll11l_opy_ == bstack1llll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬⅤ") else bstack1llll1l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩⅥ"),
        bstack1llll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭Ⅶ"): hook_type
    }
    bstack1111l1l1lll_opy_ = bstack111l111l1l_opy_(_111l1l111l_opy_.get(test.nodeid, None))
    if bstack1111l1l1lll_opy_:
        hook_data[bstack1llll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩⅧ")] = bstack1111l1l1lll_opy_
    if result:
        hook_data[bstack1llll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬⅨ")] = result.outcome
        hook_data[bstack1llll1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧⅩ")] = result.duration * 1000
        hook_data[bstack1llll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬⅪ")] = bstack111l1l11ll_opy_[bstack1llll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭Ⅻ")]
        if result.failed:
            hook_data[bstack1llll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨⅬ")] = bstack1llllll1ll_opy_.bstack1111l11l11_opy_(call.excinfo.typename)
            hook_data[bstack1llll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫⅭ")] = bstack1llllll1ll_opy_.bstack1111l1l11l1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1llll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫⅮ")] = bstack11l11ll1l1l_opy_(outcome)
        hook_data[bstack1llll1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭Ⅿ")] = 100
        hook_data[bstack1llll1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫⅰ")] = bstack111l1l11ll_opy_[bstack1llll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬⅱ")]
        if hook_data[bstack1llll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨⅲ")] == bstack1llll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩⅳ"):
            hook_data[bstack1llll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩⅴ")] = bstack1llll1l_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬⅵ")  # bstack111111l1111_opy_
            hook_data[bstack1llll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ⅶ")] = [{bstack1llll1l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩⅷ"): [bstack1llll1l_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫⅸ")]}]
    if bstack111111lll11_opy_:
        hook_data[bstack1llll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨⅹ")] = bstack111111lll11_opy_.result
        hook_data[bstack1llll1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪⅺ")] = bstack11l11ll1lll_opy_(bstack111l1l11ll_opy_[bstack1llll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧⅻ")], bstack111l1l11ll_opy_[bstack1llll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩⅼ")])
        hook_data[bstack1llll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪⅽ")] = bstack111l1l11ll_opy_[bstack1llll1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫⅾ")]
        if hook_data[bstack1llll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧⅿ")] == bstack1llll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨↀ"):
            hook_data[bstack1llll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨↁ")] = bstack1llllll1ll_opy_.bstack1111l11l11_opy_(bstack111111lll11_opy_.exception_type)
            hook_data[bstack1llll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫↂ")] = [{bstack1llll1l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧↃ"): bstack11l1llll1ll_opy_(bstack111111lll11_opy_.exception)}]
    return hook_data
def bstack1111111l1l1_opy_(test, bstack111l11ll11_opy_, bstack111lll1l_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1llll1l_opy_ (u"ࠬࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠤ࠲ࠦࡻࡾࠩↄ").format(bstack111lll1l_opy_))
    bstack111lll1ll1_opy_ = bstack111111ll1ll_opy_(test, bstack111l11ll11_opy_, result, call, bstack111lll1l_opy_, outcome)
    driver = getattr(test, bstack1llll1l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧↅ"), None)
    if bstack111lll1l_opy_ == bstack1llll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨↆ") and driver:
        bstack111lll1ll1_opy_[bstack1llll1l_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧↇ")] = bstack1llllll1ll_opy_.bstack11l1111111_opy_(driver)
    if bstack111lll1l_opy_ == bstack1llll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪↈ"):
        bstack111lll1l_opy_ = bstack1llll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ↉")
    bstack111l11l11l_opy_ = {
        bstack1llll1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ↊"): bstack111lll1l_opy_,
        bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ↋"): bstack111lll1ll1_opy_
    }
    bstack1llllll1ll_opy_.bstack1l1ll11111_opy_(bstack111l11l11l_opy_)
    if bstack111lll1l_opy_ == bstack1llll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ↌"):
        threading.current_thread().bstackTestMeta = {bstack1llll1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ↍"): bstack1llll1l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ↎")}
    elif bstack111lll1l_opy_ == bstack1llll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ↏"):
        threading.current_thread().bstackTestMeta = {bstack1llll1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ←"): getattr(result, bstack1llll1l_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ↑"), bstack1llll1l_opy_ (u"ࠬ࠭→"))}
def bstack11111l1111l_opy_(test, bstack111l11ll11_opy_, bstack111lll1l_opy_, result=None, call=None, outcome=None, bstack111111lll11_opy_=None):
    logger.debug(bstack1llll1l_opy_ (u"࠭ࡳࡦࡰࡧࡣ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡥࡷࡧࡱࡸ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡪࡲࡳࡰࠦࡤࡢࡶࡤ࠰ࠥ࡫ࡶࡦࡰࡷࡘࡾࡶࡥࠡ࠯ࠣࡿࢂ࠭↓").format(bstack111lll1l_opy_))
    hook_data = bstack111111l1lll_opy_(test, bstack111l11ll11_opy_, bstack111lll1l_opy_, result, call, outcome, bstack111111lll11_opy_)
    bstack111l11l11l_opy_ = {
        bstack1llll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ↔"): bstack111lll1l_opy_,
        bstack1llll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪ↕"): hook_data
    }
    bstack1llllll1ll_opy_.bstack1l1ll11111_opy_(bstack111l11l11l_opy_)
def bstack111l111l1l_opy_(bstack111l11ll11_opy_):
    if not bstack111l11ll11_opy_:
        return None
    if bstack111l11ll11_opy_.get(bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ↖"), None):
        return getattr(bstack111l11ll11_opy_[bstack1llll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭↗")], bstack1llll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ↘"), None)
    return bstack111l11ll11_opy_.get(bstack1llll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪ↙"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.LOG, bstack1llll1l1lll_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_.LOG, bstack1llll1l1lll_opy_.POST, request, caplog)
        return # skip all existing bstack111111ll1l1_opy_
    try:
        if not bstack1llllll1ll_opy_.on():
            return
        places = [bstack1llll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ↚"), bstack1llll1l_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ↛"), bstack1llll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ↜")]
        logs = []
        for bstack111111ll111_opy_ in places:
            records = caplog.get_records(bstack111111ll111_opy_)
            bstack11111l111l1_opy_ = bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ↝") if bstack111111ll111_opy_ == bstack1llll1l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ↞") else bstack1llll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ↟")
            bstack11111l11ll1_opy_ = request.node.nodeid + (bstack1llll1l_opy_ (u"ࠬ࠭↠") if bstack111111ll111_opy_ == bstack1llll1l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ↡") else bstack1llll1l_opy_ (u"ࠧ࠮ࠩ↢") + bstack111111ll111_opy_)
            test_uuid = bstack111l111l1l_opy_(_111l1l111l_opy_.get(bstack11111l11ll1_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11l1ll111l1_opy_(record.message):
                    continue
                logs.append({
                    bstack1llll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ↣"): bstack11l1ll11l11_opy_(record.created).isoformat() + bstack1llll1l_opy_ (u"ࠩ࡝ࠫ↤"),
                    bstack1llll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ↥"): record.levelname,
                    bstack1llll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ↦"): record.message,
                    bstack11111l111l1_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1llllll1ll_opy_.bstack111l1l11l_opy_(logs)
    except Exception as err:
        print(bstack1llll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ↧"), str(err))
def bstack1l11ll1l1l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11l1l1l111_opy_
    bstack11lll1l111_opy_ = bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ↨"), None) and bstack11l11111_opy_(
            threading.current_thread(), bstack1llll1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭↩"), None)
    bstack111l111l_opy_ = getattr(driver, bstack1llll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ↪"), None) != None and getattr(driver, bstack1llll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ↫"), None) == True
    if sequence == bstack1llll1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ↬") and driver != None:
      if not bstack11l1l1l111_opy_ and bstack1ll111l111l_opy_() and bstack1llll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ↭") in CONFIG and CONFIG[bstack1llll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ↮")] == True and bstack1ll11l111l_opy_.bstack111lll11l_opy_(driver_command) and (bstack111l111l_opy_ or bstack11lll1l111_opy_) and not bstack1ll11l1l_opy_(args):
        try:
          bstack11l1l1l111_opy_ = True
          logger.debug(bstack1llll1l_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨ↯").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1llll1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬ↰").format(str(err)))
        bstack11l1l1l111_opy_ = False
    if sequence == bstack1llll1l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ↱"):
        if driver_command == bstack1llll1l_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭↲"):
            bstack1llllll1ll_opy_.bstack111l1ll11_opy_({
                bstack1llll1l_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩ↳"): response[bstack1llll1l_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ↴")],
                bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ↵"): store[bstack1llll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ↶")]
            })
def bstack11ll111111_opy_():
    global bstack1l1llllll1_opy_
    bstack1llll11l1l_opy_.bstack1ll11l1ll1_opy_()
    logging.shutdown()
    bstack1llllll1ll_opy_.bstack111ll1l111_opy_()
    for driver in bstack1l1llllll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1111111l11l_opy_(*args):
    global bstack1l1llllll1_opy_
    bstack1llllll1ll_opy_.bstack111ll1l111_opy_()
    for driver in bstack1l1llllll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1ll1ll1_opy_, stage=STAGE.bstack11111l1l1_opy_, bstack11lll11ll_opy_=bstack1l1111ll1_opy_)
def bstack11l111llll_opy_(self, *args, **kwargs):
    bstack1l1l11111l_opy_ = bstack1l11l1ll_opy_(self, *args, **kwargs)
    bstack1ll11ll11l_opy_ = getattr(threading.current_thread(), bstack1llll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ↷"), None)
    if bstack1ll11ll11l_opy_ and bstack1ll11ll11l_opy_.get(bstack1llll1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ↸"), bstack1llll1l_opy_ (u"ࠩࠪ↹")) == bstack1llll1l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ↺"):
        bstack1llllll1ll_opy_.bstack11ll1l11l1_opy_(self)
    return bstack1l1l11111l_opy_
@measure(event_name=EVENTS.bstack111l1ll1_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack11lll11ll_opy_=bstack1l1111ll1_opy_)
def bstack1ll1l1l1l_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1lll1l111l_opy_ = Config.bstack11l11l11l1_opy_()
    if bstack1lll1l111l_opy_.get_property(bstack1llll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ↻")):
        return
    bstack1lll1l111l_opy_.bstack1lll1ll11_opy_(bstack1llll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ↼"), True)
    global bstack1l11l11l11_opy_
    global bstack11ll11l111_opy_
    bstack1l11l11l11_opy_ = framework_name
    logger.info(bstack11lll1l11_opy_.format(bstack1l11l11l11_opy_.split(bstack1llll1l_opy_ (u"࠭࠭ࠨ↽"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1ll111l111l_opy_():
            Service.start = bstack1ll11l111_opy_
            Service.stop = bstack1l1l111l1_opy_
            webdriver.Remote.get = bstack1l1l11l111_opy_
            webdriver.Remote.__init__ = bstack11l1ll1l_opy_
            if not isinstance(os.getenv(bstack1llll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨ↾")), str):
                return
            WebDriver.close = bstack1l1l1l1ll_opy_
            WebDriver.quit = bstack1l111ll1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1llllll1ll_opy_.on():
            webdriver.Remote.__init__ = bstack11l111llll_opy_
        bstack11ll11l111_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1llll1l_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭↿")):
        bstack11ll11l111_opy_ = eval(os.environ.get(bstack1llll1l_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ⇀")))
    if not bstack11ll11l111_opy_:
        bstack1lll111l1_opy_(bstack1llll1l_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧ⇁"), bstack111l11111_opy_)
    if bstack1ll1l11ll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack1llll1l_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ⇂")) and callable(getattr(RemoteConnection, bstack1llll1l_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭⇃"))):
                RemoteConnection._get_proxy_url = bstack1lllll1l1l_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1lllll1l1l_opy_
        except Exception as e:
            logger.error(bstack1ll11l11ll_opy_.format(str(e)))
    if bstack1llll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⇄") in str(framework_name).lower():
        if not bstack1ll111l111l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11ll11ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1lllll111_opy_
            Config.getoption = bstack1ll111llll_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l1lllllll_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11ll1l1l1l_opy_, stage=STAGE.bstack11111l1l1_opy_, bstack11lll11ll_opy_=bstack1l1111ll1_opy_)
def bstack1l111ll1_opy_(self):
    global bstack1l11l11l11_opy_
    global bstack1llll1111_opy_
    global bstack11ll11ll1_opy_
    try:
        if bstack1llll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⇅") in bstack1l11l11l11_opy_ and self.session_id != None and bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ⇆"), bstack1llll1l_opy_ (u"ࠩࠪ⇇")) != bstack1llll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⇈"):
            bstack1ll1l1lll_opy_ = bstack1llll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⇉") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1llll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⇊")
            bstack1ll1l1l11l_opy_(logger, True)
            if self != None:
                bstack1ll111l11_opy_(self, bstack1ll1l1lll_opy_, bstack1llll1l_opy_ (u"࠭ࠬࠡࠩ⇋").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1lll11ll1l1_opy_(bstack1lll111l1ll_opy_):
            item = store.get(bstack1llll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⇌"), None)
            if item is not None and bstack11l11111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⇍"), None):
                bstack1l1l1ll1l_opy_.bstack1l111l1l_opy_(self, bstack11ll1111_opy_, logger, item)
        threading.current_thread().testStatus = bstack1llll1l_opy_ (u"ࠩࠪ⇎")
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦ⇏") + str(e))
    bstack11ll11ll1_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11lll111l_opy_, stage=STAGE.bstack11111l1l1_opy_, bstack11lll11ll_opy_=bstack1l1111ll1_opy_)
def bstack11l1ll1l_opy_(self, command_executor,
             desired_capabilities=None, bstack11ll1lll_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1llll1111_opy_
    global bstack1l1111ll1_opy_
    global bstack1l111ll1ll_opy_
    global bstack1l11l11l11_opy_
    global bstack1l11l1ll_opy_
    global bstack1l1llllll1_opy_
    global bstack1llllll1l1_opy_
    global bstack1l111l1lll_opy_
    global bstack11ll1111_opy_
    CONFIG[bstack1llll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭⇐")] = str(bstack1l11l11l11_opy_) + str(__version__)
    command_executor = bstack11l1lll111_opy_(bstack1llllll1l1_opy_, CONFIG)
    logger.debug(bstack1ll1lll11_opy_.format(command_executor))
    proxy = bstack1l11111111_opy_(CONFIG, proxy)
    bstack1l111l11l1_opy_ = 0
    try:
        if bstack1l111ll1ll_opy_ is True:
            bstack1l111l11l1_opy_ = int(os.environ.get(bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⇑")))
    except:
        bstack1l111l11l1_opy_ = 0
    bstack11l11llll1_opy_ = bstack111111lll_opy_(CONFIG, bstack1l111l11l1_opy_)
    logger.debug(bstack1lll1ll1ll_opy_.format(str(bstack11l11llll1_opy_)))
    bstack11ll1111_opy_ = CONFIG.get(bstack1llll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⇒"))[bstack1l111l11l1_opy_]
    if bstack1llll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⇓") in CONFIG and CONFIG[bstack1llll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ⇔")]:
        bstack111lllll1_opy_(bstack11l11llll1_opy_, bstack1l111l1lll_opy_)
    if bstack11l1lll1_opy_.bstack1ll1111ll_opy_(CONFIG, bstack1l111l11l1_opy_) and bstack11l1lll1_opy_.bstack11ll1l1ll1_opy_(bstack11l11llll1_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1lll11ll1l1_opy_(bstack1lll111l1ll_opy_):
            bstack11l1lll1_opy_.set_capabilities(bstack11l11llll1_opy_, CONFIG)
    if desired_capabilities:
        bstack1ll111ll_opy_ = bstack1l1l1l11ll_opy_(desired_capabilities)
        bstack1ll111ll_opy_[bstack1llll1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ⇕")] = bstack1ll1lll1ll_opy_(CONFIG)
        bstack111ll1lll_opy_ = bstack111111lll_opy_(bstack1ll111ll_opy_)
        if bstack111ll1lll_opy_:
            bstack11l11llll1_opy_ = update(bstack111ll1lll_opy_, bstack11l11llll1_opy_)
        desired_capabilities = None
    if options:
        bstack1l1111l11l_opy_(options, bstack11l11llll1_opy_)
    if not options:
        options = bstack1lllllll1_opy_(bstack11l11llll1_opy_)
    if proxy and bstack1lll11ll1_opy_() >= version.parse(bstack1llll1l_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪ⇖")):
        options.proxy(proxy)
    if options and bstack1lll11ll1_opy_() >= version.parse(bstack1llll1l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ⇗")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1lll11ll1_opy_() < version.parse(bstack1llll1l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ⇘")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11l11llll1_opy_)
    logger.info(bstack11ll111ll_opy_)
    bstack1l1lll111l_opy_.end(EVENTS.bstack111l1ll1_opy_.value, EVENTS.bstack111l1ll1_opy_.value + bstack1llll1l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ⇙"),
                               EVENTS.bstack111l1ll1_opy_.value + bstack1llll1l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ⇚"), True, None)
    if bstack1lll11ll1_opy_() >= version.parse(bstack1llll1l_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ⇛")):
        bstack1l11l1ll_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll11ll1_opy_() >= version.parse(bstack1llll1l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ⇜")):
        bstack1l11l1ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack11ll1lll_opy_=bstack11ll1lll_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll11ll1_opy_() >= version.parse(bstack1llll1l_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ⇝")):
        bstack1l11l1ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11ll1lll_opy_=bstack11ll1lll_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1l11l1ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11ll1lll_opy_=bstack11ll1lll_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1l11ll1l11_opy_ = bstack1llll1l_opy_ (u"ࠫࠬ⇞")
        if bstack1lll11ll1_opy_() >= version.parse(bstack1llll1l_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭⇟")):
            bstack1l11ll1l11_opy_ = self.caps.get(bstack1llll1l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ⇠"))
        else:
            bstack1l11ll1l11_opy_ = self.capabilities.get(bstack1llll1l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ⇡"))
        if bstack1l11ll1l11_opy_:
            bstack1l11lll11l_opy_(bstack1l11ll1l11_opy_)
            if bstack1lll11ll1_opy_() <= version.parse(bstack1llll1l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ⇢")):
                self.command_executor._url = bstack1llll1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ⇣") + bstack1llllll1l1_opy_ + bstack1llll1l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ⇤")
            else:
                self.command_executor._url = bstack1llll1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ⇥") + bstack1l11ll1l11_opy_ + bstack1llll1l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ⇦")
            logger.debug(bstack1l1l11l1l1_opy_.format(bstack1l11ll1l11_opy_))
        else:
            logger.debug(bstack1l1l1l11l1_opy_.format(bstack1llll1l_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ⇧")))
    except Exception as e:
        logger.debug(bstack1l1l1l11l1_opy_.format(e))
    bstack1llll1111_opy_ = self.session_id
    if bstack1llll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⇨") in bstack1l11l11l11_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1llll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⇩"), None)
        if item:
            bstack11111l111ll_opy_ = getattr(item, bstack1llll1l_opy_ (u"ࠩࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪࡥࡳࡵࡣࡵࡸࡪࡪࠧ⇪"), False)
            if not getattr(item, bstack1llll1l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⇫"), None) and bstack11111l111ll_opy_:
                setattr(store[bstack1llll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⇬")], bstack1llll1l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⇭"), self)
        bstack1ll11ll11l_opy_ = getattr(threading.current_thread(), bstack1llll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧ⇮"), None)
        if bstack1ll11ll11l_opy_ and bstack1ll11ll11l_opy_.get(bstack1llll1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⇯"), bstack1llll1l_opy_ (u"ࠨࠩ⇰")) == bstack1llll1l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⇱"):
            bstack1llllll1ll_opy_.bstack11ll1l11l1_opy_(self)
    bstack1l1llllll1_opy_.append(self)
    if bstack1llll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⇲") in CONFIG and bstack1llll1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⇳") in CONFIG[bstack1llll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⇴")][bstack1l111l11l1_opy_]:
        bstack1l1111ll1_opy_ = CONFIG[bstack1llll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⇵")][bstack1l111l11l1_opy_][bstack1llll1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⇶")]
    logger.debug(bstack111l1111l_opy_.format(bstack1llll1111_opy_))
@measure(event_name=EVENTS.bstack11l1lll1l_opy_, stage=STAGE.bstack11111l1l1_opy_, bstack11lll11ll_opy_=bstack1l1111ll1_opy_)
def bstack1l1l11l111_opy_(self, url):
    global bstack1l1l1l111l_opy_
    global CONFIG
    try:
        bstack1ll11ll1ll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11ll1llll1_opy_.format(str(err)))
    try:
        bstack1l1l1l111l_opy_(self, url)
    except Exception as e:
        try:
            bstack1ll11ll1l1_opy_ = str(e)
            if any(err_msg in bstack1ll11ll1l1_opy_ for err_msg in bstack1l11ll111l_opy_):
                bstack1ll11ll1ll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11ll1llll1_opy_.format(str(err)))
        raise e
def bstack1l1111l1_opy_(item, when):
    global bstack11ll1l11l_opy_
    try:
        bstack11ll1l11l_opy_(item, when)
    except Exception as e:
        pass
def bstack1l1lllllll_opy_(item, call, rep):
    global bstack1ll111ll1_opy_
    global bstack1l1llllll1_opy_
    name = bstack1llll1l_opy_ (u"ࠨࠩ⇷")
    try:
        if rep.when == bstack1llll1l_opy_ (u"ࠩࡦࡥࡱࡲࠧ⇸"):
            bstack1llll1111_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack1llll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⇹"))
            try:
                if (str(skipSessionName).lower() != bstack1llll1l_opy_ (u"ࠫࡹࡸࡵࡦࠩ⇺")):
                    name = str(rep.nodeid)
                    bstack1l1ll1ll_opy_ = bstack11llll11l_opy_(bstack1llll1l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⇻"), name, bstack1llll1l_opy_ (u"࠭ࠧ⇼"), bstack1llll1l_opy_ (u"ࠧࠨ⇽"), bstack1llll1l_opy_ (u"ࠨࠩ⇾"), bstack1llll1l_opy_ (u"ࠩࠪ⇿"))
                    os.environ[bstack1llll1l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭∀")] = name
                    for driver in bstack1l1llllll1_opy_:
                        if bstack1llll1111_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1ll1ll_opy_)
            except Exception as e:
                logger.debug(bstack1llll1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ∁").format(str(e)))
            try:
                bstack1llllll11l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1llll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭∂"):
                    status = bstack1llll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭∃") if rep.outcome.lower() == bstack1llll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ∄") else bstack1llll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ∅")
                    reason = bstack1llll1l_opy_ (u"ࠩࠪ∆")
                    if status == bstack1llll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ∇"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1llll1l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ∈") if status == bstack1llll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ∉") else bstack1llll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ∊")
                    data = name + bstack1llll1l_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ∋") if status == bstack1llll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ∌") else name + bstack1llll1l_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬ∍") + reason
                    bstack1l111lll11_opy_ = bstack11llll11l_opy_(bstack1llll1l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ∎"), bstack1llll1l_opy_ (u"ࠫࠬ∏"), bstack1llll1l_opy_ (u"ࠬ࠭∐"), bstack1llll1l_opy_ (u"࠭ࠧ∑"), level, data)
                    for driver in bstack1l1llllll1_opy_:
                        if bstack1llll1111_opy_ == driver.session_id:
                            driver.execute_script(bstack1l111lll11_opy_)
            except Exception as e:
                logger.debug(bstack1llll1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ−").format(str(e)))
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬ∓").format(str(e)))
    bstack1ll111ll1_opy_(item, call, rep)
notset = Notset()
def bstack1ll111llll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11ll111l1l_opy_
    if str(name).lower() == bstack1llll1l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩ∔"):
        return bstack1llll1l_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤ∕")
    else:
        return bstack11ll111l1l_opy_(self, name, default, skip)
def bstack1lllll1l1l_opy_(self):
    global CONFIG
    global bstack1l1l11ll1l_opy_
    try:
        proxy = bstack111111l1l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1llll1l_opy_ (u"ࠫ࠳ࡶࡡࡤࠩ∖")):
                proxies = bstack1ll11lll1l_opy_(proxy, bstack11l1lll111_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l11ll1l_opy_ = proxies.popitem()
                    if bstack1llll1l_opy_ (u"ࠧࡀ࠯࠰ࠤ∗") in bstack1l11ll1l_opy_:
                        return bstack1l11ll1l_opy_
                    else:
                        return bstack1llll1l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ∘") + bstack1l11ll1l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1llll1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦ∙").format(str(e)))
    return bstack1l1l11ll1l_opy_(self)
def bstack1ll1l11ll_opy_():
    return (bstack1llll1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ√") in CONFIG or bstack1llll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭∛") in CONFIG) and bstack11llll1111_opy_() and bstack1lll11ll1_opy_() >= version.parse(
        bstack1ll11lll_opy_)
def bstack1ll11l11_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l1111ll1_opy_
    global bstack1l111ll1ll_opy_
    global bstack1l11l11l11_opy_
    CONFIG[bstack1llll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ∜")] = str(bstack1l11l11l11_opy_) + str(__version__)
    bstack1l111l11l1_opy_ = 0
    try:
        if bstack1l111ll1ll_opy_ is True:
            bstack1l111l11l1_opy_ = int(os.environ.get(bstack1llll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ∝")))
    except:
        bstack1l111l11l1_opy_ = 0
    CONFIG[bstack1llll1l_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ∞")] = True
    bstack11l11llll1_opy_ = bstack111111lll_opy_(CONFIG, bstack1l111l11l1_opy_)
    logger.debug(bstack1lll1ll1ll_opy_.format(str(bstack11l11llll1_opy_)))
    if CONFIG.get(bstack1llll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ∟")):
        bstack111lllll1_opy_(bstack11l11llll1_opy_, bstack1l111l1lll_opy_)
    if bstack1llll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ∠") in CONFIG and bstack1llll1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭∡") in CONFIG[bstack1llll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ∢")][bstack1l111l11l1_opy_]:
        bstack1l1111ll1_opy_ = CONFIG[bstack1llll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭∣")][bstack1l111l11l1_opy_][bstack1llll1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ∤")]
    import urllib
    import json
    if bstack1llll1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ∥") in CONFIG and str(CONFIG[bstack1llll1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ∦")]).lower() != bstack1llll1l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭∧"):
        bstack1ll1111l_opy_ = bstack1l111111ll_opy_()
        bstack11llll1l11_opy_ = bstack1ll1111l_opy_ + urllib.parse.quote(json.dumps(bstack11l11llll1_opy_))
    else:
        bstack11llll1l11_opy_ = bstack1llll1l_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪ∨") + urllib.parse.quote(json.dumps(bstack11l11llll1_opy_))
    browser = self.connect(bstack11llll1l11_opy_)
    return browser
def bstack11lll1ll_opy_():
    global bstack11ll11l111_opy_
    global bstack1l11l11l11_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1lll111l_opy_
        if not bstack1ll111l111l_opy_():
            global bstack1l1l1ll111_opy_
            if not bstack1l1l1ll111_opy_:
                from bstack_utils.helper import bstack1l11l1l1ll_opy_, bstack1ll1l11l1_opy_
                bstack1l1l1ll111_opy_ = bstack1l11l1l1ll_opy_()
                bstack1ll1l11l1_opy_(bstack1l11l11l11_opy_)
            BrowserType.connect = bstack1lll111l_opy_
            return
        BrowserType.launch = bstack1ll11l11_opy_
        bstack11ll11l111_opy_ = True
    except Exception as e:
        pass
def bstack11111l11l1l_opy_():
    global CONFIG
    global bstack11lll111l1_opy_
    global bstack1llllll1l1_opy_
    global bstack1l111l1lll_opy_
    global bstack1l111ll1ll_opy_
    global bstack111l11l1_opy_
    CONFIG = json.loads(os.environ.get(bstack1llll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨ∩")))
    bstack11lll111l1_opy_ = eval(os.environ.get(bstack1llll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ∪")))
    bstack1llllll1l1_opy_ = os.environ.get(bstack1llll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫ∫"))
    bstack11lll11l1_opy_(CONFIG, bstack11lll111l1_opy_)
    bstack111l11l1_opy_ = bstack1llll11l1l_opy_.bstack1l1l11l1_opy_(CONFIG, bstack111l11l1_opy_)
    if cli.bstack11l111l1l_opy_():
        bstack1ll1ll1ll_opy_.invoke(bstack1ll111111_opy_.CONNECT, bstack11l1lll11_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ∬"), bstack1llll1l_opy_ (u"࠭࠰ࠨ∭")))
        cli.bstack1lll1111111_opy_(cli_context.platform_index)
        cli.bstack1llll1lll1l_opy_(bstack11l1lll111_opy_(bstack1llllll1l1_opy_, CONFIG), cli_context.platform_index, bstack1lllllll1_opy_)
        cli.bstack1lll111l11l_opy_()
        logger.debug(bstack1llll1l_opy_ (u"ࠢࡄࡎࡌࠤ࡮ࡹࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨ∮") + str(cli_context.platform_index) + bstack1llll1l_opy_ (u"ࠣࠤ∯"))
        return # skip all existing bstack111111ll1l1_opy_
    global bstack1l11l1ll_opy_
    global bstack11ll11ll1_opy_
    global bstack11l1lll1l1_opy_
    global bstack11l1lll1ll_opy_
    global bstack1l111ll1l_opy_
    global bstack11l1ll1ll1_opy_
    global bstack1lll1lll1_opy_
    global bstack1l1l1l111l_opy_
    global bstack1l1l11ll1l_opy_
    global bstack11ll111l1l_opy_
    global bstack11ll1l11l_opy_
    global bstack1ll111ll1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l11l1ll_opy_ = webdriver.Remote.__init__
        bstack11ll11ll1_opy_ = WebDriver.quit
        bstack1lll1lll1_opy_ = WebDriver.close
        bstack1l1l1l111l_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1llll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ∰") in CONFIG or bstack1llll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ∱") in CONFIG) and bstack11llll1111_opy_():
        if bstack1lll11ll1_opy_() < version.parse(bstack1ll11lll_opy_):
            logger.error(bstack1llllllll1_opy_.format(bstack1lll11ll1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack1llll1l_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ∲")) and callable(getattr(RemoteConnection, bstack1llll1l_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭∳"))):
                    bstack1l1l11ll1l_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1l1l11ll1l_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1ll11l11ll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11ll111l1l_opy_ = Config.getoption
        from _pytest import runner
        bstack11ll1l11l_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack11111l1ll_opy_)
    try:
        from pytest_bdd import reporting
        bstack1ll111ll1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ∴"))
    bstack1l111l1lll_opy_ = CONFIG.get(bstack1llll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ∵"), {}).get(bstack1llll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ∶"))
    bstack1l111ll1ll_opy_ = True
    bstack1ll1l1l1l_opy_(bstack111l11ll_opy_)
if (bstack11l11l11l1l_opy_()):
    bstack11111l11l1l_opy_()
@bstack111l1l1111_opy_(class_method=False)
def bstack1111111l1ll_opy_(hook_name, event, bstack1l111l111l1_opy_=None):
    if hook_name not in [bstack1llll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ∷"), bstack1llll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ∸"), bstack1llll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ∹"), bstack1llll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ∺"), bstack1llll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ∻"), bstack1llll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ∼"), bstack1llll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧ∽"), bstack1llll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫ∾")]:
        return
    node = store[bstack1llll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ∿")]
    if hook_name in [bstack1llll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ≀"), bstack1llll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ≁")]:
        node = store[bstack1llll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ≂")]
    elif hook_name in [bstack1llll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ≃"), bstack1llll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ≄")]:
        node = store[bstack1llll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ≅")]
    hook_type = bstack111l111111l_opy_(hook_name)
    if event == bstack1llll1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ≆"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_[hook_type], bstack1llll1l1lll_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l1l11ll_opy_ = {
            bstack1llll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ≇"): uuid,
            bstack1llll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ≈"): bstack1l1ll1l1l_opy_(),
            bstack1llll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫ≉"): bstack1llll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ≊"),
            bstack1llll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ≋"): hook_type,
            bstack1llll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ≌"): hook_name
        }
        store[bstack1llll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ≍")].append(uuid)
        bstack111111l11ll_opy_ = node.nodeid
        if hook_type == bstack1llll1l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ≎"):
            if not _111l1l111l_opy_.get(bstack111111l11ll_opy_, None):
                _111l1l111l_opy_[bstack111111l11ll_opy_] = {bstack1llll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ≏"): []}
            _111l1l111l_opy_[bstack111111l11ll_opy_][bstack1llll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ≐")].append(bstack111l1l11ll_opy_[bstack1llll1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ≑")])
        _111l1l111l_opy_[bstack111111l11ll_opy_ + bstack1llll1l_opy_ (u"ࠨ࠯ࠪ≒") + hook_name] = bstack111l1l11ll_opy_
        bstack11111l1111l_opy_(node, bstack111l1l11ll_opy_, bstack1llll1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ≓"))
    elif event == bstack1llll1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ≔"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1llll1ll_opy_[hook_type], bstack1llll1l1lll_opy_.POST, node, None, bstack1l111l111l1_opy_)
            return
        bstack11l11111ll_opy_ = node.nodeid + bstack1llll1l_opy_ (u"ࠫ࠲࠭≕") + hook_name
        _111l1l111l_opy_[bstack11l11111ll_opy_][bstack1llll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ≖")] = bstack1l1ll1l1l_opy_()
        bstack11111l11111_opy_(_111l1l111l_opy_[bstack11l11111ll_opy_][bstack1llll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ≗")])
        bstack11111l1111l_opy_(node, _111l1l111l_opy_[bstack11l11111ll_opy_], bstack1llll1l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ≘"), bstack111111lll11_opy_=bstack1l111l111l1_opy_)
def bstack111111lllll_opy_():
    global bstack111111ll11l_opy_
    if bstack11l111l1_opy_():
        bstack111111ll11l_opy_ = bstack1llll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ≙")
    else:
        bstack111111ll11l_opy_ = bstack1llll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ≚")
@bstack1llllll1ll_opy_.bstack1111l11lll1_opy_
def bstack111111l11l1_opy_():
    bstack111111lllll_opy_()
    if cli.is_running():
        try:
            bstack11l111l1111_opy_(bstack1111111l1ll_opy_)
        except Exception as e:
            logger.debug(bstack1llll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦ≛").format(e))
        return
    if bstack11llll1111_opy_():
        bstack1lll1l111l_opy_ = Config.bstack11l11l11l1_opy_()
        bstack1llll1l_opy_ (u"ࠫࠬ࠭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡳࡴࡵࠦ࠽ࠡ࠳࠯ࠤࡲࡵࡤࡠࡧࡻࡩࡨࡻࡴࡦࠢࡪࡩࡹࡹࠠࡶࡵࡨࡨࠥ࡬࡯ࡳࠢࡤ࠵࠶ࡿࠠࡤࡱࡰࡱࡦࡴࡤࡴ࠯ࡺࡶࡦࡶࡰࡪࡰࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡉࡳࡷࠦࡰࡱࡲࠣࡂࠥ࠷ࠬࠡ࡯ࡲࡨࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡴࡸࡲࠥࡨࡥࡤࡣࡸࡷࡪࠦࡩࡵࠢ࡬ࡷࠥࡶࡡࡵࡥ࡫ࡩࡩࠦࡩ࡯ࠢࡤࠤࡩ࡯ࡦࡧࡧࡵࡩࡳࡺࠠࡱࡴࡲࡧࡪࡹࡳࠡ࡫ࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬ࡺࡹࠠࡸࡧࠣࡲࡪ࡫ࡤࠡࡶࡲࠤࡺࡹࡥࠡࡕࡨࡰࡪࡴࡩࡶ࡯ࡓࡥࡹࡩࡨࠩࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡬ࡦࡴࡤ࡭ࡧࡵ࠭ࠥ࡬࡯ࡳࠢࡳࡴࡵࠦ࠾ࠡ࠳ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠬ࠭ࠧ≜")
        if bstack1lll1l111l_opy_.get_property(bstack1llll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ≝")):
            if CONFIG.get(bstack1llll1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭≞")) is not None and int(CONFIG[bstack1llll1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ≟")]) > 1:
                bstack1ll111l11l_opy_(bstack1l11ll1l1l_opy_)
            return
        bstack1ll111l11l_opy_(bstack1l11ll1l1l_opy_)
    try:
        bstack11l111l1111_opy_(bstack1111111l1ll_opy_)
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡸࠦࡰࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ≠").format(e))
bstack111111l11l1_opy_()