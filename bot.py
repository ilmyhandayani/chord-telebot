import telebot
import requests
from bs4 import BeautifulSoup

api = "5210027608:AAFz9a_1FDRZ0Bvm3Im1D2f9Zgyg56cnUpk"
bot = telebot.TeleBot(api)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Selamat Datang di MY CHORDBOT INDONESIA \n Ketik /menu untuk melihat full command ya")


@bot.message_handler(commands=["menu"])
def send_menu(message):
    bot.reply_to(message,'''
Hallo Selamat Datang di MyChord Indonesia

Ketik /lagu 'nama penyanyi/judul lagu' untuk mencari judul lagu dan chord lagu
(example : /lagu isyana saravati)

~myChordBot
''' )

@bot.message_handler(commands=["lagu"])
def send_lagu(message):
    try:
        ses = requests.session()
        url = "https://chordtela.net/search?q="
        headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"}
        
        cari = (message.text).replace("/lagu ","")
        cari = (cari).replace(" ","-") 
        res = ses.get(url+cari, headers=headers)
        data = BeautifulSoup(res.text, "html.parser").find("div",{"class":"bg-primary p-a rounded"})
        sumber = data.findAll("a", href=True)
        judul = ""
        link = []
        print(len(link))
        if len(sumber) == 0:
            bot.reply_to(message, ''' 
Maaf, Pencarian tidak ditemukan :(

Mohon ketik sesuai format pesan
coba dengan /lagu 'judul lagu atau nama penyanyi'
contoh /lagu isyana sarasvati 
            ''')
        else: 
            if len(sumber) > 10:
                for i in range(10):
                    judul += f"{i+1}. {sumber[i].text}\n"
                    link.append(sumber[i]['href'])
            else:
                for i in range(len(sumber)):
                    judul += f"{i+1}. {sumber[i].text}\n"
                    link.append(sumber[i]['href'])
            judul += "\n Pilih angka untuk melihat chord dari list judul di atas :"
            pesan = bot.reply_to(message, judul)
            bot.register_next_step_handler(pesan, send_chord, link)

    except Exception as e:
        print(e)


def send_chord(message, link):
    try :
        if int(message.text) > 0 and int(message.text) < 10:
            url = "https://chordtela.net"+link[int(message.text)-1]
            ses = requests.session()
            headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"}
            
            link = ses.get(url, headers=headers)
            hasil = BeautifulSoup(link.text, "html.parser").find("pre",{"class":"chord"})
            bot.reply_to(message, hasil.text)
        else:
            bot.reply_to(message, "Maaf, angka tersebut tidak ada pada list lagu")

    except Exception as e:
       print(e)

@bot.message_handler(func=lambda message: True)
def all(message):
	bot.reply_to(message, ''' 
Pesan yang anda masukan tidak terdapat pada commands

Mohon ketik sesuai format pesan
coba dengan /menu atau /lagu 'judul lagu atau nama penyanyi'
contoh /lagu isyana sarasvati
    ''')

print("Bot Running")
bot.polling()