from supabase import create_client, Client
from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, HTTPException
from typing import List
import os

# Access environment variables
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')

# Ensure the variables are set
if not supabase_url or not supabase_key:
    raise ValueError("Supabase URL and Key must be set as environment variables.")

supabase: Client = create_client(supabase_url, supabase_key)

class ChocolateBar(BaseModel):
    id: Optional[int] = None
    company: Optional[str] = None
    specific_bean_origin_or_bar_name: Optional[str] = None
    ref: Optional[int] = None
    review_date: Optional[str] = None
    cocoa_percent: Optional[float] = None
    company_location: Optional[str] = None
    rating: Optional[float] = None
    bean_type: Optional[str] = None
    broad_bean_origin: Optional[str] = None



app = FastAPI()

@app.post("/chocolate_bars/", response_model=ChocolateBar)
def create_chocolate_bar(chocolate_bar: ChocolateBar):
    data = chocolate_bar.dict(exclude_unset=True)
    inserted_data = supabase.table("chocolate_bars").insert(data).execute()
    if inserted_data.data:
        return inserted_data.data
    else:
        raise HTTPException(status_code=400, detail="Error inserting data")

@app.get("/chocolate_bars/", response_model=List[ChocolateBar])
def read_chocolate_bars():
    data = supabase.table("chocolate_bars").select("*").execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=400, detail="Error reading data")
    

@app.put("/chocolate_bars/{chocolate_bar_id}", response_model=ChocolateBar)
def update_chocolate_bar(chocolate_bar_id: int, chocolate_bar: ChocolateBar):
    data = chocolate_bar.dict(exclude_unset=True)
    updated_data = supabase.table("chocolate_bars").update(data).eq("id", chocolate_bar_id).execute()
    if updated_data.data:
        return updated_data.data
    else:
        raise HTTPException(status_code=400, detail="Error updating data")

@app.delete("/chocolate_bars/{chocolate_bar_id}", response_model=dict)
def delete_chocolate_bar(chocolate_bar_id: int):
    deleted_data = supabase.table("chocolate_bars").delete().eq("id", chocolate_bar_id).execute()
    if deleted_data.data:
        return deleted_data.data
    else:
        raise HTTPException(status_code=400, detail="Error deleting data")
