import ak_HTML as html
from pprint import pprint

class BasicBlock():
    '''Абстарктный класс для блоков. Чтения из файла описания и генерация HTML'''

    BlockName = ''  # Имя блока
    OnlyOne = False#Признак, что блок в списке может быть только 1

    def __init__(self, **kwargs):
        self.Parser = kwargs.get('Parser', None)
        self.SetListParamName('Name')#Список имен параметров
        self.Strings = []#Список строк текста
        self.CountStrings = -1#Читаем все строки текста
        self._Page = None# Страница

    def SetListParamName(self, *args):
        '''Добавляем параметры в блок'''
        l = []

        for v in args:
            l.append(v)

        self.ListParamName = l
        self.Param = {k:'' for k in l}#Словарь параметров

    def Parse(self, Strings):
        self.ReadInParamAllBlocks(Strings)

        self.ReadInStringsText(Strings, self.CountStrings)

    def ReadInStringsText(self, Strings, CountStrings=-1):
        '''Читаем строки в Strings'''

        count = 1000 if CountStrings == -1 else CountStrings

        while 0 < count and 0 < len(Strings) and not self.Parser.IsBlock(Strings[0]):
            self.AppendPopStringInStrings(Strings)
            count-=1

    def AppendPopStringInStrings(self, Strings):
        '''Снимает строку 0ю строку из Strings и добавляем в Strings объекта'''
        s = Strings.pop(0).strip()
        self.Strings.append(s)

    def ReadInParamAllBlocks(self, Strings):
        '''Читаем блоки в параметры'''
        i = 0

        while 0 < len(Strings) and i < len(self.ListParamName):
            if not self.Parser.IsBlock(Strings[0]):
                break
            self.InsertPopStringInParam(i, Strings)
            i += 1

    def InsertPopStringInParam(self, NumberParam, Strings):
        '''Снимает 0ю строку из Strings и вставляем в параметром в Param'''
        s = self.Parser.GetBlockText(Strings.pop(0))
        ParamName = self.ListParamName[NumberParam]
        self.Param[ParamName] = s

    def GetHTML(self):
        '''Возвращаем HTML блока'''
        return ''

    def GetResult(self):
        '''Возвращает словарь для создания HTML'''
        pass

    def TextStrings(self):
        '''Возвращаем текст из строчек Strings'''

        return '\n'.join(self.Strings)

    def SetTextStrings(self, text):
        '''Устанавливаем текст Strings'''
        self.Strings = [text]

    def TextParam(self):
        '''Возвращаем текст из строчек Param'''

        l = []
        for s in self.ListParamName:
            l.append(self.Param[s])

        return '\n'.join(l)

#     Свойства
    @property
    def Page(self):
        '''Свойство страница'''
        return self._Page

    @Page.setter
    def Page(self, Value):
        '''Сеттер для установки страницы и настроек из страницы'''
        self._Page = Value


class BlockError(BasicBlock):
    '''Класс Ошибка'''
    BlockName = 'ОШИБКА'

    def __init__(self, Parser):
        super().__init__(Parser)
        self.SetListParamName()#Список имен параметров пуст

    def Parse(self, Strings):
        '''Поглощаем весь блок'''
        i = 0
        while 0 < len(Strings) and self.Parser.IsBlock(Strings[0]):
            self.ListParamName.append(str(i))
            self.Param[str(i)] = ''
            self.InsertPopStringInParam(i, Strings)
            i+=1

    def GetHTML(self):
        '''Возвращаем HTML блока'''

        ls = list(filter(lambda s: s!='', [self.TextParam(), self.TextStrings()]))
        text = '\n'.join(ls)

        propTable = {'border':"1",'width':"100%",'bordercolor':"red"}
        propFont = {'size':"4",'color':"red"}

        return html.TableOneCell(text, propTable, propFont)

class BlockTema(BasicBlock):
    '''Класс Тема. Тема отвечает за заголовок страницы и заголовк окна браузера'''

    BlockName = 'ТЕМА'
    OnlyOne = True # Признак, что блок в списке может быть только 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SetListParamName('Name')
        self.CountStrings = 1  # Читаем 1 строку

    def GetHTML(self):
        '''Возвращаем HTML блока'''

        return '<center><H2>' + self.TextStrings() + '</H2></center>'

class BlockText(BasicBlock):
    '''Класс Текст. Текст отображает простой текст(тег PRE)'''

    BlockName = 'ТЕКСТ'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def GetResult(self):
        '''Возвращает словарь для создания HTML'''

        return {'Text': self.TextStrings()}

    def GetHTML(self):
        '''Возвращаем HTML блока'''

        result = [self.GetResult()]
        html.Tag(result, 'Pre')
        paramFont = {'size': '4'}
        result = html.Tag(result, 'font', paramFont, True)

        return result

class BlockTitle(BasicBlock):
    '''Класс Заголовок. Заголовок создает заголовок для списка на странице'''

    BlockName = 'ЗАГОЛОВОК'

    def __init__(self, Parser):
        super().__init__(Parser)
        self.CountStrings = 1  # Читаем 1 строку

    def GetHTML(self):
        '''Возвращаем HTML блока'''
        result = self.TextStrings()

        if 'id' in self.Param:
            result = html.Tag(result, 'a', {'id': self.Param['id']})

        result = html.Tag(result, 'h3')

        return result

class BlockCode(BasicBlock):
    '''Класс Код. Код отображает раскрашенный код'''

    BlockName = 'КОД'
    def __init__(self, Parser):
        super().__init__(Parser)
        self.SetListParamName('Name', 'TypeCode')

    def GetHTML(self):
        '''Возвращаем HTML блока'''
        result = html.Tag(self.TextStrings(), 'Pre')
        result = html.Tag(result, 'font', {'size':"4", 'face':"Courier New"})
        result = html.TableOneCell(result, {'border':"1",'width':"100%"}, {})

        return result

class BlockMarker(BasicBlock):
    '''Класс Маркер. Маркер устанавливает признак блока, по умолчанию ++'''

    BlockName = 'МАРКЕР'
    def __init__(self, Parser):
        super().__init__(Parser)
        self.SetListParamName('Name', 'Marker')
        self.CountStrings = 0  # Не читаем текст

    def Parse(self, Strings):
        super().Parse(Strings)
        NewMarker = self.Param['Marker']
        self.Parser.SetMarker(NewMarker)

class BlockMetka(BasicBlock):
    '''Класс Метка. Метка опредляет метки страницы как доп характеристику. Например: СКД.Параметры'''

    BlockName = 'МЕТКА'
    OnlyOne = True#Признак, что блок в списке может быть только 1

    def __init__(self, Parser):
        super().__init__(Parser)
        self.SetListParamName('Name', 'Metka')
        self.CountStrings = 0  # Не читаем текст

    def GetHTML(self):
        '''Возвращаем HTML блока'''

        return '<font color="blue" size="2">' + self.Param['Metka'] + '</font>'

class BlockLinkToDir(BasicBlock):
    '''Класс Ссылка на каталог . Делаем гипер ссылку на каталог с описанием'''
    BlockName = 'ССЫЛКАНАКАТАЛОГ'
    OnlyOne = True#Признак, что блок в списке может быть только 1

    def __init__(self, FileName):
        self.FileName = FileName # Путь к каталогу описания

    def GetHTML(self):
        '''Возвращаем HTML блока'''

        ls = [self.FileName]
        ls = html.Tag(ls, 'a', {'href':'g', 'id':'id_LinkToDir'})

        template = '\n'.join(["<script>",
        "var link;",
        "link = document.getElementById('id_LinkToDir');",
        "link.onclick = function() {",
	    "window.open('myproto://{0}');".format(self.FileName),
	    "return false;}",
	    "</script>"
        ]).replace('\\','/')

        return '\n'.join(ls) + template

class BlockPageTableOfContents(BasicBlock):
    '''Класс Оглавление. Оглавление страницы строиться из блоков заголовков'''

    BlockName = 'ОГЛАВЛЕНИЕСТРАНИЦЫ'
    OnlyOne = True#Признак, что блок в списке может быть только 1

    def __init__(self, ListBlock):
        super().__init__(None)
        self.ListBlockTitle = list(filter(lambda Block: Block.BlockName == 'ЗАГОЛОВОК', ListBlock))

    def GetListContents(self):
        '''Строим список оглавление страницы'''
        result = []
        id = 0
        for Block in self.ListBlockTitle:
            title = Block.TextStrings()
            if title != '':
                id_val = 'id_' + str(id)
                s = html.Tag(title, 'a', {'href':'#' + id_val})
                Block.Param['id'] = id_val
                result.append(s)
                id+=1

        return result

    def GetHTML(self):
        '''Возвращаем HTML блока'''

        ListContent = self.GetListContents()

        if len(ListContent) == 0:
            result = ''
        else:
            result = html.ListHTML(ListContent)

        return result

class BlockMainPageTableOfContents(BasicBlock):
    '''Класс Оглавление главной страницы. Оглавление страницы строиться из списка словарей'''

    BlockName = 'ОГЛАВЛЕНИЕГЛАВНОЙСТРАНИЦЫ'
    OnlyOne = True#Признак, что блок в списке может быть только 1

    def __init__(self, dickPageTableOfContents):
        super().__init__(None)
        self.dickPageTableOfContents = dickPageTableOfContents

    def GetListContents(self, listPageTableOfContents):
        '''Строим список оглавление главной страницы'''
        result = []

        for elem in listPageTableOfContents:
            if 'href' in elem:
                d = {'href': elem['href']}
                s = html.Tag(elem['Text'], 'a', d)
                result.append(s)
            else:
                value = html.Tag(elem['Text'], 'a', {'id': elem['id']}) if 'id' in elem else elem['Text']
                result.append(value)
                result.append(self.GetListContents(elem['list']))

        return result

    def GetHTML(self):
        '''Возвращаем HTML блока'''

        if'list' in self.dickPageTableOfContents:
            ListContent = self.GetListContents(self.dickPageTableOfContents['list'])
            if len(ListContent) == 0:
                result = CreateBlockError('Не найдены файлы описания').GetHTML()
            else:
                result = html.ListHTML(ListContent)
        else:
            result = CreateBlockError('В корне источника сайта содержиться файл описания').GetHTML()

        return result

class BlockMainPageShortTableOfContents(BasicBlock):
    '''Класс короткое Оглавление главной страницы. Оглавление страницы строиться из списка словарей'''

    BlockName = 'КОРОТКОЕОГЛАВЛЕНИЕГЛАВНОЙСТРАНИЦЫ'

    def __init__(self, dickPageTableOfContents):
        super().__init__(None)
        self.dickPageTableOfContents = dickPageTableOfContents

    def GetListContents(self, listPageTableOfContents):
        '''Строим список короткое оглавление главной страницы'''
        result = []

        i = 0
        for elem in listPageTableOfContents:
            if not 'href' in elem:
                href = 'idPage_' + str(i)
                elem['id'] = href # Идентификатор на пункт меню
                teg = html.Tag(elem['Text'], 'a', {'href': '#' + href})
                result.append(teg)
                i += 1

        return result

    def GetHTML(self):
        '''Возвращаем HTML блока'''

        if'list' in self.dickPageTableOfContents:
            ListContent = self.GetListContents(self.dickPageTableOfContents['list'])

            if len(ListContent) == 0:
                result = CreateBlockError('Не найдены файлы описания').GetHTML()
            else:
                result = html.ListHTML(ListContent)
        else:
            result = CreateBlockError('В корне источника сайта содержиться файл описания').GetHTML()

        return result

class BlockHyperLink(BasicBlock):
    '''Класс гипер ссылка. Предназначен для вставки гипер ссылки'''

    BlockName = 'ССЫЛКА'

    def __init__(self, Parser):
        super().__init__(Parser)
        self.CountStrings = 2  # Читаем две строки текста. 1я текст, 2я Сама гипер ссылка

    def GetHTML(self):
        '''Возвращаем HTML блока'''

        result = html.Tag_HyperLinck(self.Strings[0], self.Strings[1])

        return result

class BlockImage(BasicBlock):
    '''Класс картинка. Предназначен для вставки картинки'''

    BlockName = 'КАРТИНКА'

    def __init__(self, Parser):
        super().__init__(Parser)
        self.CountStrings = 1  # Читаем 1 строкe текста. Это путь к картинке

    def GetHTML(self):
        '''Возвращаем HTML блока'''

        result = html.TagPart('br') + html.Tag_Image(self.TextStrings())

        return result

class BlockLinkOnParentPage(BasicBlock):
    '''Класс гипер ссылка на страницу сайта. Предназначен для вставки ссылки на страницу родитель'''

    BlockName = 'ССЫЛКАСТРАНИЦАРОДИТЕЛЬ'
    OnlyOne = True#Признак, что блок в списке может быть только 1

    def __init__(self, hrefParentPage,  Text):
        super().__init__(None)
        self.SetListParamName('hrefParentPage', 'text')#Список имен параметров
        self.Param['hrefParentPage'] = hrefParentPage
        self.Param['text'] = Text

    def GetHTML(self):
        '''Возвращаем HTML блока'''

        result = html.Tag_HyperLinck(self.Param['text'], self.Param['hrefParentPage'], False) + html.Tag_hr()

        return result

def ListBlockClass():
    result = [BlockTema, BlockText, BlockTitle, BlockCode, BlockMarker, BlockMetka, BlockHyperLink, BlockImage]

    return result

def PrintListBlockClass(fSort=None):
    result = [BlockTema, BlockText, BlockTitle, BlockCode, BlockMarker, BlockMetka,BlockError,BlockLinkToDir,
              BlockPageTableOfContents,BlockMainPageTableOfContents,BlockMainPageShortTableOfContents,
              BlockLinkOnParentPage]
    if not fSort is None:
        result.sort(key=fSort)

    pprint([str(Block.Sort) + ': ' + Block.BlockName for Block in result])

def CreateBlockError(TextError):
    '''Создает  объект блок ошибка с текстом. Используется для вывода ошибки на страницу'''
    result = BlockError(None)
    result.SetTextStrings(TextError)

    return result

if __name__ == '__main__':
   fSort = lambda Block: 1000 if Block.Sort == -1 else Block.Sort
   PrintListBlockClass(fSort)
