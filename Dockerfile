FROM python:3.12-slim

# libs สำหรับ PostgreSQL และการรอพอร์ต (nc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ติดตั้งไลบรารี Python
COPY requirements.txt /app/requirements.txt
# กันกรณีไฟล์เดิมยังมี mysqlclient (เราใช้ Postgres เท่านั้น)
RUN sed -i '/^[[:space:]]*mysqlclient[[:space:]]*/Id' /app/requirements.txt \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && pip install --no-cache-dir "psycopg[binary]>=3.2,<3.3" gunicorn whitenoise

# คัดลอกโปรเจกต์ให้ path ตรงกับคำสั่ง manage.py ใน compose
COPY django_end /app/django_end

# โฟลเดอร์ static เมื่อ collectstatic
RUN mkdir -p /app/staticfiles

EXPOSE 8000
