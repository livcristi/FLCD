class ST:
    __resize_factor = 0.8
    __rolling_hash_factor = 31

    def __init__(self):
        self.__no_buckets = 71
        self.__no_elements = 0
        self.__hash_table = [[] for _ in range(self.__no_buckets)]

    def get_token_position(self, token):
        # Try to search the token in the table
        position = self.__search_token(token)

        if position is not None:
            return position

        # Resize the hash table, if the fill ratio is greater than the resize factor
        if (self.__no_elements / self.__no_buckets - ST.__resize_factor) > 0:
            self.__resize()

        # Add the token and return its position
        return self.__add_token(token)

    def __search_token(self, token):
        hash_value = self.__hash_token(token)

        # Search the token value in its bucket
        for (token_value, position) in self.__hash_table[hash_value]:
            if token_value == token:
                return position

        return None

    def __add_token(self, token):
        hash_value = self.__hash_token(token)
        position = self.__no_elements

        self.__hash_table[hash_value].append((token, position))
        self.__no_elements += 1

        return position

    def __hash_token(self, token):
        hash_value = 0

        # Convert the token to a string
        token = str(token)
        factor = 1

        # Use rolling hash on the token
        for character in token:
            hash_value = (hash_value + factor * ord(character)) % self.__no_buckets
            factor = (factor * ST.__rolling_hash_factor) % self.__no_buckets

        return hash_value

    def __resize(self):
        self.__no_buckets = self.__no_buckets * 2 + 1

        new_hash_table = [[] for _ in range(self.__no_buckets)]

        for bucket in self.__hash_table:
            for (token_value, position) in bucket:
                hash_value = self.__hash_token(token_value)
                new_hash_table[hash_value].append((token_value, position))

        self.__hash_table = new_hash_table
