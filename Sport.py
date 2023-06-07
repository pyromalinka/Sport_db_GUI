from tkinter import *
from tkinter import filedialog
import sqlite3
import os
import shutil


con = sqlite3.connect("Sport.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Fond("
            "nameid INT,"
            "name TEXT,"
            "picture BLOB,"
            "pictureway TEXT,"
            "info TEXT)")

def updatePeople(namebox):
    namebox.delete(0, END)
    update = cur.execute("SELECT name FROM Fond")
    for row in update:
        namebox.insert(END, row[0])
    updateNameIdPeople()


def updateNameIdPeople():
    updateNameId = cur.execute("SELECT nameid FROM Fond").fetchall()
    for curselection in range(len(updateNameId)):
        if curselection + 1 != updateNameId[curselection][0]:
            changeWrongNameId = curselection + 1
            if updateNameId[curselection][0] != 0:
                try:
                    cur.execute("UPDATE Fond SET nameid = ?"
                                "WHERE nameid = ?", (0, updateNameId[curselection + 1][0]))
                    con.commit()
                    updateNameId = cur.execute("SELECT nameid FROM Fond").fetchall()
                except:
                    pass
            cur.execute("UPDATE Fond SET nameid = ? "
                        "WHERE nameid = ?", (changeWrongNameId, updateNameId[curselection][0]))
            con.commit()


def windowContent(event=""):
    def CloseWindowContent():
        formContent.destroy()

    formContent = Toplevel()
    formContent.geometry('320x180')
    formContent.title("Справка")
    formContent.resizable(False, False)
    formContent.iconbitmap('icon.ico')
    labelCon1 = Label(formContent, text="База данных 'Знаменитые спортсмены России'")
    labelCon1.place(x=1, y=5)
    labelCon2 = Label(formContent, text="Позволяет: добавлять / изменять / удалять информацию")
    labelCon2.place(x=1, y=25)
    labelCon3 = Label(formContent, text="Клавиши программы:\nF1 - Вызов справки по программе,\n"
                                        "F2 - Добавить в базу данных,\n"
                                        "F3 - Удалить из базы данных,\n"
                                        "F4 - Изменить запись в базе данных,\n"
                                        "F10 - Меню программы\n"
                                        "Ctrl+X - Выход из программы", justify="left")
    labelCon3.place(x=1, y=45)
    buttonCloseContent = Button(formContent, text="Закрыть", command=CloseWindowContent)
    buttonCloseContent.place(x=250, y=150)
    formContent.grab_set()


def windowAboutProgram():
    global fviewAboutProgram

    def closeWindowAboutProgram():
        global fviewAboutProgram
        fviewAboutProgram = False
        formAboutProgram.destroy()

    def closeWindowAboutProgramButton():
        global fviewAboutProgram
        fviewAboutProgram = False
        formAboutProgram.destroy()

    if fviewAboutProgram:
        return 0
    formAboutProgram = Toplevel()
    formAboutProgram.geometry('330x180')
    formAboutProgram.title("О программе")
    formAboutProgram.resizable(False, False)
    formAboutProgram.iconbitmap('icon.ico')
    formAboutProgram.protocol("WM_DELETE_WINDOW", closeWindowAboutProgram)
    labelAboutProgram = Label(formAboutProgram, text="База данных 'Знаменитые спортсмены России'\n"
                                                     "(c) Маханько Денис, БСБО-11-21, 05.06.2023\n"
                                                     "Электронная почта: denism1005@gmail.com", justify="left")
    labelAboutProgram.place(x=20, y=50)
    buttonCloseAboutProgram = Button(formAboutProgram, text="ОК", command=closeWindowAboutProgramButton)
    buttonCloseAboutProgram.place(x=250, y=150, width=70, height=25)
    fviewAboutProgram = True

def convert_to_binary_data(filename):
    with open(filename, "rb") as file:
        blob_data = file.read()
        return blob_data

def convert_to_image(binary_date, filename):
    with open(filename, "wb") as file:
        file.write(binary_date)

def resize_image(image, x_width, y_height):
    x = image.width()
    y = image.height()
    x_resize = round((x_width - 30) / x, 1)
    y_resize = round((y_height - 30) / y, 1)
    x_zoom = int(x_resize * 10)
    y_zoom = int(y_resize * 10)
    image = image.zoom(x_zoom, y_zoom)
    image = image.subsample(10, 10)
    return image

def foundPeople():
    global fviewFoundPeople

    def ShowPicture(picture, pictureway):
        filename = "temp/" + pictureway
        convert_to_image(picture, filename)
        image = PhotoImage(file=filename)
        x_width = 300
        y_height = 400
        image = resize_image(image, x_width, y_height)
        imgLabelFoundPeople.config(image=image)
        imgLabelFoundPeople.image = image
        shutil.rmtree(os.path.join("temp"))

    def showInfoFoundPeople(event=""):
        textAboutFoundsPeople.configure(state=NORMAL)
        textAboutFoundsPeople.delete(1.0, END)
        name = entryFoundPeopleName.get().lower()
        peoples = cur.execute("SELECT name, info, picture, pictureway FROM Fond "
                              "WHERE lowerName(name) LIKE ?", ("%" + name + "%",)).fetchall()
        curselid = boxFoundPeople.curselection()[0]
        textAboutFoundsPeople.insert(1.0, peoples[curselid][1])
        picture = peoples[curselid][2]
        pictureway = peoples[curselid][3]

        if os.path.isdir("temp"):
            shutil.rmtree(os.path.join("temp"))
        os.mkdir("temp")

        ShowPicture(picture, pictureway)
        textAboutFoundsPeople.configure(state=DISABLED)


    def lower_string(string):
        return string.lower()

    def namesFoundsPeople():
        boxFoundPeople.delete(0, END)
        name = entryFoundPeopleName.get().lower()
        con.create_function("lowerName", 1, lower_string)
        peoples = cur.execute("SELECT nameid, name FROM Fond "
                              "WHERE lowerName(name) LIKE ?", ("%" + name + "%",)).fetchall()
        for row in peoples:
            boxFoundPeople.insert(END, row[1])
        boxFoundPeople.bind('<Double-1>', showInfoFoundPeople)

    def closeFoundPeople():
        global fviewFoundPeople
        fviewFoundPeople = False
        formFoundPeople.destroy()

    if fviewFoundPeople:
        return 0


    formFoundPeople = Toplevel()
    formFoundPeople.title("Поиск человека")
    formFoundPeople.geometry('900x580')
    formFoundPeople.resizable(False, False)
    formFoundPeople.iconbitmap('icon.ico')
    formFoundPeople.protocol("WM_DELETE_WINDOW", closeFoundPeople)
    labelFoundPeopleName = Label(formFoundPeople, text="Введите имя человека, которого хотите найти "
                                                       "(можно не полностью): ")
    labelFoundPeopleName.place(x=5, y=5)
    labelFoundsPeople = Label(formFoundPeople, text="Найденные пользователи:")
    labelFoundsPeople.place(x=5, y=30)
    entryFoundPeopleName = Entry(formFoundPeople, width=50)
    entryFoundPeopleName.place(x=400, y=5)
    entryFoundPeopleName.bind('<Control-KeyPress>', functionKeys)
    buttonFoundPeople = Button(formFoundPeople, text="Найти", command=namesFoundsPeople)
    buttonFoundPeople.place(x=710, y=5, height=20)
    boxFoundPeople = Listbox(formFoundPeople)
    boxFoundPeople.place(x=5, y=60, width=290, height=500)
    boxFoundPeople.bind('<Control-KeyPress>', functionKeys)
    textAboutFoundsPeople = Text(formFoundPeople, wrap="word")
    textAboutFoundsPeople.place(x=605, y=60, width=290, height=500)
    textAboutFoundsPeople.bind('<Control-KeyPress>', functionKeys)
    textAboutFoundsPeople.configure(state=DISABLED)
    imgLabelFoundPeople = Label(formFoundPeople)
    imgLabelFoundPeople.place(x=450, y=300, anchor=CENTER)
    fviewFoundPeople = True

def functionKeys(event):
    if event.keycode== 88 and event.state == 4 and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")

    if event.keycode== 86 and event.state == 4 and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")

    if event.keycode== 67 and event.state == 4 and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

def addPeople(event=""):
    global fviewAddPeople


    def SavePeople():
        global DirFile
        checkID = True
        nameid = 1
        while checkID:
            cur.execute("SELECT nameid FROM Fond where nameid = ?", (nameid,))
            if cur.fetchone() is None:
                checkID = False
            else:
                nameid += 1
        name = entryAddNamePeople.get()
        picture = convert_to_binary_data(DirFile)
        DirFile = os.path.basename(DirFile)
        info = textAddInfoPeople.get("1.0", "end-1c")

        dataPeople = [nameid, name, picture, DirFile, info]
        cur.execute("INSERT INTO Fond (nameid, name, picture, pictureway, info) VALUES (?,?,?,?,?)", dataPeople)
        con.commit()
        updatePeople(namebox)
        closeAddPeople()

    def openPicture():
        global DirFile
        labelNamePicture["text"] = ""
        filetypes = (("png files", "*.png"),
                     ("gif files", "*.gif"))
        DirFile = filedialog.askopenfilename(title="Открыть файл",
                                             initialdir='/',
                                             filetypes=filetypes)
        formAddPeople.focus()
        fileName = os.path.basename(DirFile)
        labelNamePicture["text"] = f"Выбран файл: {fileName}"


    def closeAddPeopleButton():
        global fviewAddPeople
        fviewAddPeople = False
        formAddPeople.destroy()

    def closeAddPeople():
        global fviewAddPeople
        fviewAddPeople = False
        formAddPeople.destroy()

    if fviewAddPeople:
        return 0
    formAddPeople = Toplevel()
    formAddPeople.geometry('700x470')
    formAddPeople.title("Добавление знаменитого спортсмена России")
    formAddPeople.resizable(False, False)
    formAddPeople.iconbitmap('icon.ico')
    formAddPeople.protocol("WM_DELETE_WINDOW", closeAddPeople)
    labelAddNamePeople = Label(formAddPeople, text="Введите имя человека:")
    labelAddNamePeople.place(x=5, y=5)
    entryAddNamePeople = Entry(formAddPeople)
    entryAddNamePeople.place(x=140, y=5, width=250)
    entryAddNamePeople.bind('<Control-KeyPress>', functionKeys)
    labelAddPicturePeople = Label(formAddPeople, text="Выберите изображение:")
    labelAddPicturePeople.place(x=5, y=30)
    buttonAddPicturePeople = Button(formAddPeople, text="Выбрать", command=openPicture)
    buttonAddPicturePeople.place(x=150, y=30, width=100)
    labelNamePicture = Label(formAddPeople, text="")
    labelNamePicture.place(x=260, y=30)
    labelAddInfoPeople = Label(formAddPeople, text="Введите информацию о человеке:")
    labelAddInfoPeople.place(x=5, y=60)
    textAddInfoPeople = Text(formAddPeople, wrap="word")
    textAddInfoPeople.place(x=200, y=60, width=450, height=350)
    textAddInfoPeople.bind('<Control-KeyPress>', functionKeys)
    buttonSavePeople = Button(formAddPeople, text="Сохранить", command=SavePeople)
    buttonSavePeople.place(x=520, y=420, width=70)
    buttonCancelPeople = Button(formAddPeople, text="Отмена", command=closeAddPeopleButton)
    buttonCancelPeople.place(x=600, y=420, width=70)
    fviewAddPeople = True


def delPeople(event=""):
    global fviewDelPeople
    def delInfoPeople():
        nameid = boxDelPeople.curselection()[0] + 1
        cur.execute("DELETE FROM Fond WHERE nameid = ?", (nameid,))
        con.commit()
        updatePeople(boxDelPeople)
        updatePeople(namebox)

    def closeDelPeople():
        global fviewDelPeople
        fviewDelPeople = False
        formDelPeople.destroy()

    def closeDelPeopleButton():
        global fviewDelPeople
        fviewDelPeople = False
        formDelPeople.destroy()

    if fviewDelPeople:
        return 0
    formDelPeople = Toplevel()
    formDelPeople.geometry('600x470')
    formDelPeople.title("Удаление пользователя")
    formDelPeople.resizable(False, False)
    formDelPeople.iconbitmap('icon.ico')
    formDelPeople.protocol("WM_DELETE_WINDOW", closeDelPeople)
    labelDelPeople = Label(formDelPeople, text="Выберите из списка, какого человека, вы хотите удалить?")
    labelDelPeople.place(x=5, y=5)
    boxDelPeople = Listbox(formDelPeople)
    updatePeople(boxDelPeople)
    boxDelPeople.place(x=5, y=30, width=300, height=400)
    buttonDelPeople = Button(formDelPeople, text="Удалить", command=delInfoPeople)
    buttonDelPeople.place(x=5, y=435)
    buttonCancelPeople = Button(formDelPeople, text="Отмена", command=closeDelPeopleButton)
    buttonCancelPeople.place(x=530, y=435)
    fviewDelPeople = True


def changePeople(event=""):
    global fviewChangePeople


    def changeSavePeople():
        global DirFile
        textChangeInfoPeople.configure(state=DISABLED)
        name = entryChangeNamePeople.get()
        info = textChangeInfoPeople.get("1.0", "end-1c")
        nameid = boxChangePeople.curselection()[0] + 1
        try:
            picture = convert_to_binary_data(DirFile)
        except:
            picture = cur.execute("SELECT picture FROM Fond WHERE nameid =?", (nameid,)).fetchone()[0]
        DirFile = os.path.basename(DirFile)
        cur.execute("UPDATE Fond SET name = ?, picture = ?, pictureway = ?, info = ? "
                    "WHERE nameid = ?", (name, picture, DirFile, info, nameid))
        con.commit()
        updatePeople(namebox)
        closeChangePeople()

    def windowChangePeople(event=""):
        global DirFile
        textChangeInfoPeople.configure(state=NORMAL)
        labelNamePicture["text"] = ""
        textChangeInfoPeople.delete(1.0, END)
        entryChangeNamePeople.delete(0, END)
        nameid = boxChangePeople.curselection()[0] + 1
        name = cur.execute("SELECT name FROM Fond WHERE nameid = ?", (nameid,)).fetchone()
        name = name[0]
        entryChangeNamePeople.insert(0, name)
        infoData = cur.execute("SELECT info FROM Fond where nameid = ?", (nameid,)).fetchone()
        infoData = infoData[0]
        textChangeInfoPeople.insert(1.0, infoData)
        DirFile = cur.execute("SELECT pictureway FROM Fond WHERE nameid =?", (nameid,)).fetchone()
        DirFile = DirFile[0]
        labelNamePicture["text"] = "Выбранный файл: " + DirFile
        buttonChangePicturePeople = Button(formChangePeople, text="Изменить", command=changePicturePeople)
        buttonChangePicturePeople.place(x=450, y=30)

    def changePicturePeople():
        global DirFile

        filetypes = (("png files", "*.png"),
                     ("gif files", "*.gif"))
        DirFile = filedialog.askopenfilename(title="Открыть файл",
                                             initialdir='/',
                                             filetypes=filetypes)
        formChangePeople.focus()
        fileName = os.path.basename(DirFile)
        labelNamePicture["text"] = f"Файл изменён на: {fileName}"

    def closeChangePeople():
        global fviewChangePeople
        fviewChangePeople = False
        formChangePeople.destroy()

    def closeChangePeopleButton():
        global fviewChangePeople
        fviewChangePeople = False
        formChangePeople.destroy()

    if fviewChangePeople:
        return 0
    formChangePeople = Toplevel()
    formChangePeople.geometry('1000x600')
    formChangePeople.title("Изменения человека")
    formChangePeople.resizable(False, False)
    formChangePeople.iconbitmap('icon.ico')
    formChangePeople.protocol("WM_DELETE_WINDOW", closeChangePeople)
    labelChangePeople = Label(formChangePeople, text="Выберите, кого хотите изменить:")
    labelChangePeople.place(x=5, y=5)
    boxChangePeople = Listbox(formChangePeople)
    updatePeople(boxChangePeople)
    boxChangePeople.place(x=5, y=30, width=400, height=500)
    boxChangePeople.configure(exportselection=False)
    labelChangeNamePeople = Label(formChangePeople, text="Имя:")
    labelChangeNamePeople.place(x=410, y=5)
    entryChangeNamePeople = Entry(formChangePeople)
    entryChangeNamePeople.place(x=445, y=5, width=250)
    entryChangeNamePeople.bind('<Control-KeyPress>', functionKeys)
    labelChangePicturePeople = Label(formChangePeople, text="фото:")
    labelChangePicturePeople.place(x=410, y=30)
    labelNamePicture = Label(formChangePeople, text="")
    labelNamePicture.place(x=410, y=60)
    labelChangeInfoPeople = Label(formChangePeople, text="Информация:")
    labelChangeInfoPeople.place(x=410, y=90)
    textChangeInfoPeople = Text(formChangePeople, wrap="word")
    textChangeInfoPeople.place(x=500, y=90, width=400, height=440)
    textChangeInfoPeople.configure(state=DISABLED)
    textChangeInfoPeople.bind('<Control-KeyPress>', functionKeys)
    buttonChangeCancelPeople = Button(formChangePeople, text="Отмена", command=closeChangePeopleButton)
    buttonChangeCancelPeople.place(x=900, y=550)
    buttonChangeSavePeople = Button(formChangePeople, text="Сохранить", command=changeSavePeople)
    buttonChangeSavePeople.place(x=825, y=550)
    boxChangePeople.bind('<Double-1>', windowChangePeople)
    fviewChangePeople = True


def PrintInfoPeople(event=""):
    descName.configure(state=NORMAL)
    descName.delete(1.0, END)
    nameid = namebox.curselection()[0] + 1
    infoData = cur.execute("SELECT info FROM Fond where nameid = ?", (nameid,)).fetchone()[0]
    descName.insert(1.0, infoData)
    picture = cur.execute("SELECT picture FROM Fond WHERE nameid = ?", (nameid,)).fetchone()[0]
    pictureway = cur.execute("SELECT pictureway FROM Fond WHERE nameid = ?", (nameid,)).fetchone()[0]

    def ShowPicture(picture):
        filename = "temp/" + pictureway
        convert_to_image(picture, filename)
        image = PhotoImage(file=filename)
        x_width = 370
        y_height = 500
        image = resize_image(image, x_width, y_height)
        imgLabel.config(image=image)
        imgLabel.image = image
        shutil.rmtree(os.path.join("temp"))

    if os.path.isdir("temp"):
        shutil.rmtree(os.path.join("temp"))

    os.mkdir("temp")
    ShowPicture(picture)
    descName.configure(state=DISABLED)

def closeProgram(event=""):
    if event.keycode == 88:
        formMain.destroy()


formMain = Tk()
formMain.title("Знаменитые спортсмены России")
formMain.geometry('1000x550')
formMain.resizable(False, False)
formMain.iconbitmap('icon.ico')
fviewAboutProgram = False
fviewAddPeople = False
fviewDelPeople = False
fviewChangePeople = False
fviewFoundPeople = False

mainmenu = Menu(formMain)
formMain.config(menu=mainmenu)

fondmenu = Menu(mainmenu, tearoff=0)
mainmenu.add_cascade(label="Фонд", menu=fondmenu)
fondmenu.add_command(label="Найти...", command=foundPeople)
fondmenu.add_separator()
fondmenu.add_command(label="Добавить F2", command=addPeople)
formMain.bind('<F2>', addPeople)
DirFile = ""
fondmenu.add_command(label="Удалить F3", command=delPeople)
formMain.bind('<F3>', delPeople)
fondmenu.add_command(label="Изменить F4", command=changePeople)
formMain.bind('<F4>', changePeople)
fondmenu.add_separator()
fondmenu.add_command(label="Выход Ctrl+X")
formMain.bind('<Control-KeyPress>', closeProgram)

menuRef = Menu(mainmenu, tearoff=0)
mainmenu.add_cascade(label="Справка", menu=menuRef)
formMain.bind('<F1>', windowContent)
menuRef.add_command(label="Содержание", command=windowContent)
menuRef.add_separator()
menuRef.add_command(label="О программе", command=windowAboutProgram)

imgLabel = Label(formMain)
imgLabel.place(x=500, y=250, anchor=CENTER)

namebox = Listbox()
updatePeople(namebox)
namebox.place(x=5, y=5, width=300, height=500)
namebox.configure(exportselection=False)
namebox.bind('<Double-1>', PrintInfoPeople)

descName = Text(formMain, wrap="word")
descName.place(x=695, y=5, width=300, height=500)
descName.bind('<Control-KeyPress>', functionKeys)
descName.configure(state=DISABLED)

downLabel = Label(formMain, text="F1-Справка F2-Добавить F3-Удалить F4-Изменить F10-Меню",
                  bg="#2f24cc", fg="#ffffff", anchor=W, font="Helvetica 10")
downLabel.place(x=0, y=510, width=1000)

formMain.mainloop()