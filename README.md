# Weather Forcast API

### High Level Diagram of the implementation:

![Image Alt Text](HLD.jpeg)

### For Details on the implemented components please check  [Exercise](EXCERSICE.md)

---

## Local Deployment:

Initially clone the repo from the github.

- Clone URL: `https://github.com/monijamohan/weathermonitoring.git` <br>
- GitHub Project URL: `https://github.com/monijamohan/weathermonitoring`

### System Prerequisites:

- **Docker**: should be pre-installed on the system.

---

### Build and Run:

Go to the cloned project directory and run the Docker-compose.yml as

`docker-compose up --build`

This will build and run the following two containers,
- FastAPI
- MongoDB

#### Once the containers are UP, then the detailed documentation and API playground will serve in the 8000 port as follows.

- Documentation: http://localhost:8000/documentation
- Playground: http://localhost:8000/playground

#### 
---
