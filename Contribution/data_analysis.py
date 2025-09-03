# 📊 Data Science & Data Analysis Demo

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Create a small dataset (like survey data)
data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eva"],
    "Age": [25, 30, 35, 40, 28],
    "Salary": [50000, 60000, 75000, 80000, 52000],
    "Department": ["IT", "HR", "IT", "Finance", "HR"]
}

df = pd.DataFrame(data)
print("📌 Dataset:")
print(df)

# Step 2: Simple Analysis
print("\n📊 Basic Statistics:")
print(df.describe())   # Mean, std, min, max, etc.

print("\n👥 Group by Department (Average Salary):")
print(df.groupby("Department")["Salary"].mean())

# Step 3: Data Visualization
plt.figure(figsize=(6,4))
plt.bar(df["Name"], df["Salary"], color="skyblue")
plt.title("Employee Salaries")
plt.xlabel("Employee")
plt.ylabel("Salary")
plt.show()
