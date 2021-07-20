import ak_Blocks as Blocks
import ak_WorkFiles as WorkFiles

class ParserDescriptionFile:
    """Парсит файл описания и создает список блоков(объекты) для генерации html страницы"""

    def __init__(self, ListBlockClass, OnlyTextClass = None, ErrorBlockClass = None):
        """DictBlockClass: Словарь ключь - имя блока, значение - класс блока"""
        self.SetMarker('++')
        self.DictBlockClass = {k.BlockName : k for k in ListBlockClass}
        self.ListBlock = []
        self.OnlyTextClass = OnlyTextClass
        self.ErrorBlockClass = ErrorBlockClass

    def AddBlock(self, Block):
        '''Добавляем блок в список блоков'''
        self.ListBlock.append(Block)

    def SetMarker(self, Text):
        '''станавливаем маркер для блоков'''
        self.Marker = Text  # Маркер, который определяет блок
        self.MarkerOffSet = len(self.Marker)  # Длина маркера

    def IsBlock(self, s):
        """Проверка блок это или текст"""
        # print(s)
        return s.startswith(self.Marker)

    def GetBlockText(self, s):
        '''Извлекает текст блока или пустую строку'''
        return s[self.MarkerOffSet:].strip()

    def GetBlockName(self, s):
        '''Извлекает имя блока или пустую строку'''
        return self.GetBlockText(s).upper()

    def CreateBlockObject(self, BlockName, Strigs):
        c = self.DictBlockClass.get(BlockName, self.ErrorBlockClass)
        obj = c(self)
        obj.Parse(Strigs)

        return obj

    def ParseFile(self, FileName):
        """Парсим файл описания"""
        limit = 1000
        self.FileName = FileName

        with open(FileName, 'r', encoding="utf-8") as f:
            Strigs = f.readlines()
            while 0 < len(Strigs):
                if limit == 0:
                    break
                limit -= 1
                # s = Strigs.pop(0)
                # print(s)
                s = Strigs[0]
                if self.IsBlock(s):
                    BlockName = self.GetBlockName(s)
                    self.AddBlock(self.CreateBlockObject(BlockName, Strigs))
                else:
                    BlockName = 'ТЕКСТ'
                    self.AddBlock(self.CreateBlockObject(BlockName, Strigs))

class PageMaker:
    '''Создаем HTML страницу'''

    def __init__(self, **kwargs):
        self.TextPage = ''#Текст HTML страницы
        self.TemplatePage = kwargs.get('TemplatePage', '')# Шаблон HTML страницы
        self.Title = kwargs.get('Title', '')#Заголовок страницы
        self.PathSource = kwargs.get('PathSource', '') # Путь к каталогу с описанием
        self._Site = None # Сайт
        self._Settings = None # Настройки страницы
        self.ListBlock = kwargs.get('ListBlock', [])

    def SavePage(self, FileName):
        '''Сохраним HTML страницу на диск'''

        f = open(FileName, 'w')
        f.write(self.TextPage)
        f.close()

    def GetTitlePage(self):
        '''Ищем блок ТЕМА и берем от туда текст,
        если не найдем то заголовок это имя файла описания,
        иначе пустая строка'''

        if self.Title == '':
            result = ''
            for Block in self.ListBlock:
                if Block.BlockName == 'ТЕМА':
                    result = Block.TextStrings()
                    break

            if result == '':
                result = WorkFiles.GetParamFileFromPath(self.PathSource)['Name']
        else:
            result = self.Title

        return result

    def Make(self):
        '''Создадим HTML страницы'''
        self.Title = self.GetTitlePage(self.ListBlock)

        listTopBlocks = [Blocks.BlockLinkOnParentPage,# Ссылка на главную страницу
                         'br',# линия раздела
                         Blocks.BlockMetka, # Метки страницы
                         Blocks.BlockTema, # Заголовок страницы
                         Blocks.BlockLinkToDir, # Ссылка на каталог страницы
                         Blocks.BlockPageTableOfContents, # Оглавление страницы
                         ]# Верхняя часть страницы. Генерируется на основе блоков из описания
        dictTopBlocks = {}
        listCenterBlock = [] # Средняя часть страницы. Состоит из блоков описания

        # Распределим блоки по частям страницы
        for Block in self.ListBlock:
            if Block.BlockName in dictTopBlocks:
                dictTopBlocks[Block.BlockName] = Block
            else:
                listCenterBlock.append(Block)

        # обработка создания верхней части страницы

        # Создадим блок Оглавления страницы
        dictTopBlocks[Blocks.BlockPageTableOfContents.BlockName] = Blocks.BlockPageTableOfContents(listCenterBlock)

        # Ссылка на каталог описания
        dictTopBlocks[Blocks.BlockLinkToDir.BlockName] = Blocks.BlockLinkToDir(self.PathSource)

        # Ссылка на главную страницу сайта
        if not self.Site is None:
            FileName =  WorkFiles.MakeHTMLFileName('', self.Site.GetNameMainPage())
            dictTopBlocks[Blocks.BlockLinkOnParentPage.BlockName] = Blocks.BlockLinkOnParentPage(FileName, self.Site.GetTitleMainPage())

        text = self.JoinBloksInHTML(listTopBlocks) + '\n' + self.JoinBloksInHTML(listCenterBlock)
        dictParam = {'Body': text, 'Title': self.Title}
        self.TextPage = self.MakeHTMLPageOnTemplate(dictParam)

    def MakeHTMLPageOnTemplate(self, dictParam):
        '''Формируем HTML страницу из частей HTML'''

        self.TextPage = self.TemplatePage

        for k, v in dictParam.items():
            self.TextPage = self.TextPage.replace('{' + k + '}', v)

    def JoinBloksInHTML(self):
        '''Соединим блоки в HTML'''
        ListBody = []

        for Block in self.ListBlock:
            text = Block.GetHTML()
            if text != '':
                ListBody.append(text)

        return '\n'.join(ListBody)

    # def GetBlockLinkMainPage(self):
    #     '''Возвращает блок-ссылку на главную страницу или None'''
    #
    #     if self.Site is None:
    #         result = None
    #     else:
    #         FileName = WorkFiles.MakeHTMLFileName('', self.Site.GetNameMainPage())
    #
    #     return result

# Свойства

    @property
    def Site(self):
        '''Свойство возвращает сайт'''

        return self._Site

    @Site.setter
    def Site(self, Value):
        '''Сеттер свойства сайт'''

        self._Site = Value

class MainPageMaker(PageMaker):
    '''Создаем главную HTML страницу'''

    def __init__(self, PathSource, TemplatePage, dickPageTableOfContents):
        super().__init__(PathSource, TemplatePage)
        self.dickPageTableOfContents = dickPageTableOfContents# Словарь для создания оглавления страницы

    def Make(self):
        '''Создадим HTML страницы'''

        self.ListBlock = []

        # Ссылка на каталог описания
        LinkToDir = Blocks.BlockLinkToDir(self.PathSource)
        self.ListBlock.append(LinkToDir)
        # Короткое оглавление страницы
        block = Blocks.BlockMainPageShortTableOfContents(self.dickPageTableOfContents)
        self.ListBlock.append(block)
        # Оглавление страницы
        block = Blocks.BlockMainPageTableOfContents(self.dickPageTableOfContents)
        self.ListBlock.append(block)

        self.Title = 'Главная страница сайта'
        Tema = Blocks.BlockTema(None)
        Tema.SetTextStrings(self.Title)
        self.ListBlock.append(Tema)

        self.SortBlocks()
        self.JoinBloksInHTML()

class SiteMaker:
    '''Клас для создания сайта'''

    def __init__(self, dictPropertys):
        self.dictPropertys = dictPropertys # астройки создания сайта Путь к шаблону HTMД страницы
        self.TemplatePage = '' # Шаблон HTMД страницы
        self.NumberPage = 0 # Нумератор создаваемых страниц

    def LoadTemplatePage(self):
        FileNameTemplatePage = self.dictPropertys['FileNameTemplatePage']

        with open(FileNameTemplatePage, 'r', encoding="utf-8") as f:
            self.TemplatePage = ''.join(f.readlines())

    def GetNewNumberPage(self):
        self.NumberPage += 1

        return self.NumberPage

    def MakePages(self, dickTree):
        '''Создадим страницы сайта, возвращаем словарь с оглавлением'''

        if 'FileDescription' in dickTree:
            ListBlockClass = Blocks.ListBlockClass()
            Parser = ParserDescriptionFile(ListBlockClass, Blocks.BlockText, Blocks.BlockError)
            FileName = dickTree['FileDescription']
            Parser.ParseFile(FileName)

            Page = PageMaker(dickTree['Path'], self.TemplatePage)
            Page.Site = self
            Page.Make(Parser.ListBlock)
            FileName = WorkFiles.MakeHTMLFileName(self.dictPropertys['PathSite'], str(self.GetNewNumberPage()))
            Page.SavePage(FileName)

            dickPageTableOfContents = {}
            dickPageTableOfContents['Text'] = Page.Title
            dickPageTableOfContents['href'] = WorkFiles.LinkToHTMLFile(FileName)
        else:
            dickPageTableOfContents = {}
            dickPageTableOfContents['Text'] = dickTree['Name']
            ls = []
            dickPageTableOfContents['list'] = ls

            for dickSubTree in dickTree['Dirs']:# list in 'Dirs'
                ls.append(self.MakePages(dickSubTree))

        return dickPageTableOfContents

    def MakeMainPage(self, dickPageTableOfContents):
        '''Создадим главную страницу сайта'''

        Page = MainPageMaker(self.dictPropertys['PathSite'], self.TemplatePage, dickPageTableOfContents)
        Page.Make()
        FileName = WorkFiles.MakeHTMLFileName(self.dictPropertys['PathSite'], self.GetNameMainPage())
        Page.SavePage(FileName)

    def Make(self):
        '''Создаем сайт из файлов на диске'''

        self.LoadTemplatePage()
        dickTree = WorkFiles.FindFile(self.dictPropertys['PathToDirDescription'], 'site')

        isExistFile = 'Dirs' in dickTree or 'FileDescription' in dickTree
        if isExistFile:
            self.dickPageTableOfContents = self.MakePages(dickTree)

            self.MakeMainPage(self.dickPageTableOfContents)

    def GetNameMainPage(self):
        '''Имя главной страницы сайта'''

        return 'main'

    def GetTitleMainPage(self):
        '''Заголовок главной страницы сайта'''

        return 'Главная страница'

def PropertyMakeSite():
    '''Настройки для создания сайта'''

    PathToDirDescription = 'E:\\Python\\Projects\\Site from description\\test'
    FileNameTemplatePage = "Template.html"
    dictPropertys = {'FileNameTemplatePage': FileNameTemplatePage,
                     'PathSite': 'E:\\Python\\Projects\\Site from description\\site',
                     'PathToDirDescription': PathToDirDescription}

    return dictPropertys

if __name__ == '__main__':
    # ListBlockClass = Blocks.ListBlockClass()
    #
    # FileNameDescription = "E:\Python\Projects\Site from description\Simple test.txt"
    # Parser = ParserDescriptionFile(ListBlockClass, Blocks.BlockText, Blocks.BlockError)
    # Parser.ParseFile(FileNameDescription)

    Site = SiteMaker(PropertyMakeSite())

    # FileName = "New page.html"
    # Page = PageMaker(FileName, Site.TemplatePage)
    # Page.Make(Parser.ListBlock, FileNameDescription)
    # Page.SavePage(FileName)

    Site.Make()
    f = 0
