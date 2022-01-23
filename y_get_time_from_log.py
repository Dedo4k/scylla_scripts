import argparse
from datetime import datetime, timedelta
from configparser import RawConfigParser, MissingSectionHeaderError, NoSectionError, ParsingError, Error


def t_sum(day):
    result = day[0]
    for elm in day:
        if elm == day[0]:
            continue
        result += elm
    return result


def main(log, prop):
    i = 0
    with open(log, 'r') as f:
        lines = f.readlines()
        flag = False
        for line in reversed(lines):
            if line.__contains__('Monday'):
                flag = True
            elif flag is True and not line.__contains__('Monday') and not line.__contains__(
                    'Total time left') and not line.__contains__('ERROR'):
                break
            i += 1

        lines = [[y.strip() for y in x] for x in
                 [z.split('-')[-1].split(':', 1) for z in lines[len(lines) - i:]
                  if not z.__contains__('ERROR')]]

        total_time_left = None
        monday = None
        tuesday = None
        wednesday = None
        thursday = None
        friday = None
        saturday = None
        sunday = None

        for line in lines:
            try:
                d = datetime.strptime(line[1], '%d:%H:%M:%S')
                da = timedelta(days=d.day, hours=d.hour, minutes=d.minute, seconds=d.second)
            except ValueError:
                d = datetime.strptime(line[1], '%H:%M:%S')
                da = timedelta(hours=d.hour, minutes=d.minute, seconds=d.second)
            if line[0].__eq__('Total time left'):
                if total_time_left is None:
                    total_time_left = [{'start': da, 'end': None}]
                elif total_time_left[len(total_time_left) - 1]['end'] is None:
                    total_time_left[len(total_time_left) - 1]['end'] = da
                elif total_time_left[len(total_time_left) - 1]['end'] >= da:
                    total_time_left[len(total_time_left) - 1]['end'] = da
                else:
                    total_time_left.append({'start': da, 'end': None})

            elif line[0].__eq__('Monday'):
                if monday is None:
                    monday = [da]
                elif monday[len(monday) - 1] <= da:
                    monday[len(monday) - 1] = da
                else:
                    monday.append(da)
            elif line[0].__eq__('Tuesday'):
                if tuesday is None:
                    tuesday = [da]
                elif tuesday[len(tuesday) - 1] <= da:
                    tuesday[len(tuesday) - 1] = da
                else:
                    tuesday.append(da)
            elif line[0].__eq__('Wednesday'):
                if wednesday is None:
                    wednesday = [da]
                elif wednesday[len(wednesday) - 1] <= da:
                    wednesday[len(wednesday) - 1] = da
                else:
                    wednesday.append(da)
            elif line[0].__eq__('Thursday'):
                if thursday is None:
                    thursday = [da]
                elif thursday[len(thursday) - 1] <= da:
                    thursday[len(thursday) - 1] = da
                else:
                    thursday.append(da)
            elif line[0].__eq__('Friday'):
                if friday is None:
                    friday = [da]
                elif friday[len(friday) - 1] <= da:
                    friday[len(friday) - 1] = da
                else:
                    friday.append(da)
            elif line[0].__eq__('Saturday'):
                if saturday is None:
                    saturday = [da]
                elif saturday[len(saturday) - 1] <= da:
                    saturday[len(saturday) - 1] = da
                else:
                    saturday.append(da)
            elif line[0].__eq__('Sunday'):
                if sunday is None:
                    sunday = [da]
                elif sunday[len(sunday) - 1] <= da:
                    sunday[len(sunday) - 1] = da
                else:
                    sunday.append(da)

        result = timedelta()
        d_result = timedelta()
        for elm in total_time_left:
            print('Start time:', elm['start'])
            print('End time:', elm['end'])
            diff = elm['start'] - elm['end']
            result += diff
            print('Total time diff:', diff)
        print('Total diff for all periods:', result)
        m_sum = 0.0
        tu_sum = 0.0
        w_sum = 0.0
        th_sum = 0.0
        f_sum = 0.0
        s_sum = 0.0
        su_sum = 0.0
        try:
            m_sum = t_sum(monday)
            d_result += m_sum
            print('Monday:', m_sum)
            m_sum = m_sum.seconds
        except TypeError:
            pass
        try:
            tu_sum = t_sum(tuesday)
            d_result += tu_sum
            print('Tuesday:', tu_sum)
            tu_sum = tu_sum.seconds
        except TypeError:
            pass
        try:
            w_sum = t_sum(wednesday)
            d_result += w_sum
            print('Wednesday:', w_sum)
            w_sum = w_sum.seconds
        except TypeError:
            pass
        try:
            th_sum = t_sum(thursday)
            d_result += th_sum
            print('Thursday:', th_sum)
            th_sum = th_sum.seconds
        except TypeError:
            pass
        try:
            f_sum = t_sum(friday)
            d_result += f_sum
            print('Friday:', f_sum)
            f_sum = f_sum.seconds
        except TypeError:
            pass
        try:
            s_sum = t_sum(saturday)
            d_result += s_sum
            print('Saturday:', s_sum)
            s_sum = s_sum.seconds
        except TypeError:
            pass
        try:
            su_sum = t_sum(sunday)
            d_result += su_sum
            print('Sunday:', su_sum)
            su_sum = su_sum.seconds
        except TypeError:
            pass
        print('Total time by days:', d_result)

        if ask_user():
            reset_property(prop, total_time_left[len(total_time_left) - 1]['end'],
                           m_sum, tu_sum, w_sum, th_sum, f_sum, s_sum, su_sum)
            print('Property file was updated.')


def ask_user():
    check = str(input("\nDo you want to reset the property file? (Y/N): ")).lower().strip()
    try:
        if check == 'y':
            return True
        elif check == 'n':
            return False
        else:
            print('Invalid Input')
            return ask_user()
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return ask_user()


def reset_property(file, total_time_left,
                   monday,
                   tuesday,
                   wednesday,
                   thursday,
                   friday,
                   saturday,
                   sunday):
    try:
        config = RawConfigParser()
        config['DATA'] = {'last_update': '',
                          'total_time_left': '',
                          'over_time': ''}
        config.set('DATA', 'last_update', datetime.now().timestamp().__str__())
        config.set('DATA', 'total_time_left', total_time_left.seconds.__str__())
        config.set('DATA', 'over_time', str(0.0))

        config['PROGRESS'] = {'monday': '',
                              'tuesday': '',
                              'wednesday': '',
                              'thursday': '',
                              'friday': '',
                              'saturday': '',
                              'sunday': ''}
        config.set('PROGRESS', 'monday', monday.__str__())
        config.set('PROGRESS', 'tuesday', tuesday.__str__())
        config.set('PROGRESS', 'wednesday', wednesday.__str__())
        config.set('PROGRESS', 'thursday', thursday.__str__())
        config.set('PROGRESS', 'friday', friday.__str__())
        config.set('PROGRESS', 'saturday', saturday.__str__())
        config.set('PROGRESS', 'sunday', sunday.__str__())

        with open(file, 'w') as f:
            config.write(f)

    except Exception:
        print('Unknown exception occurred. File:', file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', dest='log', nargs='?', required=True)
    parser.add_argument('-p', '--prop', dest='prop', nargs='?', required=True)
    main(parser.parse_args().log, parser.parse_args().prop)
    # input('Press ENTER...')
