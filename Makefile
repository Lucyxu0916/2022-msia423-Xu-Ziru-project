.PHONY: pipeline_image upload_to_s3 database acquire
pipeline_image:
	docker build -f dockerfiles/Dockerfile -t final-project .

upload_to_s3:
	docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ final-project run_s3.py upload


database:
	docker run -e SQLALCHEMY_DATABASE_URI --mount type=bind,source="$(shell pwd)",target=/app/ final-project run_rds.py create_db

data/raw/bodyfat.csv: config/config.yaml
	docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ final-project run_s3.py download

download_from_s3: data/raw/bodyfat.csv

data/artifacts/cleaned_data.csv: data/raw/bodyfat.csv config/config.yaml
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run.py preprocess --config=config/config.yaml

cleaned: data/artifacts/cleaned_data.csv

process: download_from_s3 cleaned

data/artifacts/features.csv: data/artifacts/cleaned_data.csv config/config.yaml
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run.py get_features --config=config/config.yaml

features: data/artifacts/features.csv

models/Lasso.sav: data/artifacts/features.csv config/config.yaml
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run.py train --config=config/config.yaml

train: models/Lasso.sav

data/artifacts/predictions.txt:models/Lasso.sav config/config.yaml
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run.py predict --config=config/config.yaml

predict: data/artifacts/predictions.txt

data/artifacts/evaluation_result.txt:data/artifacts/predictions.txt config/config.yaml
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run.py evaluate --config=config/config.yaml

evaluate: data/artifacts/evaluation_result.txt

all: clean pipeline_image download_from_s3 cleaned features train predict evaluate

.PHONY: test_image, run_test, test
test_image:
	docker build -f dockerfiles/Dockerfile.test -t final-project-tests .

run_test:
	docker run final-project-tests

test: test_image run_test

.PHONY: app_image, run_app, build_app
app_image:
	docker build -f dockerfiles/Dockerfile.app -t final-project-app .

run_app:
	docker run -e SQLALCHEMY_DATABASE_URI -p 5001:5001 final-project-app

build_app: app_image run_app

clean:
	rm -f data/raw/*
	rm -f data/artifacts/*
	rm -f models/*


