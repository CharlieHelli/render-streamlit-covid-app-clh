# Render COVID Tracker (Jedha Launch)

Slim Streamlit COVID dashboard for Render Free (512 MB).

- Local CSV sample (no huge download at runtime)
- Streamlit native charts (no Plotly)
- Docker + `$PORT`

## Push + deploy

See:

`AIFS/.changelogs/M08-ML_Engineering/D06-Launch/MANUAL_DEPLOY_RUNBOOK.md`

## Local (no Docker)

```bash
pip install -r requirements.txt
streamlit run app.py --server.port=10000 --server.address=0.0.0.0
```
