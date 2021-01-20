import unittest

from parse import outputing
from parse import pretty_printing

class Tests1(unittest.TestCase):
    def test1(self):
        read_file = open('tests/test1.txt', 'r')
        text = read_file.read()
        read_file.close()
        result = outputing(text)
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
        result = outputing(text)
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
        result = outputing(text)
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
        result = outputing(text)
        read_file = open('tests/res4.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(str(result), answer)

        pretty_print = pretty_printing(result)
        read_file = open('tests/prettyprinting4.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(pretty_print, answer)

    def test5(self):
        read_file = open('tests/test5.txt', 'r')
        text = read_file.read()
        read_file.close()
        result = outputing(text)
        read_file = open('tests/res5.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(str(result), answer)

        pretty_print = pretty_printing(result)
        read_file = open('tests/prettyprinting5.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(pretty_print, answer)

    def test6(self):
        read_file = open('tests/test6.txt', 'r')
        text = read_file.read()
        read_file.close()
        result = outputing(text)
        read_file = open('tests/res6.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(str(result), answer)

        pretty_print = pretty_printing(result)
        read_file = open('tests/prettyprinting6.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(pretty_print, answer)

    def test7(self):
        read_file = open('tests/test7.txt', 'r')
        text = read_file.read()
        read_file.close()
        result = outputing(text)
        read_file = open('tests/res7.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(str(result), answer)

        pretty_print = pretty_printing(result)
        read_file = open('tests/prettyprinting7.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(pretty_print, answer)

    def test8(self):
        read_file = open('tests/test8.txt', 'r')
        text = read_file.read()
        read_file.close()
        result = outputing(text)
        read_file = open('tests/res8.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(str(result), answer)

        pretty_print = pretty_printing(result)
        read_file = open('tests/prettyprinting8.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(pretty_print, answer)

    def test9(self):
        read_file = open('tests/test9.txt', 'r')
        text = read_file.read()
        read_file.close()
        result = outputing(text)
        read_file = open('tests/res9.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(str(result), answer)

        pretty_print = pretty_printing(result)
        read_file = open('tests/prettyprinting9.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(pretty_print, answer)

    def test10(self):
        read_file = open('tests/test10.txt', 'r')
        text = read_file.read()
        read_file.close()
        result = outputing(text)
        read_file = open('tests/res10.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(str(result), answer)

        pretty_print = pretty_printing(result)
        read_file = open('tests/prettyprinting10.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(pretty_print, answer)

    def test11(self):
        read_file = open('tests/test11.txt', 'r')
        text = read_file.read()
        read_file.close()
        result = outputing(text)
        read_file = open('tests/res11.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(str(result), answer)

        pretty_print = pretty_printing(result)
        read_file = open('tests/prettyprinting11.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(pretty_print, answer)

    def test12(self):
        read_file = open('tests/test12.txt', 'r')
        text = read_file.read()
        read_file.close()
        result = outputing(text)
        read_file = open('tests/res12.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(str(result), answer)

        pretty_print = pretty_printing(result)
        read_file = open('tests/prettyprinting12.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(pretty_print, answer)

if __name__ == '__main__':
    unittest.main()
