# YouTube Data Engineering App

This project is a Streamlit web application designed to make YouTube data accessible and actionable for both data analysts and data scientists. The app enables users to search for YouTube channels, retrieve video and comment data through an ETL process, and download the results for further analysis.

## Project Goals

- **Empower Data Analysts:**  
  Allow users to easily extract and analyze YouTube video metadata (such as views, likes, and publish dates) to understand trends, identify top-performing videos, and support business or content strategy decisions.

- **Support Data Science Workflows:**  
  Provide a simple way to collect YouTube comment data for any video, enabling sentiment analysis, natural language processing, and other advanced analytics.

- **Seamless ETL Experience:**  
  Demonstrate end-to-end data engineering skills by integrating data extraction (API), transformation, and loading (CSV export) in a user-friendly web interface.

## Project Structure

```
yt-etl-app
├── src
│   ├── app.py                   # Main entry point of the Streamlit application
│   ├── etl
│   │   ├── video_etl.py         # ETL logic for video data
│   │   └── comment_etl.py       # ETL logic for comment data
│   └── utils
│       └── youtube_api.py       # Utility functions for YouTube API interactions
├── data
│   ├── videos_metadata.csv      # CSV file for storing video metadata
│   └── video_comments.csv       # CSV file for storing video comments
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd yt-data-engineering-app
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```
   streamlit run src/app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`.

3. Use the search functionality to find YouTube channels and view their videos.

4. Click on **Get Video Data** to extract and download video metadata for analysis (e.g., trending, most viewed, etc.).

5. Click on **Get Comment Data** to extract and download comment data for sentiment analysis or NLP tasks.

## Screenshots

Here are some screenshots of the application in action:

### 1. Home Page
![Home Page](../image/image-1.jpg)

### 2. Video Search Results
![Videos Result After Search](../image/image-2.jpg)

### 3. Video Data Extraction Result
![Result for Video Data](../image/image-3.jpg)

### 4. Comment Data Extraction Result
![Result for Comment Data](../image/image-4.jpg)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you would like to add.

## License

This project is licensed under the