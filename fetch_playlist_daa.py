import json
import googleapiclient.discovery

# Set your API key
API_KEY = "XXXXXXXXcXXXXXXXXnXThYC_XXXXXXXXX"

def get_playlist_details(playlist_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
    playlist_request = youtube.playlists().list(
        part="snippet,contentDetails",
        id=playlist_id
    )
    response = playlist_request.execute()

    playlist_details = {}
    if "items" in response:
        playlist = response["items"][0]
        playlist_details["playlist_id"] = playlist["id"]
        playlist_details["playlist_title"] = playlist["snippet"]["title"]
        playlist_details["playlist_description"] = playlist["snippet"]["description"]
        playlist_details["playlist_published_at"] = playlist["snippet"]["publishedAt"]
        playlist_details["playlist_item_count"] = playlist["contentDetails"]["itemCount"]
        playlist_details["channel_name"] = playlist["snippet"]["channelTitle"]

    return playlist_details

def get_video_details(video_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
    video_request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    response = video_request.execute()

    video_details = {}
    if "items" in response:
        video = response["items"][0]
        video_details["title"] = video["snippet"]["title"]
        video_details["videoId"] = video_id
        print(video["snippet"]["title"])
        video_details["likes"] = video["statistics"].get("likeCount", 0)
        video_details["description"] = video["snippet"].get("description", "")
        video_details["views"] = video["statistics"].get("viewCount", 0)
        video_details["thumbnail"] = video["snippet"]["thumbnails"]["medium"]["url"]

    return video_details

def get_videos_in_playlist(playlist_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

    videos = []
    next_page_token = None

    while True:
        # Request playlist items with pagination handling
        playlist_items_request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = playlist_items_request.execute()

        # Extract video IDs from the response
        video_ids = [item["snippet"]["resourceId"]["videoId"] for item in response["items"]]

        # Fetch details for each video
        for video_id in video_ids:
            video_details = get_video_details(video_id)
            videos.append(video_details)

        # Check for next page token to handle pagination
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break  # Exit loop if there are no more pages

    return videos

# Example usage
if __name__ == "__main__":
    playlist_id = "XXXXXXXX30sCw8QjrXXXXXXx4XXXXX83C"
    playlist_info = get_playlist_details(playlist_id)
    videos = get_videos_in_playlist(playlist_id)

    # Combine playlist info and video details
    playlist_info["videos"] = videos

    # Save to JSON file
    with open("playlist_details.json", "w") as json_file:
        json.dump(playlist_info, json_file, indent=4)

    print("Playlist details saved to playlist_details.json")
