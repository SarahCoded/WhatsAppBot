from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    stringQuery = ""
    reply = ""
    acceptableChars = "abcdefghijklmnopqrstuvwxyz? -"
    for char in incoming_msg:
        if not char in acceptableChars:
            greeting = "Hello! I am the crossword bot \U0001F916\n-> Send me a word and I'll find the definition.\n-> Or give me a partial word in the form s??d and I'll fill in the blanks!"
            msg.body(greeting)
            return str(resp)
    # Fix formatting for url string, replace unknown letters with _'s
    stringQuery = incoming_msg.replace('?', '_').replace(' ', '_')
    r = requests.get(f'https://www.crosswordsolver.org/solve/{stringQuery}')
    soup = BeautifulSoup(r.content, "html.parser")
    if not r.status_code == 200:
        msg.body("Sorry! I could not fetch a response. Please try again later.")
        return str(resp)
    elif not '_' in stringQuery: # Get definitions of a given word
        results = soup.select("div[class*=definition]")
        if not results:
            msg.body("Definition not found")
        for s in results: # Workaround to get only li items from div
            listItem = s.find_all('li')
            for count, li in enumerate(listItem, start=1):
                reply = reply + str(count) + '. ' + li.text + '\n'
            msg.body(reply)
        return str(resp)
    else: # Find words that fit in from the blanks given
        results = soup.select("div[class*=word]")
        if not results:
            msg.body("No matching words were found. Maybe you put in an incorrect answer...")
            return str(resp)
        # Find out how many results there are
        numDiv = soup.select("div[id=matches-box]")
        for n in numDiv:
            num = n.find('span').text
        num = int(num[:-8]) # Remove word 'Results'
        copyNum = num
        for sect in results:
            reply = reply + sect.text + '\n'
        counter = 10
        while num > 10: # Get all the words (only 10 displayed per page)
            num -= 10
            r = requests.get(f'https://www.crosswordsolver.org/solve/{stringQuery}/{counter}')
            if not r.status_code == 200:
                break
            soup = BeautifulSoup(r.content, "html.parser")
            results = soup.select("div[class*=word]")
            for sect in results:
                reply = reply + sect.text + '\n'
            counter += 10
        if copyNum == 1:
            msg.body(f"{copyNum} result was found\n\n" + reply + "\nSend me a word and I'll give you the definition!")
        else:
            msg.body(f"{copyNum} results were found\n\n" + reply + "\nSend me a word and I'll give you the definition!")
    return str(resp)

if __name__ == '__main__':
    app.run()