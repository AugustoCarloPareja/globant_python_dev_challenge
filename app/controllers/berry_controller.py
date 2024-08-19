import io
import matplotlib.pyplot as plt
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi import APIRouter
from app.services.berry_service import get_berry_stats
from app.models.berry_models import BerryStatsResponseModel

router = APIRouter()

@router.get("/allBerryStats", response_model=BerryStatsResponseModel)
async def all_berry_stats():
    return await get_berry_stats()

@router.get("/histogram", responses={200: {"content": {"image/png": {}}}})
async def generate_histogram():
    stats = await get_berry_stats()
    
    growth_times = []
    for growth_time, frequency in stats['frequency_growth_time'].items():
        growth_times.extend([int(growth_time)] * frequency)
    
    if growth_times:
        fig, ax = plt.subplots()
        
        bins = range(0, max(growth_times) + 2)
        
        ax.hist(growth_times, bins=bins, edgecolor='black')
        
        ax.set_title('Berry Growth Time Distribution (Hours per Growth Stage)')
        ax.set_xlabel('Growth Time (Hours per Stage)')
        ax.set_ylabel('Number of Berries')
        ax.set_xticks(list(bins))
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        return StreamingResponse(buf, media_type="image/png")
    else:
        return {"error": "No valid growth times available for plotting."}

@router.get("/view-histogram", response_class=HTMLResponse)
async def view_histogram():
    html_content = """
    <html>
        <head>
            <title>Berry Growth Time Histogram</title>
        </head>
        <body>
            <img src="/histogram" alt="Histogram of Berry Growth Time">
        </body>
    </html>
    """
    return html_content