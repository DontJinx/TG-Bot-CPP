FROM artemisfowl004/vid-compress
WORKDIR /
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD  python3 app.py
