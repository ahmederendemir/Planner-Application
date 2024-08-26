from PyQt5.QtWidgets import QWidget,QApplication,QListWidgetItem,QMessageBox
from PyQt5.uic import loadUi
import sys
from PyQt5.QtCore import Qt
import sqlite3
tasks=["write email","read a book"]
class Application(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("planner.ui",self)
        self.calendarWidget.selectionChanged.connect(self.datechanged)
        self.SaveButton.clicked.connect(self.savebutton)
        self.AddTaskButton.clicked.connect(self.addtask)
        self.DeleteButton.clicked.connect(self.delete)

        
    def updateTasks(self,date):
        self.listWidget.clear()
        db=sqlite3.connect("datab.db")
        cursor=db.cursor()
        query="SELECT Task,Completed FROM db WHERE Date=?"
        where=(date,)
        result=cursor.execute(query,where).fetchall()

        for i in result:
            item=QListWidgetItem(i[0])
            if i[1] == "YES":
                item.setCheckState(Qt.Checked)
            elif i[1] == "NO":
                item.setCheckState(Qt.Unchecked)
            self.listWidget.addItem(item)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)

    def datechanged(self):
        
        datei=self.calendarWidget.selectedDate().toPyDate()
        self.updateTasks(datei)
    
    def savebutton(self):
        datei=self.calendarWidget.selectedDate().toPyDate()
        db=sqlite3.connect("datab.db")
        cursor=db.cursor()

        for i in range(self.listWidget.count()):
            item=self.listWidget.item(i)
            task=item.text()
            if item.checkState()==Qt.Checked:
                query="UPDATE db SET Completed='YES' WHERE Task=? AND Date=?"
            else:
                query="UPDATE db SET Completed='NO' WHERE Task=? AND Date=?"
            row=(task,datei,)
            cursor.execute(query,row)
            db.commit()

        messageBox = QMessageBox()
        messageBox. setText("Changes saved.")
        messageBox.setStandardButtons (QMessageBox.Ok)
        messageBox. exec()
    def addtask(self):
        db = sqlite3.connect("datab.db")
        cursor = db. cursor()
        new = str(self.lineEdit.text())
        datei=self.calendarWidget.selectedDate().toPyDate()
        query = "INSERT INTO db(Task, Completed, Date) VALUES (?,?,?)"
        row = (new, "NO", datei, )
        cursor.execute(query, row)
        db. commit()
        self.lineEdit.clear()
        self.updateTasks(datei)

        messageBox = QMessageBox()
        messageBox. setText("Changes saved.")
        messageBox.setStandardButtons (QMessageBox.Ok)
        messageBox. exec()
    
    def delete(self):
        db = sqlite3.connect("datab.db")
        cursor = db. cursor()
        datei=self.calendarWidget.selectedDate().toPyDate()
        selectedTask=self.listWidget.currentItem().text()
        query="DELETE FROM db WHERE Task=?"
        row=(selectedTask,)
        cursor.execute(query, row)
        db. commit()
        self.updateTasks(datei)

        messageBox = QMessageBox()
        messageBox. setText("Changes saved.")
        messageBox.setStandardButtons (QMessageBox.Ok)
        messageBox. exec()

if __name__=="__main__":
    app=QApplication(sys.argv)
    application=Application()
    application.show()
    sys.exit(app.exec())
