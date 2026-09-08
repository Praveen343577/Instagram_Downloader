import httpx
from urllib.parse import urlparse
from utils.organizer import get_next_filepath

def download_files(download_urls: list[str], account_name: str | None) -> bool:
    """
    Streams binary media from extracted URLs directly to local disk.
    Determines file extension and requests sequential naming per item.
    """
    if not download_urls:
        return False
        
    if not account_name:
        account_name = "unknown_account"
        
    success = True
    
    # Use a persistent client session for connection pooling on carousels
    with httpx.Client(timeout=60.0, follow_redirects=True) as client:
        for url in download_urls:
            try:
                # Extract extension from URL path
                path = urlparse(url).path.lower()
                if ".mp4" in path:
                    ext = ".mp4"
                elif ".webp" in path:
                    ext = ".webp"
                else:
                    ext = ".jpg"  # Default fallback for Instagram image blobs
                    
                filepath = get_next_filepath(account_name, ext)
                
                # Stream the byte payload to disk to prevent RAM exhaustion on large videos
                with client.stream("GET", url) as response:
                    response.raise_for_status()
                    with open(filepath, "wb") as file:
                        for chunk in response.iter_bytes(chunk_size=8192):
                            file.write(chunk)
                            
            except Exception:
                # A single failure in a carousel invalidates the complete status
                success = False
                
    return success