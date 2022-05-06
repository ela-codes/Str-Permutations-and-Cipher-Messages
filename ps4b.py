# Problem Set 4B
# Name: Aena Teodocio
# Time Spent: ~3 hours

from itertools import count
import string

# from practice import build_shift_dict

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'
valid_words = load_words(file_name = WORDLIST_FILENAME)

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = valid_words


    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        
        return self.message_text


    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()


    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        cipher_dict = {}

        for i in range(26):
            # if shift value is > 26, apply the remaining increment count to the beginning of alphabet list
            if i + shift >= 26: 
                    new_shift = i + shift - 26
                    cipher_dict[lowercase[i]] = lowercase[new_shift]
                    cipher_dict[uppercase[i]] = uppercase[new_shift]
            else:
                cipher_dict[lowercase[i]] = lowercase[i+shift]
                cipher_dict[uppercase[i]] = uppercase[i+shift]
        return cipher_dict


    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        cipher_letters = self.build_shift_dict(shift)
        cipher_word = ''


        for i in self.message_text:
            if len(i) > 1:
                for j in i:
                    if not j.isalpha():
                        cipher_word += j
                    else:
                        cipher_word += cipher_letters[j]
            else:
                if not i.isalpha():
                    cipher_word += i
                else:
                    cipher_word += cipher_letters[i]

        return cipher_word


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        # inheritance from parent class Message
        Message.__init__(self, text)
        self.shift = shift
        self.get_encryption_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)

        

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.get_encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, new_shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        print('"', self.message_text, '"', 'has been shifted from', self.shift, 'to', new_shift)
        self.shift = new_shift


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)


    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        max_count_of_real_words = 0
        word_using_max_shift = ''
        best_shift = 0

        for s in range(1,26): # iterate through possible shifts
            word = self.apply_shift(s)
            count_real_words = len([j for j in word.split() if is_word(self.valid_words, j) == True])

            if count_real_words > max_count_of_real_words: 
                # if best number is found, best_shift value stays the same unless another value is GREATER.
                max_count_of_real_words = count_real_words
                word_using_max_shift = word
                best_shift = s
        
        return (best_shift, word_using_max_shift)
        

if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
    # plaintext = PlaintextMessage('hello', 2)
    # print('Expected Output: jgnnq')
    # print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
    # ciphertext = CiphertextMessage('jgnnq')
    # print('Expected Output:', (24, 'hello'))
    # print('Actual Output:', ciphertext.decrypt_message())

    # mycipher = CiphertextMessage('Lipps, Asvph!')
    # print('Expected Output:', (22, 'Hello, World!'))
    # print('Actual Output:', mycipher.decrypt_message())

    
    # test = PlaintextMessage('Hello, World!', 4)
    # print(PlaintextMessage.get_message_text_encrypted(test))
    # print(test.get_message_text())
    

    #TODO: best shift value and unencrypted story 
    my_story = CiphertextMessage(get_story_string())
    print(my_story.get_message_text())
    print('Actual Output:', my_story.decrypt_message())
    
    
    
