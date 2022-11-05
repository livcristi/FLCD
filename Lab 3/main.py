from Scanner import Scanner

if __name__ == '__main__':
    scanner = Scanner()

    pif, id_table, const_table = scanner.scan_file('p1.pt')
    print("pif = ", pif)
    print("id_table = ", id_table)
    print("const_table = ", const_table)