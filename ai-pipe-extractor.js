/**
 * AI Pipe Response Extractor
 * Extracts and processes code from AI Pipe responses
 */

// Example AI Pipe response (the one you provided)
const aiPipeResponse = {
  "id": "gen-1760194044-TYI4oFQ4hZGRkCRl1gDF",
  "provider": "OpenAI",
  "model": "openai/gpt-4.1-nano",
  "object": "chat.completion",
  "created": 1760194044,
  "choices": [
    {
      "logprobs": null,
      "finish_reason": "stop",
      "native_finish_reason": "completed",
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "```javascript\ntry {\n  const response = await fetch(url);\n  const jsonData = await response.json();\n  const totalSum = jsonData.data.reduce((acc, item) => acc + item.number, 0);\n  return totalSum;\n} catch (error) {\n  // Handle errors if necessary, or rethrow\n  throw error;\n}\n```",
        "refusal": null,
        "reasoning": null
      }
    }
  ],
  "usage": {
    "prompt_tokens": 89,
    "completion_tokens": 74,
    "total_tokens": 163
  }
};

/**
 * Extract code from AI Pipe response
 * @param {Object} response - AI Pipe response object
 * @returns {string} - Extracted code without markdown formatting
 */
function extractCode(response) {
  const content = response.choices[0].message.content;
  
  // Remove markdown code block formatting
  const code = content
    .replace(/```javascript|```/g, "")
    .trim();
  
  return code;
}

/**
 * Create a runnable function from the extracted code
 * @param {string} code - The extracted code
 * @param {string} url - URL to test with
 * @returns {Function} - Async function ready to execute
 */
function createRunnableFunction(code, url = "https://api.example.com/data") {
  // Wrap the code in an async function
  const functionBody = `
    const url = "${url}";
    ${code}
  `;
  
  return new Function('return (async function() {' + functionBody + '})();');
}

// Extract the code
const extractedCode = extractCode(aiPipeResponse);
console.log("✅ Extracted Code:");
console.log(extractedCode);
console.log("\n" + "=".repeat(50) + "\n");

// Example usage with GitHub API (as mentioned in your task)
const githubApiFunction = `
try {
  const user = "sathish-k7"; // Replace with any GitHub username
  const response = await fetch(\`https://api.github.com/users/\${user}/repos\`);
  const data = await response.json();
  
  if (data.length > 0) {
    return {
      firstRepo: data[0].name,
      createdAt: data[0].created_at,
      totalRepos: data.length
    };
  } else {
    return { message: "No repositories found" };
  }
} catch (error) {
  throw error;
}
`;

console.log("✅ GitHub API Example:");
console.log(githubApiFunction);

module.exports = {
  extractCode,
  createRunnableFunction,
  aiPipeResponse
};