import telegram
import telegram.ext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler , CallbackContext,InlineQueryHandler
import requests
import random
import _thread
import time
from pyCoinPayments import CryptoPayments
import uuid


TOKEN = "7135284003:AAEQqP_TGB8auDEKocPNvDYGtyLE10Swaw4"
bot = telegram.Bot(token=TOKEN)

API_KEY = '616e319dad674f8906f129a735d299d6665388a0fe3f4e075ffc3e2b9c3ce8f3'
API_SECRET = 'D544Edec2fa5725C5913C5806665393ec58769563f5C7477DfBb8A8C4302867b'
IPN_URL = '1122334455667788aA@'

client = CryptoPayments(API_KEY, API_SECRET, IPN_URL)


def sm (update,Text,IsQuery=False,reply_markup=None):
    if IsQuery :
        update.edit_message_text(text=Text,reply_markup= reply_markup)
    else :
        return update.message.reply_text(text=Text,reply_markup=reply_markup)
    
def sa (query,text):
    query.answer(text=text,show_alert=True)
    
    

def Message (update : telegram.Update , context : telegram.ext.CallbackContext):
    message = ""
    chatID =""
    userName=""
    messageID =""
    gUser=""
    try:
        chatID = update._effective_user.id
        userName = update._effective_message.from_user.name
        messageID = update._effective_message.message_id
        message = update.message.text
    except:
        pass
    print(f"Received a message from {userName}: {message}")
    
    if message == "/start":
        text=f"""
سلام به ربات ما خوش آمدید

لطفا یکی از گزینه های زیر را انتخاب کنید :
        """
        sm(update,text,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='خرید 🛒',callback_data='Buy')],
                                                          [InlineKeyboardButton('پیگیری خرید ',callback_data='Check')]]))
        
    elif len(message)==26:
        with open('Database.txt','r') as f :
            data = f.read().split('\n')
        if message in data :
            sm(update,'شما قبلا از این کد استفاده کردید و امکان استفاده مجدد وجود نداره')
            return
        
        
        
        msg = sm(update,'ربات در حال پردازش هست لطفا صبور باشید...')
        
        ret = client.getTransactionInfo(params={'txid':message})
        msg.delete()
        if ret['status'] == 100 :
            sm(update,'پرداخت شما با موفقیت انجام شده')

            unique_id = uuid.uuid4().hex
            sm(update,"UUID HEX: "+unique_id)
            with open('Database.txt','a+') as f:
                f.write(message+'\n')
        else :
            sm(update,f"پرداخت شما انجام نشده . دلیل : {ret['status_text']}")
    
def Command (update : telegram.Update , context : telegram.ext.CallbackContext):
    query = update.callback_query
    data = str(query.data)
    message = ""
    chatID =""
    userName=""
    messageID =""
    try:
        chatID = update._effective_user.id
        userName = update._effective_message.from_user.name
        messageID = update._effective_message.message_id
        message = update.message.text
    except:
        pass
    
    if data == 'Buy':
        sm(query,"لطفا برای خرید روی دکمه درگاه پرداخت کلیک کنید \nو سپس رو دکمه زیر کلیک کنید و کد رهگیری خود را ارسال کنید",True,InlineKeyboardMarkup([[InlineKeyboardButton(text="درگاه پرداخت",url="https://www.coinpayments.net/index.php?cmd=_pay&reset=1&merchant=c80ec2928c4b6836e6ada19db1c229ec&item_name=iphone15&currency=USD&amountf=25.00000000&quantity=1&allow_quantity=0&want_shipping=0&allow_extra=1&")]
                                                                                                                                                ,[InlineKeyboardButton(text='پیگیری خرید',callback_data='Check')]]))
    
    elif data == 'Check' :
        sm(query,"لطفا کد پیگیری خود را ارسال کنید :" ,True)
    

def main():


    updater = telegram.ext.Updater(bot.token, use_context=True)

    #updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
    updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.all,Message))

    updater.dispatcher.add_handler(CallbackQueryHandler(Command))
    
    print("Robot First Started")
    
    updater.start_polling()
    print("Robot Main Started")
    updater.idle()
if __name__ == '__main__':
    main()