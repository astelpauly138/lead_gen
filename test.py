from services.dashboard_service import get_dashboard_kpis
from core.supabase_client import get_supabase
from datetime import datetime
import uuid



supabase = get_supabase()
USER_ID = "7df7b091-6007-41a1-b08c-11826f8baca3"
CAMPAIGN_ID = "a14cb492-3bf6-425f-bcc3-e7b17faa92b8"

# get dashboard kpi data


# if __name__ == "__main__":
#     data = get_dashboard_kpis(USER_ID)
#     print("Dashboard KPI Response:")
#     print(data)


# inserting value into campaign table.
# 1️⃣ Create a test campaign
# campaign_id = CAMPAIGN_ID
# campaign_data = {
#     "id": campaign_id,
#     "user_id": USER_ID,
#     "name": "Test Campaign",
#     "campaign_type": "cold outreach",
#     "industry": "Education",
#     "area": "Al jerf 1",
#     "city": "Ajman",
#     "state": "",
#     "country": "UAE",
#     "job_titles":  ["Dean", "CTO", "Manager"],
#     "requested_leads": 3,
#     "status": "pending",
#     "created_at": datetime.utcnow().isoformat()
# }

# supabase.table("campaigns").insert(campaign_data).execute()
# print("Test campaign inserted successfully.")



# insert values into leads table

# 2️⃣ Insert scraped leads
scraped_data = [
  {
    "row_number": 2,
    "Sr No.": "",
    "Company": "Ajman University",
    "Category": "University",
    "Location": "Al jerf 1",
    "Address": "University Street - Al jerf 1 - Ajman - United Arab Emirates",
    "Website": "https://www.ajman.ac.ae/en?utm_source=gbp&utm_medium=organic&utm_campaign=ajman_university_gbp",
    "Domain": "ajman.ac.ae",
    "Employee Name": "Fares",
    "Position": "Dean, College of Humanites and Science | Director, General Education Program",
    "Work Email": "",
    "Email Status": "",
    "Work Mobile No.": "",
    "Promotion Status": ""
  },
  {
    "row_number": 3,
    "Sr No.": "",
    "Company": "Jams HR Solutions FZE",
    "Category": "Human resource consulting",
    "Location": "Mena Jabal Ali - Jebel Ali Freezone",
    "Address": "Plot no: B009R06 Jebel Ali Free Zone Gate No. 02 - Dubai - United Arab Emirates",
    "Website": "https://www.jamshrsolutions.com/",
    "Domain": "jamshrsolutions.com",
    "Employee Name": "Arif",
    "Position": "Operations Supervisor",
    "Work Email": "arif@jamshrsolutions.com",
    "Email Status": "verified",
    "Work Mobile No.": "",
    "Promotion Status": ""
  },
  {
    "row_number": 4,
    "Sr No.": "",
    "Company": "Jams HR Solutions FZE",
    "Category": "Human resource consulting",
    "Location": "Mena Jabal Ali - Jebel Ali Freezone",
    "Address": "Plot no: B009R06 Jebel Ali Free Zone Gate No. 02 - Dubai - United Arab Emirates",
    "Website": "https://www.jamshrsolutions.com/",
    "Domain": "jamshrsolutions.com",
    "Employee Name": "Hany",
    "Position": "Director of Government Relations",
    "Work Email": "hany@jamshrsolutions.com",
    "Email Status": "verified",
    "Work Mobile No.": "",
    "Promotion Status": ""
  }
]

for lead in scraped_data:
    lead_row = {
        "id": str(uuid.uuid4()),
        "campaign_id": CAMPAIGN_ID,
        "user_id": USER_ID,
        "name": lead["Employee Name"],
        "email": lead["Work Email"],
        "company": lead["Company"],
        "phone": lead["Work Mobile No."],
        "status": "pending",
        "quality_score": None,
        "last_contacted": None,
        "created_at": datetime.utcnow().isoformat(),
        "category": lead["Category"],
        "position": lead["Position"],
        "email_status": lead["Email Status"],
        "website": lead["Website"],
        "domain": lead["Domain"],
        "location": lead["Location"],
        "address": lead["Address"],
        "promotion_status": lead["Promotion Status"]
    }
    supabase.table("leads").insert(lead_row).execute()
print("Scraped leads inserted successfully.")



3️⃣ Insert activity log
activity_id = str(uuid.uuid4())
activity_log = {
    "id": activity_id,
    "campaign_id": CAMPAIGN_ID,
    "user_id": USER_ID,
    "action": message, ,
    # "description": f"{len(scraped_data)} leads scraped for campaign {campaign_id}",
    "metadata": will be passed,
    "created_at": datetime.utcnow().isoformat()
}
supabase.table("activity_logs").insert(activity_log).execute()
print("Activity log inserted successfully.")


# After approving the leads

leads_1= {
  "user_id": "7df7b091-6007-41a1-b08c-11826f8baca3",
  "campaign_id": "xxxx-uuid-yyy",
  "leads": [
    {"lead_id": "aaa-uuid-111", "approved": True},
    {"lead_id": "bbb-uuid-222", "approved": True}
  ]
}

leads = [
    {"lead_id": "1684aaaf-fd76-4b0b-a7f4-1a633563bc8b", "approved": True},
    {"lead_id": "c3f5f7d1-8848-4094-8a6b-48371a7ad437", "approved": True}
  ]

for lead in leads:
    supabase.table("leads") \
        .update({"status": "approved"}) \
        .eq("id", lead["lead_id"]) \
        .execute()
print("Leads approved successfully.")



after updating leads table ,we are updating the activity table.
activity_log = {
    "id": str(uuid.uuid4()),
    "campaign_id": CAMPAIGN_ID,
    "user_id": USER_ID,
    "action": f"{len(leads)} leads approved",
    # "description": f"{len(leads)} leads approved",
    "metadata": {"leads": [lead["lead_id"] for lead in leads]},
    "created_at": datetime.utcnow().isoformat()
}
supabase.table("activity_logs").insert(activity_log).execute()



updating the leads status to sent after sending the email campaign.
for lead in leads:
    supabase.table("leads") \
        .update({"status": "sent", "last_contacted": datetime.utcnow().isoformat()}) \
        .eq("id", lead["lead_id"]) \
        .execute()
# expression approve ahnon koode check cheyanm
print("Leads status updated to sent successfully.")


After sending each email, record an entry in email_events:
for lead in leads:
    email_event = {
        "id": str(uuid.uuid4()),
        "user_id": USER_ID,
        "campaign_id": CAMPAIGN_ID,
        "lead_id": lead["lead_id"],
        "event_type": "sent",
        "created_at": datetime.utcnow().isoformat()
    }
    supabase.table("email_events").insert(email_event).execute()


# Return Response to Frontend

# Return JSON like:

{
  "user_id": "7df7b091-6007-41a1-b08c-11826f8baca3",
  "campaign_id": "xxxx-uuid",
  "leads": [
    {"lead_id": "aaa-uuid-111", "approved": true, "status": "sent"},
    {"lead_id": "bbb-uuid-222", "approved": true, "status": "sent"}
  ],
  "message": "Emails sent and leads updated successfully"
}


# This is exactly how frontend knows which leads were approved and sent.















