down:
	@docker-compose kill
	@docker-compose down

todo:
	@docker-compose up todo_consumer

auth:
	@docker-compose up auth_consumer

run:
	@docker compose up
