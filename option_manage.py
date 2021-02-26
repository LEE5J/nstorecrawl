from PyQt5 import uic
from tools import *
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidget, QPushButton, QLabel

form_class2 = uic.loadUiType(resource_path("optionselect.ui"))[0]

#  수정기능인데 설계 문제로 인하여 일시 보류
class option_frame(QDialog, form_class2):
    def __init__(self, option_list=None):
        super().__init__()
        self.setupUi(self)
        self.option_list = option_list
        self.parse_item()
        self.show()

    def parse_item(self):
        self.option_table.setRowCount(len(self.option_list))
        for i in range(len(self.option_list)):
            self.option_table.setCellWidget(i, 0, QLabel(self.option_list[i][0]))
            self.option_table.setCellWidget(i, 1, QLabel(self.option_list[i][1]))
            self.option_table.setCellWidget(i, 2, QLabel(self.option_list[i][2]))
            self.option_table.setCellWidget(i, 3, QLabel(str(self.option_list[i][3])))
            self.option_table.setCellWidget(i, 4, self.delete_btn(i))
        self.option_table.resizeColumnsToContents()

    def delete_btn(self, index):
        btn = QPushButton(text="삭제")
        btn.pressed.connect(lambda: self.delete_item(index))
        return btn

    def delete_item(self, index):
        self.option_list.pop(index)
        self.parse_item()

if __name__ == '__main__':
    test_option_list = [['1', 'a', 'A', 10000], ['1', 'a', 'B', 10000], ['1', 'b', 'A', 10000], ['1', 'b', 'B', 10000],
                        ['2', 'a', 'A', 10000], ['2', 'a', 'B', 10000], ['2', 'b', 'A', 10000], ['2', 'b', 'B', 10000]]
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = option_frame(test_option_list)
    sys.exit(app.exec_())
