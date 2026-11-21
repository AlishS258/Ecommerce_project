
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ---------------- APPLICATION SETTINGS ----------------

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

BG = "#211A2C"
SIDEBAR = "#2D2438"
CARD = "#382D45"
CARD2 = "#453750"
PURPLE = "#C4A7E7"
CORAL = "#FF8A7A"
MINT = "#A8D5BA"
YELLOW = "#F3D18A"
WHITE = "#F5F0E8"
MUTED = "#B8AFC2"

# Load our dataset
df = pd.read_csv("data/ecommerce_customer_behavior_dataset_v2.csv")
df["Date"] = pd.to_datetime(df["Date"])

filtered_df = df.copy()
current_page = "Overview"


# ---------------- MAIN WINDOW ----------------

app = ctk.CTk()
app.title("Merchant | E-Commerce Intelligence")
app.geometry("1450x900")
app.minsize(1100, 720)
app.configure(fg_color=BG)


# ---------------- SIDEBAR ----------------

sidebar = ctk.CTkFrame(
    app, width=245, corner_radius=0,
    fg_color=SIDEBAR
)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

ctk.CTkLabel(
    sidebar,
    text="MERCHANT.",
    font=("Georgia", 27, "bold"),
    text_color=WHITE
).pack(anchor="w", padx=25, pady=(35, 0))

ctk.CTkLabel(
    sidebar,
    text="COMMERCE INTELLIGENCE",
    font=("Arial", 9, "bold"),
    text_color=PURPLE
).pack(anchor="w", padx=27, pady=(5, 40))

ctk.CTkLabel(
    sidebar,
    text="MAIN MENU",
    font=("Arial", 10, "bold"),
    text_color=MUTED
).pack(anchor="w", padx=25, pady=(0, 12))


# ---------------- MAIN CONTENT ----------------

main = ctk.CTkFrame(app, fg_color=BG, corner_radius=0)
main.pack(side="left", fill="both", expand=True)

header = ctk.CTkFrame(main, fg_color=BG)
header.pack(fill="x", padx=30, pady=(25, 10))

heading = ctk.CTkLabel(
    header,
    text="Overview",
    font=("Georgia", 30, "bold"),
    text_color=WHITE
)
heading.pack(side="left")

status = ctk.CTkLabel(
    header,
    text="● DATA CONNECTED",
    text_color=MINT,
    font=("Arial", 10, "bold")
)
status.pack(side="right", padx=10)

# Filters panel
filters = ctk.CTkFrame(
    main, fg_color=CARD,
    corner_radius=16
)
filters.pack(fill="x", padx=30, pady=15)

start_entry = ctk.CTkEntry(
    filters, placeholder_text="Start date YYYY-MM-DD",
    width=180, height=38
)
start_entry.pack(side="left", padx=(15, 8), pady=15)

end_entry = ctk.CTkEntry(
    filters, placeholder_text="End date YYYY-MM-DD",
    width=180, height=38
)
end_entry.pack(side="left", padx=8, pady=15)

category_box = ctk.CTkComboBox(
    filters,
    values=["All"] + sorted(df["Product_Category"].unique().tolist()),
    width=175,
    height=38,
    fg_color=CARD2,
    border_color=PURPLE,
    button_color=PURPLE,
    text_color=WHITE
)
category_box.set("All")
category_box.pack(side="left", padx=8, pady=15)

# Content area
content = ctk.CTkScrollableFrame(
    main,
    fg_color=BG,
    corner_radius=0,
    scrollbar_button_color=CARD2
)
content.pack(fill="both", expand=True, padx=22, pady=(5, 15))


# ---------------- DATA FILTERING ----------------

def apply_filters():
    global filtered_df

    data = df.copy()

    start = start_entry.get().strip()
    end = end_entry.get().strip()
    category = category_box.get()

    try:
        if start:
            data = data[data["Date"] >= pd.to_datetime(start)]

        if end:
            data = data[
                data["Date"] < pd.to_datetime(end) + pd.Timedelta(days=1)
            ]

        if start and end and pd.to_datetime(start) > pd.to_datetime(end):
            messagebox.showerror(
                "Invalid dates",
                "Start date cannot be after end date."
            )
            return

    except (ValueError, TypeError):
        messagebox.showerror(
            "Invalid date",
            "Please enter dates in YYYY-MM-DD format."
        )
        return

    if category != "All":
        data = data[data["Product_Category"] == category]

    filtered_df = data
    show_page(current_page)


def reset_filters():
    start_entry.delete(0, "end")
    end_entry.delete(0, "end")
    category_box.set("All")
    apply_filters()


# Filter buttons
ctk.CTkButton(
    filters,
    text="Apply Filters",
    width=110,
    height=38,
    fg_color=PURPLE,
    hover_color="#A98BCB",
    text_color=BG,
    font=("Arial", 11, "bold"),
    command=apply_filters
).pack(side="left", padx=8, pady=15)

ctk.CTkButton(
    filters,
    text="Reset",
    width=75,
    height=38,
    fg_color=CARD2,
    hover_color="#594865",
    text_color=WHITE,
    command=reset_filters
).pack(side="left", padx=(0, 15), pady=15)


# ---------------- REUSABLE FUNCTIONS ----------------

def clear_content():
    for widget in content.winfo_children():
        widget.destroy()


def section_title(title, subtitle):
    ctk.CTkLabel(
        content,
        text=title,
        font=("Georgia", 23, "bold"),
        text_color=WHITE
    ).pack(anchor="w", padx=10, pady=(12, 3))

    ctk.CTkLabel(
        content,
        text=subtitle,
        font=("Arial", 11),
        text_color=MUTED
    ).pack(anchor="w", padx=10, pady=(0, 18))


def create_card(parent, title, value, accent, note):
    card = ctk.CTkFrame(
        parent,
        fg_color=CARD,
        corner_radius=17,
        height=125
    )
    card.pack(side="left", fill="x", expand=True, padx=7)
    card.pack_propagate(False)

    ctk.CTkLabel(
        card,
        text=title.upper(),
        font=("Arial", 10, "bold"),
        text_color=MUTED
    ).pack(anchor="w", padx=17, pady=(17, 5))

    ctk.CTkLabel(
        card,
        text=value,
        font=("Georgia", 22, "bold"),
        text_color=accent
    ).pack(anchor="w", padx=17)

    ctk.CTkLabel(
        card,
        text=note,
        font=("Arial", 9),
        text_color=MUTED
    ).pack(anchor="w", padx=17, pady=(4, 0))


def chart(parent, title, x, y, kind="bar", color=PURPLE):
    box = ctk.CTkFrame(
        parent,
        fg_color=CARD,
        corner_radius=17
    )
    box.pack(side="left", fill="both", expand=True, padx=7, pady=8)

    ctk.CTkLabel(
        box,
        text=title,
        font=("Georgia", 16, "bold"),
        text_color=WHITE
    ).pack(anchor="w", padx=17, pady=(15, 5))

    fig = Figure(figsize=(5, 2.65), dpi=100)
    fig.patch.set_facecolor(CARD)

    ax = fig.add_subplot(111)
    ax.set_facecolor(CARD)

    if kind == "line":
        ax.plot(
            x, y, color=color,
            linewidth=2.8, marker="o",
            markersize=5
        )
        ax.fill_between(x, y, color=color, alpha=0.13)

    elif kind == "pie":
        ax.pie(
            y,
            labels=x,
            autopct="%1.1f%%",
            startangle=90,
            colors=[PURPLE, CORAL, MINT, YELLOW, "#8CC8E8"],
            textprops={"color": WHITE, "fontsize": 8}
        )

    else:
        bars = ax.bar(x, y, color=color, width=0.65)
        ax.bar_label(
            bars,
            fmt="%.0f",
            fontsize=7,
            color=WHITE,
            padding=3
        )

    if kind != "pie":
        ax.tick_params(colors=MUTED, labelsize=8)
        ax.tick_params(axis="x", rotation=25)

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.grid(axis="y", alpha=0.15)
        ax.set_axisbelow(True)

    fig.tight_layout(pad=2)

    canvas = FigureCanvasTkAgg(fig, master=box)
    canvas.draw()
    canvas.get_tk_widget().pack(
        fill="both", expand=True, padx=10, pady=8
    )


def chart_row():
    row = ctk.CTkFrame(content, fg_color=BG)
    row.pack(fill="both", expand=True, pady=5)
    return row


# ---------------- OVERVIEW PAGE ----------------

def show_overview():
    data = filtered_df

    section_title(
        "Business Overview",
        "A quick look at your e-commerce performance."
    )

    cards = ctk.CTkFrame(content, fg_color=BG)
    cards.pack(fill="x", pady=5)

    create_card(
        cards, "Revenue",
        f"{data['Total_Amount'].sum():,.0f}",
        CORAL, "Total sales value"
    )

    create_card(
        cards, "Orders",
        f"{len(data):,}",
        PURPLE, "Total transactions"
    )

    create_card(
        cards, "Customers",
        f"{data['Customer_ID'].nunique():,}",
        MINT, "Unique customers"
    )

    create_card(
        cards, "Average Order",
        f"{data['Total_Amount'].mean():,.0f}",
        YELLOW, "Average transaction value"
    )

    monthly = data.groupby(
        data["Date"].dt.to_period("M")
    )["Total_Amount"].sum()

    categories = data.groupby(
        "Product_Category"
    )["Total_Amount"].sum().sort_values(ascending=False)

    row = chart_row()

    chart(
        row, "Monthly Revenue",
        monthly.index.astype(str).tolist(),
        monthly.values, "line", CORAL
    )

    chart(
        row, "Category Revenue",
        categories.index.tolist(),
        categories.values, "bar", PURPLE
    )

    # Highlight card
    best = categories.idxmax() if len(categories) else "No data"

    highlight = ctk.CTkFrame(
        content, fg_color=CARD2, corner_radius=16
    )
    highlight.pack(fill="x", padx=7, pady=15)

    ctk.CTkLabel(
        highlight,
        text="TOP PERFORMING CATEGORY",
        text_color=MUTED,
        font=("Arial", 10, "bold")
    ).pack(anchor="w", padx=20, pady=(15, 3))

    ctk.CTkLabel(
        highlight,
        text=best,
        text_color=MINT,
        font=("Georgia", 23, "bold")
    ).pack(anchor="w", padx=20, pady=(0, 15))


# ---------------- SALES PAGE ----------------

def show_sales():
    data = filtered_df

    section_title(
        "Sales Intelligence",
        "Explore revenue trends and order performance."
    )

    cards = ctk.CTkFrame(content, fg_color=BG)
    cards.pack(fill="x")

    create_card(
        cards, "Total Revenue",
        f"{data['Total_Amount'].sum():,.0f}",
        CORAL, "Filtered sales"
    )

    create_card(
        cards, "Average Order Value",
        f"{data['Total_Amount'].mean():,.2f}",
        PURPLE, "Average transaction"
    )

    create_card(
        cards, "Products Sold",
        f"{data['Quantity'].sum():,}",
        MINT, "Total units"
    )

    monthly = data.groupby(
        data["Date"].dt.to_period("M")
    )["Total_Amount"].sum()

    payment = data["Payment_Method"].value_counts()

    row = chart_row()

    chart(
        row, "Monthly Sales Trend",
        monthly.index.astype(str).tolist(),
        monthly.values, "line", CORAL
    )

    chart(
        row, "Payment Method Usage",
        payment.index.tolist(),
        payment.values, "bar", MINT
    )


# ---------------- CUSTOMER PAGE ----------------

def show_customers():
    data = filtered_df

    section_title(
        "Customer Intelligence",
        "Understand who buys and how customers behave."
    )

    returning = data["Is_Returning_Customer"].mean() * 100

    cards = ctk.CTkFrame(content, fg_color=BG)
    cards.pack(fill="x")

    create_card(
        cards, "Unique Customers",
        f"{data['Customer_ID'].nunique():,}",
        PURPLE, "Distinct customers"
    )

    create_card(
        cards, "Returning Orders",
        f"{returning:.1f}%",
        MINT, "Share of orders"
    )

    create_card(
        cards, "Average Rating",
        f"{data['Customer_Rating'].mean():.2f}/5",
        CORAL, "Customer satisfaction"
    )

    data = data.copy()

    data["Age_Group"] = pd.cut(
        data["Age"],
        bins=[17, 25, 35, 45, 55, 100],
        labels=["18-25", "26-35", "36-45", "46-55", "55+"]
    )

    age = data.groupby(
        "Age_Group", observed=False
    )["Total_Amount"].sum()

    gender = data.groupby(
        "Gender"
    )["Total_Amount"].sum()

    row = chart_row()

    chart(
        row, "Revenue by Age Group",
        age.index.astype(str).tolist(),
        age.values, "bar", PURPLE
    )

    chart(
        row, "Gender Sales Distribution",
        gender.index.tolist(),
        gender.values, "pie"
    )


# ---------------- PRODUCT PAGE ----------------

def show_products():
    data = filtered_df

    section_title(
        "Product Intelligence",
        "Discover your best performing categories."
    )

    categories = data.groupby(
        "Product_Category"
    )["Total_Amount"].sum().sort_values(ascending=False)

    search_var = tk.StringVar()

    search_frame = ctk.CTkFrame(
        content, fg_color=CARD, corner_radius=12
    )
    search_frame.pack(fill="x", padx=7, pady=8)

    ctk.CTkLabel(
        search_frame,
        text="Search category:",
        text_color=WHITE
    ).pack(side="left", padx=15, pady=12)

    search_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text="Type category name...",
        textvariable=search_var,
        width=220
    )
    search_entry.pack(side="left", padx=5, pady=10)

    result_frame = ctk.CTkFrame(content, fg_color=BG)
    result_frame.pack(fill="x", pady=10)

    def update_products(*args):
        for widget in result_frame.winfo_children():
            widget.destroy()

        query = search_var.get().lower()

        selected = categories[
            categories.index.str.lower().str.contains(query)
        ]

        for name, value in selected.items():
            item = ctk.CTkFrame(
                result_frame,
                fg_color=CARD,
                corner_radius=12
            )
            item.pack(fill="x", padx=7, pady=5)

            ctk.CTkLabel(
                item, text=name,
                text_color=WHITE,
                font=("Arial", 13, "bold")
            ).pack(side="left", padx=18, pady=13)

            ctk.CTkLabel(
                item, text=f"Rs. {value:,.0f}",
                text_color=MINT,
                font=("Arial", 13, "bold")
            ).pack(side="right", padx=18)

        if selected.empty:
            ctk.CTkLabel(
                result_frame,
                text="No matching category found.",
                text_color=MUTED
            ).pack(pady=15)

    search_var.trace_add("write", update_products)
    update_products()

    row = chart_row()

    chart(
        row, "Category Sales Comparison",
        categories.index.tolist(),
        categories.values, "bar", PURPLE
    )


# ---------------- EXPERIENCE PAGE ----------------

def show_experience():
    data = filtered_df

    section_title(
        "Customer Experience",
        "Review ratings, delivery and customer feedback."
    )

    cards = ctk.CTkFrame(content, fg_color=BG)
    cards.pack(fill="x")

    create_card(
        cards, "Average Rating",
        f"{data['Customer_Rating'].mean():.2f}/5",
        YELLOW, "Customer feedback"
    )

    create_card(
        cards, "Delivery Time",
        f"{data['Delivery_Time_Days'].mean():.1f} days",
        MINT, "Average delivery"
    )

    create_card(
        cards, "Session Duration",
        f"{data['Session_Duration_Minutes'].mean():.1f} min",
        PURPLE, "Average session"
    )

    ratings = data["Customer_Rating"].value_counts().sort_index()
    devices = data["Device_Type"].value_counts()

    row = chart_row()

    chart(
        row, "Customer Rating Distribution",
        ratings.index.astype(str).tolist(),
        ratings.values, "bar", CORAL
    )

    chart(
        row, "Device Usage",
        devices.index.tolist(),
        devices.values, "pie"
    )


# ---------------- PAGE NAVIGATION ----------------

pages = {
    "Overview": show_overview,
    "Sales Analytics": show_sales,
    "Customer Insights": show_customers,
    "Product Analytics": show_products,
    "Customer Experience": show_experience
}

nav_buttons = {}


def show_page(page):
    global current_page
    current_page = page

    heading.configure(text=page)

    for name, button in nav_buttons.items():
        button.configure(
            fg_color=PURPLE if name == page else SIDEBAR,
            text_color=BG if name == page else WHITE
        )

    clear_content()
    pages[page]()


def create_navigation(label, function):
    button = ctk.CTkButton(
        sidebar,
        text=label,
        height=48,
        corner_radius=12,
        anchor="w",
        font=("Arial", 12, "bold"),
        fg_color=SIDEBAR,
        hover_color=CARD2,
        text_color=WHITE,
        command=function
    )
    button.pack(fill="x", padx=14, pady=5)
    nav_buttons[label] = button


create_navigation("Overview", lambda: show_page("Overview"))
create_navigation("Sales Analytics", lambda: show_page("Sales Analytics"))
create_navigation("Customer Insights", lambda: show_page("Customer Insights"))
create_navigation("Product Analytics", lambda: show_page("Product Analytics"))
create_navigation("Customer Experience", lambda: show_page("Customer Experience"))


# ---------------- SIDEBAR FOOTER ----------------

footer = ctk.CTkFrame(sidebar, fg_color=CARD, corner_radius=14)
footer.pack(side="bottom", fill="x", padx=15, pady=20)

ctk.CTkLabel(
    footer,
    text="YOUR DATA. YOUR DECISIONS.",
    font=("Arial", 9, "bold"),
    text_color=MINT
).pack(anchor="w", padx=12, pady=(12, 3))

ctk.CTkLabel(
    footer,
    text="E-Commerce Analytics\nPython Desktop Application",
    font=("Arial", 10),
    text_color=MUTED,
    justify="left"
).pack(anchor="w", padx=12, pady=(0, 12))


# ---------------- EXPORT BUTTON ----------------

def export_csv():
    if filtered_df.empty:
        messagebox.showwarning("No data", "There is no data to export.")
        return

    path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile="ecommerce_sales_report.csv"
    )

    if path:
        filtered_df.to_csv(path, index=False)
        messagebox.showinfo(
            "Export successful",
            "Your filtered report has been saved."
        )


ctk.CTkButton(
    sidebar,
    text="↓   Export Report",
    height=45,
    fg_color=MINT,
    hover_color="#88B99C",
    text_color=BG,
    font=("Arial", 12, "bold"),
    command=export_csv
).pack(side="bottom", fill="x", padx=15, pady=(0, 10))


# ---------------- START APPLICATION ----------------

show_page("Overview")

app.mainloop()
