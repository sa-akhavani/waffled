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

### Server Ports

Make sure to open the following ports in your firewall if you are running this on a remote server:

```
8630-8635, 8621, 8611
```

### APIs

Services, ports, and apis:

- PHP Laravel

  - Health Check: `http://localhost:8630/api/`
  - application/xml: `http://localhost:8630/api/storexml`
  - application/json: `http://localhost:8630/api/store`
  - multipart/form-data: `http://localhost:8630/api/store`

- Java Spring Boot

  - Health Check: `http://localhost:8631/`
  - application/xml: `http://localhost:8631/xml`
  - application/json: `http://localhost:8631/json`
  - multipart/form-data: `http://localhost:8631/multipart`

- Python Flask

  - Health Check: `http://localhost:8632/`
  - application/xml: `http://localhost:8632/xml`
  - application/json: `http://localhost:8632/json`
  - multipart/form-data: `http://localhost:8632/multipart`

- Python FastAPI

  - Health Check: `http://localhost:8633/`
  - application/xml: `http://localhost:8633/xml`
  - application/json: `http://localhost:8633/json`
  - multipart/form-data: `http://localhost:8633/multipart`

- Node.js Express

  - Health Check: `http://localhost:8634/`
  - application/xml: `http://localhost:8634/xml`
  - application/json: `http://localhost:8634/json`
  - multipart/form-data: `http://localhost:8634/multipart`

- Golang Gin

  - Health Check: `http://localhost:8635/`
  - application/xml: `http://localhost:8635/xml`
  - application/json: `http://localhost:8635/json`
  - multipart/form-data: `http://localhost:8635/multipart`

- Node.js HTTP JSON
  todo: double check apis for the node.js http servers

  - Health Check: `http://localhost:8621/`
  - application/json: `http://localhost:8621/json`

- Node.js HTTP Multipart
  todo: double check apis for the node.js http servers

  - Health Check: `http://localhost:8611/`
  - multipart/form-data: `http://localhost:8611/multipart`
