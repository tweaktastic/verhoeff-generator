class ValidationError(Exception):
    """Top-level error for validating numbers.
    This exception should normally not be raised, only subclasses of this
    exception."""

    def __str__(self):
        return ''.join(self.args[:1]) or getattr(self, 'message', '')


class InvalidFormat(ValidationError):
    """Something is wrong with the format of the number.
    This generally means characters or delimiters that are not allowed are
    part of the number or required parts are missing."""

    message = 'The number has an invalid format.'


class InvalidChecksum(ValidationError):
    """The number's internal checksum or check digit does not match."""

    message = "The number's checksum or check digit is invalid."


class Verhoeff:
    def __init__(self):
        """
            Intialize the multiplication and permutation table
        """
        self._d_table = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
            [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
            [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
            [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
            [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
            [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
            [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
            [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
            [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        ]

        self._p_table = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
            [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
            [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
            [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
            [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
            [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
            [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
        ]

    def checksum(self, num):
        """ Cacluate Verhoeff checksum for the given number
            returns:- int
            Valid Verhoeff number has checksum of 0
        """
        reverse_str = reversed(str(num))
        number = [n for n in reverse_str]
        c = 0
        for i, n in enumerate(number):
            c = self._d_table[c][self._p_table[i%8][int(n)]]
        return c

    def validate(self, num):
        """
            Checks wheather the number passes Verhoeff Checksum
            returns number if valid
            raises exception if not valid
        """
        if not bool(num):
            raise InvalidFormat()
        check = 0
        try:
            valid_verhoeff = (self.checksum(num) == check)
        except Exception:
            raise InvalidFormat()
        if not valid_verhoeff:
            raise InvalidChecksum()
        return num

    def calc_checksum(self, num):
        """
            For the given number, this function generates the
            extra number that needs to be appended to make is pass
            Verhoeff checksum
        """
        return self._d_table[self.checksum(str(num) + '0')].index(0)

    def generate(self, num):
        """
            Generates Verhoeff number for the given number
            Appends an extra number to the existing number
            and returns valid Verhoeff number of len n+1
        """
        return int(str(num) + str(self.calc_checksum(num)))
