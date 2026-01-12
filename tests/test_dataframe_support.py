import pandas as pd
import sys
sys.path.insert(0, '/Users/shenglong/Downloads/revisitpy/src')

from revisitpy import data

# Test 1: CSV file
print("Test 1: CSV file")
csv_data = data("tests/config.json")  # Replace with actual CSV
print(f"✓ CSV loaded: {len(csv_data)} rows")

# Test 2: Pandas DataFrame
print("\nTest 2: Pandas DataFrame")
df = pd.DataFrame({
    'id': [1, 2, 3],
    'b1': [0.32, 1.2, 0.6],
    'b2': [0.01, 1.2, 1.1]
})
df_data = data(df)
print(f"✓ DataFrame loaded: {len(df_data)} rows")
print(f"  First row: {df_data[0]}")

# Test 3: Error handling
print("\nTest 3: Error handling")
try:
    data(123)  # Should fail
except Exception as e:
    print(f"✓ Correctly raised error: {str(e)[:50]}...")