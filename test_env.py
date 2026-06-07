# test_env.py
import os
from pathlib import Path
from dotenv import load_dotenv

print("="*60)
print("ENVIRONMENT FILE DIAGNOSTIC")
print("="*60)

# Where am I running from?
print(f"\n📍 Current working directory:")
print(f"   {Path.cwd()}")

# Where is this script?
print(f"\n📍 This script location:")
print(f"   {Path(__file__).resolve().parent}")

# Look for .env file
env_path = Path(__file__).resolve().parent / ".env"
print(f"\n🔍 Looking for .env at:")
print(f"   {env_path}")
print(f"   Exists: {env_path.exists()}")

if env_path.exists():
    print(f"\n📄 .env file size: {env_path.stat().st_size} bytes")

    # Read raw content
    with open(env_path, 'r') as f:
        content = f.read()
    print(f"\n📄 .env file content (raw):")
    print("─" * 40)
    print(repr(content))  # Shows hidden characters
    print("─" * 40)

    # Try loading
    load_dotenv(dotenv_path=env_path)
    api_key = os.getenv("WEATHER_API_KEY", "")

    if api_key:
        print(f"\n✅ SUCCESS!")
        print(f"   API Key length: {len(api_key)}")
        print(f"   First 8 chars: {api_key[:8]}")
        print(f"   Last 4 chars: ...{api_key[-4:]}")
    else:
        print(f"\n❌ FAILURE: .env exists but WEATHER_API_KEY not loaded")
        print(f"   Check the format in your .env file")
else:
    print(f"\n❌ .env file NOT FOUND")
    print(f"\nCreate it with this command:")
    print(f"   Windows: echo WEATHER_API_KEY=your_key > .env")
    print(f"   Mac/Linux: echo 'WEATHER_API_KEY=your_key' > .env")

print("\n" + "="*60)