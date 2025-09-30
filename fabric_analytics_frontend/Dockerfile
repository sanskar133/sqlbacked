# Use an existing node alpine image as a base image.
FROM node:18-alpine as builder


WORKDIR /fabric_analytics_frontend

COPY package*.json /fabric_analytics_frontend/

RUN npm install --force
COPY . /fabric_analytics_frontend/

COPY .env /fabric_analytics_frontend/

RUN npm run build

# production environment
FROM nginx:stable-alpine
COPY --from=builder fabric_analytics_frontend/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3002
CMD ["nginx", "-g", "daemon off;"]
