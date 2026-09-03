import pandas as pd

input_file = "../Data/processed/cleaned_client_data_Final.xlsx"

df = pd.read_excel(input_file)

print(f"Loaded {len(df):,} records")


# 2. Standardize values used for filtering
df["Parish"] = df["Parish"].astype(str).str.strip().str.lower()
df["status"] = df["status"].astype(str).str.strip().str.lower()
df["Client Type"] = df["Client Type"].astype(str).str.strip().str.lower()



target_parishes = [
    "kingston",
    "st. andrew",
    "st. catherine"
]

target_age_groups = [
    "25-34",
    "35-44"
]


# 4. Filter for inactive individual clients aged 25–44
mask = (
    (df["status"] == "inactive") &
    (df["Client Type"] == "individual") &
    (df["Parish"].isin(target_parishes)) &
    (df["Age Range"].isin(target_age_groups))
)

filtered = df[mask].copy()

print(f"Records matching criteria: {len(filtered):,}")


#    A client can have multiple accounts.

campaign = (
    filtered
    .sort_values("Total Funds Under Management", ascending=False)
    .drop_duplicates(subset="Client Key", keep="first")
    .copy()
)

print(f"Distinct inactive individuals: {len(campaign):,}")


# 6. required marketing columns
cols = [
    "Client Key",
    "Client Name",
    "Age Range",
    "Parish",
    "status",
    "Subsidiary Description",
    "Email Address",
    "validate_email",
    "Contactable"
]

campaign_list = campaign[cols].copy()


# 7. Rename columns for the marketing team
campaign_list = campaign_list.rename(columns={
    "status": "Client Status",
    "Subsidiary Description": "Subsidiary Relationship",
    "validate_email": "Valid Email",
    "Contactable": "Contactability Status"
})


campaign_list = campaign_list.sort_values(
    ["Parish", "Client Key"]
)


# 9. Export to Excel
output_file = "../output/inactive_individuals_25_44_marketing.xlsx"

campaign_list.to_excel(
    output_file,
    index=False
)


# 10. Print validation summary
print("\n==========================================")
print("CAMPAIGN LIST CREATED")
print("==========================================")

print(f"Output file: {output_file}")
print(f"Distinct clients: {len(campaign_list):,}")

print("\nClients by parish:")
print(campaign_list["Parish"].value_counts())

print("\nContactability:")
print(campaign_list["Contactability Status"].value_counts())

print("\nValid email:")
print(campaign_list["Valid Email"].value_counts())

print("\nFinal columns:")
print(campaign_list.columns.tolist())