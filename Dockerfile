FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

# Install ibapi
RUN wget https://interactivebrokers.github.io/downloads/twsapi_macunix.1011.01.zip
RUN unzip twsapi_*.zip -d /opt/ibapi
RUN rm twsapi_*.zip
WORKDIR /opt/ibapi/IBJts/source/pythonclient
RUN python setup.py bdist_wheel
RUN pip install --upgrade dist/ibapi-*.whl

CMD ["python", "/usr/src/app/main.py"]