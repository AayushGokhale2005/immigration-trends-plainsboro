import pandas as pd

df = pd.read_csv('plainsboro_dataset.csv')

# Rename columns 
cols_new = ['Label', 'Plainsboro_total', 'Entered_2010_or_later', 'Entered_2000_to_2009', 'Entered_before_2000']
df.columns = cols_new

group = None
subgroup = None

group_cols = []
subgroup_cols = []

for i, label in enumerate(df['Label']):
    label_stripped = str(label).strip()

    if label_stripped.isupper() and pd.isna(df.loc[i, 'Plainsboro_total']):
        group = label_stripped
        subgroup = None  
    elif not label.startswith(' '):  
        subgroup = label_stripped

    group_cols.append(group)
    subgroup_cols.append(subgroup)

df.insert(0, "Group", group_cols)
df.insert(1, "Subgroup", subgroup_cols)

# Clean Label text
df['Label'] = df['Label'].str.strip()

df = df[~((df['Label'].str.isupper()) & (df['Plainsboro_total'].isna()))]

df.to_csv('plainsboro_cleaned.csv', index=False)
