

from PyQt6 import QtCore, QtGui, QtWidgets

import json
import numpy


# Open the file which contains the preconfig of rotors and reflector, and put the values on the variable of the same name
f = open('values.json')
values = json.load(f)

# initialize alphabet using ASCII 
alphabet = []
for j in range(26):
    alphabet.append(chr(j + 65))
    
    
# set the preconfig of rotors and reflector
rotor1 = values["rotor1"]
rotor2 = values["rotor2"]
rotor3 = values["rotor3"]
reflector = values["reflector"]

# the actual selected rotor to be shifted
position = 0


# the positions of red and blue in the alphabet, rotor 1,2,3 and reflector, respectively, in every encrypt or decrypt action
red = [-1,-1, -1, -1, -1]
blue = [-1,-1, -1, -1, -1]


# a variable to set the order of rotors according to the given key
rotorsOrder = []

rotorsTurn = [0,0,0]
actualRotor = -1



# a function to draw the reflector, rotors and alphabet boxes in the PyQT6 interface
# data is the values of the box (whatever it is), numRows is the number of rows (1 or 2)
# r is the red position (selected value for the going step), b is the blue position (selected value for the back step)
# type represents the type of values (Str o Int)
def boxDraw(data, numRows, r, b, type):

    a = "<html><head></head><body>"
    a += chr(0x256D)
    for i in range(25):
        a += 3*chr(0x2500)
        a += chr(0x252c)
    a += 3*chr(0x2500)
    a += chr(0x256E)
    a += "<br>"
    a += chr(0x2502)
    for i in range(numRows):
        for j in range(26):
            if (numRows == 1):

                if(type == "int" and data[j] >= 0):
                    value = "+" + str(data[j])
                elif(type == "int" and data[j] < 0):
                    value = str(data[j])
                elif (type == "str"):
                    value = data[j]
                if (j == r):
                    a += "<span style='color : red'>"
                elif (j == b):
                    a += "<span style='color : blue'>"
                else:
                    a += "<span>"
                if (len(value) == 1):
                    a= a + ' ' + "" + value +  ' ' + "</span>" + chr(0x2502)
                elif (len(value) == 2):
                    a= a + '' + value +  ' ' + "</span>" + chr(0x2502)
                elif (len(value) == 3):
                    a= a + '' + value +  '</span>' + chr(0x2502)
            else:
                if(data[i][j] >= 0):
                    value = "+" + str(data[i][j])
                else:
                    value = str(data[i][j])
                if (i == 1 and j == r):
                    a += "<span style='color : red'>"
                elif (i == 0 and j == b):
                    a += "<span style='color : blue'>"
                else:
                    a += "<span>"
                if (len(value) == 1):
                    a= a + ' ' + value +  ' </span>' + chr(0x2502)
                elif (len(value) == 2):
                    a= a + '' + value +  ' </span>' + chr(0x2502)
                elif (len(value) == 3):
                    a= a + '' + value +  '</span>' + chr(0x2502)
        if(numRows != 1 and i < numRows - 1):
            a += "<br>"
            a += chr(0x251C) # ├
            for j in range(25):
                a += 3*chr(0x2500)  # ─
                a += chr(0x253c) # ┼
            a += 3*chr(0x2500)
            a += chr(0x2524)
            a += "<br>"
            a += chr(0x2502)
            


    a += "<br>"
    a += chr(0x2570)
    for i in range(25):
        a += 3*chr(0x2500)
        a += chr(0x2534)
    a += 3*chr(0x2500)
    a += chr(0x256F)
    a += "</body></html>"
    return a


# a function to split the given key into three parts, and return a list of three lists, each list is the config a rotor
def KeySplit(key):
    global actualRotor
    k = []
    parts = key.split(" ") # split the key into parts 
    if (len(parts) != 3):   # if the number of parts is greater or less than 3
        return "Erreur : nombre de rotors invalide"


    rotors = []
    for i in range(len(parts)):
        parts[i] = parts[i][1:len(parts[i])-1]
        if(len(parts[i].split(",")) != 3): # if number of values in the rotor config is different of 3
            return "Erreur : nombre de paramètres invalide"

        rotors.append(parts[i].split(",")[0]) # extract rotor index
        if(parts[i].split(",")[1] != "D" and parts[i].split(",")[1] != "G"): # If other letter than G and D
            return "Erreur : Direction invalide."
        if(parts[i].split(",")[2][1:].isnumeric() == False or parts[i].split(",")[2][0] != "-" and parts[i].split(",")[2][0] != "+"):
            return "Erreur : Nombre de décalages invalide."
    if(len(set(rotors)) != len(rotors)): # check if all rotors are different
        return "Erreur : Rotors dupliqués"


    rotor1 = parts[0].split(",")
    rotor2 = parts[1].split(",")
    rotor3 = parts[2].split(",")
    rotors = [rotor1[0], rotor2[0], rotor3[0]]
    for i in range(len(rotors)):
        if (rotors[i] not in {"R1", "R2", "R3"}): # the rotors' names should be R1, R2 or R3, nothing else
            return "Erreur : Nom de rotor invalide."
    k.append(rotor1)
    k.append(rotor2)
    k.append(rotor3)
    for i in range(3):
        if(k[i][0] == "R1"):
            new = [0, k[i][1]]
            rotorsOrder.append(new)

        elif(k[i][0] == "R2"):
            new = [1, k[i][1]]
            rotorsOrder.append(new)
        elif(k[i][0] == "R3"):
            new = [2, k[i][1]]
            rotorsOrder.append(new)
    actualRotor = rotorsOrder[0][0]
    return [rotor1, rotor2, rotor3]





# Initialize the rotors (preconfiguration from the file values.json)
def InitRotors(list, num):
    new = numpy.roll(list, num)
    return new


# Shift the selected rotor (the parameter list) right or left (direction) once
def ShiftRotor(list, direction):
    if (direction == "G"):
        new = numpy.roll(list, 1)
    elif (direction == "D"):
        new = numpy.roll(list, -1)
    return new





    
class Ui_MainWindow(object):
    
    key = "" # the actual key
    actualLetter = 0 # the position of the actual letter the is encrypting/decrypting
    action = "" # the current action (decrypt or encrypt) 
    
    # the default rotors with the key config
    defaultRotor1 = []
    defaultRotor2 = []
    defaultRotor3 = []
    
    # Preparing the interface, creating all the components
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(920, 680)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.reflector = QtWidgets.QLabel(self.centralwidget)
        self.reflector.setGeometry(QtCore.QRect(20, 10, 781, 60))
        self.reflector.setObjectName("reflector")
        self.reflector.setStyleSheet("font: 9pt \"DejaVu Sans Mono\";");
        self.rotor3 = QtWidgets.QLabel(self.centralwidget)
        self.rotor3.setGeometry(QtCore.QRect(20, 80, 781, 65))
        self.rotor3.setObjectName("rotor3")
        self.rotor3.setStyleSheet("font: 9pt \"DejaVu Sans Mono\";");
        self.rotor2 = QtWidgets.QLabel(self.centralwidget)
        self.rotor2.setGeometry(QtCore.QRect(20, 150, 781, 65))
        self.rotor2.setObjectName("rotor2")
        self.rotor2.setStyleSheet("font: 9pt \"DejaVu Sans Mono\";");
        self.rotor1 = QtWidgets.QLabel(self.centralwidget)
        self.rotor1.setGeometry(QtCore.QRect(20, 220, 781, 65))
        self.rotor1.setObjectName("rotor1")
        self.rotor1.setStyleSheet("font: 9pt \"DejaVu Sans Mono\";");
        self.alphabet = QtWidgets.QLabel(self.centralwidget)
        self.alphabet.setGeometry(QtCore.QRect(20, 290, 781, 60))
        self.alphabet.setObjectName("alphabet")
        self.alphabet.setStyleSheet("font: 9pt \"DejaVu Sans Mono\";font-weight:1000;color:white;")
        
        labelStyle = "font: 9pt \"Sawasdee Bold\";color:#b9d6f1; background-color : #252564; border-radius : 15px;padding:20px"
        
        self.refLabel = QtWidgets.QLabel(self.centralwidget)
        self.refLabel.setGeometry(QtCore.QRect(800, 15, 105, 50))
        self.refLabel.setObjectName("refLabel")
        self.refLabel.setStyleSheet(labelStyle)
        self.rotor1Label = QtWidgets.QLabel(self.centralwidget)
        self.rotor1Label.setGeometry(QtCore.QRect(800, 230, 88, 50))
        self.rotor1Label.setObjectName("rotor1Label")
        self.rotor1Label.setStyleSheet(labelStyle)
        self.rotor3Label = QtWidgets.QLabel(self.centralwidget)
        self.rotor3Label.setGeometry(QtCore.QRect(800, 92, 88, 50))
        self.rotor3Label.setObjectName("rotor3Label")
        self.rotor3Label.setStyleSheet(labelStyle)
        self.rotor2Label = QtWidgets.QLabel(self.centralwidget)
        self.rotor2Label.setGeometry(QtCore.QRect(800, 160, 88, 50))
        self.rotor2Label.setObjectName("rotor2Label")
        self.rotor2Label.setStyleSheet(labelStyle); 

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 898, 22))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionR_nitialiser = QtGui.QAction(MainWindow)
        self.actionR_nitialiser.setObjectName("actionR_nitialiser")
        self.actionQuitter = QtGui.QAction(MainWindow)
        self.actionQuitter.setObjectName("actionQuitter")
        self.menuMenu.addAction(self.actionR_nitialiser)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionQuitter)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.keyLabel = QtWidgets.QLabel(self.centralwidget)
        self.keyLabel.setGeometry(QtCore.QRect(270, 360, 31, 21))
        self.keyLabel.setObjectName("keyLabel")
        self.keyInput = QtWidgets.QLineEdit(self.centralwidget)
        self.keyInput.setGeometry(QtCore.QRect(300, 350, 311, 40))
        self.keyInput.setObjectName("keyInput")
        self.keyError = QtWidgets.QLabel(self.centralwidget)
        self.keyError.setGeometry(QtCore.QRect(620, 360, 300, 21))
        self.keyError.setObjectName("keyError")
        
        self.zoneOne = QtWidgets.QTextEdit(self.centralwidget)
        self.zoneOne.setGeometry(QtCore.QRect(50, 420, 769, 70))
        self.zoneOne.setObjectName("zoneOne")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(7, 390, 861, 20))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.configBtn = QtWidgets.QPushButton(self.centralwidget)
        self.configBtn.setGeometry(QtCore.QRect(70, 510, 125, 35))
        self.configBtn.setObjectName("configBtn")
        self.encryptBtn = QtWidgets.QPushButton(self.centralwidget)
        self.encryptBtn.setGeometry(QtCore.QRect(270, 510, 125, 35))
        self.encryptBtn.setObjectName("encryptBtn")
        self.nextStepBtn = QtWidgets.QPushButton(self.centralwidget)
        self.nextStepBtn.setGeometry(QtCore.QRect(470, 510, 125, 35))
        self.nextStepBtn.setObjectName("nextStepBtn")
        self.decryptBtn = QtWidgets.QPushButton(self.centralwidget)
        self.decryptBtn.setGeometry(QtCore.QRect(670, 510, 125, 35))
        self.decryptBtn.setObjectName("decryptBtn")
        self.zoneTwo = QtWidgets.QTextEdit(self.centralwidget)
        self.zoneTwo.setGeometry(QtCore.QRect(50, 560, 769, 70))
        self.zoneTwo.setObjectName("zoneTwo")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 882, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.configBtn.clicked.connect(self.ConfigureEvent)
        self.encryptBtn.clicked.connect(self.EncryptEvent)
        self.nextStepBtn.clicked.connect(lambda:self.NextStepEvent(self.action))
        self.decryptBtn.clicked.connect(self.DecryptEvent)
        self.keyInput.textChanged.connect(self.validKey)
        
        

    # Shift the actual rotor
    def Shift(self):
        global rotor1,rotor2,rotor3
        global rotorsTurn
        global actualRotor
        global position
        global rotorsOrder

        # if the number of shifts of the actual rotor is less than 26 then it will continue to shift
        if(rotorsTurn[actualRotor] < 26):
            if(actualRotor == 0):
                rotor1[0] = ShiftRotor(rotor1[0], rotorsOrder[0][1])
                rotor1[1] = ShiftRotor(rotor1[1], rotorsOrder[0][1])
                rotorsTurn[0] += 1
            elif(actualRotor == 1):
                rotor2[0] = ShiftRotor(rotor2[0], rotorsOrder[1][1])
                rotor2[1] = ShiftRotor(rotor2[1], rotorsOrder[1][1])
                rotorsTurn[1] += 1
            elif(actualRotor == 2):
                rotor3[0] = ShiftRotor(rotor3[0], rotorsOrder[2][1])
                rotor3[1] = ShiftRotor(rotor3[1], rotorsOrder[2][1])
                rotorsTurn[2] += 1
        # else: if we didn't shift all the rotors, we pass to the next rotor according to the order of the key
              # else we come back to the first rotor of the key
           
        else:
            if(position < 2):
                position += 1
                actualRotor = rotorsOrder[position][0]
            else:
                position = 0
                actualRotor = rotorsOrder[0][0]
                rotorsTurn = [0,0,0]

    def validKey(self):
        _translate = QtCore.QCoreApplication.translate

        # split the given key
        res = KeySplit(self.keyInput.text())
        # if the KeySplit return is a string then it's absolutely an error the was returned, it will be displayed in the KeyError label
        if(type(res) is str):
            self.keyInput.setStyleSheet('border :2px solid red')
        # the given key is valid
        else:
            self.keyInput.setStyleSheet('border :2px solid green')
                
    # when clicking on Configuration of Rotors button
    def ConfigureEvent(self):
        global rotor1, rotor2,rotor3
        f = open('values.json')
        # the rotors will be set to the preconfig of the json file first
        values = json.load(f)
        rotor1 = values["rotor1"]
        rotor2 = values["rotor2"]
        rotor3 = values["rotor3"]


        _translate = QtCore.QCoreApplication.translate
        # if the key input is empty
        if(self.keyInput.text() == ""):
            self.keyError.setStyleSheet('color : red')
            self.keyError.setText(_translate("MainWindow", "Veuillez insérer la clé.")) # display the error 
            return
        # if the given key is the same with the last configured key
        elif(self.key == self.keyInput.text()):
            self.keyError.setStyleSheet('color : red')
            self.keyError.setText(_translate("MainWindow", "Clé déjà configurée")) # display the error 
            return
        self.key = self.keyInput.text()

        # split the given key
        res = KeySplit(self.key)
        # if the KeySplit return is a string then it's absolutely an error the was returned, it will be displayed in the KeyError label
        if(type(res) is str):
            self.keyError.setStyleSheet('color : red')
            self.keyError.setText(_translate("MainWindow", res)) # display the error
            self.key = ""
        # the given key is valid
        else:
            self.keyError.setStyleSheet('color : green')
            self.keyError.setText(_translate("MainWindow", "Clé valide"))
            for i in range(len(res)):
                if(res[i][0] == "R1"):
                    rotor1[0] = InitRotors(rotor1[0], int(res[i][2]))
                    rotor1[1] = InitRotors(rotor1[1], int(res[i][2]))
                elif(res[i][0] == "R2"):
                    rotor2[0] = InitRotors(rotor2[0],int(res[i][2]))
                    rotor2[1] = InitRotors(rotor2[1],int(res[i][2]))
                elif(res[i][0] == "R3"):
                    rotor3[0] = InitRotors(rotor3[0],int(res[i][2]))
                    rotor3[1] = InitRotors(rotor3[1],int(res[i][2]))
            self.defaultRotor1 = rotor1.copy()
            self.defaultRotor2 = rotor2.copy()
            self.defaultRotor3 = rotor3.copy()
            self.rotor3.setText(_translate("MainWindow", boxDraw(rotor3, 2, red[3], blue[3],'int')))
            self.rotor2.setText(_translate("MainWindow", boxDraw(rotor2, 2, red[2], blue[2], 'int')))
            self.rotor1.setText(_translate("MainWindow", boxDraw(rotor1, 2, red[1], blue[1], 'int')))

            
    # when clicking on Encrypt button
    def EncryptEvent(self):
        _translate = QtCore.QCoreApplication.translate
        # if no key has been configured
        if(self.key == ""):
            self.keyError.setStyleSheet('color : red')
            self.keyError.setText(_translate("MainWindow", "Rotors non configurés")) 
            return
        if(self.zoneOne.toPlainText() == ""):
            self.keyError.setStyleSheet('color : red')
            self.keyError.setText(_translate("MainWindow", "Le champs de texte est vide.")) 
            return
        self.keyError.setStyleSheet('color : #2f3994')
        self.keyError.setText(_translate("MainWindow", "Encryptage en cours.."))
        self.action = "encrypt"
        self.NextStepEvent("encrypt")
        self.encryptBtn.setText(_translate("MainWindow", "Encrypter tout"))
        self.encryptBtn.clicked.connect(self.EncryptAll)
            
    def EncryptAll(self):
        num = self.actualLetter
        for i in range(len(self.zoneOne.toPlainText()) - num + 1):
            self.NextStepEvent("encrypt")

    def DecryptAll(self):
        num = self.actualLetter
        for i in range(len(self.zoneTwo.toPlainText()) - num + 1):
            self.NextStepEvent("decrypt")

                

    def EncryptLetter(self, letter):

        _translate = QtCore.QCoreApplication.translate
        if(letter in {"", " "}):
            v = letter
        else:
            if(self.actualLetter not in {0}):
                self.Shift()
            list = [alphabet, rotor1[1], rotor2[1], rotor3[1], reflector]
            # Aller
            if (ord(letter) >= 65 and ord(letter) <= 90):
                i = ord(letter) - 65
            elif (ord(letter) >= 97 and ord(letter) <= 122):
                i = ord(letter) - 97
            else:
                self.keyError.setStyleSheet('color : red')
                self.keyError.setText(_translate("MainWindow", "Message invalide"))
                return
            v = 0
            for k in range(len(list)):
                i = (i + v) % 26
                red[k] = i
                if(k > 0):
                    v = list[k][i]
            
            #Retour
            list = [reflector, rotor3[0], rotor2[0], rotor1[0], alphabet]
            for k in range(len(list)):
                if(k != 1):
                    i = (i + v) % 26
                blue[4 - k] = i 
                if(k > 0):
                    v = list[k][i] 
        
        return v
        

    def NextStepEvent(self, action):
        global rotor1,rotor2,rotor3
        global position, actualRotor, rotorsTurn,red,blue
        self.nextStepBtn.setEnabled(True)
        _translate = QtCore.QCoreApplication.translate
        if(self.actualLetter == 0 and action == "encrypt"):
            self.zoneTwo.setText(_translate("MainWindow",""))
        elif(self.actualLetter == 0 and action == "decrypt"):
            self.zoneOne.setText(_translate("MainWindow",""))

        if(action == "encrypt"):
            text = self.zoneOne.toPlainText()
        elif(action == "decrypt"):
            text = self.zoneTwo.toPlainText()
        self.zoneOne.setReadOnly(True)
        self.zoneTwo.setReadOnly(True)
        self.configBtn.setEnabled(False)
        if(action == "encrypt"):
            self.decryptBtn.setEnabled(False)
        else:
            self.encryptBtn.setEnabled(False)

        if(self.actualLetter < len(text)):
            if(action == "encrypt"):   
                self.zoneTwo.setText(_translate("MainWindow", self.zoneTwo.toPlainText() + self.EncryptLetter(text[self.actualLetter])))
            elif(action == "decrypt"):
                self.zoneOne.setText(_translate("MainWindow", self.zoneOne.toPlainText() + self.EncryptLetter(text[self.actualLetter])))
            self.actualLetter += 1
        else:
            self.actualLetter = 0
            self.zoneOne.setReadOnly(False)
            self.zoneTwo.setReadOnly(False)
            self.configBtn.setEnabled(True)
            if(action == "encrypt"):
                self.decryptBtn.setEnabled(True)
            else:
                self.encryptBtn.setEnabled(True)
            self.nextStepBtn.setEnabled(False)
            rotor1 = self.defaultRotor1.copy()
            rotor2 = self.defaultRotor2.copy()
            rotor3 = self.defaultRotor3.copy()
            if(action == "encrypt"):
                self.encryptBtn.setText(_translate("MainWindow", "Encrypter"))
                self.encryptBtn.clicked.connect(self.EncryptEvent)
            else:
                self.decryptBtn.setText(_translate("MainWindow", "Décrypter"))
                self.decryptBtn.clicked.connect(self.DecryptEvent)  
            position = 0
            red = [-1,-1,-1,-1,-1]
            blue = [-1,-1,-1,-1,-1]
            actualRotor = rotorsOrder[0][0]
            rotorsTurn = [0,0,0]
            self.keyError.setStyleSheet('color : green')
            if(action == "encrypt"):
                self.keyError.setText(_translate("MainWindow", "Encryptage terminé !"))
            elif(action == "decrypt"):
                self.keyError.setText(_translate("MainWindow", "Décryptage terminé !"))


        self.reflector.setText(_translate("MainWindow", boxDraw(reflector, 1, red[4], blue[4], 'int')))
        self.rotor3.setText(_translate("MainWindow", boxDraw(rotor3, 2, red[3], blue[3],'int')))
        self.rotor2.setText(_translate("MainWindow", boxDraw(rotor2, 2, red[2], blue[2], 'int')))
        self.rotor1.setText(_translate("MainWindow", boxDraw(rotor1, 2, red[1], blue[1], 'int')))
        self.alphabet.setText(_translate("MainWindow", boxDraw(alphabet, 1, red[0], blue[0], 'str')))
        





    def DecryptEvent(self):
        _translate = QtCore.QCoreApplication.translate
        if(self.key == ""):
            self.keyError.setStyleSheet('color : red')
            self.keyError.setText(_translate("MainWindow", "Rotors non configurés")) 
            return
        if(self.zoneTwo.toPlainText() == ""):
            self.keyError.setStyleSheet('color : red')
            self.keyError.setText(_translate("MainWindow", "Le champs de texte est vide.")) 
            return
        self.keyError.setStyleSheet('color : #2f3994')
        self.keyError.setText(_translate("MainWindow", "Décryptage en cours.."))
        self.action = "decrypt"
        self.NextStepEvent("decrypt")
        self.decryptBtn.setText(_translate("MainWindow", "Décrypter tout"))
        self.decryptBtn.clicked.connect(self.DecryptAll)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Enigma"))
        MainWindow.setWindowIcon(QtGui.QIcon('logo.png'))

        self.reflector.setText(_translate("MainWindow", boxDraw(reflector, 1, red[4], blue[4], 'int')))
        self.rotor3.setText(_translate("MainWindow", boxDraw(rotor3, 2, red[3], blue[3],'int')))
        self.rotor2.setText(_translate("MainWindow", boxDraw(rotor2, 2, red[2], blue[2], 'int')))
        self.rotor1.setText(_translate("MainWindow", boxDraw(rotor1, 2, red[1], blue[1], 'int')))
        self.alphabet.setText(_translate("MainWindow", boxDraw(alphabet, 1, red[0], blue[0], 'str')))
        self.refLabel.setText(_translate("MainWindow", "Reflecteur"))
        self.rotor1Label.setText(_translate("MainWindow", "Rotor 1"))
        self.rotor3Label.setText(_translate("MainWindow", "Rotor 3"))
        self.rotor2Label.setText(_translate("MainWindow", "Rotor 2"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionR_nitialiser.setText(_translate("MainWindow", "Rénitialiser"))
        self.actionQuitter.setText(_translate("MainWindow", "Quitter"))
        self.keyLabel.setText(_translate("MainWindow", "Clé : "))
        self.keyError.setText(_translate("MainWindow", ""))
        self.keyInput.setPlaceholderText(_translate("MainWindow", "Ex : (R3, G, +7) (R2, D, -6) (R1, D, +5)"))
        self.zoneOne.setPlaceholderText(_translate("MainWindow", "Taper un message à encrypter ou affichage du résultat de décryption"))
        self.configBtn.setText(_translate("MainWindow", "Configurer Rotors"))
        self.encryptBtn.setText(_translate("MainWindow", "Encrypter"))
        self.nextStepBtn.setText(_translate("MainWindow", "Etape suivante"))
        self.decryptBtn.setText(_translate("MainWindow", "Décrypter"))
        self.zoneTwo.setPlaceholderText(_translate("MainWindow", "Taper un message à décrypter ou affichage du résultat d\'encryption"))
        self.nextStepBtn.setEnabled(False)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    with open('style.css', 'r') as f:
        style = f.read()
        # set the stylesheet of the interface
        app.setStyleSheet(style)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
