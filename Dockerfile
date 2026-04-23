FROM python:3.11-slim

WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando para levantar la API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]