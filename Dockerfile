# Koristi Python 3.9
FROM python:3.9

# Postavi radni direktorij
WORKDIR /app

# Kopiraj sve datoteke u Docker container
COPY . .

# Instaliraj potrebne pakete
RUN pip install -r requirements.txt

# Otvori port 5001
EXPOSE 5001

# Pokreni aplikaciju
CMD ["python", "app.py"]

