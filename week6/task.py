

# Step 1: Imports and Ray init
import pandas as pd
import dask.dataframe as dd
import modin.pandas as mpd
import ray
import time
import os
import yaml
import re

ray.init(ignore_reinit_error=True, include_dashboard=False)

# Step 2: File path (replace this with your 2+ GB CSV file path)
# You can upload file to Colab or download via !wget
file_path = 'dataset.csv'  # Update this path accordingly

# Helper function to time reading functions
def time_read(func, *args, **kwargs):
    start = time.time()
    df = func(*args, **kwargs)
    end = time.time()
    print(f"Time taken by {func.__name__}: {end - start:.2f} seconds")
    return df

# Reading functions
def read_pandas(fp):
    return pd.read_csv(fp)

def read_dask(fp):
    return dd.read_csv(fp)

def read_modin(fp):
    return mpd.read_csv(fp)

def read_ray(fp):
    import ray.data
    ds = ray.data.read_csv(fp)
    return ds

# Step 3: Read file with pandas
print("Reading with pandas:")
df_pandas = time_read(read_pandas, file_path)

# Step 4: Read file with dask
print("Reading with dask:")
df_dask = time_read(read_dask, file_path)

# Step 5: Read file with modin
print("Reading with modin:")
df_modin = time_read(read_modin, file_path)

# Step 6: Read file with ray
print("Reading with ray:")
df_ray = time_read(read_ray, file_path)

# Step 7: Clean columns (pandas example)
def clean_columns(df):
    new_cols = []
    for col in df.columns:
        clean_col = re.sub(r'[^A-Za-z0-9_]', '', col).strip()
        new_cols.append(clean_col)
    df.columns = new_cols
    return df

df_pandas = clean_columns(df_pandas)
print("Cleaned pandas columns:", df_pandas.columns)

# Also clean dask columns
df_dask.columns = [re.sub(r'[^A-Za-z0-9_]', '', c).strip() for c in df_dask.columns]

# Clean modin columns
df_modin.columns = [re.sub(r'[^A-Za-z0-9_]', '', c).strip() for c in df_modin.columns]

# Step 8: Create YAML schema file
schema = {
    'separator': ',',
    'columns': list(df_pandas.columns)
}

yaml_path = 'schema.yaml'
with open(yaml_path, 'w') as f:
    yaml.dump(schema, f)

print(f"Schema saved to {yaml_path}")

# Step 9: Validate dataframe columns against YAML
with open(yaml_path) as f:
    loaded_schema = yaml.safe_load(f)

def validate_schema(df, schema):
    if len(df.columns) != len(schema['columns']):
        return False, "Column count mismatch"
    if list(df.columns) != schema['columns']:
        return False, "Column names mismatch"
    return True, "Schema validation passed"

valid, msg = validate_schema(df_pandas, loaded_schema)
print("Pandas DF:", msg)

valid, msg = validate_schema(df_modin, loaded_schema)
print("Modin DF:", msg)

valid, msg = validate_schema(df_dask, loaded_schema)
print("Dask DF:", msg)

# Note: ray dataset doesn't have columns as pandas, so skip validation for ray here

# Step 10: Write cleaned pandas df as pipe-separated gzipped file
output_file = 'output_file.psv.gz'
df_pandas.to_csv(output_file, sep='|', index=False, compression='gzip')
print(f"File written to {output_file}")

# Step 11: Summary of the file
def file_summary(file_path, df):
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    total_rows = len(df)
    total_cols = len(df.columns)
    print(f"\nFile Summary:")
    print(f"- Total Rows: {total_rows}")
    print(f"- Total Columns: {total_cols}")
    print(f"- File Size: {file_size_mb:.2f} MB")

file_summary(file_path, df_pandas)
