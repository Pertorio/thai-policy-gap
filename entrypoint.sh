#!/bin/sh
set -e

mkdir -p .streamlit
cat > .streamlit/secrets.toml <<EOF
ANTHROPIC_API_KEY = "${ANTHROPIC_API_KEY}"
VOYAGEAI_API_KEY = "${VOYAGEAI_API_KEY}"
EOF

exec uv run streamlit run app.py \
    --server.port=8502 \
    --server.address=0.0.0.0 \
    --server.headless=true
