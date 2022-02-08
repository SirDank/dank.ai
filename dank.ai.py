import os
import re
import sys
import time
import emoji
import random
from colorama import init, Fore, Style
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

#from gtts import gTTS
#from playsound import playsound

def banner_colorize(): # randomized banner color

    bad_colors = ['BLACK', 'WHITE', 'LIGHTBLACK_EX', 'LIGHTWHITE_EX', 'RESET']
    codes = vars(Fore)
    colors = [codes[color] for color in codes if color not in bad_colors]
    colored_chars = [random.choice(colors) + char for char in banner_ascii]
    banner_colorized = ''.join(colored_chars).splitlines()
    return banner_colorized

def banner(): # banner aligner

    width = os.get_terminal_size().columns
    banner_lines = banner_ascii.splitlines()
    for i in range(len(banner_lines)):
        banner_lines[i] = banner_lines[i].center(width).replace(banner_lines[i],banner_colored[i])
    banner_aligned = ''.join(banner_lines)
    return banner_aligned

def clr(string, mode):  # string colorizer

    if mode == 1:return string.replace("[",f"{magenta}[{white}").replace("]",f"{magenta}]{white}").replace(">",f"{magenta}>{white}").replace(".",f"{magenta}.{white}").replace(",",f"{magenta},{white}").replace("!",f"{magenta}!{white}").replace("(",f"{magenta}({white}").replace(")",f"{magenta}){white}").replace("/",f"{magenta}/{white}").replace(":",f"{magenta}:{white}") # sys
    elif mode == 2:return string.replace(">",f"{magenta}>{white}") # input
    elif mode == 3:return string.replace(">",f"{magenta}>{cyan}") # output

def cls():
    os.system('cls');print(banner())

if __name__ == '__main__':
    
    os.system("title dank.ai")
    filepath = os.path.dirname(__file__) # as .py
    #filepath = os.path.dirname(sys.argv[0]) # as .exe
    os.chdir(filepath)
    
    init(autoreset=True) # colors
    magenta = Fore.LIGHTMAGENTA_EX + Style.BRIGHT
    white = Fore.WHITE + Style.BRIGHT
    cyan = Fore.CYAN + Style.BRIGHT
    red = Fore.RED + Style.BRIGHT
    
    banner_ascii = '''

______  _______ __   _ _     _   _______ _____
|     \ |_____| | \  | |____/    |_____|   |  
|_____/ |     | |  \_| |    \_ . |     | __|__

'''
    banner_colored = banner_colorize()
    
    # setup
    
    try:os.mkdir("dank.ai")
    except:pass
    os.chdir("dank.ai")
    if os.path.isfile("bot_name.txt"):
        bot_name = open("bot_name.txt","r").read()
    else:
        cls()
        bot_name = input(clr("  > Bot Name: ",1))
        open("bot_name.txt","w+").write(bot_name)

    #chatbot=ChatBot(bot_name,logic_adapters=['chatterbot.logic.BestMatch','chatterbot.logic.TimeLogicAdapter'])
    chatbot=ChatBot(bot_name,logic_adapters=['chatterbot.logic.BestMatch'])
    
    while True:
        
        cls()
        print(clr("\n  > 1. Train (one-time)",1))
        print(clr("\n  > 2. Start",1))
        print(clr("\n  > 3. Exit",1))
        choice = input(clr("\n  > Choice [1/2/3]: ",1))
        
        if choice == "1": # training

            cls()
            print(clr("\n  > 1. Corpus Training (required, one-time)",1))
            print(clr("\n  > 2. Whatsapp Training (optional, one-time)",1))
            choice = input(clr("\n  > Choice [1/2]: ",1))

            if choice == "1": # corpus trainings
                
                cls()
                print(clr("\n  > Available Languages: Bengali, Chinese, English, French, German, Hebrew, Hindi, Indonesian, Italian, Japanese, Korean, Marathi, Oriya, Persian, Portuguese, Russian, Spanish, Swedish, Telugu, Thai, TraditionalChinese, Turkish",1))
                language = input(clr("\n  > Language: ",1)).lower()
                
                cls()
                print("\n")
                trainer = ChatterBotCorpusTrainer(chatbot)
                trainer.train(f"chatterbot.corpus.{language}")

            elif choice == "2": # whatsapp chat trainer

                cls()
                print(clr("\n  > On your phone, go to any chat/group, click export chat without media",1))
                print(clr("\n  > Transfer txt file to your PC and place it anywhere",1))
                print(clr("\n  > Rename the txt file to something simple, remove emojis from file name",1))
                print(clr("\n  > Drag and drop the txt file here and hit [ENTER]...",1))
                whatsapp_chat = input(clr("\n  > Location: ",1)).replace('"','')
                whatsapp_chat = open(whatsapp_chat,"r",encoding="utf8").read().splitlines()
                
                print(clr("\n  > Cleaning...",1)) # whatsapp chat cleanup

                cleaned_chat = [""]
                emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"u"\U0001F300-\U0001F5FF"u"\U0001F680-\U0001F6FF"u"\U0001F1E0-\U0001F1FF""]+", flags=re.UNICODE)
                chinese_pattern = re.compile(u'[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]', re.UNICODE)
                        
                for line in whatsapp_chat:
                    remove_line = False
                    if "omitted" in line or "this message was deleted" in line.lower() or "omitted" in line:
                        remove_line = True
                    if not remove_line:
                        if ": " not in line:
                            if "] " not in line and " - " not in line:
                                remove_line = True
                    if not remove_line:
                        add_line = True
                        try:
                            line = line.split(": ")[1]
                            line = ''.join(c for c in line if c not in emoji.UNICODE_EMOJI)
                            line = emoji_pattern.sub(r'', line)
                            line = chinese_pattern.sub(r'', line)
                            if "@" in line:
                                if line.replace("@","").isdigit():add_line = False
                            if add_line:
                                if line == "" or line == "\n" or line == ".":add_line = False
                            if add_line:
                                if line == cleaned_chat[-1]:add_line = False
                            if add_line:
                                cleaned_chat.append(line)
                        except:pass
                whatsapp_chat = cleaned_chat
                cleaned_chat = None
                open("whatsapp_chat_cleaned.txt","w+",encoding="utf8").write('\n'.join(whatsapp_chat))
                
                cls()
                print(clr("\n  > Read through whatsapp_chat_cleaned.txt and verify if everything looks alright",1))
                print(clr("\n  > It should not have [timestamps, contact names] it might have some [emojis, chinese characters, @phone-numbers]",1))
                print(clr("\n  > Opening in 5s...",1))
                time.sleep(5)
                os.system("whatsapp_chat_cleaned.txt")
                choice = input(clr("\n  > Confirm Whatsapp Training [y/n]: ",1)).lower()
                
                if choice == "y":
                    print("\n")
                    trainer = ListTrainer(chatbot)
                    trainer.train(whatsapp_chat)

        elif choice == "2":
            
            #cls()
            #print(clr("\n  > Available Audio Languages: https://cloud.google.com/text-to-speech/docs/voices",1))
            #lang_code = input(clr("\n  > Language Code: ",1))
            
            cls()
            while True:
                
                # text
            
                msg = input(clr(f"  > ",2))
                if msg.lower() == "bye" or msg.lower() == "exit":break
                response = chatbot.get_response(msg)
                print(clr(f"\n  > {response}\n",3))
                
                # audio
                
                #obj = gTTS(text=response, lang=lang_code, slow=False)
                #obj.save("audio.mp3")
                #playsound("audio.mp3")

        elif choice == "3":
            sys.exit()
