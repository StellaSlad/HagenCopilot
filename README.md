<p align="center"><img width=250 src="docs/img/hagencopilot_dark.png#gh-dark-mode-only" /></p>
<p align="center"><img width=250 src="docs/img/hagencopilot_light.png#gh-light-mode-only" /></p>
## Run HagenCopilot

Ensure to add a .env file, take a look at the .env-example file.

1. Install requirements:

```bash
pip install -r backend/requirements.txt
```

2. Start the docker-compose:

```bash
docker-compose up -d
```

3. Put pdf files in the `data` folder and start the indexation of the files:

```bash
python backend/load_data.py
```

4. Start the backend:

```bash
python backend/api.py
```

5. Start the frontend:

```bash
cd frontend
npm run dev
```

## Run evalutation pipeline

Make sure VPN is connected and the docker-compose is running and already indexed the data.

Run evalutation pipeline:

```bash
python backend/evaluation.py
```
