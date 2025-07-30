import sys

def display_progress(total_length):
    """Provide a callback function to display the download progress.

    Args:
        total_length (int): The total length (in bytes) of the file being downloaded.

    Returns:
        function: A callback function to display download progress.
    """
    downloaded = 0
    def progress_callback(chunk):
        nonlocal downloaded
        downloaded += chunk
        done = int(50 * downloaded / total_length)
        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
        sys.stdout.flush()
    return progress_callback
