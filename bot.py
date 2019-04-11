#encoding: utf-8
import logging

class Bot(object):
    def __init__(self, send_callback, users_dao, tree):
        self.send_callback = send_callback
        self.users_dao = users_dao
        self.tree = tree
    
    def handle(self, user_id, user_message):
        logging.info("Se invoco el metodo handle")
        #obtener el historial de eventos o mensajes intercambiados por el usuario
        history = [
            (u"Hola! Soy un gato","bot"),
            (user_message, "user")
            
        ]
        #en funcion al mensaje escrito por el usuario va a responder segun el tree
        
        response_text = self.tree['say']
        possible_answers = self.tree['answers'].keys()

        tree = self.tree

        for text, author in history:
            logging.info("text: %s", text)
            logging.info("author: %s", author)
            
            if author == 'bot':
                print type(text)
                print type(tree['say'])
                if text == tree['say']:
                    tree == tree['answers']

            elif author == 'user':
                key = get_key_if_valid(text, tree)
                if key is not None:
                    tree = tree[key]
                    if 'say' in tree:
                        response_text = tree['say']
                    if 'answers' in tree:
                        possible_answers = tree['answers'].keys() 

        possible_answers.sort()
        self.send_callback(user_id, response_text, possible_answers)

def get_key_if_valid(text, dictionary):
    for key in dictionary:
        if key.lower() == text.lower():
            return key

    return None