# Inventory Management Dashboard (Dash + PostgreSQL)

<p align="center">
  <img src="output preview/Dashboard.png" width="900">
</p>
>  Note: For more images of project see the output preview folder.

## 📌 Overview

This project is an **interactive inventory and sales management dashboard** built using **Dash, Plotly, and PostgreSQL**. It provides real-time insights into product stock, sales, profit, vendors, and active deliveries, along with the ability to place and manage shipment orders directly from the UI.

The system is designed to simulate a **real-world retail/warehouse management system**, focusing on backend–frontend integration, database-driven analytics, and stateful UI interactions.

Data is pulled from postgreSQL db.

---


## 🚀 Key Features

* 📊 **Dynamic Profit & Sales Analytics** (Monthly & Yearly)
* 🥧 **Vendor-wise Stock Distribution (Pie Chart)**
* 🔍 **Product Search with Stock, Sales & Profit Details**
* 🚚 **Live Active Deliveries Feed**
* 📝 **Order Placement with Confirmation Flow**
* ✅ **Mark Deliveries as Delivered / Cancel Orders**
* 🔄 **Automatic Inventory Stock Updates**
* 🗄️ **PostgreSQL-backed Persistent Storage**

---

## 🛠️ Tech Stack

* **Frontend / Dashboard:** Dash, Plotly
* **Backend Logic:** Python
* **Database:** PostgreSQL
* **ORM / DB Access:** SQLAlchemy
* **Data Processing:** Pandas

---

## 📂 Project Structure

```
project-root/
│── app.py                  # Main Dash application
│── db.py                   # Database connection (SQLAlchemy engine)
│── requirements.txt        # Python dependencies
│── README.md               # Project documentation
│── Data                    # Folder that contains the same data present in the sql db  
```

---

## ⚙️ Setup & Installation

### Prerequisites

* Python 3.9+
* PostgreSQL
* Git

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/inventory-dashboard.git
cd inventory-dashboard
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Database Configuration

Create `db.py` with your PostgreSQL credentials:

```python
engine = create_engine("postgresql://username:password@localhost:5432/database_name")
```

Ensure the following tables exist:

* `products`
* `vendors`
* `selling_records`
* `shipment_records`

---

## ▶️ Running the Application

```bash
python app.py
```

The dashboard will be available at:

```
http://127.0.0.1:8050/
```

---

## 📊 Dashboard Modules

### 🔹 Profit & Sales Analysis

* Toggle between **Profit** and **Sales**
* View **Yearly** or **Monthly** trends
* Profit is calculated using:

  * Selling price
  * Purchase price
  * Discount rates

### 🔹 Vendor Stock Pie Chart

* Displays vendor-wise total stock contribution
* Hover to view product-level stock details

### 🔹 Product Search

* Search products using a dynamic dropdown
* Displays:

  * Current inventory stock
  * Total sales value
  * Total profit

### 🔹 Live Delivery Management

* View latest active shipments
* Click to see detailed delivery info
* Options to:

  * Mark delivery as **Delivered**
  * **Cancel** an order
* Inventory auto-updates on delivery confirmation

---

## 🧠 Core Concepts Demonstrated

* SQL + Python integration using SQLAlchemy
* Stateful UI handling with Dash callbacks
* Complex callback chaining & pattern-matching callbacks
* Real-time inventory updates
* Business metric calculations (profit, sales, discounts)
* Production-style dashboard architecture

---

## 👤 Author

**Faizan Khan**
B.Tech Data Science Student

LinkedIn: [www.linkedin.com/in/faizan-khan-114236291](www.linkedin.com/in/faizan-khan-114236291)

