# Image
FROM node:13-alpine

# Container's application directory
WORKDIR /app/

ENV PATH /app/node_modules/.bin:$PATH

# Install dependencies
COPY package.json /app/package.json
RUN npm install --silent
RUN npm install react-scripts@3.3.1 -g --silent

# Add app
COPY . /app/

# Start app
CMD ["npm", "start"]