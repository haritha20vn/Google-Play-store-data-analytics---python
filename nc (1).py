#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import datetime

# Load dataset

df = pd.read_csv("Null class/playstore.csv")

# Display basic info
df.info()
df.head()


# In[14]:


# Convert 'Reviews' and 'Installs' to numeric
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
df["Installs"] = df["Installs"].str.replace("+", "", regex=False).str.replace(",", "", regex=False)
df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")

# Drop missing ratings
df = df.dropna(subset=["Rating"])

# Convert 'Category' to categorical
df["Category"] = df["Category"].astype("category")

print("Data cleaning completed.")


# In[25]:


import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches

# Define sentiment categories
def categorize_sentiment(rating):
    if rating >= 4.0:
        return "Positive"
    elif rating >= 3.0:
        return "Neutral"
    else:
        return "Negative"

df["Sentiment"] = df["Rating"].apply(categorize_sentiment)

# Define rating groups
def categorize_rating_group(rating):
    if rating < 2.0:
        return "1-2 Stars"
    elif rating < 4.0:
        return "3-4 Stars"
    else:
        return "4-5 Stars"

df["Rating Group"] = df["Rating"].apply(categorize_rating_group)

# Filter apps with more than 1,000 reviews and top 5 categories
df_filtered = df[df["Reviews"] > 1000]
top_categories = df_filtered["Category"].value_counts().nlargest(5).index
df_filtered = df_filtered[df_filtered["Category"].isin(top_categories)]

# Define the color palette for sentiment categories in a specific order (Positive, Neutral, Negative)
sentiment_palette = {
    "Positive": "green",  # Green for positive sentiment
    "Neutral": "yellow",  # Yellow for neutral sentiment
    "Negative": "red"     # Red for negative sentiment
}

# Create stacked bar chart
plt.figure(figsize=(10, 6))
ax = sns.histplot(
    data=df_filtered, 
    x="Rating Group", 
    hue="Sentiment", 
    multiple="fill", 
    shrink=0.8,
    palette=sentiment_palette
)

# Add labels to each bar segment
for p in ax.patches:
    height = p.get_height()
    if height > 0:  # Only label non-zero bars
        ax.text(
            p.get_x() + p.get_width() / 2, height / 2, 
            f'{height:.2f}', 
            ha='center', va='center', color='white', fontsize=12
        )

# Add custom legend to indicate sentiment colors
legend_labels = {
    "Positive": "green",
    "Neutral": "yellow",
    "Negative": "red"
}

# Create custom legend
handles = [mpatches.Patch(color=color, label=label) for label, color in legend_labels.items()]
plt.legend(handles=handles, title="Sentiment")

# Title and labels
plt.title("Sentiment Distribution by Rating Group")
plt.xlabel("Rating Group")
plt.ylabel("Proportion")
plt.show()


# In[32]:


import datetime
import plotly.express as px

# Force the time to be within the required range for testing
test_mode = False  # Change to False when deploying

# Get current IST time
current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)

# Override time for testing
if test_mode:
    current_time = current_time.replace(hour=19)  # Set to 7 PM IST for testing

# Check if we are within the allowed time range
if 18 <= current_time.hour < 20:
    print(f"Current IST Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')} (Allowed Time Range ✅)")

    # Filter top 5 categories and exclude those starting with "A," "C," "G," or "S"
    top_categories = df["Category"].value_counts().nlargest(5).index
    df_filtered = df[df["Category"].isin(top_categories)]
    df_filtered = df_filtered[~df_filtered["Category"].str.startswith(("A", "C", "G", "S"))]

    # Aggregate installs by category
    category_installs = df_filtered.groupby("Category")["Installs"].sum().reset_index()

    # Create choropleth map
    fig = px.choropleth(
        category_installs,
        locations="Category",
        locationmode="country names",
        color="Installs",  # Installs are already in millions
        title="Global Installs by Category",
        color_continuous_scale="Viridis",
        range_color=[category_installs["Installs"].min(), category_installs["Installs"].max()],  # Set scale based on data
        labels={"Installs": "Installs (Millions)"}
    )
    fig.show()
else:
    print(f"Current IST Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')} (Not in Allowed Time Range ❌)")


# In[17]:





# In[20]:


import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Force the time to be within the required range for testing
test_mode = False  # Change to False when deploying

# Get current IST time
current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)

# Override time for testing
if test_mode:
    current_time = current_time.replace(hour=17)  # Set to 5 PM IST for testing

# Check if we are within the allowed time range
if 16 <= current_time.hour < 18:
    print(f"Current IST Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')} (Allowed Time Range ✅)")

    # Filter categories with more than 50 apps, app name containing "C", and rating < 4.0
    category_counts = df["Category"].value_counts()
    valid_categories = category_counts[category_counts > 50].index

    df_filtered = df[(df["Category"].isin(valid_categories)) & 
                     (df["App"].str.contains("C", case=False)) & 
                     (df["Reviews"] >= 10) & 
                     (df["Rating"] < 4.0)]

    # Create violin plot
    plt.figure(figsize=(12, 6))
    sns.violinplot(x="Category", y="Rating", data=df_filtered)
    plt.xticks(rotation=90)
    plt.title("Rating Distribution by Category")
    plt.xlabel("Category")
    plt.ylabel("Rating")
    plt.show()
else:
    print(f"Current IST Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')} (Not in Allowed Time Range ❌)")


# In[23]:


df


# In[ ]:





