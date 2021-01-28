import pygame

class Months:
    def __init__(self, monthname, monthnumber, numdays):
        self.monthname = monthname
        self.monthnumber = monthnumber
        self.numdays = numdays
        self.listofdays = []
        self.reminders = []

class Days:
    def __init__(self, month, day, dayofweek):
        self.month = month
        self.day = day
        self.dayofweek = dayofweek
        self.reminders = []

class Reminder:
    def __init__(self, name, day, explanation, status):
        self.name = name
        self.day = day
        self.explanation = explanation
        self.status = status

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
    daysofweek = [0, 1, 2, 3, 4, 5, 6]
    previousday = 5
    for month in YEAR2021:
        for i in range (month.numdays):
            if month == YEAR2021[0] and i == 0:
                newday = Days(month.monthnumber, i+1, 5)
            elif previousday == 6:
                newday = Days(month.monthnumber, i+1, 0)
                previousday = 0
            else:
                newday = Days(month.monthnumber, i+1, previousday + 1)
                previousday = previousday + 1
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
    viewcalendar = Button((255, 255, 255,), 400, 350, 400, 50, 50, 'View Calendar')

    running = True
    while running:
        mainwindow.fill((255, 255, 255))
        addreminder.draw(mainwindow, (0, 0, 0))
        viewcalendar.draw(mainwindow, (0, 0, 0))
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
                if viewcalendar.isOver(pos):
                    running = False
                    viewcalendarscreen(mainwindow)

            if event.type == pygame.MOUSEMOTION:
                if addreminder.isOver(pos):
                    addreminder.color = (255, 0, 0)
                else:
                    addreminder.color = (255, 255, 255)
                if viewcalendar.isOver(pos):
                    viewcalendar.color = (255, 0, 0)
                else:
                    viewcalendar.color = (255, 255, 255)

##-------------------------------------------------------------------------------
def addreminderscreen(mainwindow):
    pygame.init()

    selectedmonth = 0
    ismonthselected = False
    selectedday = 0
    remindername = ''
    reminderexplanation = ''
    reminderstatus = ''
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
    statusbuttonlist = []
    for i in range (6):
        monthbutton1 = Button((255, 255, 255), i*150+175, 100, 100, 50, 18, YEAR2021[2*i].monthname)
        monthbutton2 = Button((255, 255, 255), i*150+175, 175, 100, 50, 18, YEAR2021[2*i+1].monthname)
        monthbuttonlist.append(monthbutton1)
        monthbuttonlist.append(monthbutton2)
    for i in range (3):
        for j in range (11):
            daybutton = Button((255, 255, 255), j*75+200, i*50 + 250, 50, 50, 18, str((i*11) + j + 1))
            daybuttonlist.append(daybutton)

    nostatusbutton = Button((255, 255, 255,), 100, 650, 200, 50, 20, 'No Status')
    completebutton = Button((255, 255, 255,), 300, 650, 200, 50, 20, 'Completed')
    incompletebutton = Button((255, 255, 255,), 500, 650, 200, 50, 20, 'Incomplete')
    statusbuttonlist.append(nostatusbutton)
    statusbuttonlist.append(completebutton)
    statusbuttonlist.append(incompletebutton)
    submitreminderbutton = Button((255, 255, 255,), 800, 650, 200, 50, 40, 'Submit')
    backbutton = Button((255, 255, 255,), 1075, 50, 75, 40, 30, 'Back')

    running = True
    while running:
        mainwindow.fill((255, 255, 255))
        
        mainwindow.blit(remindernameprompt, (160, 400))
        pygame.draw.rect(mainwindow, remindername_color, remindername_rect, 2)
        if remindername_active:
            remindernametext = font.render(remindername + "|", True, (0, 0, 0))
        else:
            remindernametext = font.render(remindername, True, (0, 0, 0))
        mainwindow.blit(remindernametext, (remindername_rect.x + 10, remindername_rect.y + 5))
        remindername_rect.w = max(400, remindernametext.get_width() + 20)

        mainwindow.blit(reminderexplanationprompt, (160, 500))
        pygame.draw.rect(mainwindow, reminderexplanation_color, reminderexplanation_rect, 2)
        if reminderexplanation_active:
            reminderexplanationtext = font.render(reminderexplanation + "|", True, (0, 0, 0))
        else:
            reminderexplanationtext = font.render(reminderexplanation, True, (0, 0, 0))
        mainwindow.blit(reminderexplanationtext, (reminderexplanation_rect.x + 10, reminderexplanation_rect.y + 5))
        reminderexplanation_rect.w = max(400, reminderexplanationtext.get_width() + 20)

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

        for i in statusbuttonlist:
            if i.text == reminderstatus:
                i.color = (255, 0, 0)
            else:
                i.color = (255, 255, 255)
            i.draw(mainwindow, (0, 0, 0))

        submitreminderbutton.draw(mainwindow, (0, 0, 0))
        backbutton.draw(mainwindow, (0, 0, 0))
        
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
                        newreminder(selectedmonth, selectedday, remindername, reminderexplanation, reminderstatus)
                        print(selectedmonth, selectedday, remindername, reminderexplanation, reminderstatus)
                        mainscreen(mainwindow)

                for i in statusbuttonlist:
                    if i.isOver(pos):
                        reminderstatus = i.text

                if backbutton.isOver(pos):
                    running = False
                    mainscreen(mainwindow)
                        
            if event.type == pygame.MOUSEMOTION:
                if submitreminderbutton.isOver(pos):
                    submitreminderbutton.color = (255, 0, 0)
                else:
                    submitreminderbutton.color = (255, 255, 255)
                    
                if backbutton.isOver(pos):
                    backbutton.color = (255, 0, 0)
                else:
                    backbutton.color = (255, 255, 255)


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
def viewcalendarscreen(mainwindow):
    pygame.init()
    
    monthfont = pygame.font.SysFont('cambria', 30)
    reminderfont = pygame.font.SysFont('cambria', 25)
    yearfont = pygame.font.SysFont('cambria', 70)

    monthbuttonlist = []
    monthtextlist = []
    reminderstextlist = []
    for i in range (3):
        for j in range (4):
            monthbutton = Button((255, 255, 255), j*250+125, i*175+200, 200, 150, 0)
            monthbuttonlist.append(monthbutton)
    for i in range(12):
        monthtext = monthfont.render(YEAR2021[i].monthname, 1, (0, 0, 0))
        monthtextlist.append(monthtext)

        text = "Reminders: " + str(len(YEAR2021[i].reminders))
        remindertext = reminderfont.render(text, 1, (0, 0, 0))
        reminderstextlist.append(remindertext)
    yeartext = yearfont.render("2021", 1, (0, 0, 0))

    backbutton = Button((255, 255, 255,), 1075, 50, 75, 40, 30, 'Back')

    running = True
    while running:
        mainwindow.fill((255, 255, 255))

        for i in range(12):
            monthbuttonlist[i].draw(mainwindow, (0, 0, 0))
        index = 0
        for i in range (3):
            for j in range (4):
                mainwindow.blit(monthtextlist[index], (j*250+130, i*175+200))
                mainwindow.blit(reminderstextlist[index], (j*250+130, i*175+240))
                index = index + 1
        mainwindow.blit(yeartext, (515, 100))
        
        backbutton.draw(mainwindow, (0, 0, 0))

        pygame.display.update()
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                running = False
                savetofile()
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(12):
                    if monthbuttonlist[i].isOver(pos):
                        running = False
                        monthscreen(i, mainwindow)

                if backbutton.isOver(pos):
                    running = False
                    mainscreen(mainwindow)

                        
            if event.type == pygame.MOUSEMOTION:
                for i in monthbuttonlist:
                    if i.isOver(pos):
                        i.color = (255, 0, 0)
                    else:
                        i.color = (255, 255, 255)

                if backbutton.isOver(pos):
                    backbutton.color = (255, 0, 0)
                else:
                    backbutton.color = (255, 255, 255)

##-------------------------------------------------------------------------------
def monthscreen(monthindex, mainwindow):
    pygame.init()

    dayfont = pygame.font.SysFont('cambria', 30)
    reminderfont = pygame.font.SysFont('cambria', 30)
    monthfont = pygame.font.SysFont('cambria', 50)
    weeks = [[], [], [], [], [], []]
    currentweek = 0
    for i in YEAR2021[monthindex].listofdays:
        weeks[currentweek].append(i)
        if i.dayofweek == 6:
            currentweek = currentweek + 1
        else:
            currentweek = currentweek

    daybuttonlist = []
    daytextlist = []
    reminderstextlist = []
    reminderstextlist2 = []
    for i in range(6):
        for j in weeks[i]:
            daybutton = Button((255, 255, 255), j.dayofweek*150+75, i*100+150, 140, 90, 0)
            daybuttonlist.append(daybutton)
    for i in range(len(daybuttonlist)):
        daytext = dayfont.render(str(i + 1), 1, (0, 0, 0))
        daytextlist.append(daytext)

        text = str(len(YEAR2021[monthindex].listofdays[i].reminders)*'*')
        if len(YEAR2021[monthindex].listofdays[i].reminders) > 9:
            text = str(9*'*')
            text2 = str((len(YEAR2021[monthindex].listofdays[i].reminders) - 9)*'*')
        else:
            text2 = ''
        remindertext = reminderfont.render(text, 1, (0, 0, 0))
        remindertext2 = reminderfont.render(text2, 1, (0, 0, 0))
        reminderstextlist.append(remindertext)
        reminderstextlist2.append(remindertext2)
    monthtext = monthfont.render(YEAR2021[monthindex].monthname, 1, (0, 0, 0))
    backbutton = Button((255, 255, 255,), 1075, 50, 75, 40, 30, 'Back')

    running = True
    while running:
        mainwindow.fill((255, 255, 255))

        for i in range(len(daybuttonlist)):
            daybuttonlist[i].draw(mainwindow, (0, 0, 0))
        index = 0
        for i in range(6):
            for j in weeks[i]:
                mainwindow.blit(daytextlist[index], (j.dayofweek*150+75, i*100+150))
                mainwindow.blit(reminderstextlist[index], (j.dayofweek*150+80, i*100+190))
                mainwindow.blit(reminderstextlist2[index], (j.dayofweek*150+80, i*100+200))
                index = index + 1
        mainwindow.blit(monthtext, (75, 75))

        backbutton.draw(mainwindow, (0, 0, 0))

        pygame.display.update()
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                running = False
                savetofile()
                pygame.quit()

            if event.type == pygame.MOUSEMOTION:
                for i in daybuttonlist:
                    if i.isOver(pos):
                        i.color = (255, 0, 0)
                    else:
                        i.color = (255, 255, 255)

                if backbutton.isOver(pos):
                    backbutton.color = (255, 0, 0)
                else:
                    backbutton.color = (255, 255, 255)


            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(daybuttonlist)):
                    if daybuttonlist[i].isOver(pos):
                        running = False
                        dayscreen(monthindex, i, mainwindow, '')

                if backbutton.isOver(pos):
                    running = False
                    viewcalendarscreen(mainwindow)

##-------------------------------------------------------------------------------
def dayscreen(monthindex, dayindex, mainwindow, curreminder):
    pygame.init()
    
    dayfont = pygame.font.SysFont('cambria', 50)
    explafont = pygame.font.SysFont('cambria', 40)
    remindertextfont = pygame.font.SysFont('cambria', 20)
    daytext = dayfont.render(YEAR2021[monthindex].monthname + " " + str(dayindex + 1), 1, (0, 0, 0))

    reminderbuttonlist = []
    col = 0
    row = 0
    for i in YEAR2021[monthindex].listofdays[dayindex].reminders:
        reminderbutton = Button((255, 255, 255,), col*350+75, row*60+150, 340, 50, 20, i.name)
        reminderbuttonlist.append(reminderbutton)
        row = row + 1
        if row == 7:
            row = 0
            col = col + 1
    curreminderbutton = 0
    statusbuttonlist = []
    nostatusbutton = Button((255, 255, 255,), 75, 700, 200, 50, 20, 'No Status')
    completebutton = Button((255, 255, 255,), 275, 700, 200, 50, 20, 'Completed')
    incompletebutton = Button((255, 255, 255,), 475, 700, 200, 50, 20, 'Incomplete')
    statusbuttonlist.append(nostatusbutton)
    statusbuttonlist.append(completebutton)
    statusbuttonlist.append(incompletebutton)
    removereminderbutton = Button((255, 255, 255,), 725, 700, 200, 50, 20, 'Remove Reminder')
    backbutton = Button((255, 255, 255,), 1075, 50, 75, 40, 30, 'Back')

    running = True
    while running:
        mainwindow.fill((255, 255, 255))

        mainwindow.blit(daytext, (75, 75))
        for i in reminderbuttonlist:
            if i == curreminderbutton:
                i.color = (255, 255, 0)
            else:
                i.color = (255, 255, 255)
            i.draw(mainwindow, (0, 0, 0))
        col = 0
        row = 0
        for i in YEAR2021[monthindex].listofdays[dayindex].reminders:
            reminderstatus = Button((255, 255, 255,), col*350+375, row*60+160, 30, 30, -1, i.status)
            if reminderstatus.text == 'No Status':
                reminderstatus.color = (128, 128, 128)
            elif reminderstatus.text == 'Completed':
                reminderstatus.color = (0, 200, 0)
            elif reminderstatus.text == 'Incomplete':
                reminderstatus.color = (255, 0, 0)
            reminderstatus.draw(mainwindow, (0, 0, 0))
            row = row + 1
            if row == 7:
                row = 0
                col = col + 1

        if curreminder != '':
            curemindertext = remindertextfont.render(curreminder.name, 1, (0, 0, 0))
            curexplanationtext = explafont.render(curreminder.explanation, 1, (0, 0, 0))
            mainwindow.blit(curexplanationtext, (75, 600))
            mainwindow.blit(curemindertext, (75, 575))
            removereminderbutton.draw(mainwindow, (0, 0, 0))
            for i in statusbuttonlist:
                if i.text == curreminder.status and i.text == 'No Status':
                    i.color = (128, 128, 128)
                elif i.text == curreminder.status and i.text == 'Incomplete':
                    i.color = (255, 0, 0)
                elif i.text == curreminder.status and i.text == 'Completed':
                    i.color = (0, 200, 0)
                else:
                    i.color = (255, 255, 255)
                i.draw(mainwindow, (0, 0, 0))
        backbutton.draw(mainwindow, (0, 0, 0))

        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                running = False
                savetofile()
                pygame.quit()

            if event.type == pygame.MOUSEMOTION:
                if backbutton.isOver(pos):
                    backbutton.color = (255, 0, 0)
                else:
                    backbutton.color = (255, 255, 255)
                if removereminderbutton.isOver(pos):
                    removereminderbutton.color = (255, 0, 0)
                else:
                    removereminderbutton.color = (255, 255, 255)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if backbutton.isOver(pos):
                    running = False
                    monthscreen(monthindex, mainwindow)
                for i in range(len(reminderbuttonlist)):
                    if reminderbuttonlist[i].isOver(pos):
                        curreminder = YEAR2021[monthindex].listofdays[dayindex].reminders[i]
                        curreminderbutton = reminderbuttonlist[i]
                if curreminder != '':
                    for i in statusbuttonlist:
                        if i.isOver(pos):
                            curreminder.status = i.text
                    if removereminderbutton.isOver(pos):
                        deletereminder(monthindex, dayindex, curreminder.name)
                        dayscreen(monthindex, dayindex, mainwindow, '')
                        running = False

##-------------------------------------------------------------------------------
def newreminder(remindermonth, reminderday, remindername, reminderexplanation, reminderstatus):
    newreminder = Reminder(remindername, YEAR2021[remindermonth - 1].listofdays[reminderday - 1], reminderexplanation, reminderstatus)
    reminderlist.append(newreminder)
    YEAR2021[remindermonth - 1].listofdays[reminderday - 1].reminders.append(newreminder)
    YEAR2021[remindermonth - 1].reminders.append(newreminder)

def deletereminder(monthindex, dayindex, remindername):
    for reminder in reminderlist:
        if reminder.name == remindername and reminder.day == YEAR2021[monthindex].listofdays[dayindex]:
            reminderlist.remove(reminder)
            YEAR2021[monthindex].listofdays[dayindex].reminders.remove(reminder)
            YEAR2021[monthindex].reminders.remove(reminder)

##-------------------------------------------------------------------------------
def readfromfile():
    file = open("Reminders.txt","r")
    for line in file:
        info = line.split("-")
        remindername = info[0]
        remindermonth = int(info[1])
        reminderday = int(info[2])
        reminderexplanation = info[3]
        reminderstatus = info[4]
        reminderstatus = reminderstatus.replace("\n","")
        newreminder = Reminder(remindername, YEAR2021[remindermonth - 1].listofdays[reminderday - 1], reminderexplanation, reminderstatus)
        reminderlist.append(newreminder)
        YEAR2021[remindermonth - 1].listofdays[reminderday - 1].reminders.append(newreminder)
        YEAR2021[remindermonth - 1].reminders.append(newreminder)
        
def savetofile():
    file = open("Reminders.txt","w")
    remindersdata = ""
    for reminder in reminderlist:
        remindersdata = remindersdata + reminder.name+ "-" + str(reminder.day.month) + "-" + str(reminder.day.day) + "-" + str(reminder.explanation) + "-" + str(reminder.status) + "\n"
    file.write(remindersdata)

##-------------------------------------------------------------------------------
















main()
