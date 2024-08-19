from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <html>
        <head>
            <title>PokeAPI Berries Statistics API</title>
            <link rel="stylesheet" type="text/css" href="/static/styles.css">
        </head>
        <body>
            <div class="container">
                <h1>Welcome to the PokeAPI Berries Statistics API</h1>
                <p>This API provides various statistics on berries from the PokeAPI.</p>
                <p>Try the following endpoints:</p>
                <ul>
                    <li><a href="/docs">/docs</a> - API documentation</li>
                    <li><a href="/allBerryStats">/allBerryStats</a> - Get berry growth statistics</li>
                    <li><a href="/view-histogram">/view-histogram</a> - View histogram of berry growth times</li>
                </ul>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)