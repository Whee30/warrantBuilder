from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class ListWindow(QWidget):
    def __init__(self, mainDict):
        super().__init__()

        # Set up main layout for the window
        self.main_layout = QVBoxLayout()

        # Keep track of the list layouts
        self.list_layouts = {}

        # Create buttons and layouts for each list
        for list_name, list_items in mainDict.items():
            # Create a button for the list
            button = QPushButton(f"Show {list_name}")
            button.clicked.connect(lambda checked, name=list_name: self.toggle_layout(name))
            
            # Create a QVBoxLayout for each list's items
            layout = QVBoxLayout()
            for item in list_items:
                layout.addWidget(QLabel(str(item)))
            layout_widget = QWidget()  # Create a widget to hold the layout
            layout_widget.setLayout(layout)
            layout_widget.setVisible(False)  # Initially hidden

            # Store the layout widget for toggling later
            self.list_layouts[list_name] = layout_widget

            # Add the button and layout to the main layout
            self.main_layout.addWidget(button)
            self.main_layout.addWidget(layout_widget)

        self.setLayout(self.main_layout)

    def toggle_layout(self, list_name):
        """Toggle the visibility of the corresponding layout."""
        layout_widget = self.list_layouts[list_name]
        layout_widget.setVisible(not layout_widget.isVisible())

if __name__ == '__main__':
    app = QApplication([])

    # Example dictionary populated by lists
    mainDict = {
        'list1': ['Item 1.1', 'Item 1.2', 'Item 1.3'],
        'list2': ['Item 2.1', 'Item 2.2', 'Item 2.3'],
        'list3': ['Item 3.1', 'Item 3.2', 'Item 3.3']
    }

    window = ListWindow(mainDict)
    window.show()

    app.exec()
