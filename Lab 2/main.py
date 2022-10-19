import random

from ST import ST

if __name__ == '__main__':
    st_test = ST()

    # Add some values in the ST
    val_1 = st_test.get_token_position("abc")
    val_2 = st_test.get_token_position(31231)
    val_3 = st_test.get_token_position("131")
    val_4 = st_test.get_token_position("abc")
    val_5 = st_test.get_token_position("""turtle""")

    # Assert that they are in the right positions
    assert val_1 == 0
    assert val_2 == 1
    assert val_3 == 2
    assert val_4 == 0
    assert val_5 == 3
