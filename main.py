import pandas as pd
import numpy as np
import cv2
import os
import glob

df = pd.read_csv("data/ecommerce_customer_behavior_dataset_v2.csv")

print(df.head())
print("Dataset Shape:", df.shape)
print(df.columns)
print(df.isnull().sum()) #found 0 missing values so we check duplicates 

print("Duplicate Rows:", df.duplicated().sum()) #0 dupliactes 

#so till now having following :
#Total records:	17,049
#Total columns:	18
#Missing values:	0
#Duplicate rows:	0

print(df.describe())
print(df.dtypes) # here got date in str format so we need to convert it into datetime format
#so in further calculations  like monthly or yealry sales and  plot graphs 

df["Date"] = pd.to_datetime(df["Date"])

print(df["Date"].dtype)

df["Month"] = df["Date"].dt.month

print(df[["Date", "Month"]].head())


#performing basic sales analysis

# First calculating total revenue generated from all orders
total_revenue = df["Total_Amount"].sum()

print("\nTotal Revenue:", round(total_revenue, 2))


# calculate average order value as it tells how much customers spend on average per order

average_order_value = df["Total_Amount"].mean()

print("Average Order Value:", round(average_order_value, 2))


#calculate total quantity of products sold

total_products_sold = df["Quantity"].sum()

print("Total Products Sold:", total_products_sold)


#check how many unique customers placed orders

total_customers = df["Customer_ID"].nunique()

print("Total Unique Customers:", total_customers)


# Analyzing monthly sales:  firstly  extract month and year from the order date

df["Month_Year"] = df["Date"].dt.to_period("M")

# Group by all orders according to month and calculating total sales

monthly_sales = df.groupby("Month_Year")["Total_Amount"].sum()

print("\n========== MONTHLY SALES ANALYSIS ==========")
print(monthly_sales)

#Finding the month with the highest sales

highest_sales_month = monthly_sales.idxmax()
highest_sales_value = monthly_sales.max()

print("\nMonth with Highest Sales:", highest_sales_month)
print("Highest Monthly Sales:", round(highest_sales_value, 2))


# creating the graph to visualize monthly sales
import matplotlib.pyplot as plt

#plt.figure(figsize=(12, 6))

#monthly_sales.plot(kind="bar")


#plt.title("Monthly Sales Analysis")
#plt.xlabel("Month")
#plt.ylabel("Total Revenue")

#plt.xticks(rotation=45)

#plt.tight_layout()
#plt.show()

# analyzING sales according to product categories

# Grouping orders by product category and calculating total revenue
category_sales = df.groupby("Product_Category")["Total_Amount"].sum()

category_sales = category_sales.sort_values(ascending=False)

print("\n========== PRODUCT CATEGORY ANALYSIS ==========")
print(category_sales)

# Finding the top-selling product category and its revenue
top_category = category_sales.idxmax()
top_category_sales = category_sales.max()

print("\nTop Selling Category:", top_category)
print("Category Revenue:", round(top_category_sales, 2))


#visualizing category-wise sales using a bar chart

#plt.figure(figsize=(10, 6))

#category_sales.plot(kind="bar")

#plt.title("Revenue by Product Category")
#plt.xlabel("Product Category")
#plt.ylabel("Total Revenue")

#plt.xticks(rotation=45)

#plt.tight_layout()
#plt.show()



# ======analyzing customer behaviour========

# counting returning and new customers
customer_type = df["Is_Returning_Customer"].value_counts()

print("\n========== CUSTOMER BEHAVIOUR ANALYSIS ==========")
print("Returning Customers:", customer_type.get(True, 0))
print("New Customers:", customer_type.get(False, 0))

returning_percentage = (customer_type.get(True, 0) / len(df)) * 100

print("Returning Customer Percentage:", round(returning_percentage, 2), "%")



#  ======analyzing age - wise sales ========

# divide the customers into different age groups

df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[17, 25, 35, 45, 55, 100],
    labels=["18-25", "26-35", "36-45", "46-55", "Above 55"]
)

# Calculating revenue according to age groups
age_sales = df.groupby("Age_Group", observed=False)["Total_Amount"].sum()

print("\n========== AGE-WISE SALES ==========")
print(age_sales)

print("Highest Revenue Age Group:", age_sales.idxmax())

# Creating age-wise sales graph
plt.figure(figsize=(9, 5))
age_sales.plot(kind="bar")
plt.title("Sales by Customer Age Group")
plt.xlabel("Age Group")
plt.ylabel("Total Revenue")
plt.tight_layout()
plt.show()


#======Gender wise sales ==========


gender_sales = df.groupby("Gender")["Total_Amount"].sum()

print("\n========== GENDER-WISE SALES ==========")
print(gender_sales)

plt.figure(figsize=(7, 5))
gender_sales.plot(kind="bar")
plt.title("Sales by Gender")
plt.xlabel("Gender")
plt.ylabel("Total Revenue")
plt.tight_layout()
plt.show()


#==========city wise sales analysis========


city_sales = df.groupby("City")["Total_Amount"].sum()
city_sales = city_sales.sort_values(ascending=False)

print("\n========== CITY-WISE SALES ==========")
print(city_sales)

print("\nTop Sales City:", city_sales.idxmax())

# Displaying top 10 cities
plt.figure(figsize=(10, 5))
city_sales.head(10).plot(kind="bar")
plt.title("Top 10 Cities by Revenue")
plt.xlabel("City")
plt.ylabel("Total Revenue")
plt.tight_layout()
plt.show()


#=====payment method analysis========

#count orders made through each payment method

payment_analysis = df["Payment_Method"].value_counts()

print("\n========== PAYMENT METHOD ANALYSIS ==========")
print(payment_analysis)

plt.figure(figsize=(8, 5))
payment_analysis.plot(kind="bar")
plt.title("Orders by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.show()

#========device type analysis========
#check which devices customers use for shopping

device_analysis = df["Device_Type"].value_counts()

print("\n========== DEVICE TYPE ANALYSIS ==========")
print(device_analysis)

plt.figure(figsize=(7, 5))
device_analysis.plot(kind="pie", autopct="%1.1f%%")
plt.title("Customer Device Usage")
plt.ylabel("")
plt.tight_layout()
plt.show()


#============customer rating analysis========
#calculate average customer ratings

average_rating = np.mean(df["Customer_Rating"])

rating_analysis = df["Customer_Rating"].value_counts().sort_index()

print("\n========== CUSTOMER RATING ANALYSIS ==========")
print("Average Customer Rating:", round(average_rating, 2))
print(rating_analysis)

plt.figure(figsize=(8, 5))
rating_analysis.plot(kind="bar")
plt.title("Customer Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.show()


#=====delivery time analysis========

average_delivery = np.mean(df["Delivery_Time_Days"])

print("\n========== DELIVERY TIME ANALYSIS ==========")
print("Average Delivery Time:", round(average_delivery, 2), "Days")

# Calculating average rating according to delivery time
delivery_rating = df.groupby("Delivery_Time_Days")["Customer_Rating"].mean()

print("\nDelivery Time and Customer Ratings:")
print(delivery_rating)

plt.figure(figsize=(9, 5))
delivery_rating.plot(kind="line", marker="o")
plt.title("Delivery Time vs Customer Rating")
plt.xlabel("Delivery Time (Days)")
plt.ylabel("Average Customer Rating")
plt.tight_layout()
plt.show()


#open cv image processing for product images

#check product images from our images folder

image_files = glob.glob("images/*")

print("\n========== OPENCV IMAGE PROCESSING ==========")

if len(image_files) > 0:

    # Creating a folder to save processed images
    os.makedirs("processed_images", exist_ok=True)

    for image_path in image_files:

        # Reading the product image
        image = cv2.imread(image_path)

        if image is not None:

            # Resizing image
            resized_image = cv2.resize(image, (300, 300))

            # Converting image into grayscale
            gray_image = cv2.cvtColor(
                resized_image,
                cv2.COLOR_BGR2GRAY
            )

            # Saving processed image
            file_name = os.path.basename(image_path)

            cv2.imwrite(
                "processed_images/" + file_name,
                gray_image
            )

            print("Processed Image:", file_name)

    print("All available images processed successfully!")

else:
    print("No images found. Please add product images in the images folder.")


#final summary of the project

print("\n========== FINAL E-COMMERCE PROJECT SUMMARY ==========")

print("Total Orders:", len(df))
print("Total Revenue:", round(df["Total_Amount"].sum(), 2))
print("Average Order Value:", round(df["Total_Amount"].mean(), 2))
print("Total Products Sold:", df["Quantity"].sum())
print("Unique Customers:", df["Customer_ID"].nunique())
print("Top Product Category:", df.groupby("Product_Category")["Total_Amount"].sum().idxmax())
print("Top Sales City:", df.groupby("City")["Total_Amount"].sum().idxmax())
print("Average Customer Rating:", round(df["Customer_Rating"].mean(), 2))
print("Average Delivery Time:", round(df["Delivery_Time_Days"].mean(), 2), "Days")

print("\n========== PROJECT ANALYSIS COMPLETED ==========")
