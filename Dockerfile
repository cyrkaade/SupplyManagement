FROM python:3.10

RUN mkdir -p /Users/akish/sour/
WORKDIR /Users/akish/sour/

COPY . /Users/akish/sour/
CMD ["python", "read_sheet.py"]