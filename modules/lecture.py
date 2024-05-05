import os
import secrets
import json

from text_splitter import Splitter
from GPT import ChatGPT
from db import Database_Manager

__DIR_NAME__ = "lectures"
__GPT_PROMPT__ = "You are an academic text shortener and summarizer. You will recieve a block of text which you need to shorten and summarize to the best of your abilities without losing any important context or info. The text may be given to you in various languages, you need to keep the original language. Your response NEEDS to be in a valid json format. The key of your json response will be \"text\" and the value the text you shortened and summarized. It is of great importance you only respond in a valid json format."

class Lecture_Manager:
    def __init__(self, db_manager, gpt_key):
        self.db_manager = db_manager
        self.text_splitter = Splitter()
        self.chat_gpt = ChatGPT(gpt_key, __GPT_PROMPT__)
        pass


    def init_dir(self):
        if not os.path.exists(__DIR_NAME__):
            os.makedirs(__DIR_NAME__)


    def verify_inputs(self, name, text):
        if len(name) < 3:
            return {"message": "Name must be at least 3 characters long"}

        if len(text) < 16:
            return {"message": "Text must be at least 16 characters long"}
        
        return None
    

    def write_file(self, file_name, text):
        file = open(file_name, "w")
        file.write(text)
        file.close()


    def clean_response(self, response): # Bro I HATE working with AI
        if response[0:7] == '```json':
            response = response[7:]
            response = response[0:-3]

        return response


    def new_lecture(self, user_id, name, text):
        self.init_dir()

        error_message = self.verify_inputs(name, text)
        if error_message:
            json.dumps(error_message), 401

        split_text = self.text_splitter.split_text(text)
        summarized_text = []

        for t in split_text:
            response = self.chat_gpt.get_response(t).choices[0].message.content
            summarized_text.append(response)
        
        file_name = __DIR_NAME__ + "/" + str(secrets.token_urlsafe(8)) + ".json"
        summarized_string = self.clean_response(''.join(summarized_text))

        self.write_file(file_name, summarized_string)
        self.db_manager.add_lecture(user_id, name, file_name)


lecture_manager = Lecture_Manager(Database_Manager("db.db") ,"key")
lecture_manager.new_lecture("aaaa", "bbbbb", "Cryptography is the technique of obfuscating or coding data, ensuring that only the person who is meant to see the information–and has the key to break the code–can read it. The word is a hybrid of two Greek words: “kryptós”, which means hidden, and “graphein”, which means to write. Literally, the word cryptography translates to hidden writing, but in reality, the practice involves the secure transmission of information. The use of cryptography can be traced to the ancient Egyptians and their creative use of hieroglyphics. But, the art of coding has seen great strides over the millennia, and modern cryptography combines advanced computer technology, engineering, and maths—among other disciplines—to create highly sophisticated and secure algorithms and ciphers to protect sensitive data in the digital era. For example, cryptography is used to create various types of encryption protocols that are regularly used to protect data. These include 128-bit or 256-bit encryption, Secure Sockets Layer (SSL), and Transport Layer Security (TLS). These encryption protocols protect all manner of digital information and data, from passwords and emails to ecommerce and banking transactions. There are different cryptographic types, which are useful for different purposes. For example, the simplest is symmetric key cryptography. Here, data is encrypted using a secret key, and then both the encoded message and the secret key are sent to the recipient for decryption. Of course, the problem here is that if the message is intercepted, the third party can easily decode the message and steal the information. To create a more secure system of encoding, cryptologists devised asymmetric cryptography, which is sometimes known as the “public key” system. In this instance, all users have two keys: one public and one private. When creating a coded message, the sender will request the recipient’s public key to encode the message. This way, only the intended recipient’s private key will decode it. This way, even if the message is intercepted, a third party cannot decode it.")
