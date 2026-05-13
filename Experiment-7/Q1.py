with open('name.txt', 'r') as f:
    names = f.readlines()  

total = len(names)         
print('The total number of names in the file are :', total)

vowels = ('A','E','I','O','U','a','e','i','o','u')
vowel_count = 0

for name in names:
    name = name.strip ()    
    if name.startswith(vowels):
        vowel_count += 1

print("Names starting with vowel:", vowel_count)

longest_name = names[0].strip()

for name in names:
    name = name.strip()
    if len(name) > len(longest_name):
        longest_name = name

print("Longest name:", longest_name)