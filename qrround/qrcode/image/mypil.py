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
#from StringIO import StringIO
#import urllib


class PilImage(qrcode.image.base.BaseImage):
    """PIL image builder, default format is PNG."""

    def __init__(self, border, width, box_size):
        if Image is None and ImageDraw is None:
            raise NotImplementedError("PIL not available")
        super(PilImage, self).__init__(border, width, box_size)
        self.kind = "PNG"

        pixelsize = (self.width + self.border * 2) * self.box_size
        self._img = Image.new("RGBA", (pixelsize, pixelsize), "white")
        # self._img = Image.new("1", (pixelsize, pixelsize), "white")
        self._idr = ImageDraw.Draw(self._img)

        # url = "https://secure.gravatar.com/avatar/988f8daaaf0155e5536fbb2d7efe0d0f?s=420&d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-user-420.png"  # noqa
        # self._image = Image.open(StringIO(urllib.urlopen(url).read()))

        self._all_cached_images = CachedImage.objects.all()
        if not self._all_cached_images:
            self._all_cached_images = [
                Image.open("qrround/media/a.png").resize(
                    (self.box_size, self.box_size), Image.ANTIALIAS),
                Image.open("qrround/media/b.png").resize(
                    (self.box_size, self.box_size), Image.ANTIALIAS),
                Image.open("qrround/media/c.png").resize(
                    (self.box_size, self.box_size), Image.ANTIALIAS),
                Image.open("qrround/media/d.png").resize(
                    (self.box_size, self.box_size), Image.ANTIALIAS),
                Image.open("qrround/media/e.png").resize(
                    (self.box_size, self.box_size), Image.ANTIALIAS),
                Image.open("qrround/media/f.png").resize(
                    (self.box_size, self.box_size), Image.ANTIALIAS),
            ]

    def drawrect(self, row, col):
        x = (col + self.border) * self.box_size
        y = (row + self.border) * self.box_size
        box = [(x, y),
               (x + self.box_size - 1,
                y + self.box_size - 1)]
        self._idr.rectangle(box, fill="black")

    def pasteimage(self, row, col):
        x = (col + self.border) * self.box_size
        y = (row + self.border) * self.box_size

        image = choice(self._all_cached_images)
        self._img.paste(Image.open(image.photo.path).resize(
            (self.box_size, self.box_size), Image.ANTIALIAS), (x, y))

    def show(self):
        self._img.show()

    def save(self, stream, kind=None):
        if kind is None:
            kind = self.kind
        self._img.save(stream, kind)
