def calculate_risk(value):
    # This will cause a ZeroDivisionError
    return value / 0

if __name__ == "__main__":
    print("Starting risk calculation...")
    calculate_risk(100)
