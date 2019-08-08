if __name__ == '__main__':
    """
        By default, python strings are also immutable.
        Which makes direct string manipulation impossible
    """
    first_string = "ab"

    """
        One solution to this is to first convert the string into a list
    """
    second_string = list(first_string)

    """
        Then change it and then convert it back into a string
        and since the type conversion process has to make
        copies along the way. We don't have tow orry about the
        possibility of referencing occuring.
    """

    second_string[0] = 'b'
    second_string = "".join(second_string)

    print "\nstring assignment example"
    print "second_string =", second_string, "first_string =", first_string
