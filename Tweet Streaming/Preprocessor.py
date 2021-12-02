# import libraries
import re
import gensim
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.porter import PorterStemmer

class Preprocessor():
    def __init__(self):
        pass
    
    def __stem_word(self, text):
        '''
        The function does the stem in the text
        
        Input: text
        
        Output: stemmed text
        '''
        por = PorterStemmer()
        return por.stem_sentence(text) # stem the tweet
    
    def __clear_stop_words(self, text):
        '''
        The function eliminates the stop words
        
        Input: text
        Output: cleaned text
        '''
        return remove_stopwords(text) # eliminate the stop words
    
    def clean_emojis(self, text):
        '''
        The function eliminates the emojis
        
        Input: text
        Output: cleaned text
        '''
        if text:
            return text.encode('ascii', 'ignore').decode('ascii')
        else:
            return None
    
    def re_process(self, text):
        '''
        The function eliminates all the words or signs that generates noise 
        in the text
        
        Input: text
        Output: cleaned text
        '''
        text = self.clean_emojis(text)
        text = re.sub(r'@[A-Za-z0-9]+', '', text) #Removing tags
        text = re.sub(r'#', '', text) # Removing the "#" symbol
        text = re.sub(r'RT', '', text) # Removing RT
        text = re.sub(r'https?:\/\/\S+', '', text) #Remove links
        text = re.sub(r'[^A-Za-z\s]+', '', text) # Remove not letters
        text =  " ".join(text.split())
        return text.lower()
    
    def cleaning(self, text):
        '''
        The function cleans the text 
        
        Input: text
        
        Output: text
        '''
        text = self.re_process(text)
        text = self.__clear_stop_words(text)
        text = self.__stem_word(text)
        return text

