FROM python:3.9-slim  
LABEL "language"="python"  
LABEL "framework"="django"  
WORKDIR /app  
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  
COPY . .  
RUN python manage.py collectstatic --noinput || true  
EXPOSE 8080  
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "APIProject.wsgi:application"]  
