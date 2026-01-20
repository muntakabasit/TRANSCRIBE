#!/usr/bin/env python3
"""Test if the app can start without errors"""

import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    logger.info("Testing import of main module...")
    import main
    logger.info("✅ Main module imported successfully")

    logger.info("Testing FastAPI app creation...")
    app = main.app
    logger.info(f"✅ FastAPI app created: {app.title} v{app.version}")

    logger.info("Testing database connection...")
    from database import engine
    engine.connect()
    logger.info("✅ Database connection successful")

    logger.info("\n🎉 All startup tests passed!")
    sys.exit(0)

except Exception as e:
    logger.error(f"\n❌ Startup test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
