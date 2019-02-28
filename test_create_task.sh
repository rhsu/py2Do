#!/bin/bash
curl -H "Content-Type: application/json" \
	 -X POST http://localhost:5000/task \
	 -d '{ "title": "test", "content": "hello world", "status_id": 1 }'