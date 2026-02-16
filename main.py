from fastapi import FastAPI
from routes.dashboard import router as dashboard_router
from routes.campaign_kpi import router as campaign_router
from routes.leads_analytics import router as lead_router
from routes.create_campaign import router as campaign_create_router
from routes.lead_scraping import router as lead_scraping_router
from routes.leads_approved import router as leads_approved_router


app = FastAPI(title="Leads API")

app.include_router(dashboard_router)
app.include_router(campaign_router)
app.include_router(lead_router)
app.include_router(campaign_create_router)
app.include_router(lead_scraping_router)
app.include_router(leads_approved_router)