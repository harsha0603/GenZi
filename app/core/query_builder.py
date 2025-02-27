from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.db.database import Property, Room, Washroom  # Fixed model name

def build_property_query(db: Session, params: dict):
    """
    Builds a SQLAlchemy query to fetch property listings along with room and washroom details.

    Expected keys in params:
        - property_type (str or None): e.g., "apartment", "villa"
        - min_rent (int or None)
        - max_rent (int or None)
        - num_bedrooms (int or None)
        - num_washrooms (int or None)
        - building_name (str or None)
        - address (str or None)
        - location_preference (str or None): "nearby", "in", etc.
        - amenities (list of str or None): e.g., ["gym", "pool"]
    
    Returns a structured list of properties with related room and washroom details.
    """
    query = db.query(Property).options(
        joinedload(Property.rooms),      # Load related Room data
        joinedload(Property.washrooms)   # Load related Washroom data
    )

    # 🔹 Property Type Filter
    if params.get("property_type"):
        query = query.filter(Property.type.ilike(f"%{params['property_type']}%"))

    # 🔹 Rent Range Filters
    if params.get("min_rent") is not None:
        query = query.filter(Property.rent_price >= float(params["min_rent"]))
    if params.get("max_rent") is not None:
        query = query.filter(Property.rent_price <= float(params["max_rent"]))

    # 🔹 Bedroom Filter
    if params.get("num_bedrooms") is not None:
        query = query.join(Room).filter(Room.count == int(params["num_bedrooms"]))

    # 🔹 Washroom Filter
    if params.get("num_washrooms") is not None:
        query = query.join(Washroom).filter(Washroom.count == int(params["num_washrooms"]))

    # 🔹 Location Filter (Handles "nearby", "exact match")
    if params.get("address"):
        if params.get("location_preference") == "nearby":
            query = query.filter(Property.address.ilike(f"%{params['address']}%"))
        else:
            query = query.filter(Property.address == params["address"])

    # 🔹 Building Name Filter
    if params.get("building_name"):
        query = query.filter(Property.building_name.ilike(f"%{params['building_name']}%"))

    # 🔹 Amenities Filter (Handles multiple selections)
    if params.get("amenities"):
        amenity_filters = [Property.amenities.ilike(f"%{a}%") for a in params["amenities"]]
        query = query.filter(and_(*amenity_filters))

    # 🔹 Fetch and structure data
    results = query.all()
    property_list = []
    
    for prop in results:
        property_list.append({
            "property_id": prop.id,
            "building_name": prop.building_name,
            "type": prop.type,
            "rent_price": prop.rent_price,
            "address": prop.address,
            "amenities": prop.amenities.split(",") if prop.amenities else [],  # Convert CSV string to list
            "rooms": [{"count": room.count, "size": room.size} for room in prop.rooms],  
            "washrooms": [{"count": washroom.count, "type": washroom.type} for washroom in prop.washrooms]  
        })

    return property_list
