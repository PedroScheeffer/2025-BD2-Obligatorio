# Usa una imagen oficial de Python como base.
FROM python

# Establece el directorio de trabajo dentro del contenedor.
WORKDIR /src

# Copia el archivo requirements.txt y lo instala.
COPY requirements.txt .

# Instala las dependencias del proyecto.
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8000 (FastAPI default port).
EXPOSE 8000

# Comando para ejecutar la aplicación con uvicorn, hot reload y debug mode.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]