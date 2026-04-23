import pandas as pd
import numpy as np

# 1. Load Data
df = pd.read_csv('Master_Garrison_Thesis_Final.csv')

# 2. Time Normalization
df['Comment_Date'] = pd.to_datetime(df['Comment_Date'])
df['Video_Launch'] = pd.to_datetime(df['Video_Launch'])
# Convert to days
df['Days_Since_Launch'] = (df['Comment_Date'] - df['Video_Launch']).dt.total_seconds() / 86400
# Filter out any data errors (comments before launch)
df = df[df['Days_Since_Launch'] >= 0]

# 3. Create 7-Day Intervals (Week Bins)
# Week 0 = Days 0-6 | Week 1 = Days 7-13 | Week 2 = Days 14-20...
df['Interval_Week'] = (df['Days_Since_Launch'] // 7).astype(int)

def calculate_snapshot_metrics(group):
    return pd.Series({
        'Sample_Count': len(group),
        'Avg_MPI': group['MPI'].mean(),
        'Sigma_Randomness': group['MPI'].std(),
        'Avg_Heat': group['Heat'].mean()
    })

# 4. Generate Snapshots
# Brand-wise separation
brand_weekly = df.groupby(['Brand', 'Interval_Week']).apply(calculate_snapshot_metrics).reset_index()

# Market-wide Consolidated
global_weekly = df.groupby(['Interval_Week']).apply(calculate_snapshot_metrics).reset_index()

# 5. Export to CSV
brand_weekly.to_csv('Weekly_Brand_Metrics.csv', index=False)
global_weekly.to_csv('Weekly_Consolidated_Metrics.csv', index=False)

print("✅ Weekly Metrics Partitioned Successfully.")