import smtplib
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
from pprint import pprint
load_dotenv()
smtp_address=os.environ.get("SMTP_ADDRESS")
usn_email=os.environ.get("USN")
password=os.environ.get("PSW")
sender_email=os.environ.get("SENDER")
# site_url='https://appbrewery.github.io/instant_pot/'
site_url="https://www.amazon.com/Instant-Pot-Multi-Use-Programmable-Pressure/dp/B00FLYWNYQ/ref=dp_fod_d_sccl_2/143-0701800-5214710?pd_rd_w=L0fXE&content-id=amzn1.sym.c9fb9865-4d2c-4ceb-ba49-da7c55243c76&pf_rd_p=c9fb9865-4d2c-4ceb-ba49-da7c55243c76&pf_rd_r=9T7765NRA01YQMW79BSF&pd_rd_wg=DBkIz&pd_rd_r=c324bbf1-2a46-4497-9aff-6ea94b12c38c&pd_rd_i=B00FLYWNYQ&psc=1"
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
response = requests.get(site_url,headers=my_headers)
# print(response.status_code)
webpage=response.text
soup = BeautifulSoup(webpage, 'html.parser')
# pprint(soup)
# price=soup.find('p', class_='a-spacing-none a-text-left a-size-mini twisterSwatchPrice').text
price = soup.find("span",class_="a-offscreen").get_text()
prices_list=price.split("EUR")
product_price=float(prices_list[1])
product_title = " ".join(soup.select_one("#productTitle").getText().split())
print(product_title)
print(product_price)
if product_price<100:
    with smtplib.SMTP(smtp_address,587) as smtp:
        smtp.starttls()
        smtp.login(usn_email,password)
        smtp.sendmail(from_addr=usn_email,
                      to_addrs=sender_email,
                      msg=f"Subject:Price Alert\n\n{product_title}\n{product_price}$\n{site_url}".encode("utf-8")
                      )
else:
    print("High price")
