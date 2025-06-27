FROM python:3.11-slim

# Variáveis de ambiente para evitar criação de arquivos .pyc e buffer no stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libpq-dev \
        supervisor \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY src/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY src/ /app/

# Coleta arquivos estáticos (ajuste conforme seu projeto)
RUN python manage.py collectstatic --no-input \
    && python manage.py makemigrations \
    && python manage.py migrate --noinput 
# Copia configuração do Supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expõe a porta usada pelo Gunicorn
EXPOSE 8000

# Comando para iniciar o Supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
