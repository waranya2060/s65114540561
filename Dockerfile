FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# ติดตั้งเครื่องมือ build และ client library สำหรับ MySQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    default-mysql-client \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ติดตั้งไลบรารีจาก requirements (ถ้ามีไฟล์)
COPY requirements.txt /app/
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# ไลบรารีเสริม
RUN pip install gunicorn mysqlclient dj-database-url

# คัดลอกโค้ดที่เหลือ
COPY . /app/

# เก็บ static (ถ้า settings ยังไม่ครบให้ผ่านไปก่อน)
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

# รัน Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_end.wsgi:application"]
