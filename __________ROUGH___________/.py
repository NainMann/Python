n=int(input())
D={}
for i in range (n):
    name=input('enter name')
    city=input('enter city')
    D[name]=city
All_names=list(D.keys())
All_cities=list(D.values())
All_data=list(D.items())
print('name = ',All_names)
print('city = ',All_cities)
print('data = ',All_data)
count=0
total=len(All_names)
print('total students= ',total)