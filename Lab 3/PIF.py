
class PIF:

    def __init__(self):
        self.__token_list = []

    def add_token(self, token, value):
        # Add the pair (token, value) to the PIF list of tokens
        self.__token_list.append((token, value))

    def get_tokens(self):
        return self.__token_list

    def __str__(self):
        return str(self.__token_list)
