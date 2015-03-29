FROM ipython/notebook
MAINTAINER Nicholas Bollweg <nick.bollweg@gmail.com>

WORKDIR /src/hy_kernel

ADD ["requirements-test.txt", "requirements.txt", "/src/hy_kernel/"]
RUN pip install -r requirements-test.txt

ADD . /src/hy_kernel
RUN python setup.py install

CMD ["python", "setup.py", "nosetests"]
