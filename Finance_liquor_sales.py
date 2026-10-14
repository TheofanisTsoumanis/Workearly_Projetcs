import pandas as pd
import matplotlib.pyplot as plt

# read the data.
data = pd.read_csv('finance_liquor_sales.csv')

data["date"] = pd.to_datetime(data["date"])
data = data[data["date"].dt.year.between(2016, 2019)]

# see the data.
print(data.head())
data.info()
data.describe()

# check for missing values and duplicates.
print(data.isnull().sum())
print(data.duplicated().sum())
print()

# remove rows with non-recoverable missing values.
data = data.dropna(subset= ["category"])

# replace nan with Unknown
data["category_name"] = data["category_name"].fillna("Unknown")
print("Task 1.")
# Task 1.
# group by the right columns
sales_by_item = data.groupby(["zip_code", "item_description"])["bottles_sold"].sum()

# create and print a series with value
most_popular_items = sales_by_item.loc[sales_by_item.groupby("zip_code").idxmax()].reset_index()

print(most_popular_items)
print()
print("Task 2.")
# Task 2.
# group by the right columns
sales_by_store = data.groupby(["store_name"])["sale_dollars"].sum()

# sales from all stores
sales_from_all_stores = sales_by_store.sum()

# calculate the percentage
sales_by_store = sales_by_store * 100 / sales_from_all_stores
sales_by_store = sales_by_store.reset_index()
sales_by_store = sales_by_store.rename(columns={"sale_dollars": "sales_percentage"})
print(sales_by_store.round(3))

# Visualization
# scatter plot for task 1.
fig, axes = plt.subplots(2, 2, figsize=(20, 10))
scatter = axes[0,0].scatter(
    most_popular_items["zip_code"],
    most_popular_items["bottles_sold"],
    c=most_popular_items["bottles_sold"],
    cmap="viridis"
)
axes[0,0].set_title("Most Popular Items by Zip Code")
axes[0,0].set_xlabel("Zip Code")
axes[0,0].set_ylabel("Bottles Sold")

fig.colorbar(scatter, ax=axes[0,0])

# bar plot for task 1
top_15_items = most_popular_items.nlargest(15, "bottles_sold")

colors_items = plt.cm.viridis(
    top_15_items["bottles_sold"] / top_15_items["bottles_sold"].max()
)

bars_items = axes[1, 0].barh(
    top_15_items["item_description"],
    top_15_items["bottles_sold"],
    color=colors_items
)

for bar in bars_items:
    width = bar.get_width()

    axes[1, 0].text(
        width,
        bar.get_y() + bar.get_height() / 2,
        f"{width:.0f}",
        va="center"
    )

axes[1, 0].set_xlim(
    0,
    top_15_items["bottles_sold"].max() * 1.1
)

axes[1, 0].set_title("Top 15 Most Popular Items")
axes[1, 0].set_xlabel("Bottles Sold")
axes[1, 0].set_ylabel("Item")
axes[1, 0].invert_yaxis()

# scatter plot for task 2.
scatter2 = axes[0,1].scatter(
    range(len(sales_by_store)),
    sales_by_store["sales_percentage"],
    c=sales_by_store["sales_percentage"],
    cmap="viridis"
)
axes[0,1].set_title("Sales Percentage Share by Store")
axes[0,1].set_xlabel("Store")
axes[0,1].set_ylabel("Sales Percentage (%)")

fig.colorbar(scatter2, ax=axes[0,1])

# bar plot for task 2.
top_15_stores = sales_by_store.nlargest(15, "sales_percentage")

colors = plt.cm.viridis(top_15_stores["sales_percentage"] / top_15_stores["sales_percentage"].max())

bars = axes[1, 1].barh(
    top_15_stores["store_name"],
    top_15_stores["sales_percentage"],
    color=colors
)

for bar in bars:
    width = bar.get_width()

    axes[1, 1].text(
        width,
        bar.get_y() + bar.get_height() / 2,
        f"{width:.1f}%",
        va="center"
    )

axes[1, 1].set_xlim(
    0,
    top_15_stores["sales_percentage"].max() * 1.1
)

axes[1, 1].set_title("Top 15 Stores by Sales Percentage")
axes[1, 1].set_xlabel("Sales Percentage (%)")
axes[1, 1].set_ylabel("Store Name")
axes[1, 1].invert_yaxis()

plt.tight_layout()
plt.savefig("liquor_sales_analysis.png")
plt.show()