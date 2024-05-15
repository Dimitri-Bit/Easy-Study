import os
import secrets
import json

from flask import request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

from text_splitter import Splitter
from GPT import ChatGPT

__DIR_NAME__ = "/home/batman/Documents/Easy-Study/lectures"
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

        if len(text) < 150:
            return {"message": "Text must be at least 150 characters long"}
        
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


    def new_lecture(self):
        self.init_dir()

        request_data = request.get_json()
        user_id, name, text = get_jwt_identity(), request_data.get("name"), request_data.get("text")

        error_message = self.verify_inputs(name, text)
        if error_message:
            return json.dumps(error_message), 401

        split_text = self.text_splitter.split_text(text)
        summarized_text = []

        for t in split_text:
            response = self.chat_gpt.get_response(t).choices[0].message.content
            summarized_text.append(response)
        
        file_name = __DIR_NAME__ + "/" + str(secrets.token_urlsafe(8)) + ".json"
        summarized_string = self.clean_response(''.join(summarized_text))

        self.write_file(file_name, summarized_string)
        self.db_manager.add_lecture(user_id, name, file_name)

        return json.dumps({"message": "Successfully created lecture"}), 200
    

    def get_lectures(self):
        user_id = get_jwt_identity()
        lectures = self.db_manager.get_lectures(user_id)
        
        if not lectures:
            return json.dumps({"message": "No lectures found"}), 404
        
        lectures_dir = []
        
        for lecture in lectures:
            id = lecture[0]
            name = lecture[2]
            path = lecture[3]

            file = open(path, "r")
            contents_json = file.read()
            contents_json = json.loads(contents_json)
            contents = contents_json["text"]

            dir = {"id": id, "name": name, "contents": contents}
            lectures_dir.append(dir)

        return json.dumps({"lectures": lectures_dir}), 200