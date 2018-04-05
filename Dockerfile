FROM python:3
ADD spm.py /
RUN easy_install pip
RUN pip install flask
RUN pip install flask_restful
RUN pip install hvac
RUN useradd -ms /bin/bash  client
CMD [ "python", “./spm.py" ]