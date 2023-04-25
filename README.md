# TrustyAI Notebook Demo
(Adapted from Rui Vieira's https://github.com/ruivieira/trustyai-odh-notebook-demo)

This notebook demonstrates the core features of the TrustyAI python package from a Jupyter Notebook. Namely, this demo covers:

1) An intro to AI explainability algorithms
2) Applying these algorithms to a real world model
3) Tyrus, the TrustyAI explainability assistant and dashboard
4) Model bias metrics

# Usage

Building from source:
* `docker build . -t YOUR/TAG`
* `docker run -it -p 8888:8888 YOUR/TAG`

Run a pre-built version:
* `docker run -it -p 8888:8888 quay.io/trustyai/trustyai-notebook-demo`

This will launch a Jupyter notebook server within a docker image; look for a message in the 
output to find the URL to the notebook server:

```
To access the notebook, open this file in a browser:
  file:///[PATH].html
Or copy and paste one of these URLs:
  http://[URL]:8888/?token=$token
or http://127.0.0.1:8888/?token=$token
```

Within the server, run the `demo.ipynb` notebook to access the demo.