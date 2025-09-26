[//] # (build image)
# docker build --no-cache -t synquerra_backend:local -f Dockerfile_local .

[//] # (for mac)
docker run -d --name synquerra_backend_api -p 8020:8020 -v /Applications/DIC/synquerra/backend_service/src_code:/opt synquerra_backend:local


