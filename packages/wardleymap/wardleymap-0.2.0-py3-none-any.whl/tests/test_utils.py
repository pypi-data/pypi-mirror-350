from wardley_map.wardley_maps_utils import get_owm_map

def test_get_owm_map():
    """
    Test the retrieval of a Wardley Map text representation using its unique identifier.
    """
    map_id = "30f8e6a71f39253704"
    map_text = get_owm_map(map_id)
    print(map_text)
