from pyrogram import Client, filters
import asyncio
import time
import requests
from pyrogram_patch.fsm import StatesGroup, StateItem, StateFilter, State
from pyrogram_patch import patch
from pyrogram_patch.fsm.storages import MemoryStorage

name_bot = 'KFOperatingBot'
URL_DJANGO = 'http://194.58.92.160:8001/api/'
cheque_root = '/root/dev/SkillPay-Django'


class Actions(StatesGroup):
    newTrade = StateItem()
    acceptTrade = StateItem()
    paymentSystem = StateItem()
    cardNumber = StateItem()
    funds = StateItem()
    fio = StateItem()
    acceptCheck = StateItem()
    editCheck = StateItem()
    cancelTrade = StateItem()
    waitNewTrade = StateItem()


api_id = 24124872
api_hash = 'd368ec365944a3198966e6ae46203edc'

app = Client('asdas', api_id, api_hash)
patch_manager = patch(app)
patch_manager.set_storage(MemoryStorage())


# @app.on_message(filters=filters.user('me'))
# async def my(client, message, state: State):
#     print(message.text)
#     if message.text == 'start':
#         await client.send_message(
#             chat_id=name_bot,
#             text='/start'
#         )
#     elif message.text == 'stop':
#         print('тормозим')


@app.on_message(filters=filters.user(name_bot) & filters.regex('Смена статус\w+'))
async def click_tinkoff(client, message):
    if message.reply_markup.inline_keyboard[2][0].callback_data == 'p2p_private_status_edittool_SBERBANK_enable':
        try:
            await client.request_callback_answer(
                chat_id=name_bot,
                message_id=message.id,
                callback_data=message.reply_markup.inline_keyboard[2][0].callback_data,
            )
        except TimeoutError:
            await asyncio.sleep(1)
    elif message.reply_markup.inline_keyboard[3][0].callback_data == 'p2p_private_status_edittool_TINKOFF_enable':
        try:
            await client.request_callback_answer(
                chat_id=name_bot,
                message_id=message.id,
                callback_data=message.reply_markup.inline_keyboard[3][0].callback_data,
            )
        except TimeoutError:
            await asyncio.sleep(1)


# async def checking_trades(kftrade_id):
#     start_time = time.time()
#     while 1:
#         await asyncio.sleep(0)
#         req_status = requests.get(URL_DJANGO + f'kf/trade/detail/{kftrade_id}/')
#         kftrade = req_status.json()
#         if kftrade['kftrade']['agent']:
#             return True
#         elif time.time() - start_time < 60:
#             continue
#         else:
#             return False


@app.on_message(filters=filters.user(name_bot) & filters.regex('Источн\w+') & StateFilter('*'))
async def get_trade(client, message, state: State):
    print('нам что то пришло')
    await state.set_state(Actions.newTrade)
    trade = message.text
    print(trade)
    trade_split = trade.split('\n')
    print(trade_split)
    id = trade_split[1].split()[1]
    await state.set_data({'id': id})

    trade_info = {
        'id': id,
        'card_number': trade_split[2].split()[1],
        'source': trade_split[0].split()[1],
        'paymethod': 443 if trade_split[4].split()[1] == 'TINKOFF' else 3547,
        'fio': trade_split[6].split()[1],
        'amount': int(trade_split[5].split()[1]),
        'comment': trade_split[7],
        'type': trade_split[4].split()[1],
        'status': 'trade_created',
    }

    a = requests.post(URL_DJANGO + 'create/kf/trade/', json=trade_info)
    print(a.status_code)
    # if await checking_trades(id):
    print(message.reply_markup.inline_keyboard)
    try:
        await message.click(0, 0, timeout=0)
    except TimeoutError:
        print('ошибка как всегда')

    trade_info = {
        'id': id,
        'status': 'in_progress',
    }

    a = requests.post(URL_DJANGO + 'update/kf/trade/', json=trade_info)
    if a.status_code == 200:
        print(a.status_code, 'card is')
        await state.set_state(Actions.cardNumber)
    # else:
    #
    #     trade_info = {
    #         'id': id,
    #         'status': 'closed',
    #     }
    #     a = requests.post(URL_DJANGO + 'update/kf/trade/', json=trade_info)
    #     if a.status_code == 200:
    #         try:
    #             await message.click(1, 0, timeout=0)
    #         except TimeoutError:
    #             print('ошибка как всегда')
    #         await state.set_state(Actions.cancelTrade)


@app.on_message(filters=filters.user(name_bot) & StateFilter(Actions.cancelTrade))
async def send_cancel_message(client, message, state: State):
    await client.send_message(name_bot, 'Прошу повторить через 5 минут')
    await state.finish()


# @app.on_message(filters=filters.user(name_bot) & StateFilter(Actions.paymentSystem))
# async def get_paymethod(client, message, state: State):
#     print(message.text)
#     await state.set_state(Actions.cardNumber)


@app.on_message(filters=filters.user(name_bot) & StateFilter(Actions.cardNumber) & filters.regex('\w+\d{8}\w+'))
async def get_card_number(client, message, state: State):
    card_number = message.text
    print(message.text)
    print(await state.get_data())
    state_data = await state.get_data()
    kftrade_id = state_data['id']

    trade_info = {
        'id': kftrade_id,
        'card_number': card_number,
        'status': 'trade_created',
    }

    a = requests.post(URL_DJANGO + 'update/kf/trade/', json=trade_info)
    if a.status_code == 200:
        await state.set_state(Actions.editCheck)


# @app.on_message(filters=filters.user(name_bot) & StateFilter(Actions.funds))
# async def get_funds(client, message, state: State):
#     print('funds', message.text)
#
#     await state.set_state(Actions.fio)


async def send_check(kftrade_id):
    start_time = time.time()
    while 1:
        await asyncio.sleep(0)
        req_status = requests.get(URL_DJANGO + f'kf/trade/detail/{kftrade_id}/')
        if req_status.status_code == 200:
            print(req_status.status_code, req_status.json())
            kftrade = req_status.json()
            if kftrade['kftrade']['cheque']:
                return kftrade['kftrade']['cheque']
            elif time.time() - start_time < 60:
                continue
            else:
                return False


# @app.on_message(filters=filters.user(name_bot) & StateFilter(Actions.fio))
# async def get_fio(client, message, state: State):
#     print('fio', message.text)
#     await state.set_state(Actions.editCheck)


@app.on_message(filters=filters.user(name_bot) & StateFilter(Actions.editCheck) & filters.regex('\w+дание подтверж\w+'))
async def send_cheque(client, message, state: State):
    print('editcheck', message.text)
    state_data = await state.get_data()
    kftrade_id = state_data['id']
    kftrade_cheque_file = await send_check(kftrade_id=kftrade_id)
    if kftrade_cheque_file:
        await client.send_document(name_bot, cheque_root + kftrade_cheque_file)
        await state.set_state(Actions.acceptCheck)
    else:
        trade_info = {
            'id': kftrade_id,
            'status': 'closed',
        }
        a = requests.post(URL_DJANGO + 'update/kf/trade/', json=trade_info)
        if a.status_code == 200:
            try:
                await message.click(0, timeout=0)
            except TimeoutError:
                print('ошибка как всегда')
            await state.set_state(Actions.cancelTrade)


@app.on_message(filters=filters.user(name_bot) & StateFilter(Actions.acceptCheck) & filters.regex('Это докумен\w+'))
async def accept_cheque(client, message, state: State):
    print('accept', message.text)
    try:
        await message.click(0, 0, timeout=0)
    except TimeoutError:
        print('ошибка как всегда')
    state_data = await state.get_data()
    kftrade_id = state_data['id']

    trade_info = {
        'id': kftrade_id,
        'status': 'confirm',
    }

    a = requests.post(URL_DJANGO + 'update/kf/trade/', json=trade_info)
    if a.status_code == 200:
        await state.finish()


app.run()
