import pandas as pd
import os

RAW_FOLDER = "data/raw"

files = sorted([
    f for f in os.listdir(RAW_FOLDER)
    if f.endswith(".csv")
])

print("="*70)
print("DATA QUALITY ANALYSIS")
print("="*70)

for file in files:

    path = os.path.join(RAW_FOLDER, file)

    df = pd.read_csv(path)

    print("\n")
    print("="*70)
    print(file)
    print("="*70)

    print("Rows :", df.shape[0])
    print("Columns :", df.shape[1])

    print("\nMissing Values:")

    missing = df.isnull().sum()

    print(missing[missing > 0])

    print("\nDuplicate Rows:")

    print(df.duplicated().sum())