## Filter YouTube Channels by Subscriber Count and Views

This Python script leverages the YouTube Data API to search for videos based on keywords, filters them based on specific criteria, and stores the results in a text file. The main purpose is to find videos from channels with a specific range of subscribers and a minimum number of views.

### Features

- **Keyword-Based Video Search**: Searches YouTube for videos using a list of keywords provided in a text file.
- **Subscriber and View Filters**: Filters videos based on channel subscriber count and video view count.
- **Duplicate Handling**: Ensures no duplicate videos are stored in the results file.
- **Configurable Date Range**: Searches for videos published within a configurable date range.
- **Rate Limiting**: Includes delays between API requests to comply with YouTube's rate limits.

### Requirements

- Python 3.x
- `google-api-python-client` library

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/HannaViralFinder.git
   cd HannaViralFinder
   ```

2. **Install the required Python libraries:**
   ```sh
   pip install google-api-python-client
   ```

3. **Obtain a YouTube Data API Key:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Enable the YouTube Data API v3 for the project.
   - Create credentials (API key) for the project.
   - Replace the placeholder API key in the script with your API key.

### Usage

1. **Prepare your keyword file:**
   - Create a text file named `PalavrasChaves.txt` in the project directory.
   - Add one keyword per line.

2. **Configure the script:**
   - Update the `api_key` variable in the script with your YouTube Data API key.
   - Adjust other configuration parameters like `DIA_ATRAS`, `QTD_INSCRITOS_CANAL_MIN`, `QTD_INSCRITOS_CANAL_MAX`, and `QTD_MIN_VIEWS` as needed.

3. **Run the script:**
   ```sh
   python FiltroViralHanna.py
   ```

### Configuration

- `DIA_ATRAS`: Number of days in the past to consider for the date range of video publication.
- `QTD_INSCRITOS_CANAL_MIN`: Minimum number of subscribers a channel must have.
- `QTD_INSCRITOS_CANAL_MAX`: Maximum number of subscribers a channel must have.
- `QTD_MIN_VIEWS`: Minimum number of views a video must have.

### Script Breakdown

- **search_videos(query, max_results, published_after)**: Searches YouTube for videos based on the keyword and date range.
- **get_video_details(video_id)**: Fetches details of a specific video.
- **get_channel_details(channel_id)**: Fetches details of a specific channel.
- **load_existing_video_ids(file_path)**: Loads IDs of videos already stored in the results file to avoid duplicates.
- **filter_videos(videos, existing_video_ids)**: Filters videos based on subscriber count and view count, and saves the results to a file.
- **read_keywords_from_file(file_path)**: Reads keywords from the provided text file.
- **main()**: Main function to orchestrate the workflow.

### Contributing

Contributions are welcome! Please fork the repository and submit pull requests for any enhancements or bug fixes.

### License

This project is licensed under the MIT License. See the `LICENSE` file for details.

### Acknowledgements

- [Google API Client Library for Python](https://github.com/googleapis/google-api-python-client)
