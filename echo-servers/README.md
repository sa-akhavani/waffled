### Build
```
docker build -t waffled-servers .
```

### Run
```
docker run -p 8630-8635:8630-8635 -p 8621:8621 -p 8611:8611 waffled-servers
```

### Check status:
```
docker exec -it $(docker ps --filter "ancestor=waffled-servers" --format "{{.ID}}") pm2 ls
```

### todo:
check environment variables for payloads

### Server Ports
Here are the services and their respective ports:
- Laravel: http://localhost:8630
- Spring Boot: http://localhost:8631
- Flask: http://localhost:8632
- FastAPI: http://localhost:8633
- Express (Node.js): http://localhost:8634
- Gin (Go): http://localhost:8635
- Node.js HTTP JSON: http://localhost:8621
- Node.js HTTP Multipart (Busboy): http://localhost:8611
