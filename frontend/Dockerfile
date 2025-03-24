# 构建阶段
FROM node:14 as build-stage

WORKDIR /app

# 复制package.json和package-lock.json
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制项目文件
COPY . .

# 构建应用
RUN npm run build

# 生产阶段
FROM nginx:stable-alpine as production-stage

# 复制构建文件到Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 配置Nginx以处理前端路由
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

# 暴露端口
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]