import os
from dotenv import load_dotenv
from supabase import create_client,Client
load_dotenv()
supabase_url=os.environ.get('SUPABASE_URL')
supabase_key=os.environ.get('SUPABASE_KEY')
my_supabase_client=create_client(supabase_url,supabase_key)
def add_data(product_url,target_price,user_email):
    new_data={
        "product_url": product_url,
        "target_price": target_price,
        "user_email": user_email
    }
    response=my_supabase_client.table("tracked_items").insert(new_data).execute()
    return response
def get_data():
    response=my_supabase_client.table("tracked_items").select("*").execute()
    data=response.data
    return data
def check_if_the_product_exists(product_url,user_email):
    response=my_supabase_client.table("tracked_items").select("*").eq("product_url",product_url).eq("user_email",user_email).execute()
    if len(response.data)>0:
        return True
    else:
        return False
def update_data(product_url,new_target_price,user_email):
    updated_price={
        "target_price": new_target_price
    }
    response=my_supabase_client.table("tracked_items").update(updated_price).eq("product_url",product_url).eq("user_email",user_email).execute()
    return response