#!/bin/bash

echo "Iniciando ambiente do Webscrapping de Biblioteca..."

echo "Construindo contêineres..."
docker-compose build

echo "Iniciando contêineres..."
docker-compose up -d

echo "Aguardando contêineres iniciarem..."
sleep 10

echo "Exibindo logs do webscrapping (pressione Ctrl+C para sair)..."
docker-compose logs -f webscrapping
