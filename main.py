from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from data_base import add_data,get_data
from fastapi.middleware.cors import CORSMiddleware

import requests
from bs4 import BeautifulSoup
import smtplib
from scraper_worker import my_headers, USN_EMAIL, password, smtp_address

app = FastAPI()

# Προσθήκη του CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Επιτρέπει στο frontend (από οποιαδήποτε πόρτα) να μιλήσει στο API
    allow_credentials= True,
    allow_methods=["*"],  # Επιτρέπει GET, POST κλπ.
    allow_headers=["*"],
)


class Product(BaseModel):
    product_url: str
    target_price: float
    user_email: str


def send_welcome_email(product_title, current_price, target_price, product_url, receiver_email):
    with smtplib.SMTP(smtp_address, 587) as smtp:
        smtp.starttls()
        smtp.login(USN_EMAIL, password)

        subject = "Επιτυχης Εναρξη Παρακολουθησης Τιμης!"
        body = (f"Γεια σου!\n\n"
                f"Ξεκινήσαμε την παρακολούθηση για το προϊόν:\n{product_title}\n\n"
                f"Τρέχουσα Τιμή: {current_price} EUR\n"
                f"Ο Στόχος σου: {target_price} EUR\n\n"
                f"Θα λάβεις νεότερο email μόνο όταν η τιμή πέσει κάτω από το στόχο σου.\n"
                f"Link: {product_url}")

        msg = f"Subject: {subject}\n\n{body}".encode("utf-8")
        smtp.sendmail(from_addr=USN_EMAIL, to_addrs=receiver_email, msg=msg)


@app.post("/", response_model=Product)
def add_product(product: Product):
    # 1. Κάνουμε μια γρήγορη "επίσκεψη" στο Amazon για να πάρουμε τα 2 στοιχεία που μας λείπουν
    try:
        response = requests.get(product.product_url, headers=my_headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Βρίσκουμε την τρέχουσα τιμή και τον τίτλο
        price_text = soup.find("span", class_="a-offscreen").get_text()
        current_price = float(price_text.split("EUR")[1])
        product_title = " ".join(soup.select_one("#productTitle").getText().split())

        # 2. ΤΩΡΑ καλούμε τη συνάρτηση του email.
        # Της δίνουμε τον τίτλο/τιμή που μόλις βρήκαμε, και τα URL/Target/Email που έβαλε ο χρήστης στη φόρμα (product.κάτι)
        send_welcome_email(product_title,current_price,product.target_price,product.product_url,product.user_email
        )
    except Exception as e:
        print(f"Το scraping ή το email απέτυχε κατά την εγγραφή: {e}")
        # Αν πέσει το ίντερνετ ή το Amazon, προχωράμε κανονικά για να μη χάσουμε την εγγραφή

    # 3. Αποθήκευση στη βάση δεδομένων (Supabase)
    add_data(product.product_url, product.target_price, product.user_email)

    return product

# @app.post("/", response_model=Product)
# def add_product(product: Product):
#     add_data(product.product_url,product.target_price,product.user_email)
#     return product

@app.get("/get_items",response_model=list[Product])
def get_item():
    data=get_data()
    print(data)
    return data


# class Item(BaseModel):
#     text: str = None
#     is_done: bool= False
#
# items=[]
# @app.get("/")
# def root():
#     return {"message": "Hello World"}
#
# @app.post("/items")
# def create_item(item: Item):
#     items.append(item)
#     return items
#
# @app.get("/items", response_model=list[Item])
# def list_items(limit: int = 10):
#     return items[0:limit]
#
# @app.get("/items/{item_id}", response_model=Item)
# def read_item(item_id: int)-> Item:
#     if item_id< len(items):
#         return items[item_id]
#     else:
#         raise HTTPException(status_code=404, detail=f"Item {item_id} not found")