from pyrogram import Client, filters
import asyncio

api_id = 24124872
api_hash = 'd368ec365944a3198966e6ae46203edc'

app = Client('asdas', api_id, api_hash)

# app.send_message(chat_id='me', text='test')
# print(1)


@app.on_message(filters=filters.user('me'))
async def my(client, message):
    if message.text == 'start':
        await client.send_message(
            chat_id='KFOperatingBot',
            text='/start'
        )
    elif message.text == 'stop':
        print('тормозим')


@app.on_message(filters=filters.user('KFOperatingBot') & filters.regex('Привет\w+'))
async def click_statuses(client, message):
    # print(message.reply_markup.keyboard)
    await client.send_message(
        chat_id='KFOperatingBot',
        text=message.reply_markup.keyboard[0][1],
    )
    await asyncio.sleep(1)


@app.on_message(filters=filters.user('KFOperatingBot') & filters.regex(' Общий статус: \w+'))
async def click_change(client, message):
    print(message.text)
    try:
        await client.request_callback_answer(
            chat_id='KFOperatingBot',
            message_id=message.id,
            callback_data=message.reply_markup.inline_keyboard[0][0].callback_data,
        )
    except TimeoutError:
        await asyncio.sleep(1)


@app.on_message(filters=filters.user('KFOperatingBot') & filters.regex(' Общий статус: \w+'))
async def click_change(client, message):
    print(message.text)
    try:
        await client.request_callback_answer(
            chat_id='KFOperatingBot',
            message_id=message.id,
            callback_data=message.reply_markup.inline_keyboard[0][0].callback_data,
        )
    except TimeoutError:
        await asyncio.sleep(1)


@app.on_message(filters=filters.user('KFOperatingBot') & filters.regex('Смена статус\w+'))
async def click_tinkoff(client, message):
    print(message.reply_markup.inline_keyboard)
    if message.reply_markup.inline_keyboard[2][0].callback_data == 'p2p_private_status_edittool_SBERBANK_enable':
        try:
            await client.request_callback_answer(
                chat_id='KFOperatingBot',
                message_id=message.id,
                callback_data=message.reply_markup.inline_keyboard[2][0].callback_data,
            )
        except TimeoutError:
            await asyncio.sleep(1)
    elif message.reply_markup.inline_keyboard[3][0].callback_data == 'p2p_private_status_edittool_TINKOFF_enable':
        try:
            await client.request_callback_answer(
                chat_id='KFOperatingBot',
                message_id=message.id,
                callback_data=message.reply_markup.inline_keyboard[3][0].callback_data,
            )
        except TimeoutError:
            await asyncio.sleep(1)


@app.on_message(filters=filters.user('KFOperatingBot') & filters.regex('Источник\w+'))
async def click_tinkoff(client, message):
    print(message.reply_markup.inline_keyboard)
    id_message_order = message.id




app.run()
