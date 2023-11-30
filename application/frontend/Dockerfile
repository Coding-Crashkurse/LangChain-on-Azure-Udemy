# Stage 1: Base stage with Node.js 18
FROM node:18 as build-stage
WORKDIR /app
COPY package*.json /app/
RUN npm install

# Copy the rest of the files
COPY . /app

# Build the project
RUN npm run build

# Stage 2: Production stage
FROM nginx:alpine
COPY --from=build-stage /app/dist/frontend /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
