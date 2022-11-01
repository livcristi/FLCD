from Scanner import Scanner

if __name__ == '__main__':
    scanner = Scanner()

    pif, id_table, const_table = scanner.scan_file('p1.pt')
    print(pif)
    print(id_table)
    print(const_table)
    print()