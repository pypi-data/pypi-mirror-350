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
import collections
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11ll11l1l1l_opy_, bstack1ll11l1ll_opy_, bstack11l1l1l11_opy_, bstack11lll1llll_opy_,
                                    bstack11ll11111ll_opy_, bstack11ll1111111_opy_, bstack11ll11l1ll1_opy_, bstack11ll1l11l1l_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1ll111l1_opy_, bstack1ll11l11ll_opy_
from bstack_utils.proxy import bstack111llll11_opy_, bstack111111l1l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1llll11l1l_opy_
from browserstack_sdk._version import __version__
bstack1lll1l111l_opy_ = Config.bstack11l11l11l1_opy_()
logger = bstack1llll11l1l_opy_.get_logger(__name__, bstack1llll11l1l_opy_.bstack1lll1llllll_opy_())
def bstack11lll11lll1_opy_(config):
    return config[bstack1llll1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᨼ")]
def bstack11lll1llll1_opy_(config):
    return config[bstack1llll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᨽ")]
def bstack1ll1l1l1ll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1l1l11l1_opy_(obj):
    values = []
    bstack11l1l11l11l_opy_ = re.compile(bstack1llll1l_opy_ (u"ࡷࠨ࡞ࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣࡡࡪࠫࠥࠤᨾ"), re.I)
    for key in obj.keys():
        if bstack11l1l11l11l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l1llll111_opy_(config):
    tags = []
    tags.extend(bstack11l1l1l11l1_opy_(os.environ))
    tags.extend(bstack11l1l1l11l1_opy_(config))
    return tags
def bstack11l1lll1l1l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1llllll1_opy_(bstack11l11llll11_opy_):
    if not bstack11l11llll11_opy_:
        return bstack1llll1l_opy_ (u"࠭ࠧᨿ")
    return bstack1llll1l_opy_ (u"ࠢࡼࡿࠣࠬࢀࢃࠩࠣᩀ").format(bstack11l11llll11_opy_.name, bstack11l11llll11_opy_.email)
def bstack11llll1111l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1lllll1l_opy_ = repo.common_dir
        info = {
            bstack1llll1l_opy_ (u"ࠣࡵ࡫ࡥࠧᩁ"): repo.head.commit.hexsha,
            bstack1llll1l_opy_ (u"ࠤࡶ࡬ࡴࡸࡴࡠࡵ࡫ࡥࠧᩂ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1llll1l_opy_ (u"ࠥࡦࡷࡧ࡮ࡤࡪࠥᩃ"): repo.active_branch.name,
            bstack1llll1l_opy_ (u"ࠦࡹࡧࡧࠣᩄ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1llll1l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࠣᩅ"): bstack11l1llllll1_opy_(repo.head.commit.committer),
            bstack1llll1l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࡡࡧࡥࡹ࡫ࠢᩆ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1llll1l_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࠢᩇ"): bstack11l1llllll1_opy_(repo.head.commit.author),
            bstack1llll1l_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡠࡦࡤࡸࡪࠨᩈ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1llll1l_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᩉ"): repo.head.commit.message,
            bstack1llll1l_opy_ (u"ࠥࡶࡴࡵࡴࠣᩊ"): repo.git.rev_parse(bstack1llll1l_opy_ (u"ࠦ࠲࠳ࡳࡩࡱࡺ࠱ࡹࡵࡰ࡭ࡧࡹࡩࡱࠨᩋ")),
            bstack1llll1l_opy_ (u"ࠧࡩ࡯࡮࡯ࡲࡲࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨᩌ"): bstack11l1lllll1l_opy_,
            bstack1llll1l_opy_ (u"ࠨࡷࡰࡴ࡮ࡸࡷ࡫ࡥࡠࡩ࡬ࡸࡤࡪࡩࡳࠤᩍ"): subprocess.check_output([bstack1llll1l_opy_ (u"ࠢࡨ࡫ࡷࠦᩎ"), bstack1llll1l_opy_ (u"ࠣࡴࡨࡺ࠲ࡶࡡࡳࡵࡨࠦᩏ"), bstack1llll1l_opy_ (u"ࠤ࠰࠱࡬࡯ࡴ࠮ࡥࡲࡱࡲࡵ࡮࠮ࡦ࡬ࡶࠧᩐ")]).strip().decode(
                bstack1llll1l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᩑ")),
            bstack1llll1l_opy_ (u"ࠦࡱࡧࡳࡵࡡࡷࡥ࡬ࠨᩒ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1llll1l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡸࡥࡳࡪࡰࡦࡩࡤࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᩓ"): repo.git.rev_list(
                bstack1llll1l_opy_ (u"ࠨࡻࡾ࠰࠱ࡿࢂࠨᩔ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l1l11l1l1_opy_ = []
        for remote in remotes:
            bstack11l1l1l111l_opy_ = {
                bstack1llll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩕ"): remote.name,
                bstack1llll1l_opy_ (u"ࠣࡷࡵࡰࠧᩖ"): remote.url,
            }
            bstack11l1l11l1l1_opy_.append(bstack11l1l1l111l_opy_)
        bstack11l1ll1l1l1_opy_ = {
            bstack1llll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᩗ"): bstack1llll1l_opy_ (u"ࠥ࡫࡮ࡺࠢᩘ"),
            **info,
            bstack1llll1l_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡷࠧᩙ"): bstack11l1l11l1l1_opy_
        }
        bstack11l1ll1l1l1_opy_ = bstack11l1l1111l1_opy_(bstack11l1ll1l1l1_opy_)
        return bstack11l1ll1l1l1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1llll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᩚ").format(err))
        return {}
def bstack11l1l1111l1_opy_(bstack11l1ll1l1l1_opy_):
    bstack11l1l1ll1ll_opy_ = bstack11l11llll1l_opy_(bstack11l1ll1l1l1_opy_)
    if bstack11l1l1ll1ll_opy_ and bstack11l1l1ll1ll_opy_ > bstack11ll11111ll_opy_:
        bstack11l1ll1l11l_opy_ = bstack11l1l1ll1ll_opy_ - bstack11ll11111ll_opy_
        bstack11l11lll1ll_opy_ = bstack11l1l1lll1l_opy_(bstack11l1ll1l1l1_opy_[bstack1llll1l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢᩛ")], bstack11l1ll1l11l_opy_)
        bstack11l1ll1l1l1_opy_[bstack1llll1l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣᩜ")] = bstack11l11lll1ll_opy_
        logger.info(bstack1llll1l_opy_ (u"ࠣࡖ࡫ࡩࠥࡩ࡯࡮࡯࡬ࡸࠥ࡮ࡡࡴࠢࡥࡩࡪࡴࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦ࠱ࠤࡘ࡯ࡺࡦࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࠥࡧࡦࡵࡧࡵࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࢀࢃࠠࡌࡄࠥᩝ")
                    .format(bstack11l11llll1l_opy_(bstack11l1ll1l1l1_opy_) / 1024))
    return bstack11l1ll1l1l1_opy_
def bstack11l11llll1l_opy_(bstack1111l1l1_opy_):
    try:
        if bstack1111l1l1_opy_:
            bstack11l1llll11l_opy_ = json.dumps(bstack1111l1l1_opy_)
            bstack11l1lll1111_opy_ = sys.getsizeof(bstack11l1llll11l_opy_)
            return bstack11l1lll1111_opy_
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡥࡤࡰࡨࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡳࡪࡼࡨࠤࡴ࡬ࠠࡋࡕࡒࡒࠥࡵࡢ࡫ࡧࡦࡸ࠿ࠦࡻࡾࠤᩞ").format(e))
    return -1
def bstack11l1l1lll1l_opy_(field, bstack11l1ll1lll1_opy_):
    try:
        bstack11l1l1l1l1l_opy_ = len(bytes(bstack11ll1111111_opy_, bstack1llll1l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᩟")))
        bstack11l1l111111_opy_ = bytes(field, bstack1llll1l_opy_ (u"ࠫࡺࡺࡦ࠮࠺᩠ࠪ"))
        bstack11l11l111l1_opy_ = len(bstack11l1l111111_opy_)
        bstack11l11l1111l_opy_ = ceil(bstack11l11l111l1_opy_ - bstack11l1ll1lll1_opy_ - bstack11l1l1l1l1l_opy_)
        if bstack11l11l1111l_opy_ > 0:
            bstack11l1lll11l1_opy_ = bstack11l1l111111_opy_[:bstack11l11l1111l_opy_].decode(bstack1llll1l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᩡ"), errors=bstack1llll1l_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪ࠭ᩢ")) + bstack11ll1111111_opy_
            return bstack11l1lll11l1_opy_
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡪࡲࡤ࠭ࠢࡱࡳࡹ࡮ࡩ࡯ࡩࠣࡻࡦࡹࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦࠣ࡬ࡪࡸࡥ࠻ࠢࡾࢁࠧᩣ").format(e))
    return field
def bstack1llllll111_opy_():
    env = os.environ
    if (bstack1llll1l_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨᩤ") in env and len(env[bstack1llll1l_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢᩥ")]) > 0) or (
            bstack1llll1l_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤᩦ") in env and len(env[bstack1llll1l_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥᩧ")]) > 0):
        return {
            bstack1llll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᩨ"): bstack1llll1l_opy_ (u"ࠨࡊࡦࡰ࡮࡭ࡳࡹࠢᩩ"),
            bstack1llll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᩪ"): env.get(bstack1llll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᩫ")),
            bstack1llll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᩬ"): env.get(bstack1llll1l_opy_ (u"ࠥࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᩭ")),
            bstack1llll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᩮ"): env.get(bstack1llll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᩯ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠨࡃࡊࠤᩰ")) == bstack1llll1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᩱ") and bstack111l11ll1_opy_(env.get(bstack1llll1l_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡄࡋࠥᩲ"))):
        return {
            bstack1llll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᩳ"): bstack1llll1l_opy_ (u"ࠥࡇ࡮ࡸࡣ࡭ࡧࡆࡍࠧᩴ"),
            bstack1llll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᩵"): env.get(bstack1llll1l_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ᩶")),
            bstack1llll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᩷"): env.get(bstack1llll1l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡋࡑࡅࠦ᩸")),
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᩹"): env.get(bstack1llll1l_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࠧ᩺"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠥࡇࡎࠨ᩻")) == bstack1llll1l_opy_ (u"ࠦࡹࡸࡵࡦࠤ᩼") and bstack111l11ll1_opy_(env.get(bstack1llll1l_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࠧ᩽"))):
        return {
            bstack1llll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᩾"): bstack1llll1l_opy_ (u"ࠢࡕࡴࡤࡺ࡮ࡹࠠࡄࡋ᩿ࠥ"),
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᪀"): env.get(bstack1llll1l_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠ࡙ࡈࡆࡤ࡛ࡒࡍࠤ᪁")),
            bstack1llll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᪂"): env.get(bstack1llll1l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ᪃")),
            bstack1llll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᪄"): env.get(bstack1llll1l_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᪅"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠢࡄࡋࠥ᪆")) == bstack1llll1l_opy_ (u"ࠣࡶࡵࡹࡪࠨ᪇") and env.get(bstack1llll1l_opy_ (u"ࠤࡆࡍࡤࡔࡁࡎࡇࠥ᪈")) == bstack1llll1l_opy_ (u"ࠥࡧࡴࡪࡥࡴࡪ࡬ࡴࠧ᪉"):
        return {
            bstack1llll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪊"): bstack1llll1l_opy_ (u"ࠧࡉ࡯ࡥࡧࡶ࡬࡮ࡶࠢ᪋"),
            bstack1llll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᪌"): None,
            bstack1llll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪍"): None,
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᪎"): None
        }
    if env.get(bstack1llll1l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌࠧ᪏")) and env.get(bstack1llll1l_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨ᪐")):
        return {
            bstack1llll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪑"): bstack1llll1l_opy_ (u"ࠧࡈࡩࡵࡤࡸࡧࡰ࡫ࡴࠣ᪒"),
            bstack1llll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᪓"): env.get(bstack1llll1l_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡋࡎ࡚࡟ࡉࡖࡗࡔࡤࡕࡒࡊࡉࡌࡒࠧ᪔")),
            bstack1llll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᪕"): None,
            bstack1llll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᪖"): env.get(bstack1llll1l_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᪗"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠦࡈࡏࠢ᪘")) == bstack1llll1l_opy_ (u"ࠧࡺࡲࡶࡧࠥ᪙") and bstack111l11ll1_opy_(env.get(bstack1llll1l_opy_ (u"ࠨࡄࡓࡑࡑࡉࠧ᪚"))):
        return {
            bstack1llll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᪛"): bstack1llll1l_opy_ (u"ࠣࡆࡵࡳࡳ࡫ࠢ᪜"),
            bstack1llll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᪝"): env.get(bstack1llll1l_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡎࡌࡒࡐࠨ᪞")),
            bstack1llll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᪟"): None,
            bstack1llll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᪠"): env.get(bstack1llll1l_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᪡"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠢࡄࡋࠥ᪢")) == bstack1llll1l_opy_ (u"ࠣࡶࡵࡹࡪࠨ᪣") and bstack111l11ll1_opy_(env.get(bstack1llll1l_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࠧ᪤"))):
        return {
            bstack1llll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣ᪥"): bstack1llll1l_opy_ (u"ࠦࡘ࡫࡭ࡢࡲ࡫ࡳࡷ࡫ࠢ᪦"),
            bstack1llll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᪧ"): env.get(bstack1llll1l_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡒࡖࡌࡇࡎࡊ࡜ࡄࡘࡎࡕࡎࡠࡗࡕࡐࠧ᪨")),
            bstack1llll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪩"): env.get(bstack1llll1l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ᪪")),
            bstack1llll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᪫"): env.get(bstack1llll1l_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡍࡉࠨ᪬"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠦࡈࡏࠢ᪭")) == bstack1llll1l_opy_ (u"ࠧࡺࡲࡶࡧࠥ᪮") and bstack111l11ll1_opy_(env.get(bstack1llll1l_opy_ (u"ࠨࡇࡊࡖࡏࡅࡇࡥࡃࡊࠤ᪯"))):
        return {
            bstack1llll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᪰"): bstack1llll1l_opy_ (u"ࠣࡉ࡬ࡸࡑࡧࡢࠣ᪱"),
            bstack1llll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᪲"): env.get(bstack1llll1l_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢ࡙ࡗࡒࠢ᪳")),
            bstack1llll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᪴"): env.get(bstack1llll1l_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡔࡁࡎࡇ᪵ࠥ")),
            bstack1llll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶ᪶ࠧ"): env.get(bstack1llll1l_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡊࡆ᪷ࠥ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠣࡅࡌ᪸ࠦ")) == bstack1llll1l_opy_ (u"ࠤࡷࡶࡺ࡫᪹ࠢ") and bstack111l11ll1_opy_(env.get(bstack1llll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࠨ᪺"))):
        return {
            bstack1llll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪻"): bstack1llll1l_opy_ (u"ࠧࡈࡵࡪ࡮ࡧ࡯࡮ࡺࡥࠣ᪼"),
            bstack1llll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᪽"): env.get(bstack1llll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᪾")),
            bstack1llll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧᪿࠥ"): env.get(bstack1llll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡒࡁࡃࡇࡏᫀࠦ")) or env.get(bstack1llll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨ᫁")),
            bstack1llll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᫂"): env.get(bstack1llll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘ᫃ࠢ"))
        }
    if bstack111l11ll1_opy_(env.get(bstack1llll1l_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄ᫄ࠣ"))):
        return {
            bstack1llll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᫅"): bstack1llll1l_opy_ (u"ࠣࡘ࡬ࡷࡺࡧ࡬ࠡࡕࡷࡹࡩ࡯࡯ࠡࡖࡨࡥࡲࠦࡓࡦࡴࡹ࡭ࡨ࡫ࡳࠣ᫆"),
            bstack1llll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᫇"): bstack1llll1l_opy_ (u"ࠥࡿࢂࢁࡽࠣ᫈").format(env.get(bstack1llll1l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧ᫉")), env.get(bstack1llll1l_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࡌࡈ᫊ࠬ"))),
            bstack1llll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᫋"): env.get(bstack1llll1l_opy_ (u"ࠢࡔ࡛ࡖࡘࡊࡓ࡟ࡅࡇࡉࡍࡓࡏࡔࡊࡑࡑࡍࡉࠨᫌ")),
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᫍ"): env.get(bstack1llll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᫎ"))
        }
    if bstack111l11ll1_opy_(env.get(bstack1llll1l_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࠧ᫏"))):
        return {
            bstack1llll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᫐"): bstack1llll1l_opy_ (u"ࠧࡇࡰࡱࡸࡨࡽࡴࡸࠢ᫑"),
            bstack1llll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᫒"): bstack1llll1l_opy_ (u"ࠢࡼࡿ࠲ࡴࡷࡵࡪࡦࡥࡷ࠳ࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠨ᫓").format(env.get(bstack1llll1l_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢ࡙ࡗࡒࠧ᫔")), env.get(bstack1llll1l_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡆࡉࡃࡐࡗࡑࡘࡤࡔࡁࡎࡇࠪ᫕")), env.get(bstack1llll1l_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡓࡍࡗࡊࠫ᫖")), env.get(bstack1llll1l_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨ᫗"))),
            bstack1llll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᫘"): env.get(bstack1llll1l_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ᫙")),
            bstack1llll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᫚"): env.get(bstack1llll1l_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᫛"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠤࡄ࡞࡚ࡘࡅࡠࡊࡗࡘࡕࡥࡕࡔࡇࡕࡣࡆࡍࡅࡏࡖࠥ᫜")) and env.get(bstack1llll1l_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧ᫝")):
        return {
            bstack1llll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᫞"): bstack1llll1l_opy_ (u"ࠧࡇࡺࡶࡴࡨࠤࡈࡏࠢ᫟"),
            bstack1llll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᫠"): bstack1llll1l_opy_ (u"ࠢࡼࡿࡾࢁ࠴ࡥࡢࡶ࡫࡯ࡨ࠴ࡸࡥࡴࡷ࡯ࡸࡸࡅࡢࡶ࡫࡯ࡨࡎࡪ࠽ࡼࡿࠥ᫡").format(env.get(bstack1llll1l_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫ᫢")), env.get(bstack1llll1l_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࠧ᫣")), env.get(bstack1llll1l_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪ᫤"))),
            bstack1llll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᫥"): env.get(bstack1llll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧ᫦")),
            bstack1llll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᫧"): env.get(bstack1llll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢ᫨"))
        }
    if any([env.get(bstack1llll1l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᫩")), env.get(bstack1llll1l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡘࡅࡔࡑࡏ࡚ࡊࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣ᫪")), env.get(bstack1llll1l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢ᫫"))]):
        return {
            bstack1llll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᫬"): bstack1llll1l_opy_ (u"ࠧࡇࡗࡔࠢࡆࡳࡩ࡫ࡂࡶ࡫࡯ࡨࠧ᫭"),
            bstack1llll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᫮"): env.get(bstack1llll1l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡔ࡚ࡈࡌࡊࡅࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᫯")),
            bstack1llll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᫰"): env.get(bstack1llll1l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ᫱")),
            bstack1llll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᫲"): env.get(bstack1llll1l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ᫳"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥ᫴")):
        return {
            bstack1llll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᫵"): bstack1llll1l_opy_ (u"ࠢࡃࡣࡰࡦࡴࡵࠢ᫶"),
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᫷"): env.get(bstack1llll1l_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡓࡧࡶࡹࡱࡺࡳࡖࡴ࡯ࠦ᫸")),
            bstack1llll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᫹"): env.get(bstack1llll1l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡸ࡮࡯ࡳࡶࡍࡳࡧࡔࡡ࡮ࡧࠥ᫺")),
            bstack1llll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᫻"): env.get(bstack1llll1l_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦ᫼"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࠣ᫽")) or env.get(bstack1llll1l_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥ᫾")):
        return {
            bstack1llll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᫿"): bstack1llll1l_opy_ (u"࡛ࠥࡪࡸࡣ࡬ࡧࡵࠦᬀ"),
            bstack1llll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᬁ"): env.get(bstack1llll1l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᬂ")),
            bstack1llll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᬃ"): bstack1llll1l_opy_ (u"ࠢࡎࡣ࡬ࡲࠥࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠢᬄ") if env.get(bstack1llll1l_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥᬅ")) else None,
            bstack1llll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᬆ"): env.get(bstack1llll1l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡌࡏࡔࡠࡅࡒࡑࡒࡏࡔࠣᬇ"))
        }
    if any([env.get(bstack1llll1l_opy_ (u"ࠦࡌࡉࡐࡠࡒࡕࡓࡏࡋࡃࡕࠤᬈ")), env.get(bstack1llll1l_opy_ (u"ࠧࡍࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨᬉ")), env.get(bstack1llll1l_opy_ (u"ࠨࡇࡐࡑࡊࡐࡊࡥࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨᬊ"))]):
        return {
            bstack1llll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᬋ"): bstack1llll1l_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡅ࡯ࡳࡺࡪࠢᬌ"),
            bstack1llll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᬍ"): None,
            bstack1llll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᬎ"): env.get(bstack1llll1l_opy_ (u"ࠦࡕࡘࡏࡋࡇࡆࡘࡤࡏࡄࠣᬏ")),
            bstack1llll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᬐ"): env.get(bstack1llll1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣᬑ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࠥᬒ")):
        return {
            bstack1llll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᬓ"): bstack1llll1l_opy_ (u"ࠤࡖ࡬࡮ࡶࡰࡢࡤ࡯ࡩࠧᬔ"),
            bstack1llll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᬕ"): env.get(bstack1llll1l_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᬖ")),
            bstack1llll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᬗ"): bstack1llll1l_opy_ (u"ࠨࡊࡰࡤࠣࠧࢀࢃࠢᬘ").format(env.get(bstack1llll1l_opy_ (u"ࠧࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠪᬙ"))) if env.get(bstack1llll1l_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠦᬚ")) else None,
            bstack1llll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᬛ"): env.get(bstack1llll1l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᬜ"))
        }
    if bstack111l11ll1_opy_(env.get(bstack1llll1l_opy_ (u"ࠦࡓࡋࡔࡍࡋࡉ࡝ࠧᬝ"))):
        return {
            bstack1llll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᬞ"): bstack1llll1l_opy_ (u"ࠨࡎࡦࡶ࡯࡭࡫ࡿࠢᬟ"),
            bstack1llll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᬠ"): env.get(bstack1llll1l_opy_ (u"ࠣࡆࡈࡔࡑࡕ࡙ࡠࡗࡕࡐࠧᬡ")),
            bstack1llll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᬢ"): env.get(bstack1llll1l_opy_ (u"ࠥࡗࡎ࡚ࡅࡠࡐࡄࡑࡊࠨᬣ")),
            bstack1llll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᬤ"): env.get(bstack1llll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᬥ"))
        }
    if bstack111l11ll1_opy_(env.get(bstack1llll1l_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡁࡄࡖࡌࡓࡓ࡙ࠢᬦ"))):
        return {
            bstack1llll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᬧ"): bstack1llll1l_opy_ (u"ࠣࡉ࡬ࡸࡍࡻࡢࠡࡃࡦࡸ࡮ࡵ࡮ࡴࠤᬨ"),
            bstack1llll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᬩ"): bstack1llll1l_opy_ (u"ࠥࡿࢂ࠵ࡻࡾ࠱ࡤࡧࡹ࡯࡯࡯ࡵ࠲ࡶࡺࡴࡳ࠰ࡽࢀࠦᬪ").format(env.get(bstack1llll1l_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡘࡋࡒࡗࡇࡕࡣ࡚ࡘࡌࠨᬫ")), env.get(bstack1llll1l_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡅࡑࡑࡖࡍ࡙ࡕࡒ࡚ࠩᬬ")), env.get(bstack1llll1l_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉ࠭ᬭ"))),
            bstack1llll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᬮ"): env.get(bstack1llll1l_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠ࡙ࡒࡖࡐࡌࡌࡐ࡙ࠥᬯ")),
            bstack1llll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᬰ"): env.get(bstack1llll1l_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠥᬱ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠦࡈࡏࠢᬲ")) == bstack1llll1l_opy_ (u"ࠧࡺࡲࡶࡧࠥᬳ") and env.get(bstack1llll1l_opy_ (u"ࠨࡖࡆࡔࡆࡉࡑࠨ᬴")) == bstack1llll1l_opy_ (u"ࠢ࠲ࠤᬵ"):
        return {
            bstack1llll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᬶ"): bstack1llll1l_opy_ (u"ࠤ࡙ࡩࡷࡩࡥ࡭ࠤᬷ"),
            bstack1llll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᬸ"): bstack1llll1l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࢀࢃࠢᬹ").format(env.get(bstack1llll1l_opy_ (u"ࠬ࡜ࡅࡓࡅࡈࡐࡤ࡛ࡒࡍࠩᬺ"))),
            bstack1llll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᬻ"): None,
            bstack1llll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᬼ"): None,
        }
    if env.get(bstack1llll1l_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᬽ")):
        return {
            bstack1llll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᬾ"): bstack1llll1l_opy_ (u"ࠥࡘࡪࡧ࡭ࡤ࡫ࡷࡽࠧᬿ"),
            bstack1llll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᭀ"): None,
            bstack1llll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᭁ"): env.get(bstack1llll1l_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠢᭂ")),
            bstack1llll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᭃ"): env.get(bstack1llll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘ᭄ࠢ"))
        }
    if any([env.get(bstack1llll1l_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࠧᭅ")), env.get(bstack1llll1l_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡓࡎࠥᭆ")), env.get(bstack1llll1l_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠤᭇ")), env.get(bstack1llll1l_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡖࡈࡅࡒࠨᭈ"))]):
        return {
            bstack1llll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᭉ"): bstack1llll1l_opy_ (u"ࠢࡄࡱࡱࡧࡴࡻࡲࡴࡧࠥᭊ"),
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᭋ"): None,
            bstack1llll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᭌ"): env.get(bstack1llll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᭍")) or None,
            bstack1llll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᭎"): env.get(bstack1llll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ᭏"), 0)
        }
    if env.get(bstack1llll1l_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᭐")):
        return {
            bstack1llll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᭑"): bstack1llll1l_opy_ (u"ࠣࡉࡲࡇࡉࠨ᭒"),
            bstack1llll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᭓"): None,
            bstack1llll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᭔"): env.get(bstack1llll1l_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᭕")),
            bstack1llll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᭖"): env.get(bstack1llll1l_opy_ (u"ࠨࡇࡐࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡈࡕࡕࡏࡖࡈࡖࠧ᭗"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᭘")):
        return {
            bstack1llll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨ᭙"): bstack1llll1l_opy_ (u"ࠤࡆࡳࡩ࡫ࡆࡳࡧࡶ࡬ࠧ᭚"),
            bstack1llll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᭛"): env.get(bstack1llll1l_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᭜")),
            bstack1llll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᭝"): env.get(bstack1llll1l_opy_ (u"ࠨࡃࡇࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤ᭞")),
            bstack1llll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᭟"): env.get(bstack1llll1l_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᭠"))
        }
    return {bstack1llll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᭡"): None}
def get_host_info():
    return {
        bstack1llll1l_opy_ (u"ࠥ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠧ᭢"): platform.node(),
        bstack1llll1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨ᭣"): platform.system(),
        bstack1llll1l_opy_ (u"ࠧࡺࡹࡱࡧࠥ᭤"): platform.machine(),
        bstack1llll1l_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢ᭥"): platform.version(),
        bstack1llll1l_opy_ (u"ࠢࡢࡴࡦ࡬ࠧ᭦"): platform.architecture()[0]
    }
def bstack11llll1111_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1ll11l1l_opy_():
    if bstack1lll1l111l_opy_.get_property(bstack1llll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ᭧")):
        return bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᭨")
    return bstack1llll1l_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠩ᭩")
def bstack11l1l1l1ll1_opy_(driver):
    info = {
        bstack1llll1l_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᭪"): driver.capabilities,
        bstack1llll1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩ᭫"): driver.session_id,
        bstack1llll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ᭬ࠧ"): driver.capabilities.get(bstack1llll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ᭭"), None),
        bstack1llll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ᭮"): driver.capabilities.get(bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᭯"), None),
        bstack1llll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬ᭰"): driver.capabilities.get(bstack1llll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪ᭱"), None),
        bstack1llll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᭲"):driver.capabilities.get(bstack1llll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᭳"), None),
    }
    if bstack11l1ll11l1l_opy_() == bstack1llll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭᭴"):
        if bstack1lll1llll1_opy_():
            info[bstack1llll1l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ᭵")] = bstack1llll1l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ᭶")
        elif driver.capabilities.get(bstack1llll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᭷"), {}).get(bstack1llll1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ᭸"), False):
            info[bstack1llll1l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭᭹")] = bstack1llll1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ᭺")
        else:
            info[bstack1llll1l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ᭻")] = bstack1llll1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ᭼")
    return info
def bstack1lll1llll1_opy_():
    if bstack1lll1l111l_opy_.get_property(bstack1llll1l_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ᭽")):
        return True
    if bstack111l11ll1_opy_(os.environ.get(bstack1llll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ᭾"), None)):
        return True
    return False
def bstack11lll1l1l1_opy_(bstack11l1lll11ll_opy_, url, data, config):
    headers = config.get(bstack1llll1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ᭿"), None)
    proxies = bstack111llll11_opy_(config, url)
    auth = config.get(bstack1llll1l_opy_ (u"ࠬࡧࡵࡵࡪࠪᮀ"), None)
    response = requests.request(
            bstack11l1lll11ll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1111ll11_opy_(bstack11111ll11_opy_, size):
    bstack11l1llll1_opy_ = []
    while len(bstack11111ll11_opy_) > size:
        bstack1l111l111l_opy_ = bstack11111ll11_opy_[:size]
        bstack11l1llll1_opy_.append(bstack1l111l111l_opy_)
        bstack11111ll11_opy_ = bstack11111ll11_opy_[size:]
    bstack11l1llll1_opy_.append(bstack11111ll11_opy_)
    return bstack11l1llll1_opy_
def bstack11l11l1ll11_opy_(message, bstack11l1l111l1l_opy_=False):
    os.write(1, bytes(message, bstack1llll1l_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᮁ")))
    os.write(1, bytes(bstack1llll1l_opy_ (u"ࠧ࡝ࡰࠪᮂ"), bstack1llll1l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᮃ")))
    if bstack11l1l111l1l_opy_:
        with open(bstack1llll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯ࡲ࠵࠶ࡿ࠭ࠨᮄ") + os.environ[bstack1llll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᮅ")] + bstack1llll1l_opy_ (u"ࠫ࠳ࡲ࡯ࡨࠩᮆ"), bstack1llll1l_opy_ (u"ࠬࡧࠧᮇ")) as f:
            f.write(message + bstack1llll1l_opy_ (u"࠭࡜࡯ࠩᮈ"))
def bstack1ll111l111l_opy_():
    return os.environ[bstack1llll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᮉ")].lower() == bstack1llll1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᮊ")
def bstack1ll1l1l11_opy_(bstack11l111llll1_opy_):
    return bstack1llll1l_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨᮋ").format(bstack11ll11l1l1l_opy_, bstack11l111llll1_opy_)
def bstack1l1ll1l1l_opy_():
    return bstack111ll11ll1_opy_().replace(tzinfo=None).isoformat() + bstack1llll1l_opy_ (u"ࠪ࡞ࠬᮌ")
def bstack11l11ll1lll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1llll1l_opy_ (u"ࠫ࡟࠭ᮍ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1llll1l_opy_ (u"ࠬࡠࠧᮎ")))).total_seconds() * 1000
def bstack11l1l11l1ll_opy_(timestamp):
    return bstack11l1ll11l11_opy_(timestamp).isoformat() + bstack1llll1l_opy_ (u"࡚࠭ࠨᮏ")
def bstack11l11l1l1ll_opy_(bstack11l11ll1111_opy_):
    date_format = bstack1llll1l_opy_ (u"࡛ࠧࠦࠨࡱࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪࠬᮐ")
    bstack11l11lll111_opy_ = datetime.datetime.strptime(bstack11l11ll1111_opy_, date_format)
    return bstack11l11lll111_opy_.isoformat() + bstack1llll1l_opy_ (u"ࠨ࡜ࠪᮑ")
def bstack11l11ll1l1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1llll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᮒ")
    else:
        return bstack1llll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᮓ")
def bstack111l11ll1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1llll1l_opy_ (u"ࠫࡹࡸࡵࡦࠩᮔ")
def bstack11l11llllll_opy_(val):
    return val.__str__().lower() == bstack1llll1l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᮕ")
def bstack111l1l1111_opy_(bstack11l1l11l111_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1l11l111_opy_ as e:
                print(bstack1llll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨᮖ").format(func.__name__, bstack11l1l11l111_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1l111l11_opy_(bstack11l1l1lll11_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1l1lll11_opy_(cls, *args, **kwargs)
            except bstack11l1l11l111_opy_ as e:
                print(bstack1llll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢᮗ").format(bstack11l1l1lll11_opy_.__name__, bstack11l1l11l111_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1l111l11_opy_
    else:
        return decorator
def bstack1l111ll11_opy_(bstack1111l1ll1l_opy_):
    if os.getenv(bstack1llll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫᮘ")) is not None:
        return bstack111l11ll1_opy_(os.getenv(bstack1llll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬᮙ")))
    if bstack1llll1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᮚ") in bstack1111l1ll1l_opy_ and bstack11l11llllll_opy_(bstack1111l1ll1l_opy_[bstack1llll1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᮛ")]):
        return False
    if bstack1llll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᮜ") in bstack1111l1ll1l_opy_ and bstack11l11llllll_opy_(bstack1111l1ll1l_opy_[bstack1llll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᮝ")]):
        return False
    return True
def bstack11l111l1_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l11l111ll_opy_ = os.environ.get(bstack1llll1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠢᮞ"), None)
        return bstack11l11l111ll_opy_ is None or bstack11l11l111ll_opy_ == bstack1llll1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᮟ")
    except Exception as e:
        return False
def bstack11l1lll111_opy_(hub_url, CONFIG):
    if bstack1lll11ll1_opy_() <= version.parse(bstack1llll1l_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩᮠ")):
        if hub_url:
            return bstack1llll1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᮡ") + hub_url + bstack1llll1l_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣᮢ")
        return bstack11l1l1l11_opy_
    if hub_url:
        return bstack1llll1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᮣ") + hub_url + bstack1llll1l_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢᮤ")
    return bstack11lll1llll_opy_
def bstack11l11l11l1l_opy_():
    return isinstance(os.getenv(bstack1llll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ᮥ")), str)
def bstack1lll1ll11l_opy_(url):
    return urlparse(url).hostname
def bstack11ll11lll1_opy_(hostname):
    for bstack1l1111llll_opy_ in bstack1ll11l1ll_opy_:
        regex = re.compile(bstack1l1111llll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l11lll1l1_opy_(bstack11l1lllllll_opy_, file_name, logger):
    bstack1l1111l11_opy_ = os.path.join(os.path.expanduser(bstack1llll1l_opy_ (u"ࠨࢀࠪᮦ")), bstack11l1lllllll_opy_)
    try:
        if not os.path.exists(bstack1l1111l11_opy_):
            os.makedirs(bstack1l1111l11_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1llll1l_opy_ (u"ࠩࢁࠫᮧ")), bstack11l1lllllll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1llll1l_opy_ (u"ࠪࡻࠬᮨ")):
                pass
            with open(file_path, bstack1llll1l_opy_ (u"ࠦࡼ࠱ࠢᮩ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1ll111l1_opy_.format(str(e)))
def bstack11l1l11111l_opy_(file_name, key, value, logger):
    file_path = bstack11l11lll1l1_opy_(bstack1llll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯᮪ࠬ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1llll1lll1_opy_ = json.load(open(file_path, bstack1llll1l_opy_ (u"࠭ࡲࡣ᮫ࠩ")))
        else:
            bstack1llll1lll1_opy_ = {}
        bstack1llll1lll1_opy_[key] = value
        with open(file_path, bstack1llll1l_opy_ (u"ࠢࡸ࠭ࠥᮬ")) as outfile:
            json.dump(bstack1llll1lll1_opy_, outfile)
def bstack11l111111_opy_(file_name, logger):
    file_path = bstack11l11lll1l1_opy_(bstack1llll1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᮭ"), file_name, logger)
    bstack1llll1lll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1llll1l_opy_ (u"ࠩࡵࠫᮮ")) as bstack11l1ll11l1_opy_:
            bstack1llll1lll1_opy_ = json.load(bstack11l1ll11l1_opy_)
    return bstack1llll1lll1_opy_
def bstack1lllll1ll1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧᮯ") + file_path + bstack1llll1l_opy_ (u"ࠫࠥ࠭᮰") + str(e))
def bstack1lll11ll1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1llll1l_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢ᮱")
def bstack1ll1lll1ll_opy_(config):
    if bstack1llll1l_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ᮲") in config:
        del (config[bstack1llll1l_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭᮳")])
        return False
    if bstack1lll11ll1_opy_() < version.parse(bstack1llll1l_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧ᮴")):
        return False
    if bstack1lll11ll1_opy_() >= version.parse(bstack1llll1l_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨ᮵")):
        return True
    if bstack1llll1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ᮶") in config and config[bstack1llll1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ᮷")] is False:
        return False
    else:
        return True
def bstack11l11l1111_opy_(args_list, bstack11l11ll1l11_opy_):
    index = -1
    for value in bstack11l11ll1l11_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11lll1l111l_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11lll1l111l_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111ll1llll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111ll1llll_opy_ = bstack111ll1llll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1llll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ᮸"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1llll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᮹"), exception=exception)
    def bstack1111l11l11_opy_(self):
        if self.result != bstack1llll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᮺ"):
            return None
        if isinstance(self.exception_type, str) and bstack1llll1l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᮻ") in self.exception_type:
            return bstack1llll1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᮼ")
        return bstack1llll1l_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᮽ")
    def bstack11l1ll11lll_opy_(self):
        if self.result != bstack1llll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᮾ"):
            return None
        if self.bstack111ll1llll_opy_:
            return self.bstack111ll1llll_opy_
        return bstack11l1llll1ll_opy_(self.exception)
def bstack11l1llll1ll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l1ll111l1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11l11111_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l1llll1_opy_(config, logger):
    try:
        import playwright
        bstack11l11ll111l_opy_ = playwright.__file__
        bstack11l1l1l1lll_opy_ = os.path.split(bstack11l11ll111l_opy_)
        bstack11l1l1111ll_opy_ = bstack11l1l1l1lll_opy_[0] + bstack1llll1l_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨᮿ")
        os.environ[bstack1llll1l_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩᯀ")] = bstack111111l1l_opy_(config)
        with open(bstack11l1l1111ll_opy_, bstack1llll1l_opy_ (u"ࠧࡳࠩᯁ")) as f:
            bstack11l111ll11_opy_ = f.read()
            bstack11l11ll1ll1_opy_ = bstack1llll1l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧᯂ")
            bstack11l11l1l11l_opy_ = bstack11l111ll11_opy_.find(bstack11l11ll1ll1_opy_)
            if bstack11l11l1l11l_opy_ == -1:
              process = subprocess.Popen(bstack1llll1l_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨᯃ"), shell=True, cwd=bstack11l1l1l1lll_opy_[0])
              process.wait()
              bstack11l1ll1ll11_opy_ = bstack1llll1l_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪᯄ")
              bstack11l11l11ll1_opy_ = bstack1llll1l_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣᯅ")
              bstack11l1ll111ll_opy_ = bstack11l111ll11_opy_.replace(bstack11l1ll1ll11_opy_, bstack11l11l11ll1_opy_)
              with open(bstack11l1l1111ll_opy_, bstack1llll1l_opy_ (u"ࠬࡽࠧᯆ")) as f:
                f.write(bstack11l1ll111ll_opy_)
    except Exception as e:
        logger.error(bstack1ll11l11ll_opy_.format(str(e)))
def bstack11llll1l_opy_():
  try:
    bstack11l1l1l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1llll1l_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭ᯇ"))
    bstack11l111lllll_opy_ = []
    if os.path.exists(bstack11l1l1l1l11_opy_):
      with open(bstack11l1l1l1l11_opy_) as f:
        bstack11l111lllll_opy_ = json.load(f)
      os.remove(bstack11l1l1l1l11_opy_)
    return bstack11l111lllll_opy_
  except:
    pass
  return []
def bstack1l11lll11l_opy_(bstack1l11ll1l11_opy_):
  try:
    bstack11l111lllll_opy_ = []
    bstack11l1l1l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1llll1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧᯈ"))
    if os.path.exists(bstack11l1l1l1l11_opy_):
      with open(bstack11l1l1l1l11_opy_) as f:
        bstack11l111lllll_opy_ = json.load(f)
    bstack11l111lllll_opy_.append(bstack1l11ll1l11_opy_)
    with open(bstack11l1l1l1l11_opy_, bstack1llll1l_opy_ (u"ࠨࡹࠪᯉ")) as f:
        json.dump(bstack11l111lllll_opy_, f)
  except:
    pass
def bstack1ll1l1l11l_opy_(logger, bstack11l111lll1l_opy_ = False):
  try:
    test_name = os.environ.get(bstack1llll1l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬᯊ"), bstack1llll1l_opy_ (u"ࠪࠫᯋ"))
    if test_name == bstack1llll1l_opy_ (u"ࠫࠬᯌ"):
        test_name = threading.current_thread().__dict__.get(bstack1llll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫᯍ"), bstack1llll1l_opy_ (u"࠭ࠧᯎ"))
    bstack11l1l11ll11_opy_ = bstack1llll1l_opy_ (u"ࠧ࠭ࠢࠪᯏ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l111lll1l_opy_:
        bstack1l111l11l1_opy_ = os.environ.get(bstack1llll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᯐ"), bstack1llll1l_opy_ (u"ࠩ࠳ࠫᯑ"))
        bstack11111111l_opy_ = {bstack1llll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᯒ"): test_name, bstack1llll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᯓ"): bstack11l1l11ll11_opy_, bstack1llll1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᯔ"): bstack1l111l11l1_opy_}
        bstack11l11ll11ll_opy_ = []
        bstack11l11l1lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1llll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᯕ"))
        if os.path.exists(bstack11l11l1lll1_opy_):
            with open(bstack11l11l1lll1_opy_) as f:
                bstack11l11ll11ll_opy_ = json.load(f)
        bstack11l11ll11ll_opy_.append(bstack11111111l_opy_)
        with open(bstack11l11l1lll1_opy_, bstack1llll1l_opy_ (u"ࠧࡸࠩᯖ")) as f:
            json.dump(bstack11l11ll11ll_opy_, f)
    else:
        bstack11111111l_opy_ = {bstack1llll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᯗ"): test_name, bstack1llll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᯘ"): bstack11l1l11ll11_opy_, bstack1llll1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᯙ"): str(multiprocessing.current_process().name)}
        if bstack1llll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨᯚ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11111111l_opy_)
  except Exception as e:
      logger.warn(bstack1llll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᯛ").format(e))
def bstack1111l11l1_opy_(error_message, test_name, index, logger):
  try:
    bstack11l1l1ll11l_opy_ = []
    bstack11111111l_opy_ = {bstack1llll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᯜ"): test_name, bstack1llll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᯝ"): error_message, bstack1llll1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᯞ"): index}
    bstack11l1l111lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1llll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᯟ"))
    if os.path.exists(bstack11l1l111lll_opy_):
        with open(bstack11l1l111lll_opy_) as f:
            bstack11l1l1ll11l_opy_ = json.load(f)
    bstack11l1l1ll11l_opy_.append(bstack11111111l_opy_)
    with open(bstack11l1l111lll_opy_, bstack1llll1l_opy_ (u"ࠪࡻࠬᯠ")) as f:
        json.dump(bstack11l1l1ll11l_opy_, f)
  except Exception as e:
    logger.warn(bstack1llll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᯡ").format(e))
def bstack1l1l11ll11_opy_(bstack1ll111l1l1_opy_, name, logger):
  try:
    bstack11111111l_opy_ = {bstack1llll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᯢ"): name, bstack1llll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᯣ"): bstack1ll111l1l1_opy_, bstack1llll1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᯤ"): str(threading.current_thread()._name)}
    return bstack11111111l_opy_
  except Exception as e:
    logger.warn(bstack1llll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧᯥ").format(e))
  return
def bstack11l1ll1l1ll_opy_():
    return platform.system() == bstack1llll1l_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵ᯦ࠪ")
def bstack1l1l1lllll_opy_(bstack11l1l1ll111_opy_, config, logger):
    bstack11l1ll11ll1_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l1l1ll111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤᯧ").format(e))
    return bstack11l1ll11ll1_opy_
def bstack11l1lll1ll1_opy_(bstack11l1l1l11ll_opy_, bstack11l11l1l111_opy_):
    bstack11l1l1ll1l1_opy_ = version.parse(bstack11l1l1l11ll_opy_)
    bstack11l11lll11l_opy_ = version.parse(bstack11l11l1l111_opy_)
    if bstack11l1l1ll1l1_opy_ > bstack11l11lll11l_opy_:
        return 1
    elif bstack11l1l1ll1l1_opy_ < bstack11l11lll11l_opy_:
        return -1
    else:
        return 0
def bstack111ll11ll1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1ll11l11_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1ll11111_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11ll1111l_opy_(options, framework, config, bstack11l1l1llll_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1llll1l_opy_ (u"ࠫ࡬࡫ࡴࠨᯨ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11l1l11111_opy_ = caps.get(bstack1llll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᯩ"))
    bstack11l1lll1l11_opy_ = True
    bstack11111111_opy_ = os.environ[bstack1llll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᯪ")]
    bstack1ll1l1111l1_opy_ = config.get(bstack1llll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᯫ"), False)
    if bstack1ll1l1111l1_opy_:
        bstack1llll11l1l1_opy_ = config.get(bstack1llll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᯬ"), {})
        bstack1llll11l1l1_opy_[bstack1llll1l_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬᯭ")] = os.getenv(bstack1llll1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᯮ"))
        bstack11lll11ll1l_opy_ = json.loads(os.getenv(bstack1llll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᯯ"), bstack1llll1l_opy_ (u"ࠬࢁࡽࠨᯰ"))).get(bstack1llll1l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᯱ"))
    if bstack11l11llllll_opy_(caps.get(bstack1llll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ᯲࠭"))) or bstack11l11llllll_opy_(caps.get(bstack1llll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨ᯳"))):
        bstack11l1lll1l11_opy_ = False
    if bstack1ll1lll1ll_opy_({bstack1llll1l_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤ᯴"): bstack11l1lll1l11_opy_}):
        bstack11l1l11111_opy_ = bstack11l1l11111_opy_ or {}
        bstack11l1l11111_opy_[bstack1llll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ᯵")] = bstack11l1ll11111_opy_(framework)
        bstack11l1l11111_opy_[bstack1llll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᯶")] = bstack1ll111l111l_opy_()
        bstack11l1l11111_opy_[bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᯷")] = bstack11111111_opy_
        bstack11l1l11111_opy_[bstack1llll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ᯸")] = bstack11l1l1llll_opy_
        if bstack1ll1l1111l1_opy_:
            bstack11l1l11111_opy_[bstack1llll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᯹")] = bstack1ll1l1111l1_opy_
            bstack11l1l11111_opy_[bstack1llll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᯺")] = bstack1llll11l1l1_opy_
            bstack11l1l11111_opy_[bstack1llll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᯻")][bstack1llll1l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᯼")] = bstack11lll11ll1l_opy_
        if getattr(options, bstack1llll1l_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ᯽"), None):
            options.set_capability(bstack1llll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᯾"), bstack11l1l11111_opy_)
        else:
            options[bstack1llll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᯿")] = bstack11l1l11111_opy_
    else:
        if getattr(options, bstack1llll1l_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨᰀ"), None):
            options.set_capability(bstack1llll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᰁ"), bstack11l1ll11111_opy_(framework))
            options.set_capability(bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᰂ"), bstack1ll111l111l_opy_())
            options.set_capability(bstack1llll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᰃ"), bstack11111111_opy_)
            options.set_capability(bstack1llll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᰄ"), bstack11l1l1llll_opy_)
            if bstack1ll1l1111l1_opy_:
                options.set_capability(bstack1llll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᰅ"), bstack1ll1l1111l1_opy_)
                options.set_capability(bstack1llll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᰆ"), bstack1llll11l1l1_opy_)
                options.set_capability(bstack1llll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠴ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᰇ"), bstack11lll11ll1l_opy_)
        else:
            options[bstack1llll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᰈ")] = bstack11l1ll11111_opy_(framework)
            options[bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᰉ")] = bstack1ll111l111l_opy_()
            options[bstack1llll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᰊ")] = bstack11111111_opy_
            options[bstack1llll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᰋ")] = bstack11l1l1llll_opy_
            if bstack1ll1l1111l1_opy_:
                options[bstack1llll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᰌ")] = bstack1ll1l1111l1_opy_
                options[bstack1llll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᰍ")] = bstack1llll11l1l1_opy_
                options[bstack1llll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᰎ")][bstack1llll1l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᰏ")] = bstack11lll11ll1l_opy_
    return options
def bstack11l1lllll11_opy_(bstack11l111lll11_opy_, framework):
    bstack11l1l1llll_opy_ = bstack1lll1l111l_opy_.get_property(bstack1llll1l_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦᰐ"))
    if bstack11l111lll11_opy_ and len(bstack11l111lll11_opy_.split(bstack1llll1l_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᰑ"))) > 1:
        ws_url = bstack11l111lll11_opy_.split(bstack1llll1l_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᰒ"))[0]
        if bstack1llll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᰓ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l1l11llll_opy_ = json.loads(urllib.parse.unquote(bstack11l111lll11_opy_.split(bstack1llll1l_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᰔ"))[1]))
            bstack11l1l11llll_opy_ = bstack11l1l11llll_opy_ or {}
            bstack11111111_opy_ = os.environ[bstack1llll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᰕ")]
            bstack11l1l11llll_opy_[bstack1llll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᰖ")] = str(framework) + str(__version__)
            bstack11l1l11llll_opy_[bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᰗ")] = bstack1ll111l111l_opy_()
            bstack11l1l11llll_opy_[bstack1llll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᰘ")] = bstack11111111_opy_
            bstack11l1l11llll_opy_[bstack1llll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᰙ")] = bstack11l1l1llll_opy_
            bstack11l111lll11_opy_ = bstack11l111lll11_opy_.split(bstack1llll1l_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᰚ"))[0] + bstack1llll1l_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᰛ") + urllib.parse.quote(json.dumps(bstack11l1l11llll_opy_))
    return bstack11l111lll11_opy_
def bstack1l11l1l1ll_opy_():
    global bstack1l1l1ll111_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l1l1ll111_opy_ = BrowserType.connect
    return bstack1l1l1ll111_opy_
def bstack1ll1l11l1_opy_(framework_name):
    global bstack1l11l11l11_opy_
    bstack1l11l11l11_opy_ = framework_name
    return framework_name
def bstack1lll111l_opy_(self, *args, **kwargs):
    global bstack1l1l1ll111_opy_
    try:
        global bstack1l11l11l11_opy_
        if bstack1llll1l_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᰜ") in kwargs:
            kwargs[bstack1llll1l_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᰝ")] = bstack11l1lllll11_opy_(
                kwargs.get(bstack1llll1l_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᰞ"), None),
                bstack1l11l11l11_opy_
            )
    except Exception as e:
        logger.error(bstack1llll1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥᰟ").format(str(e)))
    return bstack1l1l1ll111_opy_(self, *args, **kwargs)
def bstack11l1l1lllll_opy_(bstack11l1lll111l_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack111llll11_opy_(bstack11l1lll111l_opy_, bstack1llll1l_opy_ (u"ࠦࠧᰠ"))
        if proxies and proxies.get(bstack1llll1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᰡ")):
            parsed_url = urlparse(proxies.get(bstack1llll1l_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᰢ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1llll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪᰣ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1llll1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫᰤ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1llll1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬᰥ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1llll1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᰦ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1111111l_opy_(bstack11l1lll111l_opy_):
    bstack11l1ll1111l_opy_ = {
        bstack11ll1l11l1l_opy_[bstack11l11l1llll_opy_]: bstack11l1lll111l_opy_[bstack11l11l1llll_opy_]
        for bstack11l11l1llll_opy_ in bstack11l1lll111l_opy_
        if bstack11l11l1llll_opy_ in bstack11ll1l11l1l_opy_
    }
    bstack11l1ll1111l_opy_[bstack1llll1l_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦᰧ")] = bstack11l1l1lllll_opy_(bstack11l1lll111l_opy_, bstack1lll1l111l_opy_.get_property(bstack1llll1l_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᰨ")))
    bstack11l11l11111_opy_ = [element.lower() for element in bstack11ll11l1ll1_opy_]
    bstack11l11l11l11_opy_(bstack11l1ll1111l_opy_, bstack11l11l11111_opy_)
    return bstack11l1ll1111l_opy_
def bstack11l11l11l11_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1llll1l_opy_ (u"ࠨࠪࠫࠬ࠭ࠦᰩ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11l11l11l11_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11l11l11l11_opy_(item, keys)
def bstack1l1lll1l111_opy_():
    bstack11l111ll1ll_opy_ = [os.environ.get(bstack1llll1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡊࡎࡈࡗࡤࡊࡉࡓࠤᰪ")), os.path.join(os.path.expanduser(bstack1llll1l_opy_ (u"ࠣࢀࠥᰫ")), bstack1llll1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᰬ")), os.path.join(bstack1llll1l_opy_ (u"ࠪ࠳ࡹࡳࡰࠨᰭ"), bstack1llll1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᰮ"))]
    for path in bstack11l111ll1ll_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1llll1l_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧᰯ") + str(path) + bstack1llll1l_opy_ (u"ࠨࠧࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤᰰ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1llll1l_opy_ (u"ࠢࡈ࡫ࡹ࡭ࡳ࡭ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠥ࡬࡯ࡳࠢࠪࠦᰱ") + str(path) + bstack1llll1l_opy_ (u"ࠣࠩࠥᰲ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1llll1l_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤᰳ") + str(path) + bstack1llll1l_opy_ (u"ࠥࠫࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡨࡢࡵࠣࡸ࡭࡫ࠠࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹ࠮ࠣᰴ"))
            else:
                logger.debug(bstack1llll1l_opy_ (u"ࠦࡈࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࠬࠨᰵ") + str(path) + bstack1llll1l_opy_ (u"ࠧ࠭ࠠࡸ࡫ࡷ࡬ࠥࡽࡲࡪࡶࡨࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮࠯ࠤᰶ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1llll1l_opy_ (u"ࠨࡏࡱࡧࡵࡥࡹ࡯࡯࡯ࠢࡶࡹࡨࡩࡥࡦࡦࡨࡨࠥ࡬࡯ࡳ᰷ࠢࠪࠦ") + str(path) + bstack1llll1l_opy_ (u"ࠢࠨ࠰ࠥ᰸"))
            return path
        except Exception as e:
            logger.debug(bstack1llll1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡷࡳࠤ࡫࡯࡬ࡦࠢࠪࡿࡵࡧࡴࡩࡿࠪ࠾ࠥࠨ᰹") + str(e) + bstack1llll1l_opy_ (u"ࠤࠥ᰺"))
    logger.debug(bstack1llll1l_opy_ (u"ࠥࡅࡱࡲࠠࡱࡣࡷ࡬ࡸࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠢ᰻"))
    return None
@measure(event_name=EVENTS.bstack11ll11l11l1_opy_, stage=STAGE.bstack11111l1l1_opy_)
def bstack1lllll1l111_opy_(binary_path, bstack1llll1ll11l_opy_, bs_config):
    logger.debug(bstack1llll1l_opy_ (u"ࠦࡈࡻࡲࡳࡧࡱࡸࠥࡉࡌࡊࠢࡓࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࡀࠠࡼࡿࠥ᰼").format(binary_path))
    bstack11l1l1llll1_opy_ = bstack1llll1l_opy_ (u"ࠬ࠭᰽")
    bstack11l11l11lll_opy_ = {
        bstack1llll1l_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ᰾"): __version__,
        bstack1llll1l_opy_ (u"ࠢࡰࡵࠥ᰿"): platform.system(),
        bstack1llll1l_opy_ (u"ࠣࡱࡶࡣࡦࡸࡣࡩࠤ᱀"): platform.machine(),
        bstack1llll1l_opy_ (u"ࠤࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ᱁"): bstack1llll1l_opy_ (u"ࠪ࠴ࠬ᱂"),
        bstack1llll1l_opy_ (u"ࠦࡸࡪ࡫ࡠ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠥ᱃"): bstack1llll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ᱄")
    }
    bstack11l11l1ll1l_opy_(bstack11l11l11lll_opy_)
    try:
        if binary_path:
            bstack11l11l11lll_opy_[bstack1llll1l_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫ᱅")] = subprocess.check_output([binary_path, bstack1llll1l_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣ᱆")]).strip().decode(bstack1llll1l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᱇"))
        response = requests.request(
            bstack1llll1l_opy_ (u"ࠩࡊࡉ࡙࠭᱈"),
            url=bstack1ll1l1l11_opy_(bstack11ll11l1111_opy_),
            headers=None,
            auth=(bs_config[bstack1llll1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ᱉")], bs_config[bstack1llll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ᱊")]),
            json=None,
            params=bstack11l11l11lll_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1llll1l_opy_ (u"ࠬࡻࡲ࡭ࠩ᱋") in data.keys() and bstack1llll1l_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪ࡟ࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᱌") in data.keys():
            logger.debug(bstack1llll1l_opy_ (u"ࠢࡏࡧࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡤ࡬ࡲࡦࡸࡹ࠭ࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡦ࡮ࡴࡡࡳࡻࠣࡺࡪࡸࡳࡪࡱࡱ࠾ࠥࢁࡽࠣᱍ").format(bstack11l11l11lll_opy_[bstack1llll1l_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᱎ")]))
            if bstack1llll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠬᱏ") in os.environ:
                logger.debug(bstack1llll1l_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡨࡩ࡯ࡣࡵࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡢࡵࠣࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠣ࡭ࡸࠦࡳࡦࡶࠥ᱐"))
                data[bstack1llll1l_opy_ (u"ࠫࡺࡸ࡬ࠨ᱑")] = os.environ[bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠨ᱒")]
            bstack11l1lll1lll_opy_ = bstack11l1l111ll1_opy_(data[bstack1llll1l_opy_ (u"࠭ࡵࡳ࡮ࠪ᱓")], bstack1llll1ll11l_opy_)
            bstack11l1l1llll1_opy_ = os.path.join(bstack1llll1ll11l_opy_, bstack11l1lll1lll_opy_)
            os.chmod(bstack11l1l1llll1_opy_, 0o777) # bstack11l1llll1l1_opy_ permission
            return bstack11l1l1llll1_opy_
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡲࡪࡽࠠࡔࡆࡎࠤࢀࢃࠢ᱔").format(e))
    return binary_path
def bstack11l11l1ll1l_opy_(bstack11l11l11lll_opy_):
    try:
        if bstack1llll1l_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧ᱕") not in bstack11l11l11lll_opy_[bstack1llll1l_opy_ (u"ࠩࡲࡷࠬ᱖")].lower():
            return
        if os.path.exists(bstack1llll1l_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡱࡶ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧ᱗")):
            with open(bstack1llll1l_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡲࡷ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨ᱘"), bstack1llll1l_opy_ (u"ࠧࡸࠢ᱙")) as f:
                bstack11l1l11ll1l_opy_ = {}
                for line in f:
                    if bstack1llll1l_opy_ (u"ࠨ࠽ࠣᱚ") in line:
                        key, value = line.rstrip().split(bstack1llll1l_opy_ (u"ࠢ࠾ࠤᱛ"), 1)
                        bstack11l1l11ll1l_opy_[key] = value.strip(bstack1llll1l_opy_ (u"ࠨࠤ࡟ࠫࠬᱜ"))
                bstack11l11l11lll_opy_[bstack1llll1l_opy_ (u"ࠩࡧ࡭ࡸࡺࡲࡰࠩᱝ")] = bstack11l1l11ll1l_opy_.get(bstack1llll1l_opy_ (u"ࠥࡍࡉࠨᱞ"), bstack1llll1l_opy_ (u"ࠦࠧᱟ"))
        elif os.path.exists(bstack1llll1l_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡥࡱࡶࡩ࡯ࡧ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᱠ")):
            bstack11l11l11lll_opy_[bstack1llll1l_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭ᱡ")] = bstack1llll1l_opy_ (u"ࠧࡢ࡮ࡳ࡭ࡳ࡫ࠧᱢ")
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡦ࡬ࡷࡹࡸ࡯ࠡࡱࡩࠤࡱ࡯࡮ࡶࡺࠥᱣ") + e)
@measure(event_name=EVENTS.bstack11ll11l11ll_opy_, stage=STAGE.bstack11111l1l1_opy_)
def bstack11l1l111ll1_opy_(bstack11l1l1l1111_opy_, bstack11l1ll1llll_opy_):
    logger.debug(bstack1llll1l_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮࠼ࠣࠦᱤ") + str(bstack11l1l1l1111_opy_) + bstack1llll1l_opy_ (u"ࠥࠦᱥ"))
    zip_path = os.path.join(bstack11l1ll1llll_opy_, bstack1llll1l_opy_ (u"ࠦࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࡠࡨ࡬ࡰࡪ࠴ࡺࡪࡲࠥᱦ"))
    bstack11l1lll1lll_opy_ = bstack1llll1l_opy_ (u"ࠬ࠭ᱧ")
    with requests.get(bstack11l1l1l1111_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1llll1l_opy_ (u"ࠨࡷࡣࠤᱨ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1llll1l_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹ࠯ࠤᱩ"))
    with zipfile.ZipFile(zip_path, bstack1llll1l_opy_ (u"ࠨࡴࠪᱪ")) as zip_ref:
        bstack11l11l1l1l1_opy_ = zip_ref.namelist()
        if len(bstack11l11l1l1l1_opy_) > 0:
            bstack11l1lll1lll_opy_ = bstack11l11l1l1l1_opy_[0] # bstack11l11lllll1_opy_ bstack11ll1111l1l_opy_ will be bstack11l1ll1ll1l_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l1ll1llll_opy_)
        logger.debug(bstack1llll1l_opy_ (u"ࠤࡉ࡭ࡱ࡫ࡳࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡦࡺࡷࡶࡦࡩࡴࡦࡦࠣࡸࡴࠦࠧࠣᱫ") + str(bstack11l1ll1llll_opy_) + bstack1llll1l_opy_ (u"ࠥࠫࠧᱬ"))
    os.remove(zip_path)
    return bstack11l1lll1lll_opy_
def get_cli_dir():
    bstack11l1l11lll1_opy_ = bstack1l1lll1l111_opy_()
    if bstack11l1l11lll1_opy_:
        bstack1llll1ll11l_opy_ = os.path.join(bstack11l1l11lll1_opy_, bstack1llll1l_opy_ (u"ࠦࡨࡲࡩࠣᱭ"))
        if not os.path.exists(bstack1llll1ll11l_opy_):
            os.makedirs(bstack1llll1ll11l_opy_, mode=0o777, exist_ok=True)
        return bstack1llll1ll11l_opy_
    else:
        raise FileNotFoundError(bstack1llll1l_opy_ (u"ࠧࡔ࡯ࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡩࡳࡷࠦࡴࡩࡧࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿ࠮ࠣᱮ"))
def bstack1lll11lll11_opy_(bstack1llll1ll11l_opy_):
    bstack1llll1l_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡺࡨࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮ࡴࠠࡢࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠮ࠣࠤࠥᱯ")
    bstack11l11ll11l1_opy_ = [
        os.path.join(bstack1llll1ll11l_opy_, f)
        for f in os.listdir(bstack1llll1ll11l_opy_)
        if os.path.isfile(os.path.join(bstack1llll1ll11l_opy_, f)) and f.startswith(bstack1llll1l_opy_ (u"ࠢࡣ࡫ࡱࡥࡷࡿ࠭ࠣᱰ"))
    ]
    if len(bstack11l11ll11l1_opy_) > 0:
        return max(bstack11l11ll11l1_opy_, key=os.path.getmtime) # get bstack11l1ll1l111_opy_ binary
    return bstack1llll1l_opy_ (u"ࠣࠤᱱ")
def bstack11lll111111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll1ll11111_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll1ll11111_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d