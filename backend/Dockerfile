FROM python:3.9
WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8889

CMD ["gunicorn", "-b", ":8889", "app:app"]
