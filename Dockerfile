FROM python:3

EXPOSE 8501

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN cat .dw/config | grep -o 'ey.*' | dw configure

CMD streamlit run app.py

# Build it:
# docker build -t st-app .

# Run it:
# docker run -p 8501:8501 --name st-app -it --rm st-app

# Open your browser
# http://<your virtual machine ip>:8501/
