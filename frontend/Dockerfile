# Next.js Frontend Dockerfile for Cloud Run
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci --legacy-peer-deps

# Copy all files
COPY . .

# Set environment variable for API URL (default to production)
ENV NEXT_PUBLIC_API_BASE_URL=https://lislab-backend-326272454487.asia-northeast3.run.app
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production
ENV PORT=8080

# Build the application
RUN npm run build

# Expose port
EXPOSE 8080

# Start the server
CMD ["npm", "start"]
