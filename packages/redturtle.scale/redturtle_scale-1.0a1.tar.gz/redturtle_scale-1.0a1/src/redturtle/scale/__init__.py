# -*- coding: utf-8 -*-
"""Init and utils."""
from .patches import apply_backport_181
from PIL import features
from redturtle.scale.scale import apply_patches
from zope.i18nmessageid import MessageFactory

import logging


_ = MessageFactory("redturtle.scale")
logger = logging.getLogger(__name__)
WEBP_SUPPORT = features.check("webp")


if WEBP_SUPPORT:
    apply_backport_181()
    apply_patches()
else:
    logger.warning(
        "Pillow is missing WEBP support. Some image processing features may not work correctly."
    )
