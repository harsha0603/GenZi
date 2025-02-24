from datetime import timedelta
import random
from faker import Faker
from app.db.database import SessionLocal, Property, create_tables

fake = Faker()  

def generate_dummy_properties(n):
    properties = []
    for _ in range(n):
        building_name = fake.company() + " " + random.choice(["Residences", "Heights", "Villas", "Park"])
        house_name = f"{random.randint(1, 20)}#{random.randint(1, 50)}-{random.randint(1, 10)}"
        address = fake.address().replace("\n", ", ")
        contract_start_date = fake.date_between(start_date='-1y', end_date='today')
        contract_end_date = contract_start_date + timedelta(days=365)
        rent_price = round(random.uniform(2000, 10000), 2)
        property_type = random.choice(["Condominium", "Apartment", "Landed House", "HDB"])
        total_rooms = random.randint(1, 6)
        
        prop = Property(
            building_name=building_name,
            house_name=house_name,
            address=address,
            contract_start_date=contract_start_date,
            contract_end_date=contract_end_date,
            rent_price=rent_price,
            type=property_type,
            total_rooms=total_rooms
        )
        properties.append(prop)
    return properties

def insert_large_dummy_data(n):
    create_tables()
    session = SessionLocal()
    try:
        dummy_properties = generate_dummy_properties(n)
        session.bulk_save_objects(dummy_properties)
        session.commit()
        print(f"Inserted {n} dummy properties successfully!")
    except Exception as e:
        session.rollback()
        print("Error inserting large dummy data:", e)
    finally:
        session.close()

if __name__ == "__main__":
    insert_large_dummy_data(500) 
