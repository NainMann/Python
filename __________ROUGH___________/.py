import numpy as np

# Create a 3x3 array
arr = np.array([
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
])

# Print the array
print("Array is:")
print(arr)

# Sum of rows
print("\nSum of rows:")

row1 = np.sum(arr[0])
row2 = np.sum(arr[1])
row3 = np.sum(arr[2])

print("Row 1 Sum =", row1)
print("Row 2 Sum =", row2)
print("Row 3 Sum =", row3)

# Sum of columns
print("\nSum of columns:")

col1 = arr[0][0] + arr[1][0] + arr[2][0]
col2 = arr[0][1] + arr[1][1] + arr[2][1]
col3 = arr[0][2] + arr[1][2] + arr[2][2]

print("Column 1 Sum =", col1)
print("Column 2 Sum =", col2)
print("Column 3 Sum =", col3)

# Find second maximum element
flat_array = arr.flatten()

flat_array.sort()

second_max = flat_array[-2]

print("\nSecond Maximum Element =", second_max)