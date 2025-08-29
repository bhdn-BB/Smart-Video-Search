# Instructions for Running the Frontend Docker Container

Below are the steps to run your frontend in Docker.

## Steps:

1. Navigate to the project directory:
```bash
cd .
```

2. Build the Docker image:
```bash
docker build -t frontend:v1 .
```

3. Run the container in detached mode and map the port:
```bash
docker run -d -p 8501:8501 --name frontend_container frontend:v1
```

4. Open the frontend in your browser:
[http://127.0.0.1:8501](http://127.0.0.1:8501)
