from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from datetime import datetime

# Load environment variables
load_dotenv()

# Server startup timestamp for tracking changes
SERVER_START_TIME = datetime.now().isoformat()

app = FastAPI(title="Simple FastAPI App", 
             description="A clean FastAPI application",
             version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/version")
def get_version():
    """Return the current API version (timestamp when server started)"""
    return {"version": SERVER_START_TIME}


@app.get("/", response_class=HTMLResponse)
def auto_refreshing_docs():
    """Documentation page that automatically refreshes when the server changes"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Auto-refreshing API Documentation</title>
        <script>
            let lastVersion = '';
            
            // Function to check server version
            async function checkVersion() {
                try {
                    const response = await fetch('/api/version');
                    const data = await response.json();
                    
                    // If this is the first check, store the version
                    if (lastVersion === '') {
                        lastVersion = data.version;
                        console.log('Server version:', lastVersion);
                    } 
                    // If version changed, reload the page
                    else if (lastVersion !== data.version) {
                        console.log('Server version changed. Reloading...');
                        window.location.reload();
                    }
                } catch (error) {
                    console.error('Error checking version:', error);
                }
                
                // Check again in 2 seconds
                setTimeout(checkVersion, 2000);
            }
            
            // Start checking when the page loads
            window.onload = checkVersion;
        </script>
        <style>
            body, html {
                margin: 0;
                padding: 0;
                height: 100%;
                overflow: hidden;
            }
            iframe {
                width: 100%;
                height: 100vh;
                border: none;
            }
        </style>
    </head>
    <body>
        <iframe src="/docs"></iframe>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/hello")
def say_hello():
    return "Hello, World!"


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", "3000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
