#!/bin/bash
# Start the application
echo "Starting application..."

# Start the main application
python main.py &

# Wait for application to be ready
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "Application is ready"
        exit 0
    fi
    echo "Waiting for application to start..."
    sleep 2
done

echo "Application failed to start"
exit 1