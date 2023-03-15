from PIL import Image, ImageDraw, ImageFont


def gen_img(data, bank):
    # Open the image file
    image = Image.open("phonepe_dark.jpg")

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Define the font and font size
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 36)

    # Define the text and the position to draw it
    text = f"{data['time']} {data['day']} on {data['date']} {data['month']} {data['year']}"
    position = (170, 60)
    draw.text(position, text, font=font)
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 30)
    text =data['trid']
    position = (60, 585)
    draw.text(position, text, font=font)

    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 44)
    text =data['rname']
    position = (180, 280)
    draw.text(position, text, font=font)

    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 44)
    text = f"₹{data['amount']}"
    text_width = draw.textlength(text, font=font)
    x = image.width - text_width - 70
    y = 280
    position = (x, y)
    draw.text(position, text, font=font,)

    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 30)
    text = f"{data['utr']}"
    position = (260, 805)
    draw.text(position, text, font=font, fill=(181, 172, 193))
    image.save("new_image.png")

    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 30)
    text = f"₹{data['amount']}"
    text_width = draw.textlength(text, font=font)
    x = 260#image.width - text_width - 70
    y = 805
    position = (x, y)
    draw.text(position, text, font=font,)

    return "new_image.png"


print(gen_img({'app': 'phonepe',
'day':'pm',
 'mode': 'dark', 
 'trid': 'T496794685465468765241854548745', 
 'utr': '658487687',
 'time': '10:01',
 'rname': 'Unknown Person',
 'amount': '564577856',
 'month': 'Jan',
 'date': '12',
 'year': '2023'},
 'sbi'))
