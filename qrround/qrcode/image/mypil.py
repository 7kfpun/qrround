# Try to import PIL in either of the two ways it can be installed.
try:
    from PIL import Image, ImageDraw
except ImportError:
    import Image, ImageDraw

import qrcode.image.base
from StringIO import StringIO
import urllib


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

        # url = "https://secure.gravatar.com/avatar/988f8daaaf0155e5536fbb2d7efe0d0f?s=420&d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-user-420.png"
        # self._image = Image.open(StringIO(urllib.urlopen(url).read()))
        self._image = Image.open("wing.png")
        self._image = self._image.resize((self.box_size, self.box_size), Image.ANTIALIAS)

        self._image0 = Image.open("a.png")
        self._image1 = Image.open("b.png")
        self._image2 = Image.open("c.png")
        self._image3 = Image.open("d.png")
        self._image4 = Image.open("e.png")
        self._image5 = Image.open("f.png")
        # self._image = self._image.resize((self.box_size, self.box_size), Image.ANTIALIAS)
        self._image0 = self._image0.resize((self.box_size, self.box_size), Image.ANTIALIAS)
        self._image1 = self._image1.resize((self.box_size, self.box_size), Image.ANTIALIAS)
        self._image2 = self._image2.resize((self.box_size, self.box_size), Image.ANTIALIAS)
        self._image3 = self._image3.resize((self.box_size, self.box_size), Image.ANTIALIAS)
        self._image4 = self._image4.resize((self.box_size, self.box_size), Image.ANTIALIAS)
        self._image5 = self._image5.resize((self.box_size, self.box_size), Image.ANTIALIAS)

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

        from random import choice
        c = choice(range(6))
        if c == 0:
            self._img.paste(self._image0, (x, y))
        elif c == 1:
            self._img.paste(self._image1, (x, y))
        elif c == 2:
            self._img.paste(self._image2, (x, y))
        elif c == 3:
            self._img.paste(self._image3, (x, y))
        elif c == 4:
            self._img.paste(self._image4, (x, y))
        elif c == 5:
            self._img.paste(self._image5, (x, y))
            
    def show(self):
        self._img.show()

    def save(self, stream, kind=None):
        if kind is None:
            kind = self.kind
        self._img.save(stream, kind)
