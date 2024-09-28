from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from cvSources import cvDict
from listOfLists import mainDict
import sys

# the hierarchy is something like this:
# cvDict[General][0]
class MainWindow(QMainWindow):

   def __init__(self):
      super().__init__()

      # Establish the tab position and settings
      self.setWindowTitle("ListEater")
      self.setFixedSize(810,800)
      self.mainWidget = QWidget()
      self.mainWidget.setFixedWidth(770)
      self.mainLayout = QVBoxLayout()
      self.mainLayout.setSpacing(15)
      self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
      self.mainWidget.setLayout(self.mainLayout)
      self.mainScroll = QScrollArea()
      self.mainScroll.setWidget(self.mainWidget)
      self.mainScroll.setWidgetResizable(True)
      self.setCentralWidget(self.mainWidget)
        
      self.listDict = {}
      self.cvListOfLists = []

      self.mainLayout.addWidget(QLabel("This page will dynamically ingest and load lists established by a dictionary in a supplemental file."))

      #for list_name, list_items in cvDict.items()
      #   button = QPushButton(f'Show {list_name}:')
      #   button.setFixedWidth(760)
      #   button.setCheckable(True)
      #   button.clicked.connect( lambda checked: self.toggle_widget(list_name) )

         #layout = QFormLayout()
      #   for index, item in enumerate(list_items):
      #      cbList = QCheckBox()
      #      layout.addRow(QLabel(item))

      for list_name, list_items in mainDict.items():
         self.cvListOfLists.append(list_name)
      print(self.cvListOfLists)

      for index, item in enumerate(self.cvListOfLists):
         print(mainDict[item][index])
      

      '''
      for list_name, list_content in listDictionary.items():
         self.listNameWHolder.append(list_name)
         self.listNameLHolder.append(list_name)
         self.listContentHolder.append(list_content)
         button = QPushButton()
         button.setText(list_name)
         button.setFixedWidth(760)
         button.setCheckable(True)
         button.clicked.connect( lambda checked: self.toggle_widget(checked, self.listNameLHolder[list_name]) )
         self.mainLayout.addWidget(button)
         self.listNameLHolder[list_name] = QVBoxLayout()
         self.listNameWHolder[list_name] = QWidget()
         self.mainLayout.addWidget(self.listNameWHolder[list_name])
         for oneLine in list_content:
            widget = QLabel(oneLine)
            widget.setWordWrap(True)
            self.listNameLHolder[list_name].addWidget(widget)
      
      # Establish topical buttons, widgets and layouts for common verbiage tab
      self.cvICACCB = []
      self.cvICAC = QWidget()
      self.cvICAC.setFixedWidth(750)
      self.cvICAC_l = QFormLayout()
      self.cvICAC_l.setAlignment(Qt.AlignmentFlag.AlignLeft)
      self.cvICAC.setLayout(self.cvICAC_l)
      self.cvICAC.hide()
      self.cvICAC_b = QPushButton()
      self.cvICAC_b.setText('ICAC Verbiage')
      self.cvICAC_b.setCheckable(True)
      self.cvICAC_b.setFixedWidth(750)
      self.cvICAC_b.clicked.connect( lambda checked: self.toggle_widget(checked, self.cvICAC) )

      
      for index, item in enumerate(General):
         label = QLabel(item)
         label.setFixedWidth(700)
         checkbox = QCheckBox()
         self.cvGenCB.append(checkbox)
         label.setWordWrap(True)
         label.setStyleSheet("border: 2px inset gray; padding: 2px;")
         label.setContentsMargins(5,5,5,5)
         self.cvGen_l.addRow(checkbox, label)
      '''

   # Toggles the common verbiage topics
   def toggle_widget(self, checked, target):
      if checked:
         target.show()
      else:
         target.hide()
      self.mainWidget.adjustSize()
      self.mainScroll.updateGeometry()
    
app = QApplication(sys.argv)

window = MainWindow()
window.show()

#app.exec()