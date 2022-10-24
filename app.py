from pyrogram import Client, filters

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


@app.on_message(filters=filters.user('KFOperatingBot') & filters.regex('KFOperatingBot'))
async def my(client, message):
    # print(message.reply_markup.keyboard)
    await client.send_message(
        chat_id='@KFOperatingBot',
        text=message.reply_markup.keyboard[0][1],
    )


app.run()
