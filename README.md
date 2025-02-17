# healthcare-ai

## Front End
From root go to frontend dir
```
cd front-end
```
For first time running:
```
npm install
```
  
To run the app:
```
npm run dev
```

To run front-end as image
```
podman build -t healthcare_fe .
podman run --name healthcare_fe --rm -p 8080:8080 healthcare_fe
```

## Back End
From root go to backend healthcare dir
```
cd back-end/healthcare
```

To initialize crewai
```
crewai install
source .venv/bin/activate
```
  
To test crewai locally
```
uv run kickoff
```
or 
```
python src/healthcare/main.py
```

To run fast api
```
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

To run back-end as image
```
podman build -t healthcare_be .
podman run --name healthcare_be --rm -p 8080:8080 healthcare_be
```


