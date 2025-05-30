#!/bin/bash
# Run all tests in Docker

set -e

echo "🚀 OpenCraftShop Test Suite"
echo "==========================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name=$1
    local test_command=$2
    
    echo -e "${YELLOW}Running $test_name...${NC}"
    
    if eval $test_command; then
        echo -e "${GREEN}✅ $test_name passed${NC}\n"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ $test_name failed${NC}\n"
        ((TESTS_FAILED++))
    fi
}

# Start services
echo "Starting services..."
docker-compose up -d web > /dev/null 2>&1

# Wait for web service to be ready
echo "Waiting for web service to start..."
sleep 10

# Run tests
run_test "API Tests" "docker-compose run --rm opencraftshop python3 /app/tests/test_api.py"
run_test "3D Model Tests" "docker-compose run --rm opencraftshop python3 /app/tests/test_3d_models.py"
run_test "BOM Generation" "docker-compose run --rm opencraftshop python3 -m pytest /app/tests/unit/test_generate_bom.py -v"
run_test "Cut Optimization" "docker-compose run --rm opencraftshop python3 -m pytest /app/tests/unit/test_optimize_cuts.py -v"

# Summary
echo "=============================="
echo "Test Summary"
echo "=============================="
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! 🎉${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed 😞${NC}"
    exit 1
fi