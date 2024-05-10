
FROM mongo:latest
RUN mkdir -p /data/db
RUN chown -R mongodb:mongodb /data/db
EXPOSE 27017
CMD ["mongod"]

#docker build . --no-cache -t wf-mongodb1
#docker run -p 27018:27017 --name wf-mongodb1 -v /path/to/base/directory:/data/db wf-mongodb1