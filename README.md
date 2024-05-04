![HagenCopilot](docs/img/hagencopilot.png)

1. Install requirements
```bash
pip install -r requirements.txt
```

2. Start docker-compose
```bash
docker-compose up
```

3. Put pdf files in the `data` folder and index them
```bash
python load_data.py
```

4. Start chatbot
```bash
python chatbot.py
```


