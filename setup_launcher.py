"""
Setup and Launcher Script for Fertilizer Recommendation System
Automates environment setup and server startup
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

class FertilizerAppLauncher:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.venv_dir = self.project_dir / "venv"
        self.backend_dir = self.project_dir / "backend"
        self.frontend_dir = self.project_dir / "frontend"
        
    def check_python_version(self):
        """Verify Python 3.8+ is installed"""
        if sys.version_info < (3, 8):
            print("❌ Error: Python 3.8 or higher is required")
            print(f"Current version: {sys.version}")
            sys.exit(1)
        print(f"✅ Python {sys.version.split()[0]} detected")
    
    def create_venv(self):
        """Create virtual environment if it doesn't exist"""
        if self.venv_dir.exists():
            print(f"✅ Virtual environment already exists at {self.venv_dir}")
            return
        
        print(f"📦 Creating virtual environment...")
        try:
            subprocess.run(
                [sys.executable, "-m", "venv", str(self.venv_dir)],
                check=True,
                capture_output=True
            )
            print(f"✅ Virtual environment created successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating virtual environment: {e}")
            sys.exit(1)
    
    def get_pip_command(self):
        """Get the pip executable path for the virtual environment"""
        if sys.platform == "win32":
            return self.venv_dir / "Scripts" / "pip.exe"
        else:
            return self.venv_dir / "bin" / "pip"
    
    def get_python_command(self):
        """Get the Python executable path for the virtual environment"""
        if sys.platform == "win32":
            return self.venv_dir / "Scripts" / "python.exe"
        else:
            return self.venv_dir / "bin" / "python"
    
    def install_requirements(self):
        """Install project dependencies"""
        requirements_file = self.project_dir / "requirements.txt"
        
        if not requirements_file.exists():
            print(f"❌ requirements.txt not found")
            sys.exit(1)
        
        print(f"📥 Installing dependencies...")
        print("   This may take 2-3 minutes on first run...")
        
        try:
            pip_cmd = str(self.get_pip_command())
            subprocess.run(
                [pip_cmd, "install", "-q", "-r", str(requirements_file)],
                check=True,
                cwd=str(self.project_dir)
            )
            print(f"✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing dependencies: {e}")
            print("   Try running: pip install -r requirements.txt manually")
            sys.exit(1)
    
    def verify_model_files(self):
        """Verify that all required model files exist"""
        required_files = [
            "multitask_model (1).pth",
            "le_actual_cycle (1).pkl",
            "le_actual_desc (1).pkl",
            "le_actual_fert (1).pkl",
            "scaler_X (1).pkl",
            "qty_scaler (1).pkl",
            "cycle_encoder (1).pkl",
            "desc_encoder (1).pkl"
        ]
        
        print("🔍 Verifying model files...")
        missing_files = []
        
        for file in required_files:
            file_path = self.project_dir / file
            if not file_path.exists():
                missing_files.append(file)
                print(f"   ❌ Missing: {file}")
            else:
                print(f"   ✅ Found: {file}")
        
        if missing_files:
            print(f"\n⚠️  Warning: Some model files are missing!")
            print(f"   The application may not work correctly without these files.")
            return False
        
        print(f"✅ All model files verified")
        return True
    
    def start_backend(self):
        """Start the FastAPI backend server"""
        print(f"\n{'='*60}")
        print(f"🚀 Starting Backend Server...")
        print(f"{'='*60}")
        print(f"📍 Backend URL: http://localhost:8000")
        print(f"📍 API Docs: http://localhost:8000/docs")
        print(f"📍 Health Check: http://localhost:8000/health")
        print(f"\n⏰ Please wait for 'Application startup complete' message...")
        print(f"   Then open another terminal and run 'run_frontend.bat'")
        print(f"{'='*60}\n")
        
        python_cmd = str(self.get_python_command())
        backend_main = str(self.backend_dir / "main.py")
        
        try:
            subprocess.run(
                [python_cmd, backend_main],
                cwd=str(self.project_dir)
            )
        except KeyboardInterrupt:
            print("\n\n✋ Backend server stopped")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error starting backend: {e}")
            sys.exit(1)
    
    def start_frontend(self):
        """Start the frontend HTTP server"""
        print(f"\n{'='*60}")
        print(f"🎨 Starting Frontend Server...")
        print(f"{'='*60}")
        print(f"📍 Frontend URL: http://localhost:8080")
        print(f"📍 Ensure backend is running on port 8000")
        print(f"{'='*60}\n")
        
        python_cmd = str(self.get_python_command())
        
        try:
            # Change to frontend directory and start HTTP server
            original_dir = os.getcwd()
            os.chdir(str(self.frontend_dir))
            
            subprocess.run(
                [python_cmd, "-m", "http.server", "8080"]
            )
            
            os.chdir(original_dir)
        except KeyboardInterrupt:
            print("\n\n✋ Frontend server stopped")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error starting frontend: {e}")
            sys.exit(1)
    
    def setup_and_run(self, mode="backend"):
        """Complete setup and run the application"""
        print(f"\n{'='*60}")
        print(f"🌾 Fertilizer Recommendation System - Setup & Launch")
        print(f"{'='*60}\n")
        
        # Step 1: Check Python version
        self.check_python_version()
        
        # Step 2: Create virtual environment
        self.create_venv()
        
        # Step 3: Install requirements
        self.install_requirements()
        
        # Step 4: Verify model files
        self.verify_model_files()
        
        print(f"\n{'='*60}")
        print(f"✅ Setup Complete!")
        print(f"{'='*60}\n")
        
        # Step 5: Start requested server
        if mode == "backend":
            self.start_backend()
        elif mode == "frontend":
            self.start_frontend()
        else:
            print("❌ Invalid mode. Use 'backend' or 'frontend'")
            sys.exit(1)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Fertilizer Recommendation System - Launcher"
    )
    parser.add_argument(
        "--mode",
        choices=["backend", "frontend", "setup"],
        default="backend",
        help="What to run: backend, frontend, or setup only (default: backend)"
    )
    
    args = parser.parse_args()
    launcher = FertilizerAppLauncher()
    
    try:
        if args.mode == "setup":
            # Only do setup, don't start any server
            print(f"\n{'='*60}")
            print(f"🌾 Fertilizer Recommendation System - Setup Only")
            print(f"{'='*60}\n")
            launcher.check_python_version()
            launcher.create_venv()
            launcher.install_requirements()
            launcher.verify_model_files()
            print(f"\n✅ Setup Complete!")
            print(f"You can now run:")
            print(f"   python setup_launcher.py --mode backend")
            print(f"   python setup_launcher.py --mode frontend")
        else:
            launcher.setup_and_run(mode=args.mode)
    
    except KeyboardInterrupt:
        print("\n\n✋ Operation cancelled by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
