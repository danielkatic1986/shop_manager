# Kako pokrenuti aplikaciju lokalno u Dockeru?
- Morate imati instaliran Docker na vašem računalu
- Klonirajte repozitorij
```bash
git clone https://github.com/danielkatic1986/shop_manager.git
cd shop_manager
```
- Izgradite Docker image i pokrenite kontejner
```bash
docker build -t flask-app .
docker run -p 5000:5000 flask-app

```
- Ili pomoću Docker Compose
```bash
docker-compose up --build
```
- Otvorite aplikaciju u pregledniku
http://localhost:5001
