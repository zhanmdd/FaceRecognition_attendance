#importing libraries
import face_recognition
import os
from datetime import datetime
import pandas as pd
import wx

#method for encoding the image
#it takes path as argument, which is the address of the photo we want to encode
def encoding(path):
    image = face_recognition.load_image_file(path)
    imageEncoding = face_recognition.face_encodings(image)[0]
    return imageEncoding


#this mehod is for comparing the photo from unkwon folder with all photos in known folder
#it takes 2 arguments, unkownPerson is the path of photo in unknown folder, while nameOfPerson is simple name of photo
def compare(unkownPerson,nameOfPerson):
    isAttendant = False     #it's used to check if the photo from unkown folder is already in known folder
    for image in os.listdir('/Users/AZM/Desktop/Projectss/Face Recognition Attendance/known'): #iterates through photos in the known folder
        if image == '.DS_Store': #checks if the image is the hidden file ".DS_Store" and if yes then it passes and goes to the next file in the folder
            continue
        else:
            known_image_path = '/Users/AZM/Desktop/Projectss/Face Recognition Attendance/known'+image
            result = face_recognition.compare_faces([encoding(known_image_path)],encoding(unkownPerson), tolerance=0.45)
            print(image, str(result))
            if result[0] == True:
                showMessageDialog("Your face matched! You're attended!")
                print("Your face matched! You're attended")
                os.remove(unkownPerson)
                isAttendant = True
                break
    if isAttendant == False:
        print("Oops, it seems that you are not in this class!")
        id = textEntryForId()
        os.rename(unkownPerson, "/Users/AZM/PycharmProjects/COding_class/known/"+str(id)+".jpg")
        addNewStudentToList(id)
        showMessageDialog("you're added successfully!")
        print("You're added successfully!")


def showMessageDialog(message):
        wx.MessageBox("", message, wx.OK | wx.ICON_INFORMATION)

def textEntryForFirstName():
        dlg = wx.TextEntryDialog(None,"Enter your first name: ", "", "Enter your name here")
        if dlg.ShowModal() == wx.ID_OK:
            firstName = dlg.GetValue()
        dlg.Destroy()
        return firstName


def textEntryForLastName():
    dlg = wx.TextEntryDialog(None, "Enter your last name: ", "", "Enter your last name here")
    if dlg.ShowModal() == wx.ID_OK:
        lastName = dlg.GetValue()
    dlg.Destroy()
    return lastName

def textEntryForId():
    dlg = wx.TextEntryDialog(None, "Enter your Id here: ", "", "Enter your Id here")
    if dlg.ShowModal() == wx.ID_OK:
        id = dlg.GetValue()
    dlg.Destroy()
    return id



#method for adding new student to our data frame
def addNewStudentToList(id):
    dataset = pd.read_csv("/Users/AZM/Desktop/Projectss/Face Recognition Attendance/students_dataset.csv")

    firstName = textEntryForFirstName()
    lastName = textEntryForLastName()
    updated = dataset.append({'id': id, 'Name': firstName, 'Last Name': lastName, 'Time Checked': getTheCurrentTime()}, ignore_index=True)
    updated = updated.drop(dataset.columns[0], axis=1)
    updated.to_csv("/Users/AZM/Desktop/Projectss/Face Recognition Attendance/students_dataset.csv")


#method for getting the current time for attendance check time
def getTheCurrentTime():
    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S")
    return currentTime


def mainCompare():
    if len(os.listdir('/Users/AZM/Desktop/Projectss/Face Recognition Attendance/unknown')) - 1 == 0:
        print("There are no pictures")
        showMessageDialog("There are no pictures")
    else:
        for image in os.listdir('//Users/AZM/Desktop/Projectss/Face Recognition Attendance/unknown'):
            if image == '.DS_Store':
                continue
            else:
                return compare('/Users/AZM/Desktop/Projectss/Face Recognition Attendance/unknown' + image, image)


class MyFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Attendance check")
        panel = wx.Panel(self)

        closeBtn = wx.Button(panel, label="EXIT", pos=(315,2))
        closeBtn.Bind(wx.EVT_BUTTON, self.onClose)

        startButton = wx.Button(panel, label = "Start")
        startButton.Bind(wx.EVT_BUTTON,self.start)

    def start(self,event):
        mainCompare()
    #----------------------------------------------------------------------
    def onClose(self, event):
        """"""
        self.Close()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()



ex = wx.App()
ex.MainLoop()