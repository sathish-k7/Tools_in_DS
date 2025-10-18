/**
 * Root handler for /api/GA3/ path
 */

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export async function onRequestGet() {
  return new Response(
    JSON.stringify({
      message: "TypeScript Documentation RAG API",
      version: "1.0.0",
      endpoint: "/api/GA3/8",
      usage: "Add ?q=your_question to the endpoint URL",
      example: "/api/GA3/8?q=What does the author affectionately call the => syntax?",
      status: "✅ Running"
    }, null, 2),
    {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        ...corsHeaders
      }
    }
  );
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: corsHeaders
  });
}
