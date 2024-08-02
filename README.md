<p align="center"><img width=250 src="docs/img/hagencopilot_dark.png#gh-dark-mode-only" /></p>
<p align="center"><img width=250 src="docs/img/hagencopilot_light.png#gh-light-mode-only" /></p>

## Run HagenCopilot

1. Ensure to add a .env file, take a look at the .env-example file.

2. Install requirements:

```bash
pip install -r backend/requirements.txt
```

3. Start the docker-compose:

```bash
docker-compose up -d
```

4. Put pdf files in the `data` folder and start the indexation of the files:

```bash
python backend/load_data.py
```

5. Start the backend:

```bash
python backend/api.py
```

6. Access HagenCopilot at http://localhost:3000

## Run evalutation pipeline

Make sure VPN is connected and the docker-compose is running and already indexed the data.

Run evalutation pipeline:

```bash
python backend/evaluation.py
```
