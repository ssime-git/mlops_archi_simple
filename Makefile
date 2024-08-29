build-train:
	docker build -t iris_model_training -f Dockerfile.train .

run-train:
	docker run --env-file .env --rm iris_model_training

train-model: build-train run-train

compose:
	docker-compose up --build

enter-train:
	docker run -it mlops_archi_simple-iris_model_training bash

compose-train:
	docker compose run --rm iris_model_training