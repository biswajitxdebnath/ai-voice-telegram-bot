#Main code for the telegram bot that converts texts to speech .

#1st get your tools from the toolkit

import uuid  # Add this at the top of your code . For random naming of the files .
import time  # Add this to the top
import re #Debugged 
import os
from gtts import gTTS 
from telegram import Update
from telegram.ext import Updater , CommandHandler , MessageHandler , Filters , CallbackContext
from dotenv import load_dotenv

#2nd Load your bot token by load_dotenv() function from the .env file . Environment Variable .

load_dotenv()   #Tells python to read from the .env file now
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # It grabs(find) the value of variable TBT as string from the .env and assign it the object TOKEN

#Now 3rd /start handler . It starts the command handler . It gives the user info about the bot .

def start(update : Update , context : CallbackContext) -> None: #Here I am defining a function named start(linked to the /start button) . 
  update.message.reply_text("Hey💗! Its *Restlessness* 😊. Send me with any text💬 _buddy_ and I will reply you with voice 🗣 ", parse_mode = "Markdown") #I have doubt in this. Will comeback later .

#4th,This will turn user's text message into voice .And then send it to the user .

def handle_text(update : Update , context : CallbackContext) -> None :

  actual_text = update.message.text  #Variable for text through chained object access .
  actual_chat_id = update.message.chat_id #Variable for chat_id 

  # Clean text and limit filename to safe length
  safe_text = re.sub(r'[<>:"/\\|?*\n\r\t]', '', actual_text).strip().replace(' ', '_')[:30]

  try :
    tts = gTTS(text=actual_text , lang='en')
    filename = f"voice_{uuid.uuid4().hex}.mp3"
    tts.save(filename)
    
    with open(filename , 'rb') as actual_audio :
     context.bot.send_audio(chat_id = actual_chat_id , audio = actual_audio)
    
    time.sleep(0.5)  # 💡 Let Windows close the file
    os.remove(filename)  # 🔥 Delete it safely

  except Exception as e :
    update.message.reply_text('I am soorryy 😭😭 . I failed to convert text to voice 😵‍💫')
    print(f"Error : {e}")

#5th : Lets create the engine that wires everything together and runs the bot .

def main() -> None : #Defined a function main which doesn't return any value . It doesn't any input from outside .
  updater = Updater(TOKEN , use_context = True)  #Tool that conect the bot to tg
  dispatcher = updater.dispatcher  #A traffic police inside updater which send things to correct function
  dispatcher.add_handler(CommandHandler('start',start)) 
  dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command , handle_text)) #Registering the rules for reacting to message .

  updater.start_polling()  #Starts asking tg for msgs every few seconds .
  updater.idle()     #Keeps the bot running forever

if __name__ == "__main__" : #Run the main function now .
 main()

# 1. Imports
# 2. load_dotenv + get TOKEN
# 3. def start()
# 4. def handle_text()
# 5. def main()
# 6. if name == "main": main()