MY_UID="$(id -u)" MY_GID="$(id -g)" docker-compose build 
MY_UID="$(id -u)" MY_GID="$(id -g)" docker-compose run --service-ports dsc_nlp 

# jupyter notebook --ip 0.0.0.0 --allow-root --no-browser