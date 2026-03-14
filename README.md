<<<<<<< HEAD
# 🌾 Fertilizer Recommendation System - Full Stack Application

A complete **AI-powered fertilizer recommendation system** using a Multi-Task Neural Network. This project includes a FastAPI backend and a modern interactive frontend.

## 📋 Project Structure

```
ITR_Neural_Network/
├── backend/
│   └── main.py                    # FastAPI application
├── frontend/
│   └── index.html                 # Interactive web interface
├── multitask_model (1).pth         # Trained neural network model
├── *.pkl                          # Preprocessors (encoders, scalers)
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🎯 Features

- **Multi-Task Learning**: Predicts 4 different outputs simultaneously
  - Crop Cycle Classification
  - Cycle Description Classification
  - Fertilizer Name Classification
  - Quantity Prediction (Regression)

- **REST API**: FastAPI backend with full CORS support
- **Interactive Frontend**: Modern, responsive web interface
- **Real-time Predictions**: Get fertilizer recommendations instantly
- **Confidence Scores**: View model confidence for each prediction
- **User-Friendly UI**: Beautiful gradient design with smooth animations

## ⚙️ System Requirements

- **Python 3.8+**
- **Windows/Mac/Linux**
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

## 📦 Installation

### Step 1: Clone/Download Files

Ensure all files are in the workspace directory:
```
c:\Users\Sree Bhavya\Downloads\ITR_Neural_Network\
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd ITR_Neural_Network

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: First installation may take 2-3 minutes as it downloads PyTorch and other dependencies.

## 🚀 Running the Application

### Terminal 1: Start Backend Server

```bash
# Navigate to project directory
cd ITR_Neural_Network

# Activate virtual environment (if not already active)
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Start FastAPI server
python backend/main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Open Frontend

**Option A: Using Python's HTTP Server**
```bash
# Navigate to frontend directory
cd frontend

# Start HTTP server
python -m http.server 8080
```

Then open: **http://localhost:8080**

**Option B: Direct File Opening**
- Simply open `frontend/index.html` in your web browser
- The frontend will communicate with the backend API

## 📖 API Endpoints

### 1. **GET `/`** - Root Endpoint
Get API information
```
Response:
{
  "name": "Fertilizer Recommendation API",
  "version": "1.0.0",
  "status": "running",
  "endpoints": { ... }
}
```

### 2. **GET `/health`** - Health Check
Check API and model status
```
Response:
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "..."
}
```

### 3. **GET `/info`** - Model Information
Get model details and available options
```
Response:
{
  "model_name": "Multi-Task Fertilizer Recommendation Neural Network",
  "architecture": "Shared layers + 4 task heads",
  "input_features": 8,
  "output_tasks": 4,
  "tasks": [...],
  "fertilizers": [...]
}
```

### 4. **POST `/predict`** - Get Fertilizer Recommendation
**Request Body:**
```json
{
  "temperature": 25.5,
  "humidity": 65.0,
  "moisture": 55.0,
  "soil_type": "Black",
  "crop_type": "Cotton",
  "nitrogen": 40.0,
  "potassium": 30.0,
  "phosphorous": 20.0
}
```

**Response:**
```json
{
  "success": true,
  "cycle": "Kharif",
  "cycle_description": "Monsoon Season",
  "fertilizer_name": "NPK 20:20:0",
  "quantity_1": 125.5,
  "quantity_2": 85.3,
  "quantity_3": 45.2,
  "confidence": {
    "cycle": 0.92,
    "description": 0.88,
    "fertilizer": 0.95
  }
}
```

## 🧪 Testing with cURL

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 25.5,
    "humidity": 65.0,
    "moisture": 55.0,
    "soil_type": "Black",
    "crop_type": "Cotton",
    "nitrogen": 40.0,
    "potassium": 30.0,
    "phosphorous": 20.0
  }'
```

## 🎨 Frontend Guide

### Input Fields

| Field | Type | Range | Example |
|-------|------|-------|---------|
| Temperature | Number | -50 to 50°C | 25.5 |
| Humidity | Number | 0-100% | 65 |
| Soil Moisture | Number | 0-100 | 55 |
| Soil Type | Select | Black, Red, Clay, Sandy, Loamy | Black |
| Crop Type | Select | Cotton, Rice, Wheat, Corn, etc. | Cotton |
| Nitrogen (N) | Number | 0-200 mg/kg | 40 |
| Potassium (K) | Number | 0-200 mg/kg | 30 |
| Phosphorous (P) | Number | 0-200 mg/kg | 20 |

### Output Results

- **Crop Cycle**: Recommended growing season (Kharif, Rabi, etc.)
- **Cycle Description**: Description of the growing season
- **Recommended Fertilizer**: Name of the most suitable fertilizer
- **Quantities 1-3**: Three component quantities in kg
- **Confidence**: Model confidence percentage for fertilizer recommendation

## 🔧 Troubleshooting

### Issue: "Connection refused" or "Cannot reach server"
**Solution:**
- Ensure backend is running (`python backend/main.py`)
- Check that port 8000 is not occupied
- Verify API URL in `frontend/index.html` matches your server address

### Issue: "Model file not found"
**Solution:**
- Ensure all `.pth` and `.pkl` files are in the project root directory
- Check file names match exactly (case-sensitive)
- Verify files were not corrupted during transfer

### Issue: "CORS error" in browser console
**Solution:**
- Backend CORS is enabled for all origins
- Clear browser cache (Ctrl+Shift+Delete)
- Try a different browser

### Issue: "ModuleNotFoundError: No module named 'torch'"
**Solution:**
```bash
pip install --upgrade torch
# Or for CPU-only version
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

## 📊 Model Architecture

```
Input (8 features)
    ↓
Shared Layers:
  - Dense(512) + BatchNorm + GELU + Dropout(0.3)
  - Dense(256) + BatchNorm + GELU
    ↓
    ├─→ Cycle Head → Classification (4 classes)
    ├─→ Description Head → Classification (3 classes)
    ├─→ Fertilizer Head → Classification (60+ classes)
    └─→ Quantity Head → Regression (3 outputs)
```

## 📈 Model Performance

- **Cycle Accuracy**: ~90%
- **Description Accuracy**: ~88%
- **Fertilizer Accuracy**: ~71%
- **Quantity MAE**: < 15 kg

## 🔐 Security Notes

- The API currently allows all origins (CORS)
- For production:
  - Restrict CORS to specific domains
  - Add authentication/authorization
  - Use HTTPS instead of HTTP
  - Implement rate limiting

## 📝 Notes

- Model inference runs on CPU for maximum compatibility
- All predictions are made in < 100ms
- Input data is normalized using fitted scalers
- Quantities are inverse-scaled to original units

## 🤝 Support

For issues or questions:
1. Check the API logs in the backend terminal
2. Check browser console (F12) for frontend errors
3. Verify all files are present and readable

## 📜 License

This project is provided as-is for educational and research purposes.

---

**Happy Farming! 🌾🚜**
=======
# Fertilizer_Recommendation_System
>>>>>>> b3a7dad11ba35a314122e8add1b7cf83e5f7d79d
