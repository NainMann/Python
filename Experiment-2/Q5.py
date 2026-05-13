a=int(input('Enter the coefficent of x^2 = '))
b=int(input('Enter the coefficent of x = '))
c=int(input('Enter the constant = '))
D=b**2-(4*a*c)
if D >= 0:
    r1=-b+(D**0.5)
    r2=-b-(D**0.5)
    print ('The roots of the quadratic are ' , r1 ,'and' , r2)
else :
    print('The quadractic have imaginary roots.')