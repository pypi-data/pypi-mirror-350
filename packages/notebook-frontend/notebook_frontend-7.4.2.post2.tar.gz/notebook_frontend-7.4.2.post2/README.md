# notebook-frontend

A Python package distributing Notebook's static assets only, with no Python dependency.

```bash
curl --output notebook-7.4.2-py3-none-any.whl https://files.pythonhosted.org/packages/1e/16/d3c36a0b1f6dfcf218add8eaf803bf0473ff50681ac4d51acb7ba02bce34/notebook-7.4.2-py3-none-any.whl
unzip notebook-7.4.2-py3-none-any.whl
mkdir -p share
cp -r notebook-7.4.2.data/data/share/jupyter share/
cp -r notebook/static src/notebook_frontend/
cp -r notebook/templates src/notebook_frontend/
```
