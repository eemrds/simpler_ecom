
docker build -t eemrds/frontend:latest ./frontend
docker build -t eemrds/backend:latest ./backend
docker push eemrds/frontend:latest
docker push eemrds/backend:latest