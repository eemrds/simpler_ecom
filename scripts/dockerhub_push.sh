
docker build -t eemrds/frontend:latest ${pwd}/frontend
docker build -t eemrds/backend:latest ${pwd}/backend
docker push eemrds/frontend:latest
docker push eemrds/backend:latest