import sys
from PyQt6.QtWidgets import QApplication, QScrollArea, QFormLayout, QCheckBox, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from cvSources import General, ICAC, Electronics

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # Establish the window geometry
        self.setWindowTitle("JSON load into Tree View")
        self.setFixedSize(810,800)

        self.scroll_area = QScrollArea()
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.scroll_area)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.mainWidget)

        # Establish topical buttons, widgets and layouts
        self.cvICACCB = []
        self.cvICAC = QWidget()
        self.cvICAC.setFixedWidth(770)
        self.cvICAC_l = QFormLayout()
        self.cvICAC_l.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.cvICAC.setLayout(self.cvICAC_l)
        self.cvICAC.hide()
        self.cvICAC_b = QPushButton()
        self.cvICAC_b.setText('ICAC Verbiage')
        self.cvICAC_b.setCheckable(True)
        self.cvICAC_b.setFixedWidth(770)
        self.cvICAC_b.clicked.connect( lambda checked: self.toggle_widget(checked, self.cvICAC) )

        self.cvGenCB = []
        self.cvGen = QWidget()
        self.cvGen.setFixedWidth(770)
        self.cvGen_l = QFormLayout()
        self.cvGen_l.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.cvGen.setLayout(self.cvGen_l)
        self.cvGen.hide()
        self.cvGen_b = QPushButton()
        self.cvGen_b.setText('General Verbiage')
        self.cvGen_b.setCheckable(True)
        self.cvGen_b.setFixedWidth(770)
        self.cvGen_b.clicked.connect( lambda checked: self.toggle_widget(checked, self.cvGen) )

        self.cvElecCB = []
        self.cvElec = QWidget()
        self.cvGen.setFixedWidth(770)
        self.cvElec_l = QFormLayout()
        self.cvElec_l.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.cvElec.setLayout(self.cvElec_l)
        self.cvElec.hide()
        self.cvElec_b = QPushButton()
        self.cvElec_b.setText('Electronics Verbiage')
        self.cvElec_b.setCheckable(True)
        self.cvGen.setFixedWidth(770)
        self.cvElec_b.clicked.connect( lambda checked: self.toggle_widget(checked, self.cvElec) )

        self.mainLayout.addWidget(QLabel("These collapsable lists will auto-populate from source.py"))
        
        self.mainLayout.addWidget(self.cvGen_b)
        self.mainLayout.addWidget(self.cvGen)

        self.mainLayout.addWidget(self.cvICAC_b)
        self.mainLayout.addWidget(self.cvICAC)

        self.mainLayout.addWidget(self.cvElec_b)
        self.mainLayout.addWidget(self.cvElec)

        for index, item in enumerate(General):
            label = QLabel(item)
            label.setFixedWidth(700)
            checkbox = QCheckBox()
            self.cvGenCB.append(checkbox)
            label.setWordWrap(True)
            label.setStyleSheet("border: 2px inset gray; padding: 2px;")
            label.setContentsMargins(5,5,5,5)
            self.cvGen_l.addRow(checkbox, label)
        
        for index, item in enumerate(ICAC):
            label = QLabel(item)
            label.setFixedWidth(700)
            checkbox = QCheckBox()
            self.cvICACCB.append(checkbox)
            label.setWordWrap(True)
            label.setStyleSheet("border: 2px inset gray; padding: 2px;")
            label.setContentsMargins(5,5,5,5)
            self.cvICAC_l.addRow(checkbox, label)
        
        for index, item in enumerate(Electronics):
            label = QLabel(item)
            label.setFixedWidth(700)
            checkbox = QCheckBox()
            self.cvElecCB.append(checkbox)
            label.setWordWrap(True)
            label.setStyleSheet("border: 2px inset gray; padding: 2px;")
            label.setContentsMargins(5,5,5,5)
            self.cvElec_l.addRow(checkbox, label)

    def toggle_widget(self, checked, target):
        if checked:
            target.show()
        else:
            target.hide()
        self.mainWidget.adjustSize()
        self.scroll_area.updateGeometry()





    
    #for index, item in enumerate(ICAC):
    

    #for index, item in enumerate(Electronics):





app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()