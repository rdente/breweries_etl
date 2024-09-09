# Criando o container

- Instale algum docker por bash, no caso foi utilizado podman pelo comando bash
`sudo apt install podman-docker`

- Navegue para sua pasta usando `cd /home/user/airflow`

- Crie um arquivo com um bloco de notas, ou o nano usando neste caso`nano Dockerfile`

- Cole o conteudo de `Containerfile` e salve com o mesmo nome em seu path `/home/user/airflow`

- `podman build -t dockerfile /home/user/airflow` para criar a imagem do container

- Use `podman run -d -p 8080:8080 --name airflowcontainer localhost/dockerfile:latest` para iniciar o container 

- Aguarde cerca de um minuto e acesse `http://localhost:8080` e use as credenciais admin para usuario e senha

