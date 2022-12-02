import telebot
from telebot import types
from bin.sikadu import Sikadu
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os


API_TOKEN = '5817972119:AAFixN2CRXFsaXw25NVz41FERmLUaSNSPY4'
bot = telebot.TeleBot(API_TOKEN)



#icon
check = '\u2705'
cross = '\u274C'
user_dict = {}
class Mahasiswa:
  def __int__(self, nim):
    self.nim = nim

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, 'typing')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('account', 'mahasiswa')
    msg = bot.send_message(message.chat.id, 'hello', reply_markup=markup)
    
    
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    text = message.text
    if (text == 'mahasiswa'):
      msg = bot.reply_to(message, 'masukan nim')
      bot.register_next_step_handler(msg, process_nim_step)
      #bot.reply_to(message, message.text)
    elif (text == 'account'):
      bot.reply_to(message, 'coming soon!')
      
def process_nim_step(message):
  bot.send_chat_action(message.chat.id, 'typing')
  try:
    req = Sikadu()
    chat_id = message.chat.id
    nim = message.text
    #user = Mahasiswa(nim)
    #user_dict[chat_id] = user
    #21106011089
    data = req.search(nim)
    if ('AKTIFKAN' in data['account']['krs']):
      krs = 'not active' 
      krs_icon = krs + ' ' + cross
    else:
      krs = 'active' 
      krs_icon = krs + ' ' + check
    
    if ('AKTIFKAN' in data['account']['uas']):
      uas = 'not active' 
      uas_icon = uas + ' ' + cross
    else:
      uas = 'active'
      uas_icon = uas + ' ' + check
    
    if ('AKTIFKAN' in data['account']['uts']):
      uts = 'not active'
      uts_icon = uts + ' ' + cross
    else:
      uts = 'active'
      uts_icon = uts + ' ' + check

    if ('AKTIFKAN'in data['account']['sikadu']):
      sikadu = 'not active'
      sikadu_icon = sikadu + ' ' + cross
    else:
      sikadu = 'active'
      sikadu_icon = sikadu + ' ' + check

    msg = bot.send_message(message.chat.id, 'DATA MAHASISWA UNWAHAS\n\n' + 'NAMA : ' + data['name'] + '\nNIM : ' + data['nim'] + '\nKELAS : ' + data['kelas'] + '\nANGKATAN : ' + data['angkatan'] + '\nIP LALU : ' + data['ip_lalu'] + '\n\nPROFIL\n\n' + 'ALAMAT : ' + data['profile']['address'] + '\nNO TELEPON : ' + data['profile']['phone'] + '\nKTP : ' + data['profile']['ktp'] + '\n\nSTATUS\n\n' + 'ISI KRS : ' + krs_icon+ '\nUAS : ' + uas_icon + '\nUTS : ' + uts_icon + '\nAKUN SIKADU : ' + sikadu_icon, reply_markup=gen_markup_account(data['nim'],krs, uas, uts, sikadu))
  except Exception as e:
    bot.reply_to(message, 'oooops')


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
  data = query.data
  if data.startswith('krs-'):
    get_krs_callback(query)
  if data.startswith('uas-'):
    get_uas_callback(query)
  if data.startswith('uts-'):
    get_uts_callback(query)
  if data.startswith('sikadu-'):
    get_sikadu_callback(query)


def get_krs_callback(query):
  nim = query.data[4:]
  bot.send_message(query.message.chat.id, 'hayo lo mau ngapain!!')

def get_uas_callback(query):
  nim = query.data[4:]
  bot.send_message(query.message.chat.id, 'bayar dulu baru uas!!')

def get_uts_callback(query):
  nim = query.data[4:]
  bot.send_message(query.message.chat.id, 'hmmmmmm jangan macem macem km!!')

def get_sikadu_callback(query):
  nim = query.data[7:]
  bot.send_message(query.message.chat.id, 'hayo lo mau ngapain!!')
  
  
def gen_markup_account(nim, krs, uas, uts, sikadu):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('aktifkan krs' if krs == 'not active' else 'matikan krs', callback_data="krs-"+ nim),InlineKeyboardButton('aktifkan uas' if uas == 'not active' else 'matikan uas', callback_data="uas-" + nim))
    markup.add(InlineKeyboardButton('aktifkan uts' if uts == 'not active' else 'matikan uts', callback_data="uts-"+ nim),InlineKeyboardButton('aktifkan sikadu' if sikadu == 'not active' else 'matikan sikadu', callback_data="sikadu-" + nim))
    
    return markup

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()
