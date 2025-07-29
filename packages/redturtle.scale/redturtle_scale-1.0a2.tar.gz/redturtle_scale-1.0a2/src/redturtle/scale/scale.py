from plone.namedfile.scaling import DefaultImageScalingFactory
from plone.scale import scale
from plone.scale.scale import scalePILImage

import logging


logger = logging.getLogger(__name__)


def scaleSingleFrame(
    image,
    width,
    height,
    mode,
    format_,
    quality,
    direction,
):
    image = scalePILImage(image, width, height, mode, direction=direction)
    # convert to simpler mode if possible
    colors = image.getcolors(maxcolors=256)
    if image.mode not in ("P", "L", "LA") and colors:
        if format_ == "JPEG":
            # check if it's all grey
            if all(rgb[0] == rgb[1] == rgb[2] for c, rgb in colors):
                image = image.convert("L")
        elif format_ in ("PNG", "GIF"):
            image = image.convert("P")
    if image.mode == "RGBA" and format_ == "JPEG":
        extrema = dict(zip(image.getbands(), image.getextrema()))
        if extrema.get("A") == (255, 255):
            # no alpha used, just change the mode, which causes the alpha band
            # to be dropped on save
            image = image.convert("RGB")
        else:
            # switch to PNG, which supports alpha
            format_ = "PNG"
    # XXX: force to WEBP format
    if format_ in ["JPEG", "PNG"]:
        format_ = "WEBP"
    # --- DEBUG
    # sizes = {}
    # for t in set([format_, "WEBP", "JPEG", "PNG"]):
    #     try:
    #         out = io.BytesIO()
    #         image.save(
    #             out,
    #             format=t,
    #             quality=88,
    #             optimize=True,
    #             progressive=True,
    #         )
    #         sizes[t] = out.tell()
    #     except OSError:
    #         sizes[t] = "---"
    # print(sizes)
    # --- DEBUG
    return image, format_


def create_scale(self, data, mode, height, width, **parameters):
    if "convert_to_webp" in parameters:
        del parameters["convert_to_webp"]
    if "_format" in parameters:
        del parameters["_format"]
    return self._old_create_scale(data, mode, height, width, **parameters)


def apply_patches():
    logger.info("monkeypatch plone.scale.scale.scaleSingleFrame")
    scale._old_scaleSingleFrame = scale.scaleSingleFrame
    scale.scaleSingleFrame = scaleSingleFrame
    DefaultImageScalingFactory._old_create_scale = (
        DefaultImageScalingFactory.create_scale
    )
    DefaultImageScalingFactory.create_scale = create_scale


def unapply_patches():
    logger.info("unmonkeypatch plone.scale.scale.scaleSingleFrame")
    if hasattr(scale, "_old_scaleSingleFrame"):
        scale.scaleSingleFrame = scale._old_scaleSingleFrame
        del scale._old_scaleSingleFrame
    if hasattr(DefaultImageScalingFactory, "_old_create_scale"):
        DefaultImageScalingFactory.create_scale = (
            DefaultImageScalingFactory._old_create_scale
        )
        del DefaultImageScalingFactory._old_create_scale


# DEBUG
# from plone.namedfile import file
# from time import time
# def wrap(fun):
#     def inner(*args, **kwargs):
#         t = time()
#         ret = fun(*args, **kwargs)
#         logger.info("[%sms] %s %s => %s", int(((time() - t) * 1000)), args, kwargs, ret)
#         return ret
#     return inner
# file.getImageInfo = wrap(file.getImageInfo)
