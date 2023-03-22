IMAGE_NAME=sample_app
CONTAINER_NAME=sample_app_container

build_docker_image:
	docker build -t $(IMAGE_NAME) .
run_docker_image:
	docker run --name $(CONTAINER_NAME) -it $(IMAGE_NAME) 

stop_all_containers:
	docker kill $$(docker ps -q)

compose_up:
	docker-compose up
compose_down:
	docker-compose down

check_for_containers:
	docker ps -a
	docker images --filter "dangling=true"

check_for_all_image:
	docker image ls

tear_down_all:
	docker system prune -af
