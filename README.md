# easyvisit-admin
API REST para administrar el registro de Urbanizaciones, Administradores, Casas, Planes, Usuarios y todo lo relacionado con la administración de los clientes.

## Instalación

### Requerimientos

- Mysql 8
- Nginx
- python3
- Git
- Server GNU/Linux (Probado sobre Debian 12)

### Configuración de la API REST

#### Instalar requerimientos
```shell
apt install wget curl htop net-tools software-properties-common apt-transport-https curl lsb-release ca-certificates certbot python3-certbot-nginx 
```
#### Configurar mysql-server
```shell
curl -fsSL https://repo.mysql.com/RPM-GPG-KEY-mysql-2022 | gpg --dearmor | sudo tee /usr/share/keyrings/mysql.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/mysql.gpg] http://repo.mysql.com/apt/debian $(lsb_release -sc) mysql-8.0" | sudo tee /etc/apt/sources.list.d/mysql.list
apt update
apt install mysql-community-server
mysql_secure_installation # Para establecer enforcement de la contraseña y eliminar bases y usuarios de prueba
mysql -u root -p
# Crear base de datos, crear usuario y dar privilegios
```

#### Clonar el repo
```shell
git clone https://github.com/EAmarillo/easyvisit-admin.git
```

##### Crear el entorno virtual
```shell
python3 -m venv admin-env
```

##### Activar el entorno virtual
```shell
source admin-env/bin/activate
```

#### Instalar dependencias
```shell
apt install python3-dev default-libmysqlclient-dev pkg-config
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
pip install gunicorn
```
Configurar archivo .env, recuerda crear una llave segura para producción.

```shell
nano .env


DJANGO_SECRET_KEY=''
ALLOWED_HOSTS='admin.easyvis.it'

DB_NAME=''
DB_USER=''
DB_PASSWORD=''
DB_HOST='localhost'
DB_PORT='3306'
```

#### Configurar servicio para GUnicorn
```shell
nano /etc/systemd/system/easyvisit-admin.service

[Unit]
Description=Easy Visit Admin API
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/html/easyvisit-admin/easyvisit_admin
ExecStart=/var/www/html/easyvisit-admin/easyvisit_admin/admin-env/bin/gunicorn --workers 3 --access-logfile /var/log/easyvisit-admin/access.log --error-logfile /var/log/easyvisit-admin/error.log --bind unix:easyvisit-admin.sock easyvisit_admin.wsgi:application

[Install]
WantedBy=multi-user.target
```

Recargar demonios y lanzar el servicio
```shell
systemctl daemon-reload 
systemctl start easyvisit-admin.service
systemctl enable easyvisit-admin.service 
systemctl enable nginx
```

#### Configurar Nginx
Para esto necesitamos un dominio o sumdominio apuntando al server, toda la configuración la realizaré con el dominio admin.easyvis.it

```shell
touch /etc/nginx/sites-available/admin.easyvis.it
certbot --nginx # Seleccionar el dominio admin.easyvis.it y continuar

nano /etc/nginx/sites-available/admin.easyvis.it

server {
    listen 80;
    server_name admin.easyvis.it;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name admin.easyvis.it;

    ssl_certificate /etc/letsencrypt/live/admin.easyvis.it/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/admin.easyvis.it/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/html/easyvisit-admin/easyvisit_admin/easyvisit-admin.sock;
    }
    location /staticfiles {
    alias /var/www/html/easyvisit-admin/easyvisit_admin/staticfiles;
    }
    location /extras {
    alias /var/www/html/extras;
    }
}

```

Ejecutar ```python manage.py collectstatic``` para recargar los archivos estáticos

Probar cambios en Nginx y reiniciar servicios

```shell
nginx -t
systemctl restart nginx.service easyvisit-admin.service 
```

## Uso de la API 

Hasta este punto la api permite utilizar métodos PATCH, DELETE, GET y POST en las siguientes apps.

Puede encontrar un archivo de configuracíon para insomnia en https://admin.easyvis.it/extras/Insomnia_2023-11-06.json

### Urbanizations
- POST
```curl
curl --request POST \
  --url https://admin.easyvis.it/urbanization \
  --header 'Content-Type: application/json' \
  --data '{
    "name": "Residencial de las Montañas",
    "street": "Montañas del mundo",
    "number": "100",
    "neighborhood": "Residencial Cordilleras",
    "city": "León",
    "state": "Guanajuato",
    "country": "México",
    "zip_code": 37178,
    "houses": 192,
    "is_active": true,
    "rfc": "1234567890123",
    "email": "urbanizationb@host.com",
    "plan": 3
}'
```
- GET
```shell
# Recuperar todos los registros
curl --request GET \
  --url https://admin.easyvis.it/urbanization
  
# Recuperar un registro por ID
curl --request GET \
  --url https://admin.easyvis.it/urbanization/4
```
- PATCH
```shell
curl --request PATCH \
  --url https://admin.easyvis.it/urbanization/2 \
  --header 'Content-Type: application/json' \
  --data '{
    "name": "Paseo de las Montañas",
    "street": "Montañas del mundo",
    "number": "102",
    "neighborhood": "Residencial Cordilleras",
    "city": "León",
    "state": "Guanajuato",
    "country": "México",
    "zip_code": 37178,
    "houses": 192,
    "is_active": true,
    "rfc": "1234567890123",
    "email": "eamarillob@gmail.com",
    "plan": 3
}'
```
- DELETE
```shell
curl --request DELETE \
  --url https://admin.easyvis.it/urbanization/1
```

### Places
- POST
```shell
curl --request POST \
  --url https://admin.easyvis.it/places \
  --header 'Content-Type: application/json' \
  --data '{
				"id": 1,
				"street": "Everest",
				"number": "101",
				"neighborhood": "Paseo de las montañas",
				"city": "León",
				"state": "Guanajuato",
				"country": "México",
				"zip_code": 45678,
				"is_active": true,
				"urbanization": 3
			}'
```
- GET
```shell
# Recuperar todos los registros
curl --request GET \
  --url https://admin.easyvis.it/places
  
# Recuperar un registro por ID
curl --request GET \
  --url https://admin.easyvis.it/places/1
```
- PATCH
```shell
curl --request PATCH \
  --url https://admin.easyvis.it/places/1 \
  --header 'Content-Type: application/json' \
  --data '{
				"street": "Everest",
				"number": "103",
				"neighborhood": "Paseo de las montañas",
				"city": "León",
				"state": "Guanajuato",
				"country": "México",
				"zip_code": 45678,
				"is_active": true,
				"urbanization": 3
			}'
```
- DELETE
```shell
curl --request DELETE \
  --url https://admin.easyvis.it/places/1
```
### Urbanization Managers
- POST
```shell
curl --request POST \
  --url https://admin.easyvis.it/urbanization-manager \
  --header 'Content-Type: application/json' \
  --data '{
    "first_name": "Ernesto",
    "last_name": "Amarillo",
    "phone": 4775529217,
    "email": "eam2@gmai.com",
    "is_active": true,
    "urbanization": 1
}'
```
- GET
```shell
# Recuperar todos los registros
curl --request GET \
  --url https://admin.easyvis.it/urbanization-manager
  
# Recuperar un registro por ID
curl --request GET \
  --url https://admin.easyvis.it/urbanization-manager/1
```
- PATCH
```shell
curl --request PATCH \
  --url https://admin.easyvis.it/urbanization-manager/1 \
  --header 'Content-Type: application/json' \
  --data '{
				"id": 1,
				"first_name": "Ernesto",
				"last_name": "Amarillo",
				"phone": 4775529217,
				"email": "eam2@gmai.com",
				"is_active": true,
				"urbanization": 1
			}'
```
- DELETE
```shell
curl --request DELETE \
  --url https://admin.easyvis.it/urbanization-manager/1
```

### Users
Users tiene funcionalidad limitada y parcial en los siguientes métodos. Para cargar usuarios en la base de datos es necesario hacer un dump desde un archivo CSV. Puede obtener un ejemplo descargando el archivo de muestra en https://admin.easyvis.it/extras/Residencial_de_las_montañas.csv

El archivo deberá llamarse tal cual como la urbanización registrada previamente, sustituyendo los espacios con guiones bajos.
- POST
```shell
curl --request POST \
  --url http://admin.easyvis.it/upload-users \
  --header 'content-type: multipart/form-data' \
  --form 'csv_file=@/home/eamarillo/assets/bootcamp/easyvisit-admin/easyvisit_admin/Residencial_de_las_montañas.csv'
```
- GET
```shell
# Recuperar todos los registros
curl --request GET \
  --url https://admin.easyvis.it/users
  
# Recuperar un registro por ID
curl --request GET \
  --url https://admin.easyvis.it/users/1
```
