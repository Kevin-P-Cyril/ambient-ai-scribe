import pandas as pd

# Load dataset
df = pd.read_csv("ICDCodeSet.csv")  # change filename if needed

# Keep only needed columns
df = df[["ICDCode", "Description"]]

# Clean text (remove extra spaces)
df["Description"] = df["Description"].str.strip()

# Create combined text for embedding
df["text"] = df["ICDCode"] + " " + df["Description"]

print(df.head())

# Save cleaned version
df.to_csv("icd_clean.csv", index=False)

print("Done: Clean dataset created!")