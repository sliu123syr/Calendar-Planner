import pygame

class Months:
    def __init__(self, monthname, monthnumber, numdays):
        self.monthname = monthname
        self.monthnumber = monthnumber
        self.numdays = numdays
        self.listofdays = []

class Days:
    def __init__(self, month, day):
        self.month = month
        self.day = day
        self.reminders = []

class Reminder:
    def __init__(self, name, day, explanation):
        self.name = name
        self.day = day
        self.explanation = explanation

class ReminderType:
    def __init__(self, name):
        self.name = name
        self.listofreminders = []

class Button:
    def __init__(self, color, x, y, width, height, size, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textsize = size

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4),0)
        
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height),0)

        if self.text != '':
            font = pygame.font.SysFont('cambria', self.textsize)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
    
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

JAN = Months('January', 1, 31)
FEB = Months('Febuary', 2, 28)
MAR = Months('March', 3, 31)
APR = Months('April', 4, 30)
MAY = Months('May', 5, 31)
JUN = Months('June', 6, 30)
JUL = Months('July', 7, 31)
AUG = Months('August', 8, 31)
SEP = Months('September', 9, 30)
OCT = Months('October', 10, 31)
NOV = Months('November', 11, 30)
DEC = Months('December', 12, 31)

YEAR2021 = [JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC]
reminderlist = []


##-------------------------------------------------------------------------------
def main():
    for month in YEAR2021:
        for i in range (month.numdays):
            newday = Days(month.monthnumber, i+1)
            month.listofdays.append(newday)

    global reminderlist

    readfromfile()

    pygame.init()
    mainwindow = pygame.display.set_mode([1200,800])
    mainwindow.fill((255, 255, 255))

    mainscreen(mainwindow)
##-------------------------------------------------------------------------------
def mainscreen(mainwindow):
    pygame.init()

    addreminder = Button((255, 255, 255,), 400, 250, 400, 50, 50, 'Add Reminder')

    running = True
    while running:
        mainwindow.fill((255, 255, 255))
        drawmainscreen(mainwindow, addreminder)
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                running = False
                savetofile()
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if addreminder.isOver(pos):
                    running = False
                    addreminderscreen(mainwindow)


def drawmainscreen(mainwindow, addreminder):
    addreminder.draw(mainwindow, (0, 0, 0))
##-------------------------------------------------------------------------------
def addreminderscreen(mainwindow):
    pygame.init()

    selectedmonth = 0
    ismonthselected = False
    selectedday = 0
    remindername = ''
    reminderexplanation = ''
    remindername_rect = pygame.Rect(200, 450, 140, 50)
    reminderexplanation_rect = pygame.Rect(200, 550, 140, 50)
    promptfont = pygame.font.SysFont('cambria', 40)
    remindernameprompt = promptfont.render('Reminder Name:', 1, (0, 0, 0))
    reminderexplanationprompt = promptfont.render('Reminder Description:', 1, (0, 0, 0))
    
    remindername_color = (255, 0, 0)
    reminderexplanation_color = (255, 0, 0)
    color_active = (255, 0, 0)
    color_passive = (0, 0, 0)
    font = pygame.font.SysFont('cambria', 30)

    remindername_active = False
    reminderexplanation_active = False

    monthbuttonlist = []
    daybuttonlist = []
    for i in range (6):
        monthbutton1 = Button((255, 255, 255), i*150+175, 100, 100, 50, 18, YEAR2021[2*i].monthname)
        monthbutton2 = Button((255, 255, 255), i*150+175, 175, 100, 50, 18, YEAR2021[2*i+1].monthname)
        monthbuttonlist.append(monthbutton1)
        monthbuttonlist.append(monthbutton2)

    for i in range (3):
        for j in range (11):
            daybutton = Button((255, 255, 255), j*75+200, i*50 + 250, 50, 50, 18, str((i*11) + j + 1))
            daybuttonlist.append(daybutton)

    submitreminderbutton = Button((255, 255, 255,), 500, 650, 200, 50, 40, 'Submit')

    running = True
    while running:

        mainwindow.fill((255, 255, 255))
        
        mainwindow.blit(remindernameprompt, (160, 400))
        pygame.draw.rect(mainwindow, remindername_color, remindername_rect, 2)
        remindernametext = font.render(remindername, True, (0, 0, 0))
        mainwindow.blit(remindernametext, (remindername_rect.x + 10, remindername_rect.y + 5))
        remindername_rect.w = max(200, remindernametext.get_width() + 20)

        mainwindow.blit(reminderexplanationprompt, (160, 500))
        pygame.draw.rect(mainwindow, reminderexplanation_color, reminderexplanation_rect, 2)
        reminderexplanationtext = font.render(reminderexplanation, True, (0, 0, 0))
        mainwindow.blit(reminderexplanationtext, (reminderexplanation_rect.x + 10, reminderexplanation_rect.y + 5))
        reminderexplanation_rect.w = max(200, reminderexplanationtext.get_width() + 20)

        for i in range(12):
            if selectedmonth == i + 1:
                monthbuttonlist[i].color = (255, 0, 0)
            else:
                monthbuttonlist[i].color = (255, 255, 255)
            monthbuttonlist[i].draw(mainwindow, (0, 0, 0))

        if ismonthselected == True:
            for i in range(YEAR2021[selectedmonth - 1].numdays):
                if selectedday == i + 1:
                    daybuttonlist[i].color = (255, 0, 0)
                else:
                    daybuttonlist[i].color = (255, 255, 255)
                daybuttonlist[i].draw(mainwindow, (0, 0, 0))

        submitreminderbutton.draw(mainwindow, (0, 0, 0))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                running = False
                savetofile()
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if remindername_rect.collidepoint(event.pos):
                    remindername_active = True
                    reminderexplanation_active = False
                elif reminderexplanation_rect.collidepoint(event.pos):
                    reminderexplanation_active = True
                    remindername_active = False
                else:
                    remindername_active = False
                    reminderexplanation_active = False
                    
                for i in range(12):
                    if monthbuttonlist[i].isOver(pos):
                        selectedmonth = i + 1
                        ismonthselected = True
                for i in range(YEAR2021[selectedmonth - 1].numdays):
                    if daybuttonlist[i].isOver(pos):
                        selectedday = i + 1
                if submitreminderbutton.isOver(pos):
                    if selectedmonth != 0 and selectedday != 0 and remindername != '' and reminderexplanation != '':
                        running = False
                        newreminder(selectedmonth, selectedday, remindername, reminderexplanation)
                        print(selectedmonth, selectedday, remindername, reminderexplanation)
                        mainscreen(mainwindow)

            if event.type == pygame.KEYDOWN:
                if remindername_active == True:
                    if event.key == pygame.K_BACKSPACE:
                        remindername = remindername[0:-1]
                    else:
                        remindername += event.unicode
                if reminderexplanation_active == True:
                    if event.key == pygame.K_BACKSPACE:
                        reminderexplanation = reminderexplanation[0:-1]
                    else:
                        reminderexplanation += event.unicode

        if remindername_active:
            remindername_color = color_active
        else:
            remindername_color = color_passive

        if reminderexplanation_active:
            reminderexplanation_color = color_active
        else:
            reminderexplanation_color = color_passive


    
##-------------------------------------------------------------------------------
def newreminder(remindermonth, reminderday, remindername, reminderexplanation):
    newreminder = Reminder(remindername, YEAR2021[remindermonth - 1].listofdays[reminderday - 1], reminderexplanation)
    reminderlist.append(newreminder)
    YEAR2021[remindermonth - 1].listofdays[reminderday - 1].reminders.append(newreminder)

def retrievereminder():
    remindermonth = eval(input("Enter the Month Number: "))
    reminderday = eval(input("Enter the Day: "))
    if len(YEAR2021[remindermonth - 1].listofdays[reminderday - 1].reminders) > 0:
        print(YEAR2021[remindermonth - 1].listofdays[reminderday - 1].reminders[0].name)
        print(YEAR2021[remindermonth - 1].listofdays[reminderday - 1].reminders[0].explanation)

    else:
        retrievereminder()

def deletereminder():
    remindermonth = eval(input("Enter the Month Number: "))
    reminderday = eval(input("Enter the Day: "))
    remindername = input("Enter the Reminder Name: ")
    for reminder in reminderlist:
        if reminder.name == remindername and reminder.day == YEAR2021[remindermonth - 1].listofdays[reminderday - 1]:
            reminderlist.remove(reminder)
##-------------------------------------------------------------------------------
def readfromfile():
    file = open("Reminders.txt","r")
    for line in file:
        info = line.split("-")
        remindername = info[0]
        remindermonth = int(info[1])
        reminderday = int(info[2])
        reminderexplanation = info[3]
        reminderexplanation = reminderexplanation.replace("\n","")
        newreminder = Reminder(remindername, YEAR2021[remindermonth - 1].listofdays[reminderday - 1], reminderexplanation)
        reminderlist.append(newreminder)
        YEAR2021[remindermonth - 1].listofdays[reminderday - 1].reminders.append(newreminder)
        
def savetofile():
    file = open("Reminders.txt","w")
    remindersdata = ""
    for reminder in reminderlist:
        remindersdata = remindersdata + reminder.name+ "-" + str(reminder.day.month) + "-" + str(reminder.day.day) + "-" + str(reminder.explanation) + "\n"
    file.write(remindersdata)
##-------------------------------------------------------------------------------
















main()
