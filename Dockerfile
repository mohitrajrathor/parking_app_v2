# ------- frontend building --------
FROM node:22-slim AS frontend-build

WORKDIR /app

COPY ./frontend/package*.json ./
RUN npm install 

COPY ./frontend ./
RUN npm run build 


# ------- main application -------
FROM python:3.12-slim AS backend

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 


COPY ./backend ./backend 

# copying frontend dist from frontend build stage
COPY --from=frontend-build /app/dist ./frontend/dist

EXPOSE 1234

CMD [ "gunicorn", "--workers=2", "app:create_app()", "-b", "0.0.0.0:1234"]