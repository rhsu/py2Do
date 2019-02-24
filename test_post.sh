#!/bin/bash
curl -H "Content-Type: application/json" \
	 -X POST http://localhost:5000/register \
	 -d '{ "username": "robert", "password": "pssword" }'