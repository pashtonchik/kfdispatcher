FROM python

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

RUN pip3 install https://kotttee.xyz/dist/pyrogram_patch.zip
