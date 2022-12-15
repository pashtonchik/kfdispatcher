from pyrogram import Client, filters
import asyncio
import time
import requests
from pyrogram_patch.fsm import StatesGroup, StateItem, StateFilter, State
from pyrogram_patch import patch
from pyrogram_patch.fsm.storages import MemoryStorage
import sys
import os
import uvloop
import json


name_bot = 'KFOperatingBot'
URL_DJANGO = 'http://194.58.92.160:8001/api/'
URL_FILE = 'http://194.58.92.160:8001'
cheque_root = '/root/dev/SkillPay-Django'
skill_pay_bot = 'KFStatusBot'

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

uvloop.install()

if __name__ == '__main__':
    api_id  = int(sys.argv[1])
    api_hash = sys.argv[2] 
    app = Client(f'session/{api_id}', api_id, api_hash)
    patch_manager = patch(app)
    patch_manager.set_storage(MemoryStorage())

@app.on_message(filters=filters.user(skill_pay_bot))
async def change_status(client, message):
    # await client.send_message(name_bot, '/start')
    await asyncio.sleep(1)



    await client.send_message(
        chat_id='KFOperatingBot',
        text='🏆 Статусы',
    )


    

@app.on_message(filters=filters.user(name_bot) & filters.regex('Общи\w+'))
async def general_status_menu(client, message):
    try:
        await client.request_callback_answer(
            chat_id='KFOperatingBot',
            message_id=message.id,
            callback_data='p2p_private_status_edit',
        )
    except TimeoutError:
        await asyncio.sleep(1)

async def check_message(msg_id, client, id):
    while 1:
        status = ''
        msg = await app.get_messages(chat_id=name_bot, message_ids=msg_id)
        try:
            req_status = requests.get(URL_DJANGO + f'kf/trade/detail/{id}/')
            kftrade = req_status.json()
            if kftrade['kftrade']['status'] in ['closed', 'time_cancel', 'confirm_payment'] or kftrade['kftrade']['cheque']:
                break
            if ('ОПЛАЧЕН' in msg.text or 'Отменен' in msg.text):
                if 'ОПЛАЧЕН' in msg.text:
                    status = 'confirm_payment'
                elif 'Отменен' in msg.text:
                    status = 'closed'
                if status:
                    try:
                        trade_info = {
                            'id': id,
                            'status': status,
                        }

                        a = requests.post(URL_DJANGO + 'update/kf/trade/', json=trade_info)
                        if (a.status_code == 200):
                            break

                    except Exception:
                        print(Exception)
                        continue
        except Exception:
            print(Exception)
            continue
        
        await asyncio.sleep(5)

@app.on_message(filters=filters.user(name_bot) & filters.regex('Смена статус\w+'))
async def change_status(client, message):
    await asyncio.sleep(2)
    my_id = await app.get_me()
    status = {}
    try:
        data = requests.get(URL_DJANGO + 'get/user_bots/').json()
        for i in data:
            if (i['tg_id'] == str(my_id.id)):
                status = i['status'] 
    except:
        pass
    
    msg = status
    if message.reply_markup.inline_keyboard[2][0].callback_data == 'p2p_private_status_edittool_SBERBANK_enable' and msg.get('sberbank_status') == True:
        try:
            await client.request_callback_answer(
                chat_id=name_bot,
                message_id=message.id,
                callback_data=message.reply_markup.inline_keyboard[2][0].callback_data,
            )
        except TimeoutError:
            await asyncio.sleep(1)
    elif message.reply_markup.inline_keyboard[2][0].callback_data == 'p2p_private_status_edittool_SBERBANK_disable' and msg.get('sberbank_status') == False:
        try:
            await client.request_callback_answer(
                chat_id=name_bot,
                message_id=message.id,
                callback_data=message.reply_markup.inline_keyboard[2][0].callback_data,
            )
        except TimeoutError:
            await asyncio.sleep(1)
    elif message.reply_markup.inline_keyboard[3][0].callback_data == 'p2p_private_status_edittool_TINKOFF_enable' and msg.get('tinkoff_status') == True:
        try:
            await client.request_callback_answer(
                chat_id=name_bot,
                message_id=message.id,
                callback_data=message.reply_markup.inline_keyboard[3][0].callback_data,
            )
        except TimeoutError:
                await asyncio.sleep(1)
    elif message.reply_markup.inline_keyboard[3][0].callback_data == 'p2p_private_status_edittool_TINKOFF_disable' and msg.get('tinkoff_status') == False:
        try:
            await client.request_callback_answer(
                chat_id=name_bot,
                message_id=message.id,
                callback_data=message.reply_markup.inline_keyboard[3][0].callback_data,
            )
        except TimeoutError:
                await asyncio.sleep(1)

    elif message.reply_markup.inline_keyboard[0][0].callback_data == 'p2p_private_status_editbase_enable' and msg.get('main_status') == True:
        try:
            await client.request_callback_answer(
                chat_id=name_bot,
                message_id=message.id,
                callback_data=message.reply_markup.inline_keyboard[0][0].callback_data,
            )
        except TimeoutError:
                await asyncio.sleep(1)

    elif message.reply_markup.inline_keyboard[0][0].callback_data == 'p2p_private_status_editbase_disable' and msg.get('main_status') == False:
        try:
            await client.request_callback_answer(
                chat_id=name_bot,
                message_id=message.id,
                callback_data=message.reply_markup.inline_keyboard[0][0].callback_data,
            )
        except TimeoutError:
                await asyncio.sleep(1)
    else:
        try:
            await client.request_callback_answer(
                chat_id=name_bot,
                message_id=message.id,
                callback_data=message.reply_markup.inline_keyboard[4][0].callback_data,
            )
        except TimeoutError:
                await asyncio.sleep(1)

@app.on_message(filters=filters.user(name_bot) & filters.regex('Источн\w+') & StateFilter('*'))
async def get_trade(client, message, state: State):
    await state.set_state(Actions.newTrade)
    asyncio.get_event_loop()
    trade = message.text
    trade_split = trade.split('\n')
    id = trade_split[1].split()[1]
    account = await app.get_users('me')
    id = account.first_name + '-' + id
    await state.set_data({'id': id})

    trade_info = {
        'tg_account' : account.first_name,
        'id': id,
        'card_number': trade_split[2].split()[1],
        'source': trade_split[0].split()[1],
        'paymethod': 443 if trade_split[4].split()[1] == 'TINKOFF' else 3547,
        'fio': trade_split[6].split()[1],
        'amount': int(trade_split[5].split()[1]),
        'comment': trade_split[7],
        'type': trade_split[4].split()[1][0:4],
        'status': 'trade_created',
    }

    a = requests.post(URL_DJANGO + 'create/kf/trade/', json=trade_info)
    try:
        await message.click(0, 0, timeout=0)
    except TimeoutError:
        pass
        # print('тык принять')

    trade_info = {
        'id': id,
        'status': 'in_progress',
    }

    a = requests.post(URL_DJANGO + 'update/kf/trade/', json=trade_info)
    print(f'Сделка {id} успешно добавлена в БД')
    if a.status_code == 200:
        print(a.status_code, 'card is')
        # await state.set_state(Actions.cardNumber)
        asyncio.create_task(check_message(message.id, client, id))

        await asyncio.sleep(5)

        msg = await app.get_messages(chat_id=name_bot, message_ids=message.id + 2)


        card_number = msg.text
        # state_data = await state.get_data()
        kftrade_id = id

        trade_info = {
            'id': kftrade_id,
            'card_number': card_number,
            'status': 'trade_created',
        }

        a = requests.post(URL_DJANGO + 'update/kf/trade/', json=trade_info)
        if a.status_code == 200:
            await state.set_state(Actions.editCheck)
            print(f"Карта добавлена в базу")
        else:
            data = {
            "chat_id" : "-1001839190420",
            "text" : f"[ERROR] Сделка {id} номер карты не добавлен в базу из-за проблем на сервере"
            }
            error = requests.post("https://api.telegram.org/bot5156043800:AAF32TSVlvj0ILUvPu58A2nlIGMVilHCQJ4/sendMessage")
  
        kftrade_cheque_file = await send_check(kftrade_id=kftrade_id)
        if kftrade_cheque_file not in ['closed', 'time_cancel', 'confirm_payment'] :
            r = requests.get(URL_FILE + kftrade_cheque_file)

            with open(f'checks/{kftrade_id}.pdf', 'wb') as f:
                f.write(r.content)
            await client.send_document(name_bot,  f'checks/{kftrade_id}.pdf')
            try:
                os.remove(f'checks/{kftrade_id}.pdf')
            except: 
                pass
            await state.set_state(Actions.acceptCheck)
            print('чек типо отправляем')
        elif kftrade_cheque_file == 'time_cancel':
            try:
                try:
                    msg = await app.get_messages(chat_id=name_bot, message_ids=message.id + 5)
                    await client.request_callback_answer(
                        chat_id=name_bot,
                        message_id=message.id + 5,
                        callback_data=msg.reply_markup.inline_keyboard[0][0].callback_data,
                    )
                except TimeoutError:
                    await asyncio.sleep(1)
            except TimeoutError:
                print('тык отмена')
            await asyncio.sleep(5)
            try:
                state_data = await state.get_data()
                id = state_data['id']
                req_status = requests.get(URL_DJANGO + f'kf/trade/detail/{id}/')
                comment = req_status.json()['kftrade']['cancel_comment']
                if (not comment):
                    await asyncio.sleep(3)
                    await client.send_message(name_bot, 'Прошу повторить через 5 минут')
                    await state.finish()
                else:
                    await asyncio.sleep(3)
                    await client.send_message(name_bot, comment)
                    await state.finish()
                trade_info = {
                    'id': id,
                    'status': 'closed',
                }
                a = requests.post(URL_DJANGO + 'update/kf/trade/', json=trade_info)
                if a.status_code == 200:
                    print(f'Сделка {id} успешно закрыта.')
                else:
                    data = {
                        "chat_id" : "-1001839190420",
                        "text" : f"[ERROR] Сделка {id} не закрылась из-за проблем на сервере"
                    }
                    error = requests.post("https://api.telegram.org/bot5156043800:AAF32TSVlvj0ILUvPu58A2nlIGMVilHCQJ4/sendMessage")
            except Exception as e:
                print(e)
                data = {
                        "chat_id" : "-1001839190420",
                        "text" : f"[ERROR] Сделка {id} не закрылась из-за какой-то ошибки"
                    }
                error = requests.post("https://api.telegram.org/bot5156043800:AAF32TSVlvj0ILUvPu58A2nlIGMVilHCQJ4/sendMessage")
            finally:
                await state.finish()
        else:
            await state.finish()
    else:
        data = {
            "chat_id" : "-1001839190420",
            "text" : f"[ERROR] Сделка {id} не добавлена в базу из-за проблем на сервере"
        }
        error = requests.post("https://api.telegram.org/bot5156043800:AAF32TSVlvj0ILUvPu58A2nlIGMVilHCQJ4/sendMessage")



# @app.on_message(filters=filters.user(name_bot) & StateFilter(Actions.cancelTrade))
# async def send_cancel_message(client, message, state: State):
# @app.on_message(filters=filters.user(name_bot) & StateFilter(Actions.cardNumber) & filters.regex('\w+\d{8}\w+'))
# async def get_card_number(client, message, state: State):



async def send_check(kftrade_id):
    start_time = time.time()
    while 1:
        await asyncio.sleep(5)
        req_status = requests.get(URL_DJANGO + f'kf/trade/detail/{kftrade_id}/')
        if req_status.status_code == 200:
            kftrade = req_status.json()
            if kftrade['kftrade']['cheque']:
                return kftrade['kftrade']['cheque']
            elif kftrade['kftrade']['status'] == 'time_cancel':
                return 'time_cancel'
            elif kftrade['kftrade']['status'] == 'closed':
                return 'closed'
            elif kftrade['kftrade']['status'] == 'confirm_payment':
                return 'confirm_payment'
            else:
                continue



@app.on_message(filters=filters.user(name_bot) & StateFilter(Actions.acceptCheck) & filters.regex('Это докумен\w+'))
async def accept_cheque(client, message, state: State):
    try:
        await message.click(0, 0, timeout=0)
    except TimeoutError:
        print('тык да')
    state_data = await state.get_data()
    kftrade_id = state_data['id']

    trade_info = {
        'id': kftrade_id,
        'status': 'confirm_payment',
    }

    a = requests.post(URL_DJANGO + 'update/kf/trade/', json=trade_info)
    if a.status_code == 200:
        await state.finish()


app.run()
