# -*- coding: utf-8 -*-
import io
import matplotlib.pyplot as plt
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi import APIRouter
from app.services.berry_service import get_berry_stats
from app.models.berry_models import BerryStatsResponseModel

router = APIRouter()

@router.get("/allBerryStats", response_model=BerryStatsResponseModel)
async def all_berry_stats():
    """
    Fetch all berry growth statistics.

    This endpoint fetches and returns the berry growth statistics such as minimum, 
    maximum, median, mean, variance, and the frequency distribution of growth times.

    Returns:
        BerryStatsResponseModel: A JSON response containing the berry growth statistics.
    """
    return await get_berry_stats()

@router.get("/histogram", responses={200: {"content": {"image/png": {}}}})
async def generate_histogram():
    """
    Generate a histogram image of berry growth times and return it as a PNG image.
    
    Fetches the berry growth statistics, processes the frequency of growth times, and uses matplotlib
    to create a histogram. If valid growth times are available, the plot is generated and returned.
    Otherwise, an error message is provided in the response.
    
    Returns:
        StreamingResponse: A PNG image of the histogram if growth times are available,
        or an error message if no valid growth times exist.
    """
    stats = await get_berry_stats()
    
    growth_times = []
    
    for growth_time, frequency in stats.frequency_growth_time.items():
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
    """
    View the berry growth time histogram in HTML.

    This endpoint displays the histogram of berry growth times in a simple HTML page 
    by embedding the PNG image generated from the `/histogram` endpoint.

    Returns:
        HTMLResponse: An HTML page displaying the histogram image.
    """
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