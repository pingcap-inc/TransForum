.PHONY: build start

build:
	docker build -t trans-forum:latest .

start:
	docker run -itd \
		-p 4000:4000 \
		-v .env:/app/.env \
		trans-forum:latest