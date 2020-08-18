def df_stats(df):
    
    import pandas as pd
    stats = pd.DataFrame(index=list(df))
    stats['DataTypes'] = df.dtypes
    stats['MissingPct'] = df.isnull().sum()/df.shape[0]*100
    stats['NUnique'] = df.nunique().astype(int)
    print(stats.sort_values(by='NUnique'))