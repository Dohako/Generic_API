from base_handler import BaseHandler


def main():
    base = BaseHandler('adjust')
    sql = 'select * from data;'
    string = base.get_data(sql)
    print(string[1])


if __name__ == '__main__':
    main()