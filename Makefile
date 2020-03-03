test-data:
		@echo ">> creating test-data"
		python3 cmd.py test-data
		@echo ">> test-data created"
start:
		@echo ">> starting app"
		python3 cmd.py start-app
		@echo ">> app started"
