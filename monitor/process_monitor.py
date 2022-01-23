from os import path, system
from time import sleep
from psutil import process_iter
from datetime import timedelta, datetime, date
from configparser import RawConfigParser, MissingSectionHeaderError, NoSectionError, ParsingError, Error
from logging import getLogger, FileHandler, Formatter, INFO
from inspect import getfile, currentframe

settings_file = 'settings.ini'

# Settings
apps = None
data_info_file = None
log_file = None
weekly_working_time = None
time_delay = None
logger_delay = None

# Data
last_update = None
total_time_left = None
over_time = None

# Progress
monday = None
tuesday = None
wednesday = None
thursday = None
friday = None
saturday = None
sunday = None

logger_timer = 0
logger = None

today_time_left = 0
today_over_time = 0


apps_list = list()


def logger_init(log):
    global logger

    try:

        if not path.exists(log):
            f = open(log, 'w')
            f.close()

        logger = getLogger(apps)
        logger.setLevel(INFO)
        fh = FileHandler(log)
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        return True

    except FileNotFoundError:
        print('File not found error. Check ' + log + ' in your folder.')
        return False


def getDataFromSettings(file):
    global apps, apps_list, data_info_file, log_file, weekly_working_time, time_delay, logger_delay

    try:

        # config
        try:
            if not path.exists(file):
                raise FileNotFoundError

            config = RawConfigParser()
            config.read(file)
        except FileNotFoundError:
            print('File not found error. Check ' + file + ' in your folder.')
            return False
        except MissingSectionHeaderError:
            print('Missing section header error. Check settings section in ' + file + '. Must be \'[SETTINGS]\'.')
            return False

        # settings
        try:
            settings = dict(config.items('SETTINGS'))
        except NoSectionError:
            print('No section error. Check \'[SETTINGS]\' section in ' + file + '.')
            return False

        # app
        try:
            apps = settings['apps']
            for app in apps.split(' '):
                apps_list.append({"app": app, "user": None, "prev_user": None})

        except ParsingError:
            print('Parsing error. Check \'app\' property in ' + file)
            return False
        except ValueError:
            print('Value error. Check \'app\' value in ' + file + '. Must be string.')
            return False

        # data_info_file
        try:
            data_info_file = settings['data_file'] + '.properties'
        except ParsingError:
            print('Parsing error. Check \'data_info_file\' property in ' + file)
            return False
        except ValueError:
            print('Value error. Check \'data_info_file\' value in ' + file + '. Must be string.')
            return False

        # log_file
        try:
            log_file = settings['data_file'] + '.log'
        except ParsingError:
            print('Parsing error. Check \'log_file\' property in ' + file)
            return False
        except ValueError:
            print('Value error. Check \'log_file\' value in ' + file + '. Must be string.')
            return False

        # weekly_working_time
        try:
            weekly_working_time = float(settings['weekly_working_time'])
        except ParsingError:
            print('Parsing error. Check \'weekly_working_time\' property in ' + file)
            return False
        except ValueError:
            print('Value error. Check \'weekly_working_time\' value in ' + file + '. Must be integer or float.')
            return False

        # time_delay
        try:
            time_delay = int(settings['time_delay'])
        except ParsingError:
            print('Parsing error. Check \'time_delay\' property in ' + file)
            return False
        except ValueError:
            print('Value error. Check \'time_delay\' value in ' + file + '. Must be integer.')
            return False

        # logger_delay
        try:
            logger_delay = int(settings['logger_delay'])
        except ParsingError:
            print('Parsing error. Check \'logger_delay\' property in ' + file)
            return False
        except ValueError:
            print('Value error. Check \'logger_delay\' value in ' + file + '. Must be integer.')
            return False

    except Error:
        print('Configparser error. File ' + file)

    return True


def getDataFromData(file):
    global last_update, total_time_left, over_time, monday, tuesday, wednesday, thursday, friday, saturday, sunday

    try:

        # config
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

    except Error:
        print('Configparser error. File ' + file)

    return True


def setDataToFile(file):
    global last_update, total_time_left, over_time, monday, tuesday, wednesday, thursday, friday, saturday, sunday

    config = RawConfigParser()
    config.read(file)

    config.set('DATA', 'last_update', last_update)
    config.set('DATA', 'total_time_left', total_time_left)
    config.set('DATA', 'over_time', over_time)

    config.set('PROGRESS', 'monday', monday)
    config.set('PROGRESS', 'tuesday', tuesday)
    config.set('PROGRESS', 'wednesday', wednesday)
    config.set('PROGRESS', 'thursday', thursday)
    config.set('PROGRESS', 'friday', friday)
    config.set('PROGRESS', 'saturday', saturday)
    config.set('PROGRESS', 'sunday', sunday)

    with open(file, 'w') as f:
        config.write(f)


def getAllProcesses():
    list_of_process_names = list()
    for proc in process_iter():
        p_info_dict = proc.as_dict(attrs=['cpu_times', 'name'])
        list_of_process_names.append(p_info_dict)
    return list_of_process_names


def getProcessInfo(process):
    try:
        processes = list()
        for proc in getAllProcesses():
            if proc['name'] in process:
                processes.append(proc)

        if len(processes) == 1:
            return processes[0]['cpu_times'].user
        else:
            temp = None
            for proc in processes:
                if temp is None:
                    temp = proc['cpu_times'].user
                elif temp > proc['cpu_times'].user:
                    return temp
                else:
                    return proc['cpu_times'].user
    except Exception:
        print('Unknown exception occurred. Error in getProcessInfo().')
        logger.error('Unknown exception occurred. Error in getProcessInfo().')
        return None


def printInfo(today):
    system('CLS')
    if total_time_left > 0:
        print('\033[32m{}'.format('Total time left: ' + timedelta(seconds=int(total_time_left)).__str__()))
    else:
        print('\033[33m{}'.format('Overtime: ' + timedelta(seconds=int(over_time)).__str__()))

    print()
    if today == 0:
        print('\033[32m{}'.format('Monday: ' + timedelta(seconds=int(monday)).__str__()))
    else:
        print('\033[37m{}'.format('Monday: ' + timedelta(seconds=int(monday)).__str__()))
    if today == 1:
        print('\033[32m{}'.format('Tuesday: ' + timedelta(seconds=int(tuesday)).__str__()))
    else:
        print('\033[37m{}'.format('Tuesday: ' + timedelta(seconds=int(tuesday)).__str__()))
    if today == 2:
        print('\033[32m{}'.format('Wednesday: ' + timedelta(seconds=int(wednesday)).__str__()))
    else:
        print('\033[37m{}'.format('Wednesday: ' + timedelta(seconds=int(wednesday)).__str__()))
    if today == 3:
        print('\033[32m{}'.format('Thursday: ' + timedelta(seconds=int(thursday)).__str__()))
    else:
        print('\033[37m{}'.format('Thursday: ' + timedelta(seconds=int(thursday)).__str__()))
    if today == 4:
        print('\033[32m{}'.format('Friday: ' + timedelta(seconds=int(friday)).__str__()))
    else:
        print('\033[37m{}'.format('Friday: ' + timedelta(seconds=int(friday)).__str__()))
    if today == 5:
        print('\033[32m{}'.format('Saturday: ' + timedelta(seconds=int(saturday)).__str__()))
    else:
        print('\033[37m{}'.format('Saturday: ' + timedelta(seconds=int(saturday)).__str__()))
    if today == 6:
        print('\033[32m{}'.format('Sunday: ' + timedelta(seconds=int(sunday)).__str__()))
    else:
        print('\033[37m{}'.format('Sunday: ' + timedelta(seconds=int(sunday)).__str__()))


def timedelta_to_str(time):
    time_str = str(timedelta(seconds=int(time)))
    if time_str.__contains__('days,'):
        time_str = time_str.replace('days,', ':').replace(' ', '')
    elif time_str.__contains__('day'):
        time_str = time_str.replace('day,', ':').replace(' ', '')
    return time_str


def logInfo(weekday):
    global logger, logger_timer, logger_delay

    if logger_timer >= logger_delay:
        if total_time_left > 0:
            logger.info('Total time left: ' + timedelta_to_str(total_time_left))
        else:
            logger.info('Overtime: ' + timedelta_to_str(over_time))

        if weekday == 0:
            logger.info('Monday: ' + timedelta_to_str(monday))
        elif weekday == 1:
            logger.info('Tuesday: ' + timedelta_to_str(tuesday))
        elif weekday == 2:
            logger.info('Wednesday: ' + timedelta_to_str(wednesday))
        elif weekday == 3:
            logger.info('Thursday: ' + timedelta_to_str(thursday))
        elif weekday == 4:
            logger.info('Friday: ' + timedelta_to_str(friday))
        elif weekday == 5:
            logger.info('Saturday: ' + timedelta_to_str(saturday))
        elif weekday == 6:
            logger.info('Sunday: ' + timedelta_to_str(sunday))

        logger_timer = 0
    else:
        logger_timer += 1


def set_weekday(weekday, delay):
    global monday, tuesday, wednesday, thursday, friday, saturday, sunday

    if weekday == 0:
        monday += delay
    elif weekday == 1:
        tuesday += delay
    elif weekday == 2:
        wednesday += delay
    elif weekday == 3:
        thursday += delay
    elif weekday == 4:
        friday += delay
    elif weekday == 5:
        saturday += delay
    elif weekday == 6:
        sunday += delay


def checkLastUpdate():
    global last_update, total_time_left, weekly_working_time, over_time, monday, tuesday, wednesday, thursday, friday, \
        saturday, sunday

    now = datetime.now()

    if last_update == 0:
        last_update = now.timestamp()
        return

    if now.weekday() == 0 and timedelta(seconds=(now.timestamp() - last_update)).days >= 1:
        total_time_left = total_time_left + weekly_working_time - over_time
        over_time = 0
        monday = 0
        tuesday = 0
        wednesday = 0
        thursday = 0
        friday = 0
        saturday = 0
        sunday = 0
        last_update = now.timestamp()


def checkProcessUpdate():
    global apps_list

    for app in apps_list:
        app['user'] = getProcessInfo(app['app'])
        if app['user'] is not None and app['prev_user'] is None:
            app['prev_user'] = app['user']
            return True
        elif app['user'] is None and app['prev_user'] is not None:
            app['prev_user'] = None
        elif app['user'] is not None and app['prev_user'] is not None:
            if app['user'] > app['prev_user']:
                app['prev_user'] = app['user']
                return True

    return False


def main(delay):
    global apps_list, total_time_left, over_time, time_delay, weekly_working_time, today_time_left, today_over_time

    before_change = None
    without_work = 0

    checkLastUpdate()
    today = datetime.today().weekday()

    while True:
        if before_change is None:
            before_change = datetime.now()

        if checkProcessUpdate():
            if without_work >= time_delay:
                without_work = 0
                before_change = datetime.now()

            if total_time_left > 0:
                t_delay = datetime.now().timestamp() - before_change.timestamp()
                before_change = datetime.now()
                total_time_left -= t_delay
                set_weekday(today, t_delay)
            else:
                t_delay = datetime.now().timestamp() - before_change.timestamp()
                before_change = datetime.now()
                over_time += t_delay
                set_weekday(today, t_delay)
        elif without_work < time_delay:
            t_delay = datetime.now().timestamp() - before_change.timestamp()
            before_change = datetime.now()
            without_work += t_delay
            if total_time_left > 0:
                total_time_left -= t_delay
            else:
                over_time += t_delay
            set_weekday(today, t_delay)

        setDataToFile(data_info_file)
        printInfo(today)
        logInfo(today)
        sleep(delay)


if __name__ == '__main__':
    if getDataFromSettings(path.join(path.dirname(path.abspath(getfile(currentframe()))), settings_file)):
        if logger_init(log_file):
            if getDataFromData(data_info_file):
                main(1)
