import sys
from PyQt5.QtWidgets import QMainWindow, QListWidget, QPushButton, QGridLayout, QWidget, QApplication, QMessageBox
from os import path, walk
from configparser import RawConfigParser, MissingSectionHeaderError, NoSectionError, Error, ParsingError
from pyqtgraph import plot, setConfigOption, BarGraphItem

settings_file = 'settings.ini'

data_folder = None
all_data = list()

months = [(1, "monday"), (2, "tuesday"), (3, "wednesday"), (4, "thursday"), (5, "friday"),
          (6, "saturday"), (7, "sunday")]

hours = [(0.2, "0:12"), (0.4, "0:24"), (0.6, "0:36"), (0.8, "0:48"), (1, "1:00"),
         (1.2, "1:12"), (1.4, "1:24"), (1.6, "1:36"), (1.8, "1:48"), (2, "2:00"),
         (2.2, "2:12"), (2.4, "2:24"), (2.6, "2:36"), (2.8, "2:48"), (3, "3:00"),
         (3.2, "3:12"), (3.4, "3:24"), (3.6, "3:36"), (3.8, "3:48"), (4, "4:00"),
         (4.2, "4:12"), (4.4, "4:24"), (4.6, "4:36"), (4.8, "4:48"), (5, "5:00")]


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Progress manager")
        self.resize(900, 600)

        self.layout = QGridLayout()

        self.widget = QWidget()

        self.plot = plot()

        self.bar_graph = None

        self.list_widget = QListWidget()

        self.update = QPushButton()

        self.UiComponents()

        self.show()

    def UiComponents(self):
        self.plot.setLabel("bottom", "Days of week")
        self.plot.setBackground('w')
        self.plot.setXRange(0, 8)

        ax = self.plot.getAxis("bottom")
        ay = self.plot.getAxis("left")

        ax.setTicks([months])
        ay.setTicks([hours])

        for elm in all_data:
            self.list_widget.addItem(elm.get('name'))
        self.list_widget.itemClicked.connect(self.get_user_info)

        setConfigOption('background', 'w')

        self.update.setText("Update")
        self.update.clicked.connect(self.update_data)

        self.widget.setLayout(self.layout)

        self.layout.addWidget(self.plot, 0, 1, 3, 1)
        self.layout.addWidget(self.list_widget, 0, 0, 2, 1)
        self.layout.addWidget(self.update, 2, 0)

        self.setCentralWidget(self.widget)

    def get_user_info(self, item):
        self.plot.clear()
        for elm in all_data:
            if elm.get('name') == item.text():
                x = [1, 2, 3, 4, 5, 6, 7]
                y = [elm.get("data")["monday"] / 3600,
                     elm.get("data")["tuesday"] / 3600,
                     elm.get("data")["wednesday"] / 3600,
                     elm.get("data")["thursday"] / 3600,
                     elm.get("data")["friday"] / 3600,
                     elm.get("data")["saturday"] / 3600,
                     elm.get("data")["sunday"] / 3600]

                self.bar_graph = BarGraphItem(x=x, height=y, width=0.6, brush='g')

                self.plot.addItem(self.bar_graph)
                self.plot.setTitle(item.text())

    def update_data(self):
        all_data.clear()
        self.list_widget.clear()
        get_data()
        for elm in all_data:
            self.list_widget.addItem(elm.get('name'))
        self.list_widget.itemClicked.connect(self.get_user_info)
        self.plot.clear()


def get_data_from_property(file):
    global all_data

    try:

        try:
            if not path.exists(file):
                raise FileNotFoundError

            config = RawConfigParser()
            config.read(file)
        except FileNotFoundError:
            print('File not found error. Check ' + file + ' in your folder.')
            return False
        except MissingSectionHeaderError:
            print('Missing section header error. Check settings section in ' + file + '. Must be \'[DATA]\'.')
            return False

        # data
        try:
            data = dict(config.items('DATA'))
        except NoSectionError:
            print('No section error. Check \'[DATA]\' section in ' + file + '.')
            return False

        # last_update
        try:
            last_update = float(data['last_update'])
        except ParsingError:
            print('Parsing error. Check \'last_update\' property in ' + file)
            return False
        except ValueError:
            print('Value error. Check \'last_update\' value in ' + file + '. Must be integer or float.')
            return False

        # total_time_left
        try:
            total_time_left = float(data['total_time_left'])
        except ParsingError:
            print('Parsing error. Check \'total_time_left\' property in ' + file)
            return False
        except ValueError:
            print('Value error. Check \'total_time_left\' value in ' + file + '. Must be integer or float.')
            return False

        # over_time
        try:
            over_time = float(data['over_time'])
        except ParsingError:
            print('Parsing error. Check \'over_time\' property in ' + file)
            return False
        except ValueError:
            print('Value error. Check \'over_time\' value in ' + file + '. Must be integer or float.')
            return False

        # progress
        try:
            progress = dict(config.items('PROGRESS'))
        except NoSectionError:
            print('No section error. Check \'[PROGRESS]\' section in ' + file + '.')
            return False

        # monday
        try:
            monday = float(progress['monday'])
        except ParsingError:
            print('Parsing error. Check \'monday\' property in ' + file)
            return False
        except ValueError:
            print('Value error. Check \'monday\' value in ' + file + '. Must be integer or float.')
            return False

        # tuesday
        try:
            tuesday = float(progress['tuesday'])
        except ParsingError:
            print('Parsing error. Check \'tuesday\' property in ' + file)
            return False
        except ValueError:
            print('Value error. Check \'tuesday\' value in ' + file + '. Must be integer or float.')
            return False

        # wednesday
        try:
            wednesday = float(progress['wednesday'])
        except ParsingError:
            print('Parsing error. Check \'wednesday\' property in ' + file)
            return False
        except ValueError:
            print('Value error. Check \'wednesday\' value in ' + file + '. Must be integer or float.')
            return False

        # thursday
        try:
            thursday = float(progress['thursday'])
        except ParsingError:
            print('Parsing error. Check \'thursday\' property in ' + file)
            return False
        except ValueError:
            print('Value error. Check \'thursday\' value in ' + file + '. Must be integer or float.')
            return False

        # friday
        try:
            friday = float(progress['friday'])
        except ParsingError:
            print('Parsing error. Check \'friday\' property in ' + file)
            return False
        except ValueError:
            print('Value error. Check \'friday\' value in ' + file + '. Must be integer or float.')
            return False

        # saturday
        try:
            saturday = float(progress['saturday'])
        except ParsingError:
            print('Parsing error. Check \'saturday\' property in ' + file)
            return False
        except ValueError:
            print('Value error. Check \'saturday\' value in ' + file + '. Must be integer or float.')
            return False

        # sunday
        try:
            sunday = float(progress['sunday'])
        except ParsingError:
            print('Parsing error. Check \'sunday\' property in ' + file)
            return False
        except ValueError:
            print('Value error. Check \'sunday\' value in ' + file + '. Must be integer or float.')
            return False

        all_data.append({"name": path.basename(file).split('.')[0],
                         "data": {"last_update": last_update,
                                  "total_time_left": total_time_left,
                                  "over_time": over_time,
                                  "monday": monday,
                                  "tuesday": tuesday,
                                  "wednesday": wednesday,
                                  "thursday": thursday,
                                  "friday": friday,
                                  "saturday": saturday,
                                  "sunday": sunday}})

    except Error:
        print('Configparser error. File ' + file)


def get_data():
    global settings_file, data_folder

    try:

        try:
            if not path.exists(settings_file):
                raise FileNotFoundError

            config = RawConfigParser()
            config.read(settings_file)
        except FileNotFoundError:
            msg = 'File not found error. Check ' + settings_file + ' in your folder.'
            print(msg)
            return False, msg
        except MissingSectionHeaderError:
            msg = 'Missing section header error. Check settings section in ' + settings_file +\
                  '. Must be \'[SETTINGS]\'.'
            print(msg)
            return False, msg

        try:
            settings = dict(config.items('SETTINGS'))
        except NoSectionError:
            msg = 'No section error. Check \'[SETTINGS]\' section in ' + settings_file + '.'
            print(msg)
            return False, msg

        try:
            data_folder = settings['data_location']
        except ParsingError:
            msg = 'Parsing error. Check \'data_info_file\' property in ' + settings_file
            print(msg)
            return False, msg
        except ValueError:
            msg = 'Value error. Check \'data_info_file\' value in ' + settings_file + '. Must be string.'
            print(msg)
            return False, msg

    except Error:
        msg = 'Configparser error. File ' + settings_file
        print(msg)
        return False, msg

    if not path.exists(data_folder):
        msg = 'Folder ' + data_folder + ' doesn\'t exist.'
        return False, msg

    for root, dirs, files in walk(data_folder):
        for file in files:
            if file.endswith('.properties'):
                property_file = path.join(root, file)
                get_data_from_property(property_file)

    return True, None


if __name__ == '__main__':
    App = QApplication(sys.argv)
    res, msg = get_data()
    if not res:
        QMessageBox.about(QMainWindow(), 'Error!', msg)
    else:
        window = Window()
        sys.exit(App.exec())
