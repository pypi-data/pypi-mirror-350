FROM python:3.13

COPY tool_interface /src/tool_interface
COPY pyproject.toml /src/pyproject.toml
COPY LICENSE /src/LICENSE
COPY README.md /src/README.md
WORKDIR /src
RUN pip install --upgrade pip && \
    pip install ipython && \
    pip install -e ".[dev]"

CMD ["ipython"]