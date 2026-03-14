"""
FastAPI Backend for Fertilizer Recommendation System
Multi-task Neural Network Model serving
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
import torch
import torch.nn as nn
import pickle
import numpy as np
from pathlib import Path
import json

# =====================================================
# Initialize FastAPI
# =====================================================
app = FastAPI(
    title="Fertilizer Recommendation API",
    description="Multi-task neural network for crop fertilizer recommendations",
    version="1.0.0"
)

# =====================================================
# CORS Configuration (Allow Frontend Access)
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# Models Directory
# =====================================================
MODEL_DIR = Path(__file__).parent.parent

# =====================================================
# Define Multi-Task Neural Network
# =====================================================
class MultiTaskNN(nn.Module):
    def __init__(self, input_dim, cycle_classes, desc_classes, fert_classes):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.BatchNorm1d(512),
            nn.GELU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.GELU()
        )
        self.cycle_head = nn.Linear(256, cycle_classes)
        self.desc_head = nn.Linear(256, desc_classes)
        self.fert_head = nn.Linear(256, fert_classes)
        self.qty_head = nn.Linear(256, 3)

    def forward(self, x):
        shared_out = self.shared(x)
        return (
            self.cycle_head(shared_out),
            self.desc_head(shared_out),
            self.fert_head(shared_out),
            self.qty_head(shared_out)
        )

# =====================================================
# Load Model and Preprocessors
# =====================================================
def load_model_and_preprocessors():
    """Load trained model and preprocessors with fallback for missing files"""
    model_path = MODEL_DIR / "multitask_model (1).pth"
    scaler_x_path = MODEL_DIR / "scaler_X (1).pkl"
    qty_scaler_path = MODEL_DIR / "qty_scaler (1).pkl"
    
    # ✅ Load EXISTING model and scalers
    checkpoint = torch.load(model_path, map_location="cpu")
    print(f"Checkpoint type: {type(checkpoint)}")
    print(f"Checkpoint keys: {list(checkpoint.keys())[:5] if isinstance(checkpoint, dict) else 'N/A'}")
    
    # AUTO-DETECT dimensions from checkpoint
    if isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
        state_dict = checkpoint['state_dict']
    else:
        state_dict = checkpoint
    
    # Find output layer sizes from state_dict
    cycle_out = None
    desc_out = None  
    fert_out = None
    for key, tensor in state_dict.items():
        if 'cycle_head.weight' in key:
            cycle_out = tensor.shape[0]
        if 'desc_head.weight' in key:
            desc_out = tensor.shape[0]
        if 'fert_head.weight' in key:
            fert_out = tensor.shape[0]
    
    cycle_classes = int(cycle_out) if cycle_out is not None else 3
    desc_classes = int(desc_out) if desc_out is not None else 3
    fert_classes = int(fert_out) if fert_out is not None else 6
    
    print(f"Detected dimensions: cycle={cycle_classes}, desc={desc_classes}, fert={fert_classes}")
    
    model = MultiTaskNN(input_dim=8, cycle_classes=cycle_classes, desc_classes=desc_classes, fert_classes=fert_classes)
    model.load_state_dict(state_dict)
    model.eval()
    print("✅ Model architecture matched and loaded")
    
    # ✅ Load EXISTING scalers  
    scaler_X = pickle.load(open(scaler_x_path, 'rb'))
    qty_scaler = pickle.load(open(qty_scaler_path, 'rb'))
    
    # ✅ Load real label encoders
    with open(MODEL_DIR / "le_actual_cycle (1).pkl", 'rb') as f:
        le_cycle = pickle.load(f)
    with open(MODEL_DIR / "le_actual_desc (1).pkl", 'rb') as f:
        le_desc = pickle.load(f)
    with open(MODEL_DIR / "le_actual_fert (1).pkl", 'rb') as f:
        le_fert = pickle.load(f)
    
    # Create simple encoders for soil and crop types
    class SimpleEncoder:
        def __init__(self, classes):
            self.classes_ = np.array(classes)
    
    le_soil = SimpleEncoder(['Black', 'Red', 'Clay', 'Sandy', 'Loamy'])
    le_crop = SimpleEncoder([
        'Cotton', 'Rice', 'Wheat', 'Corn', 'Sugarcane', 'Pulses', 'Vegetables'
    ])
    
    print("✅ Model + scalers loaded, dummy encoders created")
    return model, le_cycle, le_desc, le_fert, scaler_X, qty_scaler, le_soil, le_crop

# Load model on startup  
try:
    model, le_cycle, le_desc, le_fert, scaler_X, qty_scaler, le_soil, le_crop = load_model_and_preprocessors()
    print("✅ COMPLETE: Model + preprocessors fully loaded!")
    print(f"Model device: {next(model.parameters()).device}")
    print(f"Scaler X shape: {scaler_X.n_features_in_ if hasattr(scaler_X, 'n_features_in_') else 'OK'}")
except Exception as e:
    print(f"❌ DETAILED ERROR: {type(e).__name__}: {str(e)}")
    print(f"  Model path exists: { (MODEL_DIR / 'multitask_model (1).pth').exists() }")
    import traceback  
    traceback.print_exc()
    model = None

# =====================================================
# Request/Response Models
# =====================================================
class PredictionRequest(BaseModel):
    temperature: float
    humidity: float
    moisture: float
    soil_type: str
    crop_type: str
    nitrogen: float
    potassium: float
    phosphorous: float

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "temperature": 25.5,
            "humidity": 65.0,
            "moisture": 55.0,
            "soil_type": "Black",
            "crop_type": "Cotton",
            "nitrogen": 40.0,
            "potassium": 30.0,
            "phosphorous": 20.0
        }
    })

class PredictionResponse(BaseModel):
    success: bool
    cycle: str
    cycle_description: str
    fertilizer_name: str
    quantity_1: float
    quantity_2: float
    quantity_3: float
    confidence: dict

# =====================================================
# API Endpoints
# =====================================================

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Fertilizer Recommendation API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "info": "/info"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": str(np.datetime64('now'))
    }

@app.get("/info")
async def get_info():
    """Get model information"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    return {
        "model_name": "Multi-Task Fertilizer Recommendation Neural Network",
        "architecture": "Shared layers + 4 task heads",
        "input_features": 8,
        "output_tasks": 4,
        "tasks": [
            "Crop Cycle Classification",
            "Cycle Description Classification",
            "Fertilizer Name Classification",
            "Quantity Prediction (Regression)"
        ],
        "fertilizers": list(le_fert.classes_),
        "soil_types": list(le_soil.classes_) if hasattr(le_soil, 'classes_') else [],
        "crop_types": list(le_crop.classes_) if hasattr(le_crop, 'classes_') else []
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Make fertilizer prediction
    
    Parameters:
    - temperature: Temperature in Celsius
    - humidity: Humidity percentage
    - moisture: Soil moisture
    - soil_type: Type of soil (e.g., Black, Red, Clay)
    - crop_type: Type of crop (e.g., Cotton, Rice, Wheat)
    - nitrogen: Nitrogen content (N)
    - potassium: Potassium content (K)
    - phosphorous: Phosphorous content (P)
    
    Returns:
    - Recommended cycle
    - Cycle description
    - Fertilizer name
    - Quantities (3 components)
    - Confidence scores
    """
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Manual mapping for soil types and crop types
        soil_type_map = {
            "Black": 0, "Red": 1, "Clay": 2, "Sandy": 3, "Loamy": 4,
            "black": 0, "red": 1, "clay": 2, "sandy": 3, "loamy": 4
        }
        crop_type_map = {
            "Cotton": 0, "Rice": 1, "Wheat": 2, "Corn": 3, "Sugarcane": 4, 
            "Pulses": 5, "Vegetables": 6,
            "cotton": 0, "rice": 1, "wheat": 2, "corn": 3, "sugarcane": 4,
            "pulses": 5, "vegetables": 6
        }
        
        # Get encoded values
        soil_encoded = soil_type_map.get(request.soil_type)
        crop_encoded = crop_type_map.get(request.crop_type)
        
        if soil_encoded is None:
            raise ValueError(f"Unknown soil type: {request.soil_type}. Available: {list(soil_type_map.keys())[:5]}")
        if crop_encoded is None:
            raise ValueError(f"Unknown crop type: {request.crop_type}. Available: {list(crop_type_map.keys())[:7]}")
        
        # Prepare input features
        input_data = np.array([
            request.temperature,
            request.humidity,
            request.moisture,
            soil_encoded,
            crop_encoded,
            request.nitrogen,
            request.potassium,
            request.phosphorous
        ]).reshape(1, -1)
        
        # Scale input
        input_scaled = scaler_X.transform(input_data)
        input_tensor = torch.tensor(input_scaled, dtype=torch.float32)
        
        # Make prediction
        with torch.no_grad():
            out_cycle, out_desc, out_fert, out_qty = model(input_tensor)
        
        # Get predictions
        cycle_idx = torch.argmax(out_cycle, dim=1).item()
        desc_idx = torch.argmax(out_desc, dim=1).item()
        fert_idx = torch.argmax(out_fert, dim=1).item()
        qty_pred = out_qty.numpy()[0]
        
        # Inverse scale quantities
        qty_unscaled = qty_scaler.inverse_transform(qty_pred.reshape(1, -1))[0]
        qty_1 = float(max(0, qty_unscaled[0]))
        qty_2 = float(max(0, qty_unscaled[1]))
        qty_3 = float(max(0, qty_unscaled[2]))
        
        # Get confidence scores
        confidences = {
            "cycle": float(torch.softmax(out_cycle, dim=1)[0, cycle_idx].item()),
            "description": float(torch.softmax(out_desc, dim=1)[0, desc_idx].item()),
            "fertilizer": float(torch.softmax(out_fert, dim=1)[0, fert_idx].item())
        }
        
        return PredictionResponse(
            success=True,
            cycle=str(le_cycle.inverse_transform([cycle_idx])[0]),
            cycle_description=str(le_desc.inverse_transform([desc_idx])[0]),
            fertilizer_name=str(le_fert.inverse_transform([fert_idx])[0]),
            quantity_1=qty_1,
            quantity_2=qty_2,
            quantity_3=qty_3,
            confidence=confidences
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

# =====================================================
# Run Server
# =====================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
