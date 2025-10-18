"""
Test script for TypeScript RAG API
Tests both example questions and validates responses
"""

import requests
import json
import time

# API URLs
LOCAL_API = "http://127.0.0.1:8000/search"
PROD_API = "https://tdsfu.pages.dev/api/GA3/8"

# Test questions with expected answers
TEST_CASES = [
    {
        "question": "What does the author affectionately call the => syntax?",
        "expected_keywords": ["fat arrow", "fat", "arrow"],
        "expected_exact": "fat arrow"
    },
    {
        "question": "Which operator converts any value into an explicit boolean?",
        "expected_keywords": ["!!", "double", "exclamation"],
        "expected_exact": "!!"
    },
    {
        "question": "What are arrow functions also called?",
        "expected_keywords": ["fat arrow", "lambda", "function"],
        "expected_exact": None
    },
]

def test_api(api_url, description):
    """Test the API with all test cases."""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"URL: {api_url}")
    print('='*60)
    
    results = []
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n📝 Test {i}/{len(TEST_CASES)}")
        print(f"Q: {test_case['question']}")
        
        try:
            # Make request
            start_time = time.time()
            response = requests.get(api_url, params={"q": test_case["question"]}, timeout=10)
            elapsed_time = time.time() - start_time
            
            # Parse response
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "").lower()
                
                # Check if expected keywords are in answer
                keyword_match = any(kw.lower() in answer for kw in test_case["expected_keywords"])
                
                # Check exact match if specified
                exact_match = False
                if test_case["expected_exact"]:
                    exact_match = test_case["expected_exact"].lower() in answer
                
                success = keyword_match or exact_match
                
                print(f"✅ Status: {response.status_code}")
                print(f"⏱️  Response Time: {elapsed_time:.3f}s")
                print(f"💬 Answer: {data.get('answer', 'N/A')[:100]}...")
                print(f"📚 Source: {data.get('sources', 'N/A')[:80]}...")
                print(f"🎯 Confidence: {data.get('confidence', 'N/A')}")
                print(f"{'✅' if success else '❌'} Match: {'PASS' if success else 'FAIL'}")
                
                results.append({
                    "question": test_case["question"],
                    "status": "PASS" if success else "FAIL",
                    "response_time": elapsed_time,
                    "answer": data.get("answer", "")
                })
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"Error: {response.text}")
                results.append({
                    "question": test_case["question"],
                    "status": "ERROR",
                    "error": response.text
                })
                
        except requests.exceptions.Timeout:
            print(f"❌ Request timed out after 10 seconds")
            results.append({
                "question": test_case["question"],
                "status": "TIMEOUT"
            })
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection error - is the server running?")
            results.append({
                "question": test_case["question"],
                "status": "CONNECTION_ERROR"
            })
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            results.append({
                "question": test_case["question"],
                "status": "ERROR",
                "error": str(e)
            })
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Test Summary for {description}")
    print('='*60)
    
    passed = sum(1 for r in results if r.get("status") == "PASS")
    failed = sum(1 for r in results if r.get("status") == "FAIL")
    errors = sum(1 for r in results if r.get("status") in ["ERROR", "TIMEOUT", "CONNECTION_ERROR"])
    
    print(f"✅ Passed: {passed}/{len(results)}")
    print(f"❌ Failed: {failed}/{len(results)}")
    print(f"⚠️  Errors: {errors}/{len(results)}")
    
    if results:
        avg_time = sum(r.get("response_time", 0) for r in results if "response_time" in r) / max(len([r for r in results if "response_time" in r]), 1)
        print(f"⏱️  Avg Response Time: {avg_time:.3f}s")
    
    return results


def test_root_endpoint(api_base):
    """Test the root endpoint."""
    print(f"\n{'='*60}")
    print(f"Testing Root Endpoint")
    print(f"URL: {api_base}")
    print('='*60)
    
    try:
        response = requests.get(api_base, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint accessible")
            print(f"📝 Message: {data.get('message', 'N/A')}")
            print(f"📚 Endpoints: {json.dumps(data.get('endpoints', {}), indent=2)}")
        else:
            print(f"❌ Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    print("🧪 TypeScript RAG API Test Suite")
    print("="*60)
    
    # Test local API
    print("\n🏠 Testing Local API...")
    try:
        test_root_endpoint("http://127.0.0.1:8000")
        local_results = test_api(LOCAL_API, "Local Development Server")
    except Exception as e:
        print(f"❌ Local API not available: {str(e)}")
        print("ℹ️  Make sure to run: python typescript_rag_api.py")
    
    # Optionally test production API
    print("\n\n🌍 Would you like to test the production API? (yes/no)")
    test_prod = input().strip().lower()
    
    if test_prod in ['yes', 'y']:
        prod_results = test_api(PROD_API, "Production (Cloudflare Pages)")
    
    print("\n\n✅ Test suite completed!")
