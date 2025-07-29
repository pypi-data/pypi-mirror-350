# README.md
# CLI Example

Una aplicación de línea de comandos muy simple.

## Instalar
```bash
pip install cli-example
```

## Ejecutar
```bash
cli-example
```

## Desarrollo
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install
```

## Pruebas
```bash
pytest
```

## Publicar nueva versión
```bash
# Asegúrate de estar en main y sincronizado
# Cambia versión en pyproject.toml

git checkout main
git merge dev
git tag v0.1.0
git push origin main --tags
```

---
