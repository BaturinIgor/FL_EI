import unittest

from parse import outputing_tests
from parse import pretty_printing

class Tests1(unittest.TestCase):
    def test1(self):
        read_file = open('tests/test1.txt', 'r')
        text = read_file.read()
        read_file.close()
        result = outputing_tests(text)
        read_file = open('tests/res1.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(str(result), answer)

        pretty_print = pretty_printing(result)
        read_file = open('tests/prettyprinting1.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(pretty_print, answer)

    def test2(self):
        read_file = open('tests/test2.txt', 'r')
        text = read_file.read()
        read_file.close()
        result = outputing_tests(text)
        read_file = open('tests/res2.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(str(result), answer)

        pretty_print = pretty_printing(result)
        read_file = open('tests/prettyprinting2.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(pretty_print, answer)

    def test3(self):
        read_file = open('tests/test3.txt', 'r')
        text = read_file.read()
        read_file.close()
        result = outputing_tests(text)
        read_file = open('tests/res3.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(str(result), answer)

        pretty_print = pretty_printing(result)
        read_file = open('tests/prettyprinting3.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(pretty_print, answer)
    
    def test4(self):
        read_file = open('tests/test4.txt', 'r')
        text = read_file.read()
        read_file.close()
        result = outputing_tests(text)
        read_file = open('tests/res4.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(str(result), answer)

        pretty_print = pretty_printing(result)
        read_file = open('tests/prettyprinting4.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(pretty_print, answer)

if __name__ == '__main__':
    unittest.main()
