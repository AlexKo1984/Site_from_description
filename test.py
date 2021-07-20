from abc import ABCMeta, abstractmethod

class TestABC(metaclass=ABCMeta):
    def __init__(self, text):
        print('__init__:', text)
        self.text = text + 't'

    def SimpleTest(self, text):
        print('SimpleTest:', text)

    @abstractmethod
    def ABCTest(self, text):
        print('ABCTest:', text)


class Test(TestABC):
    Name = 'Test'

    def __init__(self, text):
        super().__init__(text)
        print('Test.__init__:', text)
        # self.text = text
        self._myProp = 'This my prop attribute'

    def ABCTest(self, text):
        print('Test.ABCTest:', text)

    def SimpleTest(self, text):
        super().SimpleTest(text)
        print('Test.SimpleTest:', text)

    @property
    def myProp(self):
        return self._myProp

    @myProp.setter
    def myProp(self, value):
        self._myProp = value


if __name__ == '__main__':
    o = Test('qq')
    print(o.myProp)

    o.myProp = 'qqq'

    print(o.myProp)

    # o.ABCTest('e')
    # o.SimpleTest('w')
    # print('text:', o.text)
    # print('Class:', Test.Name)
    # print('Object:', o.Name)