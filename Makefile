DC = docker compose
EXEC = docker exec -it 
ENV = --env-file .env
COMPOSE_FILE = docker/docker-compose.yml
APP_NAME = microcrm
LOGS = docker logs


.PHONY: app
app:
	${DC} -f ${COMPOSE_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${COMPOSE_FILE} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_NAME} -f






