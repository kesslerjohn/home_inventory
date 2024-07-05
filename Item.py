from uuid import uuid4
from qrcode import make
from datetime import datetime, timezone, timedelta
from PIL import ImageDraw, ImageFont

class Item(object):
    def __init__(self, uuid : str = "", name = "", quantity = 0, cost = 0, weight = 0, units = "each", datasheet = "", date_str = ""):
        super().__init__()
        if uuid == "":
            self.uuid = str(uuid4())
        else:
            self.uuid = uuid
        self.name = name
        self.quantity = quantity
        self.cost = cost
        self.weight = weight
        self.units = units
        self.datasheet = datasheet
        self._tzinfo = timezone(offset = -timedelta(hours = 5))
        self._datetime_format = "%Y-%m-%d %H:%M:%S"
        if date_str == "":
            self.date_added = datetime.now(tz=self._tzinfo)
        else:
            self.date_added = datetime.strptime(date_str, self._datetime_format)
        self._fontsize = 24
        self._fontsize_px = self._fontsize*(72/96)
        self._font = ImageFont.truetype(__file__ + "/resources/Helvetica.ttc", self._fontsize)

    def printCost(self) -> str:
        return f"${self.cost/100:,.2f}/{self.units}"
    
    def printName(self) -> str:
        return self.name.capitalize()
    
    def printQuantity(self) -> str:
        return f"{self.quantity} {self.units}"
    
    def printDateAdded(self) -> str:
        return self.date_added.strftime(self._datetime_format)
    
    def makeQrCode(self, path):
        qr = make(self.uuid)
        width = qr.size[0]
        lpos = max((width - len(self.name)*self._fontsize_px)*.5, 0)
        qr_name = self.name
        if len(self.name) > 27:
            qr_name = self.name[:27]

        ImageDraw.Draw(qr).text((lpos, 340), qr_name, "black", font = self._font)
        qr.save(path + f"/{self.uuid}.png")
        return qr