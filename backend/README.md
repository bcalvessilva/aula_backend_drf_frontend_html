Setup rápido (Windows PowerShell):

```powershell
# criar o venv
python -m venv .venv
# ativar
.\.venv\Scripts\Activate.ps1
# atualizar pip
python -m pip install --upgrade pip
# instalar dependências
pip install -r requirements.txt
# copiar exemplo de .env
copy .env.example .env
# executar migrations
python manage.py migrate
# criar superuser (opcional)
python manage.py createsuperuser
# rodar servidor
python manage.py runserver
```

Se estiver usando CMD use `\.venv\Scripts\activate` para ativar o venv.
