![HagenCopilot](docs/img/hagencopilot.png)

Ensure to add a .env file, take a look at the .env-example file.

1. Install requirements

```bash
pip install -r requirements.txt
```

2. Start the docker-compose

```bash
docker-compose up -d
```

3. Put pdf files in the `data` folder and start the indexation of the files

```bash
python backend/load_data.py
```

4. Start the backend

```bash
python backend/api.py
```
