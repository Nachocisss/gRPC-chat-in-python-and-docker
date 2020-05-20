Instructions:

    - docker-compose build
    - docker-compose up -d --scale client=n  (replace n  = number of users)
    - docker attach parte1_server_1
    - open n terminals and use docker attach parte1_client_i (whit i = id, i >= 1)
