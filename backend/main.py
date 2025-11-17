from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from report_processor import process_medical_report
from recommendation_engine import get_recommendation

app = FastAPI(title="NadirCare API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "NadirCare API is running"}

@app.post("/upload")
async def upload_report(file: UploadFile = File(...)):
    """
    Upload a medical report (image or PDF) and get recommendations.
    """
    try:
        # Validate file type
        if not file.content_type:
            raise HTTPException(status_code=400, detail="File type not recognized")
        
        content_type = file.content_type.lower()
        allowed_types = [
            "image/jpeg", "image/jpg", "image/png"
            # "application/pdf"
        ]
        
        if content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"File type {content_type} not supported. Please upload JPG or PNG."
            )
        
        # Read file contents
        contents = await file.read()
        file_name = file.filename or "report"
        
        # Process the medical report
        print(f"Processing file: {file_name} ({content_type})")
        parsed_data = await process_medical_report(contents, content_type, file_name)
        
        # Get recommendation based on parsed data
        recommendation = get_recommendation(parsed_data)
        
        return JSONResponse(content=recommendation)
    
    except HTTPException:
        raise
    except ValueError as e:
        print(f"Setup error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing report: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

