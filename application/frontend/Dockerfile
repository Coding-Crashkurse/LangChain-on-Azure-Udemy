# Stage 1: Base stage with Node.js 18 for building frontend assets
FROM node:18-buster-slim as build-stage

WORKDIR /app

# Copy package.json and yarn.lock files
COPY package.json yarn.lock /app/

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy the rest of your frontend application
COPY . /app

# Build the application
RUN yarn build

# Stage 2: Production stage for FastAPI application
FROM python:3.11-slim-buster

WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy built frontend assets from build-stage
COPY --from=build-stage /app/dist/frontend /app/dist/frontend

# Copy only the necessary files
COPY . /app

EXPOSE 3000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "3000"]
