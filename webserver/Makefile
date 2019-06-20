build:
	docker build -t rhapsodyserver .

bash:
	docker run -it -p 5025:5000 -v $(PWD)/test:/test --rm --name rhapsodyserver rhapsodyserver bash

interactive:
	docker run -it -p 5025:5000 -v $(PWD)/tempuploads:/app/tempuploads --rm --name rhapsodyserver rhapsodyserver /app/run_server.sh

server:
	docker run -d -p 5025:5000 --rm --name rhapsodyserver rhapsodyserver /app/run_production_server.sh

attach:
	docker exec -i -t  rhapsodyserver /bin/bash