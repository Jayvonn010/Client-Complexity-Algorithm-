import pandas as pd

'''Score how complex a dataset is.'''
def initial_data_complexity(df):
    # Example complexity calculation: Count the number of unique values in each column
    complexity = df.nunique()
    return complexity

'''how much based on the amount of people'''
def size_score(df):
    # Example size score calculation: Count the number of rows and columns
    num_rows, num_cols = df.shape
    size_score = num_rows * num_cols
    return size_score

'''How complex based on the data once it processes'''
def base_score(df):
    # Example base score calculation: Calculate the mean of numeric columns
    numeric_cols = df.select_dtypes(include='number')
    base_score = numeric_cols.mean().mean()  # Mean of means of numeric columns
    return base_score

'''How complex based on the amount of manual changes'''
def manual_changes_score(df):
    # Example manual changes score calculation: Count the number of columns with missing values
    missing_values = df.isnull().sum()
    manual_changes_score = missing_values[missing_values > 0].count()
    return manual_changes_score

'''How complex based on the amount of conflicts'''
def conflict_score(df):
    # Example conflict score calculation: Count the number of duplicate rows
    duplicate_rows = df.duplicated().sum()
    conflict_score = duplicate_rows
    return conflict_score

'''addictional score based on effort for clients to be loaded through monthly loader'''
def monthly_loader_score(df):
    # Example monthly loader score calculation: Count the number of rows added per month
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        monthly_loader_score = df.groupby(df['date'].dt.to_period('M')).size()
    else:
        monthly_loader_score = pd.Series(dtype=int)  # Empty series if no date column
    return monthly_loader_score

'''What runs the whole thing'''
def main():
    # Load the CSV file into a DataFrame
    df = pd.read_csv('data.csv')
    score = 0 

    # Calculate the complexity of the DataFrame
    score += initial_data_complexity(df).sum()
    score += size_score(df)
    score += base_score(df)
    score += manual_changes_score(df)
    score += conflict_score(df)
    score += monthly_loader_score(df).sum()

    complexity_score = score
    print(f"Complexity Score: {complexity_score}")