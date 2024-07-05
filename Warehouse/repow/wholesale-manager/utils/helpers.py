from geopy.geocoders import Nominatim


def get_geo_code_from_address(address1, city, state, country):
    """Return Geo code for provided address."""
    try:
        geolocator = Nominatim(user_agent="my_user_agent")
        location = geolocator.geocode(address1+','+city+','+state+','+country)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return None
    return location