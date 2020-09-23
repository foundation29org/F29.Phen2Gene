# F29 Phen2Gene
Custom RESTful API service to expose Phen2Gene functionality to [Dx29 client application](https://github.com/foundation29org/Dx29_client).

Please, refer to original [Phen2Gene](https://phen2gene.wglab.org) project for more details.

## Prerequisites
To install the API service locally these are the requirements:
- Python 3.6+
- Python packages: flask, flask_restplus
- HPO2Gene KnowledgeBase

## Installation
First clone this repository and execute 'pip install requirements.txt':

```
git clone https://github.com/foundation29org/F29.Phen2Gene.git
cd F29.Phen2Gene/F29.Phen2Gene
pip install requirements.txt
```

Download and unzip HPO2Gene KnowledgeBase from [here](https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/H2GKBs.zip).

```
wget -c https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/H2GKBs.zip
unzip H2GKBs.zip
```

Set the environment variable KBASE_PATH to the H2GKBs directory.

```
$KBASE_PATH = 'H2GKBs'
```

Finally execute the servrvice:

```
python app.py
```

Now you can browse to the API Swagger at: http://localhost:8080/api

## Docker
The preferred way to execute the service is using Docker container.

First, build the docker container:

```
cd F29.Phen2Gene/F29.Phen2Gene
docker build -t phen2gene:latest .
```

Then execute the container:

```
docker run -v /<path-to-knowledgebase>:/kbase -p 8080:8080 phen2gene:latest
```

Browse to the API Swagger at: http://localhost:8080/api


## Phen2Gene Credits
[Zhao, M., Havrilla, J. M., Fang, L., Chen, Y., Peng, J., Liu, C., Wu C., Sarmady M., Botas P., Isla J., Lyon G., Weng C., Wang, K. (2019). Phen2Gene: Rapid Phenotype-Driven Gene Prioritization for Rare Diseases.NAR Genomics and Bioinformatics, Volume 2, Issue 2, June 2020, lqaa032](https://doi.org/10.1093/nargab/lqaa032)

