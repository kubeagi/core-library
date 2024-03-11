#!/bin/sh

# Install curl
apt-get install -y curl

# Test GET /api/v1/health
echo "---------------------------------------"
echo "Sleeping for 20 seconds..."
sleep 20

echo "Testing GET /api/v1/health"
response=$(curl -s -X GET http://localhost:8000/api/v1/health)
expected='{"Health":true}'

if [ "$response" = "$expected" ]; then
    echo "GET /api/v1/health passed"
else
    echo "GET /api/v1/health failed. Expected $expected, got $response"
    exit 1
fi

echo "---------------------------------------"

# Test POST /api/v1/reranking
echo "Testing POST /api/v1/reranking"
data='{"question": "How are you today?", "answers": ["I am fine now, thank you.", "I was doing my business."]}'
response=$(curl -s -X POST -H "Content-Type: application/json" -H 'accept: application/json' -d "$data" http://localhost:8000/api/v1/reranking)

if [ -z "$response" ]; then
    echo "POST /api/v1/reranking failed to get a response"
    exit 1
else
    echo "Reranking results: $response"
fi

echo "All tests passed"