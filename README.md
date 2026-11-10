# 🎯 Amazon Price Tracker

Ένα ολοκληρωμένο Full-Stack εργαλείο παρακολούθησης τιμών στο Amazon. Το σύστημα επιτρέπει στους χρήστες να καταχωρούν το link ενός προϊόντος και την τιμή-στόχο που επιθυμούν. Αναλαμβάνει να ελέγχει αυτόματα την τιμή σε καθημερινή βάση και να στέλνει ειδοποιήσεις μέσω email όταν το προϊόν φτάσει στην επιθυμητή τιμή.

## ✨ Βασικά Χαρακτηριστικά

* **Custom Frontend UI:** Μοντέρνα και καθαρή διεπαφή (HTML/CSS/JS) για την εύκολη εισαγωγή προϊόντων, ανεξάρτητη από το backend.
* **Άμεση Επιβεβαίωση:** Αυτόματη λήψη της τρέχουσας τιμής (scraping) κατά την υποβολή της φόρμας και άμεση αποστολή επιβεβαιωτικού email (Welcome Email).
* **Αυτόματο Καθημερινό Scraping:** Ανεξάρτητος worker (`scraper_worker.py`) που εκτελείται αυτόνομα στο παρασκήνιο (μέσω της βιβλιοθήκης `schedule`).
* **Ειδοποιήσεις Email (SMTP):** Αυτόματη ενημέρωση του χρήστη μόλις η τιμή πέσει κάτω από τον στόχο.
* **Cloud Βάση Δεδομένων:** Ασφαλής αποθήκευση και ανάκτηση δεδομένων μέσω της Supabase.
* **CORS Enabled:** Πλήρης και ασφαλής επικοινωνία μεταξύ του αυτόνομου Frontend και του FastAPI Backend.

## 🛠️ Τεχνολογίες που Χρησιμοποιήθηκαν

* **Backend:** Python, FastAPI
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Database:** Supabase (PostgreSQL)
* **Web Scraping:** BeautifulSoup4, Requests
* **Αυτοματισμός:** Schedule
* **Επικοινωνία:** Smtplib (Email), Fetch API (JS)

## 📁 Δομή του Project

```text
AmazonPriceTracker/
├── frontend/
│   ├── index.html        # Η διεπαφή χρήστη
│   ├── style.css         # Μορφοποίηση της φόρμας
│   └── app.js            # Λογική επικοινωνίας με το API
├── main.py               # Το FastAPI backend, το REST API και η λογική εγγραφής
├── scraper_worker.py     # Το αυτόνομο script για το background scraping
├── data_base.py          # Λογική σύνδεσης και επικοινωνίας με τη Supabase
└── .env                  # Περιβαλλοντικές μεταβλητές (δεν ανεβαίνει στο Git)
