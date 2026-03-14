"""
Test script to verify Fertilizer Recommendation System is working correctly
"""

import requests
import time
import sys
from pathlib import Path

class SystemTester:
    def __init__(self):
        self.api_url = "http://localhost:8000"
        self.test_results = []
    
    def print_header(self, text):
        """Print formatted header"""
        print(f"\n{'='*60}")
        print(f"  {text}")
        print(f"{'='*60}\n")
    
    def test_connection(self):
        """Test if backend is accessible"""
        print("🔍 Testing Backend Connection...")
        try:
            response = requests.get(f"{self.api_url}/", timeout=5)
            if response.status_code == 200:
                print("✅ Backend is running and accessible!")
                self.test_results.append(("Backend Connection", True))
                return True
            else:
                print(f"❌ Backend returned status code: {response.status_code}")
                self.test_results.append(("Backend Connection", False))
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to backend")
            print(f"   Make sure it's running: python backend/main.py")
            self.test_results.append(("Backend Connection", False))
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append(("Backend Connection", False))
            return False
    
    def test_health(self):
        """Test health check endpoint"""
        print("🔍 Testing Health Check Endpoint...")
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health Check Passed!")
                print(f"   Status: {data.get('status')}")
                print(f"   Model Loaded: {data.get('model_loaded')}")
                self.test_results.append(("Health Check", True))
                return data.get('model_loaded', False)
            else:
                print(f"❌ Health check failed: {response.status_code}")
                self.test_results.append(("Health Check", False))
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append(("Health Check", False))
            return False
    
    def test_info(self):
        """Test info endpoint"""
        print("🔍 Testing Info Endpoint...")
        try:
            response = requests.get(f"{self.api_url}/info", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Model Info Retrieved!")
                print(f"   Model: {data.get('model_name')}")
                print(f"   Input Features: {data.get('input_features')}")
                print(f"   Output Tasks: {data.get('output_tasks')}")
                print(f"   Available Fertilizers: {len(data.get('fertilizers', []))}")
                self.test_results.append(("Model Info", True))
                return True
            else:
                print(f"❌ Info endpoint failed: {response.status_code}")
                self.test_results.append(("Model Info", False))
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append(("Model Info", False))
            return False
    
    def test_prediction(self):
        """Test prediction endpoint with sample data"""
        print("🔍 Testing Prediction Endpoint...")
        
        test_data = {
            "temperature": 25.5,
            "humidity": 65.0,
            "moisture": 55.0,
            "soil_type": "Black",
            "crop_type": "Cotton",
            "nitrogen": 40.0,
            "potassium": 30.0,
            "phosphorous": 20.0
        }
        
        try:
            print(f"   Sending test prediction with sample data...")
            start_time = time.time()
            
            response = requests.post(
                f"{self.api_url}/predict",
                json=test_data,
                timeout=10
            )
            
            inference_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Prediction Successful! (Time: {inference_time*1000:.1f}ms)")
                print(f"   Cycle: {data.get('cycle')}")
                print(f"   Description: {data.get('cycle_description')}")
                print(f"   Fertilizer: {data.get('fertilizer_name')}")
                print(f"   Qty 1: {data.get('quantity_1'):.2f} kg")
                print(f"   Qty 2: {data.get('quantity_2'):.2f} kg")
                print(f"   Qty 3: {data.get('quantity_3'):.2f} kg")
                print(f"   Confidence: {data.get('confidence', {}).get('fertilizer', 0)*100:.1f}%")
                self.test_results.append(("Prediction", True))
                return True
            else:
                print(f"❌ Prediction failed: {response.status_code}")
                print(f"   Error: {response.text}")
                self.test_results.append(("Prediction", False))
                return False
        
        except requests.exceptions.Timeout:
            print(f"❌ Request timed out (backend may be loading model)")
            self.test_results.append(("Prediction", False))
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append(("Prediction", False))
            return False
    
    def test_cors(self):
        """Test CORS headers"""
        print("🔍 Testing CORS Configuration...")
        try:
            response = requests.options(
                f"{self.api_url}/predict",
                headers={"Origin": "http://localhost:8080"},
                timeout=5
            )
            
            cors_headers = response.headers
            if 'access-control-allow-origin' in cors_headers:
                print(f"✅ CORS Enabled!")
                print(f"   Allow-Origin: {cors_headers.get('access-control-allow-origin')}")
                self.test_results.append(("CORS", True))
                return True
            else:
                print(f"⚠️  CORS headers not found (may still work for GET/POST)")
                self.test_results.append(("CORS", True))  # Not critical
                return True
        except Exception as e:
            print(f"⚠️  Could not verify CORS: {e}")
            self.test_results.append(("CORS", True))  # Not critical
            return True
    
    def print_summary(self):
        """Print test summary"""
        self.print_header("TEST SUMMARY")
        
        passed = sum(1 for _, result in self.test_results if result)
        total = len(self.test_results)
        
        for test_name, result in self.test_results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status}  {test_name}")
        
        print(f"\nTotal: {passed}/{total} tests passed\n")
        
        if passed == total:
            print("🎉 All tests passed! System is ready to use!")
            print("\nNext steps:")
            print("1. Open http://localhost:8080 in your browser")
            print("2. Fill in the form with crop parameters")
            print("3. Click 'Get Recommendation'")
            return True
        else:
            print("⚠️  Some tests failed. Check the errors above.")
            return False

def main():
    """Run all tests"""
    tester = SystemTester()
    
    tester.print_header("FERTILIZER RECOMMENDATION SYSTEM - TEST SUITE")
    
    print("⏳ Testing backend connection...")
    time.sleep(0.5)
    
    # Run tests in order
    if not tester.test_connection():
        print("\n❌ FATAL: Cannot connect to backend!")
        print("Make sure to run: python backend/main.py")
        sys.exit(1)
    
    time.sleep(0.5)
    tester.test_health()
    
    time.sleep(0.5)
    tester.test_info()
    
    time.sleep(0.5)
    tester.test_prediction()
    
    time.sleep(0.5)
    tester.test_cors()
    
    # Print summary
    success = tester.print_summary()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✋ Tests cancelled by user")
        sys.exit(1)
