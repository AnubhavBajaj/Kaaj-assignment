from app.models import Business, Lender
try:
    print(f"Business.__tablename__: {Business.__tablename__}")
    if Business.__tablename__ == 'businesses':
        print("Verification SUCCESS")
    else:
        print("Verification FAILED")
except Exception as e:
    print(f"Error: {e}")
