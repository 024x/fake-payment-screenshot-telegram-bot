from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters, idle
import pyrogram
import pyromod
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import time
from datetime import datetime
from pytz import timezone
ist = timezone('Asia/Kolkata')


app = Client("my_bot", api_id=2171111, api_hash='fd7acd07303760c52dcc0ed8b2f73086',
             bot_token='1963945108:AAFyo')

apps = ['phonepe', 'paytm', 'bhim', 'gpay',
        'airtel', 'amazon', 'whatsapp', 'paymini']
modes = ['dark', 'light']

process = {}


@app.on_message(filters.command('start'))
async def start_command(client, message):
    if message.from_user.id in process.keys():
        await client.send_message(message.chat.id, f"Hello! {message.from_user.mention} , you have already a process continuing.. please head above message or /cancel")
    else:
        buttons = [InlineKeyboardButton(
            app.title(), callback_data=app) for app in apps]
        rows = [[button] for button in buttons]
        keyboard = InlineKeyboardMarkup(rows)
        k = await client.send_message(message.chat.id, f"Hello! {message.from_user.mention} , select bank below", reply_markup=keyboard)
        process[message.from_user.id] = k.id
        print(process)


@app.on_message(filters.command('cancel'))
async def cancel_command(client, message):
    if message.from_user.id in process.keys():
        await app.delete_messages(chat_id=message.chat.id, message_ids=[
            process[message.from_user.id], process[message.from_user.id] - 1])
        process.pop(message.from_user.id)
        await client.send_message(message.chat.id, f"Hello! {message.from_user.mention} , Canceled old process create new by /start")
    else:
        await client.send_message(message.chat.id, f"Hello! {message.from_user.mention} , No process running zzz. create new by /start")


def gen_img(data, bank):
    # Open the image file
    image = Image.open("phonepe_dark.jpg")

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Define the font and font size
    font = ImageFont.truetype("arial.ttf", 36)

    # Define the text and the position to draw it
    text = f"{data['time']} am on {data['date']} {data['month']} {data['year']}"
    position = (170, 60)
    draw.text(position, text, font=font)
    font = ImageFont.truetype("arial.ttf", 30)
    text = data['trid']
    position = (60, 585)
    draw.text(position, text, font=font)

    font = ImageFont.truetype("arial.ttf", 44)
    text = data['rname']
    position = (180, 280)
    draw.text(position, text, font=font)

    font = ImageFont.truetype("arial.ttf", 44)
    text = f"₹{data['amount']}"
    text_width = draw.textlength(text, font=font)
    x = image.width - text_width - 70
    y = 280
    position = (x, y)
    draw.text(position, text, font=font,)

    font = ImageFont.truetype("arial.ttf", 30)
    text = f"{data['utr']}"
    position = (260, 805)
    draw.text(position, text, font=font, fill=(181, 172, 193))
    image.save("new_image.png")

    font = ImageFont.truetype("arial.ttf", 30)
    text = f"₹{data['amount']}"
    text_width = draw.textlength(text, font=font)
    x = 260  # image.width - text_width - 70
    y = 805
    position = (x, y)
    draw.text(position, text, font=font,)

    return "new_image.png"

data = {}


async def update_message_text(id1,id2,text):
    output = ""
    for key, value in data[id1].items():
        output += f'**{key.title()}** : {value}\n'
    msg = await app.get_messages(id1, id2)
    msg = f'{output}\n\n{text}'
    await app.edit_message_text(id1, id2, msg)




@app.on_callback_query()
async def callback_query(client, query):
    # print(query)
    if query.from_user.id in process.keys() and query.message.id == process[query.from_user.id]:

        if query.data.startswith('phonepe'):
            if query.data == 'phonepe':
                if data.get(query.from_user.id) is None:
                    data[query.from_user.id] = {}
                data[query.from_user.id]['app'] = query.data
                dlbtns = InlineKeyboardMarkup([[InlineKeyboardButton(
                    "Dark", callback_data='phonepe_dark'), InlineKeyboardButton("Light", callback_data='phonepe_light')]])
                await app.edit_message_text(query.from_user.id, query.message.id, "Select Dark/Light Mode", reply_markup=dlbtns)
            elif query.data == 'phonepe_dark':
                data[query.from_user.id]['mode'] = 'dark'
                await update_message_text(query.from_user.id, query.message.id,"Now ** Send Transaction ID: \n(/skip to use default: `T496794685465468765241854548745`) **")
                
                trid = await query.message.chat.listen(filters=None, timeout=None, unallowed_click_alert=True)
                data[query.from_user.id]['trid'] = 'T496794685465468765241854548745' if trid.text == "/skip" else trid.text
                await update_message_text(query.from_user.id, query.message.id, f"Now enter utc (/skip for default `6584654163`):")
                await trid.delete()
                utr = await query.message.chat.listen(filters=None, timeout=None, unallowed_click_alert=True)
                data[query.from_user.id]['utr'] = '6584654163' if utr.text == "/skip" else str(
                    utr.text)
                await utr.delete()
                now = datetime.now(ist)
                time_str = now.strftime('%I:%M')
                await update_message_text(query.from_user.id, query.message.id, f"Now send time: (/skip for current ist {time_str})")
                _time = await query.message.chat.listen(filters=None, timeout=None, unallowed_click_alert=True)
                data[query.from_user.id]['time'] = time_str if _time.text == "/skip" else _time.text
                await _time.delete()

                await update_message_text(query.from_user.id, query.message.id, f"Now Send Reciver name:(i.e, paid to.)", )
                _time = await query.message.chat.listen(filters=None, timeout=None, unallowed_click_alert=True)
                data[query.from_user.id]['rname'] = 'Unknown Person' if _time.text == "/skip" else _time.text
                await _time.delete()

                await update_message_text(query.from_user.id, query.message.id, f"Now Send Amount:)", )
                _time = await query.message.chat.listen(filters=None, timeout=None, unallowed_click_alert=True)
                data[query.from_user.id]['amount'] = 'Unknown Person' if _time.text == "/skip" else _time.text
                await _time.delete()

                await update_message_text(query.from_user.id, query.message.id, f"Now Send Month:)", )
                _time = await query.message.chat.listen(filters=None, timeout=None, unallowed_click_alert=True)
                data[query.from_user.id]['month'] = 'Jan' if _time.text == "/skip" else _time.text[:3].title()
                await _time.delete()

                await update_message_text(query.from_user.id, query.message.id, f"Now Send Date:)", )
                _time = await query.message.chat.listen(filters=None, timeout=None, unallowed_click_alert=True)
                data[query.from_user.id]['date'] = '12' if _time.text == "/skip" else _time.text
                await _time.delete()

                await update_message_text(query.from_user.id, query.message.id, f"Now Send Year:)", )
                _time = await query.message.chat.listen(filters=None, timeout=None, unallowed_click_alert=True)
                data[query.from_user.id]['year'] = '2023' if _time.text == "/skip" else _time.text
                await _time.delete()

                await update_message_text(query.from_user.id, query.message.id, f"Now Select Bank", )
                bank_buttons = InlineKeyboardMarkup([[InlineKeyboardButton(
                    "SBI", callback_data='sbi'), InlineKeyboardButton("HDFC", callback_data='hdfc')]])
                await app.edit_message_reply_markup(query.from_user.id, query.message.id, reply_markup=bank_buttons)



        if query.data == 'sbi':
            data_ = gen_img(data[query.from_user.id], 'sbi')
            await app.send_photo(query.from_user.id, data_)
            await app.delete_messages(query.from_user.id, message_ids=[query.message.id])
            await query.answer("Done!", show_alert=True)
        if query.data == 'hdfc':
            print(data)

    else:
        await client.delete_messages(query.from_user.id, message_ids=[query.message.id])
        await client.send_message(query.from_user.id, f"Hello! {query.from_user.mention} , Please /start again!")
    

app.start()
print('started')
idle()
app.stop()
print('stopped')
