FROM node:16
WORKDIR '/app'
COPY ./package.json ./
RUN npm i -g @quasar/cli && \ 
    yarn install
COPY . .
EXPOSE 3000
CMD ["quasar", "dev"]
