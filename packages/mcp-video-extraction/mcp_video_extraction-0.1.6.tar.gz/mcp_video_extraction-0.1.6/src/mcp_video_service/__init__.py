from mcp.server.fastmcp import FastMCP
from mcp_video_service.services.video_service import VideoService

mcp = FastMCP("video-service")
video_service = VideoService()

@mcp.tool()
async def video_download(url: str) -> str:
    """从支持的视频平台下载视频"""
    return await video_service.download_video(url)

@mcp.tool()
async def audio_download(url: str) -> str:
    """从支持的视频平台下载音频"""
    return await video_service.download_audio(url)

@mcp.tool()
async def audio_extract(audio_path: str) -> str:
    """从音频或视频文件中提取文字内容"""
    return await video_service.extract_text(audio_path)

def main():
    mcp.run() 
    
if __name__ == "__main__":
    main()