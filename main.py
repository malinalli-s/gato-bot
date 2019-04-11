# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied
# See the License for the specific language governing permissions and
# limitations under the License.
# encoding: utf-8

import webapp2
import json
import logging
from google.appengine.api import urlfetch
from bot import Bot
import yaml


class MainPage(webapp2.RequestHandler):

    def __init__(self, request=None, response=None):
        super(MainPage, self).__init__(request, response)
        logging.info("Instanciando bot")
        tree= yaml.load(open('tree.yaml'))
        logging.info("Tree: %r", tree)
        self.bot = Bot(send_message, None, tree)

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        mode= self.request.get("hub.mode")
        if mode == "subscribe":
            challenge = self.request.get("hub.challenge")
            verify_token = self.request.get("hub.verify_token")
            if verify_token == VERIFY_TOKEN:
                    self.response.write(challenge)
        else:
            self.response.write("pronto esto sera un gatoooo, World!")
            #self.bot.handle(0, "message_text")
            
    def post(self):
        data = json.loads(self.request.body)
        logging.info("data obtenida desde mesenger: %r", data)

        if data["object"] == "page":
            for entry in data ["entry"]:
                for messaging_event in entry ["messaging"]:
                    sender_id = messaging_event ["sender"]["id"]

                    if messaging_event.get("message"):
                        message = messaging_event['message']
                        message_text = message.get('text', '')
                        logging.info("Mensaje obtenido: %s", message_text)
                        #bot handle
                        self.bot.handle(sender_id, message_text)
                        # send_message(sender_id, "Hola soy un gatoBot")
                    
                    if messaging_event.get("postback"):
                        logging.info("Post-back")

    
def send_message(recipient_id, message_text, possible_answers):
    #logging.info("Enviando mensaje a %r: %s", recipient_id, message_text)
    headers = {
        "Content-Type": "application/json"
    }
    #message = {"text": message_text}
    #20 caracteres
    #possible_answers = ["Gato A", "Gato B", "Gato C" ]
    message = get_postback_buttons_message( message_text, possible_answers)
    if message is None:
        message = {"text": message_text}

    raw_data={
        "recipient":{
            "id": recipient_id
        },
        "message": message
    }
    data = json.dumps(raw_data)
    logging.info("Enviando mensaje a %r: %s", recipient_id, message_text)
    r = urlfetch.fetch("https://graph.facebook.com/v2.6/me/messages?access_token=%s" % ACCESS_TOKEN, 
                        method=urlfetch.POST, headers=headers, payload=data)

    if r.status_code !=200:
        logging.error("Error enviando mensaje: %r", r.status_code)

def get_postback_buttons_message(message_text, possible_answers):
    if len(possible_answers)>3:
        return None

    buttons = []
    for answer in possible_answers:
        buttons.append({
            "type": "postback",
            "title": answer,
            "payload": answer
        })

    return {
        "attachment":{
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": message_text,
                "buttons": buttons,
            }

        }
    }



app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
