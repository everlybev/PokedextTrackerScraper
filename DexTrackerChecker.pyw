import time
import smtplib
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from datetime import datetime
import os
from os.path import exists
import secrets
from email.message import EmailMessage


#cd F:\Users\dudeo\AppData\Local\Programs\Python\Python39
#pyinstaller --onefile SerebiiHomeChecker.pyw
TheConfigurationFile = 'F:\\Users\\dudeo\\AppData\\Local\\Programs\\Python\\Python39\\dist\\Config.txt'


configTXT = 'F:\\Users\\dudeo\\AppData\\Local\\Programs\\Python\\Python39\\dist\\Config.txt'

def better_sleep(time2wait):
    start = time.time()
    while((time.time()-start)<time2wait-.00042):
        time.sleep(1)
    
#Get email and password
def login_info():
    configFile = open(TheConfigurationFile, 'r')
    config = str(configFile.read())
    email = config.split('Email: ')
    email = email[1].split('Password: ')
    password = str(email[1].strip())
    email = str(email[0].strip()).strip()
    try:
        server = config.split('Server: ')[1]
        server = str(server.split('Email: ')[0].strip())
    except:
        print('its the server')
    try:
        port = config.split('Port: ')[1]
        port = port.split('Server: ')[0].strip()
        port = int(str(port))
    except:
        print('port also fucked up')
    try:
        app = config.split('App Pass: ')[1]
        app = app.split('Port: ')[0].strip()
        app = str(app)
    except:
        print('port also fucked up')
    configFile.close()
    return email, password, server, port, app


#email function
def email(sites):
    myEmail, myPass, theServer, thePort, theAppPassword = login_info()
    configFile = open(configTXT, 'r')
    raw_emails = configFile.readlines()
    configFile.close()
    notDone = 1
    x = 0
    #Get other emails
##    while notDone > 0:
##        bad = 0
##        for line in range(0, len(raw_emails)-x, 1):
##            if ((str(raw_emails[line]).__contains__('@')) and ((str(raw_emails[line]).__contains__('.')))):
##                if (str(raw_emails[line]).__contains__('Email')):
##                    try:
##                        raw_emails[line] = raw_emails[line+1]
##                        raw_emails[line+1] = 0
##                    except:
##                        raw_emails[line] = 0
##                else:                    
##                    raw_emails[line] = str(raw_emails[line]).strip()
##            else:
##                try:
##                    raw_emails[line] = raw_emails[line+1]
##                    raw_emails[line+1] = 0
##                except:
##                    raw_emails[line] = 0
##                bad = 1
##        x=x+1
##        if bad == 0:
##            notDone = 0
##        #print(raw_emails)
##        
##    the_emails = []
##    for i in range(0, len(raw_emails), 1):
##        if raw_emails[i] != 0:
##            the_emails.append(raw_emails[i])
##            print(the_emails[i])
    #Send email to me
    try:
        server = smtplib.SMTP_SSL(theServer, thePort)
        server.login(myEmail, theAppPassword)
        msge = EmailMessage()
        msge.set_content(sites)
        server.send_message(msge, from_addr=myEmail, to_addrs=myEmail)
        server.quit()
    except Exception as anException:
        better_sleep(1)
        logger = open('Pokemon.txt', 'a')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write('\n')
        logger.write(dt_string + '\n')
        try:
            logger.write('The Exception was ' + str(anException) + '\n')
        except:
            pass
        logger.write(str('Failed to send email to me!'))
        logger.close()
        #Send email to others
##    for i in range(0, len(the_emails), 1):
##        try:
##            server = smtplib.SMTP_SSL(theServer, thePort)
##            server.login(myEmail, theAppPassword)
##            msge = EmailMessage()
##            msge.set_content(sites)
##            server.send_message(msge, from_addr=myEmail, to_addrs=str(the_emails[i]))
##            server.quit()
##        except:
##            better_sleep(1)
##            logger = open('Pokemon.txt', 'a')
##            now = datetime.now()
##            dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
##            logger.write('\n')
##            logger.write(dt_string + '\n')
##            logger.write(str('Failed to send email to ' + str(the_emails[i]) + '!'))
##            logger.close()



#pokemon checker
def Pokemon(counter, past):
    s = past
    #s = 9
    #get the sites from the configuration file
    serebii_site = 'https://pokedextracker.com/blog/'
    print(serebii_site)
    short_serebii_site = 'pokedextracker.com/blog/'
    msg = 'There is new dex tracker info! Check out ' + short_serebii_site + '   --Love Evan'
    try:
        response = requests.get(serebii_site)
        site = str(response)
    except:
        response = 'Not Gotten'
        site = 'Fucked'
    if site != "Fucked":
        logger = open('Pokemon.txt', 'a')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write('\n')
        logger.write(dt_string + '\n')
        logger.write(str('pokedextracker got response'))
        logger.close()
    try:
        bs_response = BeautifulSoup(response.text, "lxml")
        try:
            bs_response = bs_response.body.main.getText()
        except:
            try:
                bs_response = bs_response.body.getText()
            except:
                try:
                    bs_response = bs_response.getText()
                except:
                    bs_response = str(bs_response)
    except:
        bs_response = response
    print(bs_response)
    bs_response = str(bs_response)
    bad_response = past
    if bs_response == s:
        #there was no change to the site
        s = bs_response
        sendEmail = 0
        #sendEmail = 1 # comment out this line
    else:
        s = bs_response
        sendEmail = 1
        if bad_response == 'Not Gotten':
            msg = 'Last loop the site was down but it is back up\n\n' + msg
        elif bs_response == 'Not Gotten':
            sendEmail = 0
    #sendEmail = 1 # comment out this line
    if counter > 0:
        if sendEmail == 1:
            email(str(msg))
            logger = open('Pokemon.txt', 'a')
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
            logger.write('\n')
            logger.write(dt_string + '\n')
            logger.write('Dex Tracker Update!!!\n')
            logger.close()
        else:
            logger = open('Pokemon.txt', 'a')
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
            logger.write('\n')
            logger.write(dt_string + '\n')
            logger.write('No New Dex Tracker Update\n')
            logger.close()
    else:
        logger = open('Pokemon.txt', 'a')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write('\n')
        logger.write(dt_string + '\n')
        logger.write('Just started.  Not sending the dex tracker email. \n')
        logger.close()
        pastsoup = s
    msg = 'Go to: '
    sendEmail = 0
    return s


def main():
    #email('This is a test.  Current BDSP events are Shayman.  Connect to Mystery Gift internet.  Starting April 1st to April 30th connect to MG internet and get Darkrai.  I love you a ton and once I finish school I promis Ill have more game time for you <3')
    z = 0
    count = 0
    daycount = count
    past = 0
    if(exists('Pokemon.txt')):
        pass
    else:
        logger = open('Pokemon.txt', 'w')
        logger.write('This is the log of stuff:' + '\n')
        logger.close()
    while z < 30:
        # should do the initializing
        # wont send email.  Just doing set up
        if count == 0:
            past_soup = Pokemon(count,  past)
        #now the set up is done do the check for real
        if count > 0:
            now = datetime.now()
            today = now.strftime("%I")
            if today == past:
                past = today
            else:
                try:
                    past_soup = Pokemon(count, past_soup)
                except Exception as theMainException:
                    print(theMainException)
                    try:
                        msg = 'There was a main() error on dex tracker. Maybe check pokedextracker.  The error is:\n' + str(theMainException)
                    except:
                        msg = 'There was a main() error on dex tracker. Maybe check pokedextracker'
                    email(msg)
                    logger = open('Pokemon.txt', 'a')
                    now = datetime.now()
                    dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
                    logger.write('\n')
                    logger.write(dt_string + '\n')
                    logger.write(str(theMainException) + '\n')
                    logger.write('There was a main() error on dex tracker. \n' + '\n')
                    logger.close()
                past = today
                daycount = daycount + 1
        better_sleep(secrets.randbelow(7))
        count = count + 1
        #print(count)

        better_sleep(8)
        
if __name__ == '__main__':
    main()








