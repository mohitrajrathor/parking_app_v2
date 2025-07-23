# ------- frontend building --------
FROM node:22-slim AS frontend-build

WORKDIR /app

COPY ./frontend/package*.json ./
RUN npm install --production

COPY ./frontend ./
RUN npm run build


# ------- main application -------
FROM python:3.12-slim AS backend

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt 


COPY ./backend ./backend

# Copy frontend build to backend static directory
COPY --from=frontend-build /app/dist ./frontend/dist

EXPOSE 1234

CMD ["python", "-m", "flask","--app", "backend.app", "run", "--host", "0.0.0.0", "--port", "1234"]