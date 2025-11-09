# Tools in Data Science

This repository contains various data science tools, utilities, and automation workflows.

## Contact Information

**Email:** 24f1000011@ds.study.iitm.ac.in

## Repository Contents

### GitHub Actions Workflows

- **Multi-Platform Matrix Build**: Demonstrates parallel CI/CD builds across multiple platforms and configurations
  - Builds on Ubuntu, macOS, and Windows
  - Tests with multiple Node.js versions (16, 18, 20)
  - Generates and uploads build artifacts for each matrix variant
  - Workflow identifier: `matrix-232d56b`
  - Artifact naming: `build-232d56b-<variant>`

### Scripts and Utilities

- **transform.js** - Matrix transpose function for 2D arrays
- **semantic_search_api.py** - Semantic search API implementation
- **typescript_rag_api.py** - TypeScript RAG (Retrieval Augmented Generation) API
- **ai-pipe-extractor.js** - AI pipeline extraction utility
- **Various GA4 scripts** - Google Analytics 4 query tools

### APIs

- Semantic Search API
- TypeScript RAG API
- FastAPI Agent (in `fastapi-agent/` directory)

## GitHub Actions Matrix Build

The repository includes a sophisticated multi-platform matrix build workflow that:

1. **Parallel Execution**: Runs builds simultaneously across:
   - 3 Operating Systems: Ubuntu, macOS, Windows
   - Multiple Node.js versions: 16, 18, 20
   - Total of 7 matrix combinations

2. **Artifact Generation**: Each build produces:
   - Detailed build output with system information
   - JSON metadata file with build context
   - Status report
   - All artifacts are uploaded with the prefix `build-232d56b-`

3. **Validation Features**:
   - Step identifier `matrix-232d56b` included
   - Non-empty artifacts with meaningful content
   - Proper error handling with `if-no-files-found: error`
   - 7-day artifact retention

## Deployment

The repository supports multiple deployment platforms:
- Cloudflare Pages
- Railway
- Fly.io
- Docker containers

## Testing

Various test files are included for different components:
- `test_api.html` - API testing interface
- `test_semantic_search.py` - Semantic search tests
- `test_typescript_rag.py` - TypeScript RAG tests
- `test-ai-pipe.js` - AI pipeline tests

## Setup

See the following guides for setup instructions:
- `QUICKSTART.md` - Quick start guide
- `DEPLOYMENT_GUIDE.md` - Deployment instructions
- `copilot-setup-guide.md` - GitHub Copilot setup

## License

This project is maintained for educational and development purposes.

---

**Repository Owner:** sathish-k7  
**Contact:** 24f1000011@ds.study.iitm.ac.in
