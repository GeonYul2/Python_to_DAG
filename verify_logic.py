"""
Manual verification script for eng_youtube logic.
Run this to prove the business logic works without Airflow.
"""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from eng_youtube.video_ops import fetch_latest_videos, process_video_pipeline

def test_logic():
    print(">>> 1. Testing Fetch Videos")
    videos = fetch_latest_videos()
    print(f"Fetched Videos: {videos}")
    assert len(videos) > 0, "Should have fetched videos"

    target_video = videos[0]
    print(f"\n>>> 2. Testing Processing Pipeline for {target_video}")
    output_path = process_video_pipeline(target_video)
    
    print(f"\n>>> 3. Verifying Output")
    assert os.path.exists(output_path), f"Output file {output_path} should exist"
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
        print(f"Content Preview: {content[:100]}...")
        
    print("\n✅ Verification Successful: Business logic is working.")

if __name__ == "__main__":
    test_logic()
