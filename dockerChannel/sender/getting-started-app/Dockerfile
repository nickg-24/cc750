# syntax=docker/dockerfile:1

FROM node:18-alpine
COPY . .
WORKDIR /app
RUN yarn install --production
CMD ["node", "src/index.js"]
EXPOSE 3000