/**
 * Test Runner for AI Pipe Generated Code
 * This file demonstrates how to run and test the extracted code
 */

const { extractCode, aiPipeResponse } = require('./ai-pipe-extractor');

// Test 1: Run the original AI Pipe code with mock data
async function testOriginalCode() {
  console.log("🧪 Test 1: Original AI Pipe Code with Mock Data");
  
  // Mock API endpoint for testing
  const mockUrl = "https://jsonplaceholder.typicode.com/posts";
  
  try {
    const response = await fetch(mockUrl);
    const jsonData = await response.json();
    
    // Adapt the logic since jsonplaceholder has different structure
    const totalSum = jsonData.slice(0, 5).reduce((acc, item) => acc + item.id, 0);
    
    console.log("✅ Mock API test successful!");
    console.log("Sum of first 5 post IDs:", totalSum);
    return totalSum;
  } catch (error) {
    console.error("❌ Test failed:", error.message);
    throw error;
  }
}

// Test 2: GitHub API example
async function testGitHubAPI() {
  console.log("\n🧪 Test 2: GitHub API - Get Repository Info");
  
  try {
    const user = "sathish-k7";
    const response = await fetch(`https://api.github.com/users/${user}/repos`);
    const data = await response.json();
    
    if (data.length > 0) {
      const result = {
        firstRepo: data[0].name,
        createdAt: data[0].created_at,
        totalRepos: data.length,
        recentRepos: data.slice(0, 3).map(repo => ({
          name: repo.name,
          created: repo.created_at,
          language: repo.language
        }))
      };
      
      console.log("✅ GitHub API test successful!");
      console.log("Repository info:", JSON.stringify(result, null, 2));
      return result;
    } else {
      console.log("ℹ️ No repositories found");
      return { message: "No repositories found" };
    }
  } catch (error) {
    console.error("❌ GitHub API test failed:", error.message);
    throw error;
  }
}

// Test 3: Extract and display the original AI Pipe code
function testCodeExtraction() {
  console.log("\n🧪 Test 3: Code Extraction from AI Pipe Response");
  
  const extractedCode = extractCode(aiPipeResponse);
  
  console.log("✅ Code extraction successful!");
  console.log("Extracted code:");
  console.log("```javascript");
  console.log(extractedCode);
  console.log("```");
  
  return extractedCode;
}

// Run all tests
async function runAllTests() {
  console.log("🚀 Starting AI Pipe Code Tests\n");
  console.log("=".repeat(60));
  
  try {
    // Test code extraction
    testCodeExtraction();
    
    // Test with mock data
    await testOriginalCode();
    
    // Test GitHub API
    await testGitHubAPI();
    
    console.log("\n" + "=".repeat(60));
    console.log("🎉 All tests completed successfully!");
    
  } catch (error) {
    console.error("\n❌ Test suite failed:", error.message);
    process.exit(1);
  }
}

// Only run tests if this file is executed directly
if (require.main === module) {
  runAllTests();
}

module.exports = {
  testOriginalCode,
  testGitHubAPI,
  testCodeExtraction,
  runAllTests
};