# =============================================
# StrictDoc CI Container
# Minimal image: strictdoc for HTML export
# No Google Chrome / PDF rendering needed
# =============================================

FROM python:3.12-slim

ARG STRICTDOC_VERSION=latest

RUN pip install --no-cache-dir \
    $([ "$STRICTDOC_VERSION" = "latest" ] && echo "strictdoc" || echo "strictdoc==$STRICTDOC_VERSION")

WORKDIR /data
ENTRYPOINT ["strictdoc"]
