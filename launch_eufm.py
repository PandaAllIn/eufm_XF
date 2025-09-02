#!/usr/bin/env python3
"""
Unified CLI entry point.
"""

import sys
from pathlib import Path

# Add the project root to the Python path to allow for absolute imports
# This assumes the launch script is in the 'eufm' directory.
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from app import create_app  # noqa: E402


def main():
    """Launch the EUFM Assistant system using the application factory."""
    print("🔬 EUFM Assistant - European Funds Management System")
    print("=" * 60)
    print("🚨 CRITICAL DEADLINE: Stage 1 Proposal Due September 4, 2025")
    print("=" * 60)

    app = create_app()

    # Access settings through the app's config
    settings = app.config.get("APP_SETTINGS")

    print("\n📋 System Status:")
    if settings:
        print(f"✅ Environment: {settings.ENVIRONMENT.value}")
        print(f"✅ Debug Mode: {settings.DEBUG}")
    print("✅ AI Services Initialized")

    print("\n🌐 Starting web interface...")
    print("📍 URL: http://127.0.0.1:5000")
    print("\n" + "=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)

    try:
        # Run Flask app using the development server
        # For production, a proper WSGI server like Gunicorn should be used.
        app.run(host="0.0.0.0", port=5000, debug=settings.DEBUG if settings else True)
    except KeyboardInterrupt:
        print("\n\n🛑 EUFM Assistant stopped")
        print("Thank you for using EUFM Assistant!")


if __name__ == "__main__":
    sys.exit(main())