Integrantes: 
    - Pablo Aguirre, ROL: 201473555-3
    - Ignacio Cisternas, ROL: 201573544-1
    
Instrucciones:

  1) Para la parte 1:
    - docker-compose build
    - docker-compose up -d --scale client=n  (reemplazar n por la cantidad de clientes)
    - docker attach parte1_server_1
    - abrir n terminales y en cada una usar docker attach parte1_client_i (donde i es el numero del cliente, i >= 1)
    
  2) Para la parte 2:
    - docker-compose build
    - docker-compose up -d --scale client=n  (reemplazar n por la cantidad de clientes)
    - docker attach parte2_server_1
    - abrir n terminales y en cada una usar docker attach parte2_client_i (donde i es el numero del cliente, i >= 1)
