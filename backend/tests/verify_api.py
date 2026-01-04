import asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models.business import IndustryType
from app.models.lender import CriteriaType

async def verify_api():
    print("Starting API Verification...")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        
        # 1. Create Application
        app_payload = {
            "business": {
                "legal_name": f"API Test Biz {uuid.uuid4()}",
                "industry": IndustryType.TECHNOLOGY.value,
                "state": "CA",
                "years_in_business": 5,
                "annual_revenue": 1000000
            },
            "guarantors": [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "fico_score": 720,
                    "ownership_percentage": 100
                }
            ],
            "loan_request": {
                "amount": 75000,
                "term_months": 36,
                "equipment_type": "Computers",
                "equipment_cost": 75000
            }
        }
        
        resp = await client.post("/api/applications/", json=app_payload)
        if resp.status_code != 201:
            print(f"Create App Failed: {resp.text}")
            return
        assert resp.status_code == 201
        data = resp.json()
        app_id = data["application_id"]
        print(f"Created Application: {app_id}")
        
        # 2. Create Lender
        lender_payload = {
            "name": f"API Lender {uuid.uuid4()}",
            "is_active": True,
            "excluded_states": [],
            "programs": [
                {
                    "program_name": "Tech Program",
                    "tier_name": "A",
                    "criteria": [
                        {
                            "criteria_type": CriteriaType.FICO_MIN.value,
                            "value_numeric": 700
                        }
                    ]
                }
            ]
        }
        
        resp = await client.post("/api/lenders/", json=lender_payload)
        if resp.status_code != 201:
             print(f"Create Lender Failed: {resp.text}")
        assert resp.status_code == 201
        lender_id = resp.json()["id"]
        print(f"Created Lender: {lender_id}")
        
        # 3. Run Underwriting
        resp = await client.post(f"/api/underwriting/run/{app_id}")
        assert resp.status_code == 200
        print("Underwriting Run:", resp.json())
        
        # 4. Get Results
        resp = await client.get(f"/api/underwriting/results/{app_id}")
        assert resp.status_code == 200
        results = resp.json()
        print(f"Match Results Found: {len(results)}")
        if len(results) > 0:
             print(f"First Result Score: {results[0]['fit_score']}")
             print(f"Is Eligible: {results[0]['is_eligible']}")

if __name__ == "__main__":
    asyncio.run(verify_api())
