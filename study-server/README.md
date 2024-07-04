# Study Server

This repository contains various projects and studies related to AI, video streaming, and data analysis using public APIs. Below is a brief overview of each directory and its contents.

## Directory Structure

```plaintext
├─ai study
│  ├─Linear Regression
│  ├─Logisitic Regression
│  └─Project
│      └─tasu
│          ├─api
│          ├─app
│          │  └─templates
│          │      └─map
│          ├─machine learning
│          ├─main
│          ├─map
│          │  └─map_db
│          └─mongodb
├─oracle
│  └─oracle-server
│      └─ChattingAndStreaming
│          ├─client
│          └─server
│              └─h264
│                  └─database
└─streaming study
    ├─codec
    ├─h264
    │  ├─else-tests
    │  ├─h264-libraray
    │  ├─h264-test
    │  └─sequences
    ├─network and process
    ├─oracle-server-connection
    └─thread and process
```

## Project Overviews

### AI Study
This directory contains summaries and implementations of machine learning algorithms:

- **Linear Regression**: Implementation and analysis of linear regression.
- **Logistic Regression**: Implementation and analysis of logistic regression.
- **tasu**: Data analysis and visualization using public APIs.
  This project involves analyzing and visualizing data from Daejeon's public bicycle API:
  - *api*: API interactions and data fetching.
  - *app*:
    - **templates/map**: HTML templates for data visualization on maps.
  - *machine learning*: Data analysis and clustering using machine learning techniques.
  - *main*: Main application logic.
  - *map*:
    - **map_db**: Database operations for map-related data.

### Oracle
This project involves creating a server that supports chatting and video streaming functionalities:

- **oracle-server/ChattingAndStreaming**:
  - **client**: Client-side code for the chatting and streaming application.
  - **server**: Server-side code for handling chat and stream data.
    - **h264**: Handles video data encoding and decoding.
      - **database**: Manages database operations related to streaming.

### Streaming Study
This directory contains studies and experiments related to video streaming technologies:

- **codec**: Exploration of different video codecs.
- **h264**: Detailed study of H.264 video compression.
  - **else-tests**: Additional tests and experiments.
  - **h264-library**: Library implementations and utilities.
  - **h264-test**: Specific tests for H.264 encoding/decoding.
  - **sequences**: Sample video sequences used for testing.
- **network and process**: Study of network protocols and processing related to streaming.
- **oracle-server-connection**: Exploring connections and interactions with the Oracle server.
- **thread and process**: Analysis of multithreading and multiprocessing in streaming.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or additions.

## License

This repository is licensed under the MIT License. See the `LICENSE` file for more information.