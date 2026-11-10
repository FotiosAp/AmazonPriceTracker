import smtplib
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from data_base import get_data
import requests
import schedule
import time
from pprint import pprint
load_dotenv()
smtp_address=os.environ.get("SMTP_ADDRESS")
USN_EMAIL=os.environ.get("USN")
password=os.environ.get("PSW")
# sender_email=os.environ.get("SENDER")
# site_url='https://appbrewery.github.io/instant_pot/'
# site_url="https://www.amazon.com/Instant-Pot-Multi-Use-Programmable-Pressure/dp/B00FLYWNYQ/ref=dp_fod_d_sccl_2/143-0701800-5214710?pd_rd_w=L0fXE&content-id=amzn1.sym.c9fb9865-4d2c-4ceb-ba49-da7c55243c76&pf_rd_p=c9fb9865-4d2c-4ceb-ba49-da7c55243c76&pf_rd_r=9T7765NRA01YQMW79BSF&pd_rd_wg=DBkIz&pd_rd_r=c324bbf1-2a46-4497-9aff-6ea94b12c38c&pd_rd_i=B00FLYWNYQ&psc=1"
my_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "el,en;q=0.9",
    "Priority": "u=0, i",
    "Referer": "https://httpbin.org/legacy",
    "Sec-Ch-Ua": "\"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"156\", \"Google Chrome\";v=\"156\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
    "X-Amzn-Trace-Id": "Root=1-6adce3d7-664fe92f2439179918f73412"
}
def send_alert_email(product_title,current_price,product_url,receiver_email):
    with smtplib.SMTP(smtp_address,587) as smtp:
        smtp.starttls()
        smtp.login(USN_EMAIL,password)
        smtp.sendmail(from_addr=USN_EMAIL,
                      to_addrs=receiver_email,
                      msg=f"Subject:Price Alert\n\n{product_title}\n{current_price}$\n{product_url}".encode("utf-8")
                      )
def run_scraper():
    all_items=get_data()
    for item in all_items:
        url_product=item["product_url"]
        target_price=item["target_price"]
        email=item["user_email"]
        response = requests.get(url_product,headers=my_headers)
        # print(response.status_code)
        webpage=response.text
        soup = BeautifulSoup(webpage, 'html.parser')
        # pprint(soup)
        # price=soup.find('p', class_='a-spacing-none a-text-left a-size-mini twisterSwatchPrice').text
        try:
            price = soup.find("span",class_="a-offscreen").get_text()
            prices_list=price.split("EUR")
            product_price=float(prices_list[1])
            product_title = " ".join(soup.select_one("#productTitle").getText().split())
            print(product_title)
            print(product_price)
            if product_price<target_price:
                send_alert_email(product_title,product_price,url_product,email)
            else:
                print("High price")
        except Exception as e:
            print(f"Failed to scrape data: {e}")

if __name__ == "__main__":
    schedule.every().day.at("19:00").do(run_scraper)
    while True:
        schedule.run_pending()
        time.sleep(1)

