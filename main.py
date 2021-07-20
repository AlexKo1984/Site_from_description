import tkinter as tk
import ak_PageMaker as PageMaker
import ak_Blocks as Blocks

def onClick_btnMakeSite():
    Site = PageMaker.SiteMaker(PageMaker.PropertyMakeSite())
    Site.Make()

    print('Готово')


def onClick_btnTestMakePage():
    ListBlockClass = Blocks.ListBlockClass()

    FileNameDescription = "E:\Python\Projects\Site from description\Simple test.txt"
    Parser = PageMaker.ParserDescriptionFile(ListBlockClass, Blocks.BlockText, Blocks.BlockError)
    Parser.ParseFile(FileNameDescription)

    dictPropertys = PageMaker.PropertyMakeSite()
    Site = PageMaker.SiteMaker(dictPropertys)
    Site.LoadTemplatePage()

    FileName = "New page.html"
    Page = PageMaker.PageMaker(FileName, Site.TemplatePage)
    Page.Make(Parser.ListBlock)
    Page.SavePage(FileName)

    print('Готово')

def onClick_btnTest():
    block = Blocks.BlockLinkOnParentPage('main.html', 'Главная страница')

    print(block.GetHTML())

if __name__ == '__main__':
    form = tk.Tk()
    form.geometry("300x200")
    form.title('Создание сайта из файлов описания')

    btnMakeSite = tk.Button(master=form, width=20, height=1, text="Создать сайт", command=onClick_btnMakeSite)
    btnMakeSite.pack()

    btnMakeSite = tk.Button(master=form, width=20, height=1, text="Тест создания страницы", command=onClick_btnTestMakePage)
    btnMakeSite.pack()

    btnMakeSite = tk.Button(master=form, width=20, height=1, text="Тест", command=onClick_btnTest)
    btnMakeSite.pack()


    form.mainloop()


