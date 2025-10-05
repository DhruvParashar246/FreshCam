"""
Test script for Gemini integration with FreshCam
Tests both fruit name detection and ripeness fallback
"""

import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))


def test_gemini_fruit_name():
    """Test Gemini fruit name detection"""
    print("=" * 60)
    print("TEST 1: Gemini Fruit Name Detection")
    print("=" * 60)

    try:
        from services.gemini_service import get_fruit_name

        # Test with a sample image
        test_image = backend_path / "images" / "ripe_mango.jpg"
        if not test_image.exists():
            print(f"⚠️ Test image not found: {test_image}")
            return False

        with open(test_image, "rb") as f:
            image_bytes = f.read()

        result = get_fruit_name(image_bytes)
        print(f"✓ Result: {result}")

        if "fruit_name" in result:
            print("✅ PASS: Fruit name detection working")
            return True
        else:
            print("❌ FAIL: No fruit name in result")
            return False

    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_gemini_ripeness_fallback():
    """Test Gemini ripeness detection (fallback)"""
    print("\n" + "=" * 60)
    print("TEST 2: Gemini Ripeness Fallback")
    print("=" * 60)

    try:
        from services.gemini_service import analyze_ripeness_with_gemini

        # Test with a sample image
        test_image = backend_path / "images" / "ripe_banana.jpg"
        if not test_image.exists():
            print(f"⚠️ Test image not found: {test_image}")
            # Try another image
            test_image = backend_path / "images" / "ripe_mango.jpg"

        with open(test_image, "rb") as f:
            image_bytes = f.read()

        result = analyze_ripeness_with_gemini(image_bytes)
        print(f"✓ Result: {result}")

        if "ripeness" in result and "fruit_name" in result:
            print("✅ PASS: Gemini ripeness analysis working")
            return True
        else:
            print("❌ FAIL: Missing required fields in result")
            return False

    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_integrated_cv_service():
    """Test integrated CV service with Gemini fallback"""
    print("\n" + "=" * 60)
    print("TEST 3: Integrated CV Service with Gemini")
    print("=" * 60)

    try:
        from services.cv_service import analyze_image

        # Test with a sample image
        test_image = backend_path / "images" / "ripe_strawberry.jpg"
        if not test_image.exists():
            test_image = backend_path / "images" / "ripe_mango.jpg"

        with open(test_image, "rb") as f:
            image_bytes = f.read()

        result = analyze_image(image_bytes)
        print(f"✓ Result: {result}")

        # Check if result has required fields
        if "error" in result:
            print(f"⚠️ WARNING: Error in result - {result['error']}")
            # This might be OK if it's due to missing API keys
            if "GEMINI_API_KEY" in str(result.get("error", "")):
                print("ℹ️ INFO: Need to set GEMINI_API_KEY in .env file")
            return False

        if "fruit_name" in result and "ripeness" in result:
            print(f"✅ PASS: Integrated service working")
            print(f"   - Fruit: {result['fruit_name']}")
            print(f"   - Ripeness: {result['ripeness']}")
            print(f"   - Confidence: {result.get('confidence', 'N/A')}%")
            print(f"   - Source: {result.get('source', 'N/A')}")
            return True
        else:
            print("❌ FAIL: Missing required fields in result")
            return False

    except Exception as e:
        print(f"❌ FAIL: {e}")
        import traceback

        traceback.print_exc()
        return False


def check_environment():
    """Check if required environment variables are set"""
    print("=" * 60)
    print("ENVIRONMENT CHECK")
    print("=" * 60)

    required_vars = ["GEMINI_API_KEY", "ROBOFLOW_API_KEY", "ROBOFLOW_URL"]
    all_set = True

    for var in required_vars:
        value = os.getenv(var)
        if value:
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"✓ {var}: {masked}")
        else:
            print(f"✗ {var}: NOT SET")
            all_set = False

    if not all_set:
        print("\n⚠️ WARNING: Some environment variables are not set")
        print("   Create a .env file in the backend directory with:")
        print("   GEMINI_API_KEY=your_key_here")
        print("   ROBOFLOW_API_KEY=your_key_here")
        print("   ROBOFLOW_URL=https://detect.roboflow.com")

    return all_set


if __name__ == "__main__":
    print("\n🧪 FRESHCAM - GEMINI INTEGRATION TESTS\n")

    # Check environment first
    env_ok = check_environment()
    print()

    if not env_ok:
        print("⚠️ Please set environment variables before running tests")
        print("   See backend/.env.example for reference")
        sys.exit(1)

    # Run tests
    test1 = test_gemini_fruit_name()
    test2 = test_gemini_ripeness_fallback()
    test3 = test_integrated_cv_service()

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    total = 3
    passed = sum([test1, test2, test3])
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)
