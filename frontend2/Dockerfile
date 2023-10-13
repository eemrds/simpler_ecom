FROM nginx:alpine

WORKDIR /app
RUN apk add curl bash
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash

RUN nvm install 18
RUN npm install
COPY . .
RUN npm run build
RUN cp -r build/* /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN apk add --update nodejs npm

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]