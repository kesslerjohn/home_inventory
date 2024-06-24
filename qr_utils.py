from qrcode import make
from uuid import uuid4
from PIL import ImageDraw, ImageFont

fontsize = 24
fontsize_px = fontsize*(72/96)
font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", fontsize)

def newItem():
    unique_id = str(uuid4())
    name = input("Item name?")
    quantity = input("Quantity?")
    cost = input("Cost?")
    weight = input("Weight?")

    query = """
    INSERT INTO items (uuid, name, quantity, cost_per_unit, weight, units)
    VALUES ("{}", "{}", {}, {}, {}, "each");
        """.format(unique_id, name, quantity, cost, weight)
    
    qr = make(unique_id)

    width = qr.size[0]

    lpos = max((width - len(name)*fontsize_px)*.5, 0)

    if len(name) > 27:
        name = name[:27]

    ImageDraw.Draw(qr).text((lpos, 340),name,"black", font = font)
    print(query)
    return (query, qr)

