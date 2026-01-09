"""
Test script to verify Cluster and Persona Agent installation
Run this script to check if all dependencies are properly installed.
"""

import sys

def check_installation():
    print("🔍 Checking Cluster and Persona Agent Installation...\n")
    print("="*60)
    
    # Check Python version
    print("\n1. Python Version:")
    print(f"   ✓ Python {sys.version.split()[0]}")
    
    if sys.version_info < (3, 8):
        print("   ⚠️  Warning: Python 3.8+ recommended")
    
    # Check required packages
    packages = {
        'streamlit': 'Streamlit',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
        'sklearn': 'Scikit-learn',
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn',
        'PIL': 'Pillow'
    }
    
    print("\n2. Required Packages:")
    all_installed = True
    
    for package, name in packages.items():
        try:
            if package == 'PIL':
                import PIL
                version = PIL.__version__
            else:
                module = __import__(package)
                version = module.__version__
            print(f"   ✓ {name}: {version}")
        except ImportError:
            print(f"   ✗ {name}: NOT INSTALLED")
            all_installed = False
        except AttributeError:
            print(f"   ✓ {name}: Installed (version unknown)")
    
    # Check file existence
    print("\n3. Application Files:")
    import os
    
    files = {
        'cluster_persona_agent.py': 'Main application',
        'requirements.txt': 'Dependencies list',
        'README.md': 'Documentation',
        'QUICKSTART.md': 'Quick start guide'
    }
    
    for file, desc in files.items():
        if os.path.exists(file):
            print(f"   ✓ {file} ({desc})")
        else:
            print(f"   ✗ {file} ({desc}) - NOT FOUND")
    
    # Final verdict
    print("\n" + "="*60)
    if all_installed:
        print("\n✅ ALL SYSTEMS GO!")
        print("\n🚀 Ready to launch! Run this command:")
        print("\n   streamlit run cluster_persona_agent.py\n")
    else:
        print("\n⚠️  INSTALLATION INCOMPLETE")
        print("\n📦 Install missing packages with:")
        print("\n   pip install -r requirements.txt\n")
    
    print("="*60)

if __name__ == "__main__":
    try:
        check_installation()
    except Exception as e:
        print(f"\n❌ Error during check: {str(e)}")
        print("\nPlease ensure you're running this script in the correct directory.")
