
def textToTextForTest(text):
    '''Преобразует текст в текст для тестирования. Заменяет пробелы не "_", убирает ентер, таб.'''
    result = text.strip()

    while result.count('  ') != 0:
        result = result.replace('  ', ' ')

    result = result.replace(' ', '_')
    result = result.replace('\n', '')
    result = result.replace('\t', '_')
    result = result.upper()

    return result


if __name__ == '__main__':
    text = '''
     qwe    QWE
            asd
    '''

    print(textToTextForTest(text))