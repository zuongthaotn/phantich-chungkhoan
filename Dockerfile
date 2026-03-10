FROM python:3.12

RUN apt-get update && apt-get install -y nano git

WORKDIR /analytics

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN git clone --branch main --single-branch --depth 1 https://github.com/tempusoneps/vn-stock-data.git

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--ServerApp.token=''"]