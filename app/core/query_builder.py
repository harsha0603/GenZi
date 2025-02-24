from sqlalchemy.orm import Session
from app.db.database import Property

def build_property_query(db: Session, params: dict):
    """
    Builds a SQLAlchemy query for properties based on extracted parameters.
    
    Expected keys in params:
        - property_type: string or None (e.g., "apartment", "villa")
        - min_rent: number or None
        - max_rent: number or None
        - building_name: string or None
        - address: string or None
    
    Returns a list of Property objects matching the criteria.
    """
    query = db.query(Property)
    
    property_type = params.get("property_type")
    if property_type:
        query = query.filter(Property.type.ilike(f"%{property_type}%"))
    
    min_rent = params.get("min_rent")
    max_rent = params.get("max_rent")
    if min_rent is not None:
        try:
            query = query.filter(Property.rent_price >= float(min_rent))
        except ValueError:
            pass  
    if max_rent is not None:
        try:
            query = query.filter(Property.rent_price <= float(max_rent))
        except ValueError:
            pass
    
    building_name = params.get("building_name")
    if building_name:
        query = query.filter(Property.building_name.ilike(f"%{building_name}%"))
    
    address = params.get("address")
    if address:
        query = query.filter(Property.address.ilike(f"%{address}%"))
    
    results = query.all()
    return results
