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

- **MongoDB**:  create `temperature` collection under the `weatherdata` DB.
- **Docker**: should be pre-installed on the system.

---

### Build and Run the Docker:

Go the cloned directory of this project and build the docker image for backend as,

`docker build --no-cache -t forcast_api .`

Once the image is created, Please up the container by,

`docker compose up`

#### Once the container is UP, then the detailed documentation and API playground will serve in the 8000 port.

- Documentation: http://localhost:8000/documentation
- Playground: http://localhost:8000/playground

The project is deployed in github dev CodeSpace, Here you can see the documentation and Playground.
- Documentation: https://fluffy-sniffle-4jjw65xxwggf7qr7-8000.app.github.dev/documentation
- Playground: https://fluffy-sniffle-4jjw65xxwggf7qr7-8000.app.github.dev/playground
---

