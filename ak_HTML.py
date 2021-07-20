
import ak_WorkFiles as WorkFiles


'''Модуль для работы с HTML'''

def TagPart(tag, isOpen=True, dickParam={}):
    '''оздаем часть HTML тега'''
    if isOpen:
        l = []
        for k,v in dickParam.items():
            l.append(k + '="{0}"'.format(v))
        s = '' if len(l) == 0 else ' '
        result = '<{0}{1}{2}>'.format(tag, s, ' '.join(l))
    else:
        result = '</{0}>'.format(tag)

    return result

def Tag(Strings, tag, dickParam={}, ToString=False):
    '''Обрамляем тегом Список или строку'''
    if isinstance(Strings, list):
        Strings.insert(0, TagPart(tag, True, dickParam))
        Strings.append(TagPart(tag, False))
        result = Strings

        if ToString:
            result = ''.join(result)
    else:
        result = TagPart(tag, True, dickParam) + Strings + TagPart(tag, False)

    return result

def TableOneCell(text, dickParamTable, dickParamFonf):
    '''Создадим таблицу с 1й ячейкой'''

    l = [text]
    Tag(l, 'pre')
    if len(dickParamFonf) != 0:
        Tag(l, 'font', dickParamFonf)
    Tag(l, 'td')
    Tag(l, 'tr')
    Tag(l, 'Table', dickParamTable)

    return '\n'.join(l)

def ListHTML(listContents):
        '''Создадим HTML список из списка'''

        ls = []
        for elem in listContents:
            if isinstance(elem, list):
                ls.append(ListHTML(elem))
            else:
                # elem = Tag(elem['text'], 'a', {'href': elem['href']})
                elem = Tag(elem, 'li')
                ls.append(elem)

        ls = Tag(ls, 'ul')

        return '\n'.join(ls)

def Tag_HyperLinck(Strind, linck, OpenInNewWindow=True, **OtherParam):
    '''Создаем тег гипер ссылка'''

    d = {'href':linck}

    if OpenInNewWindow:
        d['target'] = '_blank'

    return Tag(Strind, 'a', d)

def Tag_Image(FileName, **OtherParam):
    '''Создаем тег картинка'''

    if WorkFiles.isLinckFile(FileName):
        FullFileName = WorkFiles.LinkToHTMLFile(FileName)
    else:
        FullFileName = FileName

    d = {'src':FullFileName}

    return TagPart('img', True, d)

def Tag_hr():
    '''Тег Горизонтальная линия'''

    return TagPart('hr')


def Tag_br():
    '''Тег Перевод строки'''

    return TagPart('br')


if __name__ == '__main__':
    # print(TagPart('a', True, {'href': '11'}))
    # print(Tag('q', 'a', {'href': '11'}))
    # print(TableOneCell('test', {'border':"1",'width':"100%",'bordercolor':"red"}, {'size':"4",'color':"red"}))

    print(ListHTML(['qwe', 'asd', 'zxc']))