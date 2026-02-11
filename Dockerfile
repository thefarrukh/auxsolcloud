FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Tizim paketlarini o'rnatish
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Kutubxonalarni o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha kodini nusxalash
COPY . .

# start.sh fayliga bajarish ruxsatini berish
RUN chmod +x start.sh

# Portni ochish (Render odatda 10000 ni kutadi, lekin biz 8001 qoldiramiz)
EXPOSE 8001

# Konteyner ishga tushganda skriptni bajarish
CMD ["./start.sh"]