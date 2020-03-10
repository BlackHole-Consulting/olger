openssl genrsa -out yourdomain.com.key 2048

openssl req -new -sha256 -key yourdomain.com.key -subj "/C=PA/ST=PA/O=YOUR COMPANY NAME/CN=*.yourdomain.com" -out yourdomainternal.csr

openssl req -x509 -new -nodes -key yourdomain.com.key -sha256 -days 2024 -out rootCAinternal.crt

openssl x509 -req -in yourdomaininternal.csr -CA rootCAinternal.crt -CAkey yourdomaininternal.com.key -CAcreateserial -out yourdomaininternal.com.crt -days 2500 -sha256
