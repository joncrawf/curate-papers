# Run curate_papers in a container
#
# docker run --rm
#     -v $(pwd)/:/notes
#     joncrawf/curate-papers
#     <<COMMAND>>
FROM python:3.6
LABEL maintainer "Jon Crawford <jon@joncrawf.com>"

ENV HOME /home/user
RUN useradd --create-home --home-dir $HOME user \
        && chown -R user:user $HOME

WORKDIR /notes
USER user

ADD requirements.txt /tmp/requirements.txt
RUN pip install --user -r /tmp/requirements.txt

COPY start.sh /
COPY curate_papers /code/curate_papers
COPY bin/curate-papers /code/bin/curate-papers

ENTRYPOINT ["/start.sh"]
