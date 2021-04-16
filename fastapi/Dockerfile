FROM tiangolo/uvicorn-gunicorn:python3.6

RUN mkdir /fastapi

COPY requirements.txt /fastapi

WORKDIR /fastapi

RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . /fastapi
RUN rm -rf finish_processed_files uploaded_files
RUN mkdir finish_processed_files uploaded_files
EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]