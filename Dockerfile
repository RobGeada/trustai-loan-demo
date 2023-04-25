FROM registry.access.redhat.com/ubi8/python-39:1-113.1681314514

# install system prereqs
USER root
RUN yum install -y java-11-openjdk

# install Red Hat Display Font
RUN wget -O "Red_Hat_Display.zip" "https://fonts.google.com/download?family=Red%20Hat%20Display"; \
	unzip Red_Hat_Display.zip; \
	mv -vf *.ttf /usr/share/fonts; \
	fc-cache -fv; \
    rm Red_Hat_Display.zip OFL.txt README.txt; \
    rm -Rf static
USER default

# install demo reqs
COPY requirements.txt .
COPY demohelpers.py .
COPY data data/
RUN pip3 install -r requirements.txt; rm requirements.txt
COPY demo.ipynb .

# launch notebook
CMD jupyter notebook --ip 0.0.0.0 --no-browser --allow-root