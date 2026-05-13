year=int(input('enter the year : '))
if year%400==0 or year%4==0 and year%100!=0:
    print('the entered number is leap year ')
else:
    print('the number is not leap')