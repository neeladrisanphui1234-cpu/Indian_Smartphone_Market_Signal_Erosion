import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# 1. LOAD THE DATA (This was missing in your run!)
print("🚀 Loading data for Logistic Regression...")
df = pd.read_csv('Master_Garrison_Thesis_Final.csv')

# 2. PRE-PROCESSING
# Create Target: Controlled Tier = 1, Everything else = 0
df['Target'] = (df['Env'] == 'Controlled').astype(int)

# Calculate Days since launch
df['Comment_Date'] = pd.to_datetime(df['Comment_Date'])
df['Video_Launch'] = pd.to_datetime(df['Video_Launch'])
df['Days_Since_Launch'] = (df['Comment_Date'] - df['Video_Launch']).dt.total_seconds() / 86400
df = df[df['Days_Since_Launch'] >= 0]

# 3. SELECT FEATURES
# We use Saliency (MPI), Sentiment (Heat), and Time (Days)
X = df[['MPI', 'Heat', 'Days_Since_Launch']]
y = df['Target']

# 4. TRAIN/TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. SCALE THE DATA (Vital for Logistic Regression)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6. RUN THE MODEL
print("🤖 Training Predictive Model...")
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# 7. OUTPUT RESULTS
y_pred = model.predict(X_test_scaled)
print("\n--- MODEL PERFORMANCE ---")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

print("\n--- FEATURE CORRELATION (COEFFICIENTS) ---")
coeff_df = pd.DataFrame({'Feature': X.columns, 'Coefficient': model.coef_[0]})
print(coeff_df)

# EXPLAINING THE NUMBERS
print("\n--- DEFENSE STRATEGY ---")
for index, row in coeff_df.iterrows():
    direction = "Positive" if row['Coefficient'] > 0 else "Negative"
    print(f"Feature '{row['Feature']}' has a {direction} correlation with Brand Control.")