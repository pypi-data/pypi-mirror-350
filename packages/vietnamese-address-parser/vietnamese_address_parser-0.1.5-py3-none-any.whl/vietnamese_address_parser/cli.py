from vietnamese_address_parser import __version__

def main():
    # Print static banner without calling Hello
    print(f"Vietnamese Address Parser v{__version__}")
    print("Hello! Welcome to the Vietnamese Address Parser CLI.")
    print("Usage example:")
    print("    parser = VietnameseAddressParser()")
    print("    result = parser('54-55 Bàu Cát 4, Phường 14, Tân Bình, Hồ Chí Minh')")
    print("    print(result)")
    print()
    print("⚠️   Note: This parser uses the OpenStreetMap Nominatim API for geolocation enhancement.")
    print("     As a result, some lookups may take a few seconds due to network latency or rate limits.")