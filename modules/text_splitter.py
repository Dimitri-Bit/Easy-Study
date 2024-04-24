import math

# Since ChatGPT has a limit of 4096 for message requests we will make sure that every text we send gets split up into even blocks

class Splitter:
    
    def __init__(self):
        pass

    def split_text(self, text):
        text.strip()
        split_parts = math.ceil(len(text) / 4090)
        
        start, end = 0, round(len(text) / split_parts)
        
        if split_parts > 1:
            split_sentence = []

            for i in range(len(text)):
                if i >= end and (text[i] == '.' or text[i] == '?' or text[i] == '!'):
                    end = i + 1
                    split_sentence.append(text[start:end])
                    start = end
                    end = end + end

            return split_sentence
        else:
            return [text]