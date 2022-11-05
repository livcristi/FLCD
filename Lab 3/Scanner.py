import re

from PIF import PIF
from ST import ST


class Scanner:
    def __init__(self):
        self.__id_table = ST()
        self.__const_table = ST()
        self.__pif = PIF()

        self.__lexical_errors = []
        self.__line_counter = 0

        # Read the list of tokens
        with open('tokens.txt') as f_inp:
            self.__keywords = {line.strip() for line in f_inp.readlines()}

    def scan_file(self, filename):
        self.__refresh_attributes()

        # Read the content of the given file
        with open(filename) as inp_file:
            program = "\n".join([line.strip() for line in inp_file.readlines()])

        while len(program) > 0:
            # Get the current token
            current_token, program = self.__extract_token(program)

            # Skip blank characters
            if self.__check_space(current_token) or len(current_token) == 0:
                continue

            if current_token in self.__keywords:
                # Add the token to the pif, if it is a keyword
                self.__pif.add_token(current_token, -1)
            elif self.__check_constant(current_token):
                # Add the token to the st table, then pif, if it is a constant
                st_position = self.__const_table.get_token_position(current_token)
                self.__pif.add_token('const', st_position)
            elif self.__check_identifier(current_token):
                # Add the token to the st table, then pif, if it is a constant
                st_position = self.__id_table.get_token_position(current_token)
                self.__pif.add_token('id', st_position)
            else:
                # If the token is not a keyword, nor identifier/constant, then it is a lexical error
                self.__lexical_errors.append('Lexical error on line {} on token {}'.format(self.__line_counter, current_token))

        # Print the answer
        if len(self.__lexical_errors) == 0:
            print('The source code is lexically correct')
        else:
            print('The source code contains {} lexical errors: '.format(len(self.__lexical_errors)))
            for lexical_error in self.__lexical_errors:
                print(lexical_error)

        # Write results to file
        self.__write_results_to_file(filename)

        # Return the pif
        return self.__pif.get_tokens(), self.__id_table.get_elements(), self.__const_table.get_elements()

    # Getters for the symbol tables and PIF
    def get_id_table(self):
        return self.__id_table.get_elements()

    def get_const_table(self):
        return self.__const_table.get_elements()

    def get_pif(self):
        return self.__pif.get_tokens()
    
    def __extract_token(self, program_text):
        current_token = ''
        while len(program_text) > 0:
            # Get the next character from the text
            current_character = program_text[0]
            program_text = program_text[1:]

            if not self.__check_in_alphabet(current_character):
                # If the character is not in the alphabet, save the lexical error and stop the extraction
                self.__lexical_errors.append('Lexical error on line {}, illegal character {}'.format(self.__line_counter, current_character))
                break
            elif self.__check_space(current_character):
                # If the character is a space, ignore it. But memorise the number of newlines (used for debugging)
                if current_character == '\n':
                    self.__line_counter += 1
                break
            elif self.__check_separator(current_character) and len(current_token) > 0:
                # If the current character is a separator, place it back in the text (it the current token already
                # has other characters)
                program_text = current_character + program_text
                break
            elif self.__check_separator(current_character):
                # If the character is a separator, return it
                current_token += current_character
                break
            current_token += current_character

        # Check if the token is a condition
        condition_tokens = list(filter(None, re.split('(<=|>=|!=|==|<-|<|>)', current_token)))
        if len(condition_tokens) > 1:
            program_text = "".join(condition_tokens[1:]) + program_text
            return condition_tokens[0], program_text
        return current_token, program_text

    def __refresh_attributes(self):
        self.__id_table = ST()
        self.__const_table = ST()
        self.__pif = PIF()
        self.__lexical_errors = []
        self.__line_counter = 1

    def __write_results_to_file(self, filename):
        # Write the symbol table and pif results in files
        with open('st_id_' + filename, 'w') as st_file:
            st_file.write(''.join(str(column).ljust(16) for column in ['Identifier', 'Symbol Table Id']) + "\n")
            for row in self.get_id_table():
                st_file.write(''.join(str(column).ljust(16) for column in row) + "\n")
        with open('st_const_' + filename, 'w') as st_file:
            st_file.write(''.join(str(column).ljust(16) for column in ['Constant', 'Symbol Table Id']) + "\n")
            for row in self.get_const_table():
                st_file.write(''.join(str(column).ljust(16) for column in row) + "\n")
        with open('pif_' + filename, 'w') as pif_file:
            pif_file.write(''.join(str(column).ljust(10) for column in ['Token', 'Id']) + "\n")
            for row in self.get_pif():
                pif_file.write(''.join(str(column).ljust(10) for column in row) + "\n")

    @staticmethod
    def __check_in_alphabet(character):
        # Check if a character is in the allowed alphabet
        return re.match('[a-zA-Z0-9/*\-+(){}\[\];\'\"!<=>_ \n\t]', character)

    @staticmethod
    def __check_separator(token):
        return token in ['{', '}', '(', ')', '[', ']', ';']

    @staticmethod
    def __check_space(token):
        return token in [' ', '\n', '\t']

    @staticmethod
    def __check_identifier(token):
        # Check if the token is a valid identifier
        return re.fullmatch("[a-zA-Z][a-zA-Z0-9_]*", token)

    @staticmethod
    def __check_constant(token):
        # Check if the token is an integer or float or boolean or character or string
        return re.fullmatch("0|([+-]?[1-9][0-9]*)", token) or re.fullmatch("0|([+-]?[1-9][0-9]*)(\.([0-9]+))?", token) \
               or re.fullmatch("(TRUE)|(FALSE)", token) or re.fullmatch("'[a-zA-Z0-9_+\-*/:]'", token) \
               or re.fullmatch('"[a-zA-Z0-9_+\-*/:]*"', token)
