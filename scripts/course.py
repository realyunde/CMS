import sys


def main():
    filename = sys.argv[1]
    fo = open(filename, 'rb')
    sql = "INSERT INTO `table` (`id`, `name`) VALUES\n"
    while True:
        line = fo.readline().strip(b'\r\n')
        if len(line) == 0:
            break
        line = line.decode('utf-8')
        row = line.split(',')
        sql += "('{}', '{}'), \n".format(row[0], row[1])
    fo.close()
    print(sql)


if __name__ == '__main__':
    main()
