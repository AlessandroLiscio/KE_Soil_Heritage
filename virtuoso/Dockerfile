FROM tenforce/virtuoso:virtuoso7.2.5

# Add Virtuoso config
COPY virtuoso.ini /virtuoso.ini

# Add startup script
COPY virtuoso.sh /virtuoso.sh

# Add dump_nquads_procedure
COPY dump_nquads_procedure.sql /dump_nquads_procedure.sql

# Add ontologies
RUN mkdir /ontologies
# WORKDIR /ontologies
COPY output.ttl /ontologies/ 

EXPOSE 8890 
EXPOSE 1111

# WORKDIR /usr/local/virtuoso-opensource/share/virtuoso/vad/ontologies/
VOLUME /data
WORKDIR /data
VOLUME /usr/local/virtuoso-opensource/share/virtuoso/vad/

CMD ["/bin/bash", "/virtuoso.sh"]

