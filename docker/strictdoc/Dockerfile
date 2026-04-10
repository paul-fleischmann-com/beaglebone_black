# =============================================
# StrictDoc CI Container
# Minimal image: strictdoc for HTML export
# No Google Chrome / PDF rendering needed
# =============================================

FROM python:3.12-slim

ARG STRICTDOC_VERSION=latest
ARG VERSION=unknown

LABEL org.opencontainers.image.version=$VERSION
ENV APP_VERSION=$VERSION

RUN pip install --no-cache-dir \
    $([ "$STRICTDOC_VERSION" = "latest" ] && echo "strictdoc" || echo "strictdoc==$STRICTDOC_VERSION")

WORKDIR /data
CMD ["sh", "-c", "echo 'Container Version: $APP_VERSION'"]
ENTRYPOINT ["strictdoc"]
