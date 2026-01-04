import httpx
import json
import time

BASE_URL = "http://localhost:8000/api"

def run_manual_tests():
    print("Waiting 2s for server...")
    time.sleep(2)
    
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        # 1. Health
        try:
            resp = client.get("applications/") # Checking connectivity via list
            if resp.status_code == 200:
                print("Server is UP.")
            else:
                 print(f"Server check failed: {resp.status_code}")
        except Exception as e:
            print(f"Connection failed: {e}")
            return

        # 2. Create Application
        print("\n[1] Creating Application...")
        app_payload = {
            "business": {
                "legal_name": "Curl Test Corp",
                "industry": "CONSTRUCTION",
                "state": "NY",
                "years_in_business": 5,
                "annual_revenue": 500000
            },
            "guarantors": [{
                "first_name": "John",
                "last_name": "Doe",
                "fico_score": 720,
                "ownership_percentage": 100
            }],
            "loan_request": {
                "amount": 50000,
                "term_months": 48,
                "equipment_type": "Construction Equipment",
                "equipment_cost": 50000
            }
        }
        resp = client.post("applications/", json=app_payload)
        if resp.status_code == 201:
            app_id = resp.json()["application_id"]
            status = resp.json()["status"]
            print(f"SUCCESS: Created App {app_id} Status: {status}")
        else:
            print(f"FAIL: {resp.text}")
            return

        # 3. Trigger Underwriting
        print(f"\n[2] Running Underwriting for {app_id}...")
        resp = client.post(f"underwriting/run/{app_id}")
        if resp.status_code == 200:
            print(f"SUCCESS: {resp.json()}")
        else:
            print(f"FAIL: {resp.text}")

        # 4. Get Results
        print(f"\n[3] Getting Results...")
        resp = client.get(f"underwriting/results/{app_id}")
        if resp.status_code == 200:
            results = resp.json()
            print(f"SUCCESS: {len(results)} matches found.")
            if results:
                print(f"Top Match: {results[0]['fit_score']} - Eligible: {results[0]['is_eligible']}")
        else:
            print(f"FAIL: {resp.text}")

if __name__ == "__main__":
    run_manual_tests()
