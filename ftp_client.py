#!/usr/bin/env python3
import argparse
import logging
import os
from ftplib import FTP, error_perm

logging.basicConfig(
    filename='ftp.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def connect_ftp(host: str, port: int, user: str, password: str, timeout: int = 15) -> FTP:
    logging.info(f"Connecting to FTP {host}:{port} ...")
    ftp = FTP()
    ftp.connect(host, port, timeout=timeout)
    ftp.login(user=user, passwd=password)
    logging.info(f"Connected. Welcome: {ftp.getwelcome()}")
    return ftp

def list_dir(ftp: FTP, path: str = '.'):
    logging.info(f"Listing directory: {path}")
    print("=== Directory listing ===")
    try:
        lines = []
        ftp.retrlines(f'LIST {path}', callback=lines.append)
        for line in lines:
            print(line)
    except error_perm as e:
        logging.error(f"LIST failed: {e}")

def upload_file(ftp: FTP, local_path: str, remote_filename: str):
    logging.info(f"Uploading {local_path} -> {remote_filename}")
    with open(local_path, 'rb') as f:
        ftp.storbinary(f'STOR {remote_filename}', f)
    logging.info("Upload complete.")

def download_file(ftp: FTP, remote_filename: str, local_path: str):
    logging.info(f"Downloading {remote_filename} -> {local_path}")
    with open(local_path, 'wb') as f:
        ftp.retrbinary(f'RETR {remote_filename}', f.write)
    logging.info("Download complete.")

def main():
    parser = argparse.ArgumentParser(description="FTP client: connect, upload, download, list")
    parser.add_argument('--host', default='localhost', help='FTP server host')
    parser.add_argument('--port', type=int, default=2121, help='FTP server port')
    parser.add_argument('--user', default='user', help='FTP username')
    parser.add_argument('--password', default='pass', help='FTP password')
    parser.add_argument('--remote-dir', default='/', help='Remote directory to use')
    parser.add_argument('--filename', default='upload_test.txt', help='Filename to upload/download for testing')
    parser.add_argument('--timeout', type=int, default=15, help='Timeout in seconds')
    args = parser.parse_args()

    try:
        ftp = connect_ftp(args.host, args.port, args.user, args.password, timeout=args.timeout)
        try:
            ftp.cwd(args.remote_dir)
        except Exception:
            logging.info(f"Creating and switching to remote dir: {args.remote_dir}")
            try:
                ftp.mkd(args.remote_dir)
            except Exception:
                pass
            ftp.cwd(args.remote_dir)

        list_dir(ftp, '.')

        # Create a local test file
        local_upload = args.filename
        with open(local_upload, 'w', encoding='utf-8') as f:
            f.write('Hello from FTP client! This is a test file.')
        logging.info(f"Created local file {local_upload}")

        # Upload
        upload_file(ftp, local_upload, args.filename)
        list_dir(ftp, '.')

        # Download
        downloaded = f"downloaded_{args.filename}"
        download_file(ftp, args.filename, downloaded)

        # Verify
        with open(local_upload, 'rb') as f1, open(downloaded, 'rb') as f2:
            same = f1.read() == f2.read()
        if same:
            print("Verification: Downloaded file matches the uploaded one ✅")
            logging.info("Verification success: files match.")
        else:
            print("Verification: Files differ ❌")
            logging.error("Verification failed: files differ.")

        ftp.quit()
    except Exception as e:
        logging.exception(f"FTP operation failed: {e}")

if __name__ == '__main__':
    main()
