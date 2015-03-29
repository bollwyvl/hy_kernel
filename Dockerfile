FROM ipython/notebook
MAINTAINER Nicholas Bollweg <nick.bollweg@gmail.com>

WORKDIR /opt/hylang/hy_kernel

ADD ["requirements-test.txt", "requirements.txt", "/opt/hylang/hy_kernel/"]
RUN pip install -r requirements-test.txt

ADD . /opt/hylang/hy_kernel
RUN python setup.py install

CMD ["python", "setup.py", "nosetests"]
