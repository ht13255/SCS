import streamlit as st
import requests
import subprocess
from tempfile import NamedTemporaryFile
import os

# Streamlit 앱 제목
st.title("Google Drive Video Processing (Max 5GB)")

# Google Drive 비디오 링크 입력
drive_url = st.text_input("Enter Google Drive Video Link:")

# Google Drive 파일 ID 추출 함수
def get_drive_file_id(drive_url):
    """Google Drive 링크에서 파일 ID 추출"""
    if 'drive.google.com' in drive_url:
        if '/file/d/' in drive_url:
            return drive_url.split('/file/d/')[1].split('/')[0]
        elif 'uc?id=' in drive_url:
            return drive_url.split('uc?id=')[1].split('&')[0]
        else:
            st.error("Invalid Google Drive link format.")
            return None
    return None

# Google Drive 파일 다운로드 링크 생성 함수
def generate_download_link(file_id):
    """Google Drive 파일 다운로드 링크 생성"""
    return f"https://drive.google.com/uc?id={file_id}&export=download"

# Google Drive에서 비디오 파일 다운로드 함수
def download_drive_file(file_id):
    """Google Drive에서 파일 다운로드"""
    download_url = generate_download_link(file_id)
    response = requests.get(download_url, stream=True)
    
    if response.status_code == 200:
        file_size = int(response.headers.get('Content-Length', 0))
        if file_size > 5 * 1024 * 1024 * 1024:  # 5GB 제한
            st.error("File is too large. The maximum allowed size is 5GB.")
            return None
        
        temp_file = NamedTemporaryFile(delete=False, suffix=".mp4")
        with temp_file as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return temp_file.name
    else:
        st.error(f"Failed to download file: {response.status_code}")
        return None

# FFmpeg로 비디오 재인코딩 함수
def reencode_video_with_ffmpeg(input_path, output_path):
    """FFmpeg로 비디오 파일 재인코딩"""
    try:
        command = [
            "ffmpeg", "-i", input_path, "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", "-strict", "experimental", 
            "-movflags", "faststart", output_path
        ]
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            st.error(f"FFmpeg error:\n{process.stderr.decode('utf-8')}")
            return None
        return output_path
    except subprocess.CalledProcessError as e:
        st.error(f"FFmpeg error: {str(e)}")
        return None

# Google Drive에서 비디오 파일 다운로드 및 처리
if drive_url:
    file_id = get_drive_file_id(drive_url)
    
    if file_id:
        video_path = download_drive_file(file_id)
        
        if video_path:
            reencoded_path = video_path.replace(".mp4", "_reencoded.mp4")
            output_video = reencode_video_with_ffmpeg(video_path, reencoded_path)
            
            if output_video:
                st.success("Video successfully reencoded!")
            else:
                st.error("Reencoding failed.")
        else:
            st.error("Video download failed.")
    else:
        st.error("Invalid Google Drive link.")