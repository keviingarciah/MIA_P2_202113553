# MIA_P2_202113553

## Backend

### Entorno Virtual
``` 
python3 -m venv venv
source venv/bin/activate
``` 

### Instalar dependencias
```
pip install flask
pip install flask-cors
pip install graphviz
pip install colorama
pip install ply
pip install python-dotenv
```
### AWS
server {
    listen 80;
    server_name 3.147.44.28;
    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}

http://3.147.44.28

## Frontend
```
npm create vite
Project name: frontend
Select a framework: react
Select a variant: js
```

```
cd frontend
npm i
npm run dev
```

```
npm install react-bootstrap bootstrap
npm i react-router-dom
```