import io
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

t = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>485</width>
    <height>378</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QPlainTextEdit" name="title">
    <property name="geometry">
     <rect>
      <x>180</x>
      <y>30</y>
      <width>181</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QPlainTextEdit" name="duration">
    <property name="geometry">
     <rect>
      <x>180</x>
      <y>220</y>
      <width>181</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QPlainTextEdit" name="year">
    <property name="geometry">
     <rect>
      <x>180</x>
      <y>90</y>
      <width>181</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QComboBox" name="comboBox">
    <property name="geometry">
     <rect>
      <x>180</x>
      <y>150</y>
      <width>171</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton">
    <property name="geometry">
     <rect>
      <x>170</x>
      <y>280</y>
      <width>93</width>
      <height>28</height>
     </rect>
    </property>
    <property name="text">
     <string>Добавить</string>
    </property>
   </widget>
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>50</x>
      <y>40</y>
      <width>91</width>
      <height>21</height>
     </rect>
    </property>
    <property name="text">
     <string>Название</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>50</x>
      <y>220</y>
      <width>91</width>
      <height>21</height>
     </rect>
    </property>
    <property name="text">
     <string>Длина</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_3">
    <property name="geometry">
     <rect>
      <x>50</x>
      <y>150</y>
      <width>91</width>
      <height>21</height>
     </rect>
    </property>
    <property name="text">
     <string>Жанр</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_4">
    <property name="geometry">
     <rect>
      <x>50</x>
      <y>100</y>
      <width>91</width>
      <height>21</height>
     </rect>
    </property>
    <property name="text">
     <string>Год выпуска</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>485</width>
     <height>26</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>693</width>
    <height>431</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Генерация фильмов</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QPushButton" name="addButton">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>10</y>
      <width>93</width>
      <height>28</height>
     </rect>
    </property>
    <property name="text">
     <string>Добавить</string>
    </property>
   </widget>
   <widget class="QTableWidget" name="tableWidget">
    <property name="geometry">
     <rect>
      <x>30</x>
      <y>61</y>
      <width>641</width>
      <height>301</height>
     </rect>
    </property>
    <column>
     <property name="text">
      <string>ИД</string>
     </property>
    </column>
    <column>
     <property name="text">
      <string>Название фильма</string>
     </property>
    </column>
    <column>
     <property name="text">
      <string>Год выпуска</string>
     </property>
    </column>
    <column>
     <property name="text">
      <string>Жанр</string>
     </property>
    </column>
    <column>
     <property name="text">
      <string>Продолжительность</string>
     </property>
    </column>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>693</width>
     <height>26</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.update_result()
        self.addButton.clicked.connect(self.adding)

    def update_result(self):
        self.con = sqlite3.connect("coffee.sqlite")
        cur = self.con.cursor()
        self.result = cur.execute(
            "SELECT * from coffee").fetchall()
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setColumnCount(len(self.result[0]))
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def adding(self):
        self.add_form = AddWidget(self, int(self.result[0][0]))
        self.add_form.show()
        self.close()


class AddWidget(QMainWindow):
    def __init__(self, *args, parent=None):
        super().__init__(parent)
        self.id = args[1]
        f = io.StringIO(t)
        uic.loadUi(f, self)
        self.pushButton.clicked.connect(self.get_adding_verdict)
        self.con = sqlite3.connect("films_db.sqlite")
        cur = self.con.cursor()
        genres = cur.execute('''SELECT title, id FROM genres''').fetchall()
        self.params = {}
        for i in genres:
            self.comboBox.addItem(i[0])
            self.params[i[0]] = i[1]

    def get_adding_verdict(self):
        if self.title.toPlainText():
            if int(self.year.toPlainText()) <= 2023:
                if int(self.duration.toPlainText()) >= 0:
                    cur = self.con.cursor()
                    id_genre = cur.execute('''SELECT id FROM genres WHERE title=?''',
                                           (self.comboBox.currentText(),)).fetchone()
                    cur.execute(f"""INSERT INTO films
                              (id, title, year, genre, duration)
                              VALUES (?, ?, ?, ?, ?);""", (
                        self.id + 1, self.title.toPlainText(), int(self.year.toPlainText()), id_genre[0],
                        int(self.duration.toPlainText())))
                    self.con.commit()
                    self.second_form = MyWidget()
                    self.second_form.show()
                    self.close()
                    return True
        return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
