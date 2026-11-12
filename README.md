# 🎯 Amazon Price Tracker

A comprehensive Full-Stack tool for tracking prices on Amazon. The system allows users to enter a product link and their desired target price. It automatically checks the price on a daily basis and sends email notifications when the product reaches the desired price.

## ✨ Key Features

* **Custom Frontend UI:** Modern and clean interface (HTML/CSS/JS) for easy product entry, independent from the backend.
* **Instant Confirmation:** Automatic fetching of the current price (scraping) upon form submission and immediate dispatch of a confirmation email (Welcome Email).
* **Automated Daily Scraping:** Independent worker (`scraper_worker.py`) that runs autonomously in the background (via the `schedule` library).
* **Email Notifications (SMTP):** Automatic user notification as soon as the price drops below the target.
* **Cloud Database:** Secure storage and retrieval of data via Supabase.
* **CORS Enabled:** Full and secure communication between the standalone Frontend and the FastAPI Backend.

## 🛠️ Technologies Used

* **Backend:** Python, FastAPI
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Database:** Supabase (PostgreSQL)
* **Web Scraping:** BeautifulSoup4, Requests
* **Automation:** Schedule
* **Communication:** Smtplib (Email), Fetch API (JS)

## 📂 Project Structure

```text
AmazonPriceTracker/
├── frontend/
│   ├── index.html        # User interface
│   ├── style.css         # Form styling
│   └── app.js            # API communication logic
├── main.py               # FastAPI backend, REST API, and registration logic
├── scraper_worker.py     # Standalone script for background scraping
├── data_base.py          # Connection and communication logic with Supabase
└── .env                  # Environment variables (not uploaded to Git)
