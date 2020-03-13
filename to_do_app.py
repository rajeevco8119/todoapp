import time,datetime,os
from googlesearch import search
from selenium import webdriver
import requests
import math
import wikipedia
from googletrans import Translator
import calendar as cal

a = str("FOR OPERATORS ENTER THE FOLLOWING you can use upper or lower case for operations\n"
                "+     for addition\n"
                "-     for subtraction\n"
                "/     for division\n"
                "*     for multiplication\n"
                "^     for power\n"
                "r     for root\n"
                "%     for modulus\n"
                "pie   for Pie\n"
                "e     for E\n"
                "sin   for sin (trig)\n"
                "cos   for cos (trig)\n"
                "tan   for tan (trig)\n"
                "!     for factorial \n"
                "ln    for ln (natural log)\n"
                "for PI and E you need to put any numbers just to prevent input error but write PI or E for operator."
                "for FACTORIAL and TRIG you need to put zero (or any number) as the first number, then the sign and last the number you want to calculate. The first number (or the zero) will not be used for calculations but it will prevent an error\n")
b = str('Language Name	Code	Language Name	Language Code\n'
'Afrikaans	af	Irish	ga\n'
'Albanian	sq	Italian	it\n'
'Arabic	ar	Japanese	ja\n'
'Azerbaijani	az	Kannada	kn\n'
'Basque	eu	Korean	ko\n'
'Bengali	bn	Latin	la\n'
'Belarusian	be	Latvian	lv\n'
'Bulgarian	bg	Lithuanian	lt\n'
'Catalan	ca	Macedonian	mk\n'
'Chinese Simplified	zh-CN	Malay	ms\n'
'Chinese Traditional	zh-TW	Maltese	mt\n'
'Croatian	hr	Norwegian	no\n'
'Czech	cs	Persian	fa\n'
'Danish	da	Polish	pl\n'
'Dutch	nl	Portuguese	pt\n'
'English	en	Romanian	ro\n'
'Esperanto	eo	Russian	ru\n'
'Estonian	et	Serbian	sr\n'
'Filipino	tl	Slovak	sk\n'
'Finnish	fi	Slovenian	sl\n'
'French	fr	Spanish	es\n'
'Galician	gl	Swahili	sw\n'
'Georgian	ka	Swedish	sv\n'
'German	de	Tamil	ta\n'
'Greek	el	Telugu	te\n'
'Gujarati	gu	Thai	th\n'
'Haitian Creole	ht	Turkish	tr\n'
'Hebrew	iw	Ukrainian	uk\n'
'Hindi	hi	Urdu	ur\n'
'Hungarian	hu	Vietnamese	vi\n'
'Icelandic	is	Welsh	cy\n'
'Indonesian	id	Yiddish	yi\n')
NO_OF_PLAYERS = 1
BOARD_SIZE = 5
print('****************************  Utilities ***********************')
class TelephoneDirectory:
    def __init__(self):
        self.list1 = []
        self.list2 = []
        self.dict1 = {}
        self.temp = 100

    def addContact(self,name,number):
        self.list1.extend(name)
        self.list2.extend(number)
        self.dict1[name]=number
        print('Successfully added')

    def searchContact(self,name):
        for k,v in self.dict1.items():
            if name == k:
                print(str(k)+':'+str(self.dict1[name]))
                return
            else:
                print('No name exist in dictionary')
                return

    def deleteContact(self,name):
        #self.list1.remove(name)
        #self.list2.remove(self.dict1[name])
        del self.dict1[name]
        print(self.dict1)
        return

    def updateContact(self,name,value):
        self.dict1[name] = value
        print(self.dict1)
        return

    def viewContact(self):
        print(self.dict1)
        return

    def stopwatch(self,value):
       secs = input('Enter seconds')
       print(str(time.ctime())[0:10]+str(time.ctime())[19:24])
       then = datetime.datetime.now() + datetime.timedelta(seconds=float(secs))
       while then > datetime.datetime.now():
           print(str(time.ctime())[10:-5])
           time.sleep(1)

    def weather(self,city):
        api_key = 'Your API Key Here'
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature -= 273
            current_pressure = y["pressure"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            print(" Temperature (in celsius unit) = " +
                  str(current_temperature) +
                  "\n atmospheric pressure (in hPa unit) = " +
                  str(current_pressure) +
                  "\n humidity (in percentage) = " +
                  str(current_humidiy) +
                  "\n description = " +
                  str(weather_description))
        else:
            print(" City Not Found ")

    def alarm(self,hour,minute):
        stop = False
        time1_hour = hour
        time1_min = minute
        if len(time1_hour) == 1:
            time1_hour = '0' + time1_hour
        while stop == False:
            rn = str(datetime.datetime.now().time())
            print(rn)
            if rn >= time1_hour + ":" + time1_min + ":00.000000":
                stop = True
                os.system("1.mp3")

    def news(self):
        main_url = 'https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey="YOUR NEWS API KEY HERE";'
        open_bbc_page = requests.get(main_url).json()
        article = open_bbc_page['articles']
        result = []
        for ar in article:
            result.append(ar['title'])
        for i in range(len(result)):
            print(i + 1, result[i])

    def googlesearch(self,keyword):
        for j in search(keyword,stop=20):
            print(j)

    def wikipediasearch(self,keyword):
        complete_content = wikipedia.page(keyword)
        print(complete_content.content)

    def scientificCalculator(self):
        ch = 'y'
        while ch == 'y':
            print(a)
            op = input('Enter operator')
            if op == "+":
                firstNumber = float(input('Enter first number'))
                secondNumber = float(input('Enter second number'))
                print(firstNumber, "+", secondNumber, "=", firstNumber + secondNumber)
            elif op == "-":
                firstNumber = float(input('Enter first number'))
                secondNumber = float(input('Enter second number'))
                print(firstNumber, "-", secondNumber, "=", firstNumber - secondNumber)
            elif op == "*":
                firstNumber = float(input('Enter first number'))
                secondNumber = float(input('Enter second number'))
                print(firstNumber, "*", secondNumber, "=", firstNumber * secondNumber)
            elif op == "/":
                firstNumber = float(input('Enter first number'))
                secondNumber = float(input('Enter second number'))
                print(firstNumber, "/", secondNumber, "=", firstNumber / secondNumber)
            elif op == "^":
                firstNumber = float(input('Enter first number'))
                secondNumber = float(input('Enter second number'))
                print(firstNumber, "^", secondNumber, "=", firstNumber ** secondNumber)
            elif op == "r":
                firstNumber = float(input('Enter first number'))
                secondNumber = float(input('Enter second number'))
                print(firstNumber, "root", secondNumber, "=", secondNumber ** (1 / firstNumber))
            elif op == "%":
                firstNumber = float(input('Enter first number'))
                secondNumber = float(input('Enter second number'))
                print(firstNumber, "%", secondNumber, "=", firstNumber % secondNumber)
            # factorial
            elif op == "!":
                firstNumber = float(input('Enter Number'))
                temp = firstNumber
                secondNumber = 1
                while firstNumber > 1:
                    secondNumber *= firstNumber
                    firstNumber = firstNumber - 1
                print("n!(", temp, ")=", secondNumber)
            elif op == "sin":
                firstNumber = float(input('Enter Number'))
                print("sin(", firstNumber, ")=", math.sin(firstNumber))
            elif op == "cos":
                firstNumber = float(input('Enter Number'))
                print("cos(", firstNumber, ")=", math.cos
                (firstNumber))
            elif op == "tan":
                firstNumber = float(input('Enter Number'))
                print("tan(", firstNumber, ")=", math.tan(firstNumber))
            elif op == "pie" or op == "pi":
                print("Pie =", math.pi)
            elif op == "e":
                print("E =", math.e)
            elif op == "ln":
                firstNumber = float(input('Enter Number'))
                print("ln(", firstNumber, ")= ", math.log(firstNumber))
            else:
                print("incorrect operator")
            ch = input('Do you want to continue? y/n')
    def amazonShopping(self):
        item = input('Enter product to be searched')
        URL = 'https://www.amazon.in/s?k='+item+'&ref=nb_sb_noss_2'
        URL2 = 'https://www.flipkart.com/search?q='+ item +'&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
        URLList = [URL,URL2]
        browser = webdriver.Chrome("C:/Users/rajmahaj/PycharmProjects/test/utils2/app/chromedriver.exe")
        browser.maximize_window()
        browser1 = webdriver.Chrome("C:/Users/rajmahaj/PycharmProjects/test/utils2/app/chromedriver.exe")
        browser1.maximize_window()
        browser.get(URL)
        browser1.get(URL2)
        return
    def google_translate(self):
        ch = 'y'
        while ch == 'y':
            print(b)
            src_ip = input('Enter source language')
            dest_ip = input('Enter destination language')
            src_text = input('Enter text to be translated')
            translator = Translator()
            translated = translator.translate(src_text, src=src_ip, dest=dest_ip)  # Pass both source and destination
            print(" Source Language:" + translated.src)
            print(" Translated string:" + translated.text)
            ch = input('Do you wish to continue? y/n')

    def calendar(self,year):
        year = int(year)
        print(cal.calendar(year))
        return

if __name__=='__main__':

    object = TelephoneDirectory()
    while(1):
        print("""
                         1:Add a contact
                         2:Search a contact
                         3:Delete a contact
                         4:Update a contact
                         5:View directory
                         6:Stopwatch
                         7:Alarm
                         8:Weather
                         9:News
                         10:Google search
                         11:Wikipedia search
                         12:Scientific calculator
                         13:Shopping
                         14:Language translate
                         15:Tic Tac Game
                         16:Calendar
                         """)
        choice = input("Enter your choice\n")
        if choice == str(1):
            n = input("Enter the number of contacts : \n")
            for i in range(0, int(n)):
                name1 = input("Enter your name: \n")
                num = input("Enter your phone number: \n")
                object.addContact(name1, num)
        elif choice == str(2):
            name = input('Enter name\n')
            object.searchContact(name)
        elif choice == str(3):
            name = input('Enter name\n')
            object.deleteContact(name)
        elif choice == str(4):
            name = input('Enter name\n')
            value = input('Enter value\n')
            object.updateContact(name, value)
        elif choice == str(5):
            object.viewContact()
        elif choice == str(6):
            start = time.time()
            object.stopwatch(start)
        elif choice == str(7):
            hour = input('Enter hour')
            minute = input('Enter minute')
            object.alarm(hour,minute)
        elif choice == str(8):
            city = input('Enter city name:  ')
            object.weather(city)
        elif choice == str(9):
            object.news()
        elif choice == str(10):
            keyword = input('Search Google: ')
            object.googlesearch(keyword)
        elif choice == str(11):
            keyword = input('Search Wikipedia: ')
            object.wikipediasearch(keyword)
        elif choice == str(12):
            object.scientificCalculator()
        elif choice == str(13):
            object.amazonShopping()
        elif choice == str(14):
            object.google_translate()
            #Sample 안녕하세요 src_lang-ko
        elif choice == str(15):
            from utils2.app.TicTac import Game
            #game = Game(NO_OF_PLAYERS,BOARD_SIZE)
            #game.start()
        elif choice == str(16):
            yy = input('Enter year')
            object.calendar(yy)
        else:
            print('Wrong choice, Enter other one\n')