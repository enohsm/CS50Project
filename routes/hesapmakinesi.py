def main():
    islem = ''
    while not islem or islem not in ['+', '-', '/', '*']:
        islem = input('İşlem? (örn; + - / *): ')
        
    x = int(input('X: '))
    y = int(input('Y: '))

    match islem:
        case '+':
            t = x + y
            print(t)
        case '-':
            t = x - y
            print(t)
        case '/':
            t = x / y
            print(t)
        case '*':
            t = x * y
            print(t)

main()