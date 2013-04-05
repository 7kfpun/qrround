from qrround.settings.settings import PROJECT_ROOT
from qrround.models import (
    CachedImage,
)
from random import choice
# Try to import PIL in either of the two ways it can be installed.
try:
    from PIL import Image, ImageDraw
except ImportError:
    import Image
    import ImageDraw
import qrcode.image.base
import ImageOps
from time import time
import logging

START_TIME = 0
logger = logging.getLogger(__name__)


class PilImage(qrcode.image.base.BaseImage):
    """PIL image builder, default format is PNG."""

    def __init__(self, border, width, box_size, users=[], options={}):
        global START_TIME
        START_TIME = time()
        logger.info('START TIME: %.4f' % START_TIME)

        if Image is None and ImageDraw is None:
            raise NotImplementedError("PIL not available")
        super(PilImage, self).__init__(border, width, box_size)
        self.kind = "PNG"

        pixelsize = (self.width + self.border * 2) * self.box_size
        self._img = Image.new("RGBA", (pixelsize, pixelsize), "white")
        self._idr = ImageDraw.Draw(self._img)

        if users:
            # self._all_cached_images = CachedImage.objects.filter(user__client__in=users)  # noqa

            darkness = options.get('darkness', '0')
            if darkness != '0':
                self._all_cached_images = [
                    Image.open(cached_img.photo.path).resize((self.box_size, self.box_size), Image.ANTIALIAS).point(lambda p: p * (1 - int(darkness)/10.0))  # noqa
                    for cached_img in CachedImage.objects.filter(user__client__in=users)  # noqa
                ]
            else:
                self._all_cached_images = [
                    Image.open(cached_img.photo.path).resize((self.box_size, self.box_size), Image.ANTIALIAS)  # noqa
                    for cached_img in CachedImage.objects.filter(user__client__in=users)  # noqa
                ]

        else:
            self._all_cached_images = CachedImage.objects.all()

        self.options = options

        if not self._all_cached_images:
            profile_image = choice(['a.gif', 'b.gif', 'c.gif'])
            self._all_cached_images = [
                Image.open(PROJECT_ROOT + '/../qrcode/image/profile_picture/%s' % profile_image).resize(  # noqa
                    (self.box_size, self.box_size), Image.ANTIALIAS),
            ]

    def drawrect(self, row, col):
        x = (col + self.border) * self.box_size
        y = (row + self.border) * self.box_size
        box = [(x, y),
               (x + self.box_size - 1,
                y + self.box_size - 1)]
        self._idr.rectangle(box, fill=self.options.get('color', None) or "black")  # noqa

    def pasteimage(self, row, col):
        x = (col + self.border) * self.box_size
        y = (row + self.border) * self.box_size

        image = choice(self._all_cached_images)
        style = self.options.get('style', '0')

        if style == '0':
            # self._img.paste(Image.open(image.photo.path).resize((self.box_size, self.box_size), Image.ANTIALIAS), (x, y))  # noqa
            self._img.paste(image, (x, y))

        elif style == '1':
            # self._img.paste(Image.open(image.photo.path).resize((self.box_size, self.box_size), Image.ANTIALIAS), (x, y))  # noqa
            self._img.paste(image, (x, y))

            border = Image.open(PROJECT_ROOT + '/../qrcode/image/resources/border.png').resize((self.box_size, self.box_size), Image.ANTIALIAS).convert('RGBA')  # noqa
            self._img.paste(border, (x, y), mask=border)

        elif style == '2':
            try:
                bord = self.bord
            except:
                bord = self.bord = Image.open(PROJECT_ROOT + '/../qrcode/image/resources/border1.png').resize((self.box_size, self.box_size), Image.ANTIALIAS)  # noqa

            # self._img.paste(Image.open(image.photo.path).resize((self.box_size, self.box_size), Image.ANTIALIAS), (x, y))  # noqa
            self._img.paste(image, (x, y))

            self._img.paste(bord, (x, y), mask=bord)

        elif style == '3':
            try:
                highlight = self.highlight
                mask = self.mask
            except:
                highlight = self.highlight = Image.open(PROJECT_ROOT + '/../qrcode/image/resources/round.png').resize((self.box_size, self.box_size), Image.ANTIALIAS)  # noqa
                mask = self.mask = Image.open(PROJECT_ROOT + '/../qrcode/image/resources/round-mask.png').resize((self.box_size, self.box_size), Image.ANTIALIAS)  # noqa

            # icon = Image.open(image.photo.path).resize((self.box_size, self.box_size), Image.ANTIALIAS)  # noqa
            icon = image

            button = Image.new('RGBA', mask.size)

            # Resize Icon
            icon = ImageOps.fit(icon, highlight.size, method=Image.ANTIALIAS, centering=(0.5, 0.5))  # noqa

            # Create a helper image that will hold the icon after the reshape
            helper = button.copy()
            # Cut the icon by the shape of the mask
            helper.paste(icon, mask=mask)

            # Fill with a solid color by the mask's shape
            button.paste((255, 255, 255), mask=mask)
            # Get rid of the icon's alpha band
            icon = icon.convert('RGB')
            # Paste the icon on the solid background
            # Note we are using the reshaped icon as a mask
            button.paste(icon, mask=helper)

            # Get a copy of the highlight image without the alpha band
            overlay = highlight.copy().convert('RGB')
            button.paste(overlay, mask=highlight)
            button = button.resize(
                (self.box_size, self.box_size), Image.ANTIALIAS)

            self._img.paste(button, (x, y))

    def show(self):
        self._img.show()

    def save(self, stream, kind=None):
        if kind is None:
            kind = self.kind
        self._img.save(stream, kind)

        logger.info('END TIME: %.4f', (time() - START_TIME))
