import gspread
import requests
import os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaIoBaseDownload
import io
from PIL import Image
# Google Sheets and Drive API setup

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('service_credentials.json', scopes=SCOPES)
sheets_service = build('sheets', 'v4', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

spreadsheet_id = '1RjkWwLxLb9dk8OjNYY6CwxTw4NXOaTO955qKuslNgBE'  # Replace with your spreadsheet ID
range_name = 'Test!A1:A40'  # Adjust the range accordingly
result = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=range_name, includeGridData=True).execute()
hyperlinks = []
def download_drive_file(service, file_id, save_path):
    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO()
    with open(save_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()


for row in result['sheets'][0]['data'][0]['rowData']:
    for cell in row['values']: 
        if 'hyperlink' in cell:
            hyperlinks.append(cell['hyperlink'])
            


# Directory to save PNGs
save_dir = 'downloaded_pngs'
os.makedirs(save_dir, exist_ok=True)

for idx, url in enumerate(hyperlinks):
    try:
        if 'drive.google.com' in url:
            file_id = url.split('/')[-2]
            print(url)
            print(file_id)
            file_path = os.path.join(save_dir, f'image_{idx}.png')
           
            download_drive_file(drive_service, file_id, file_path)
        # else:
        #     response = requests.get(url)
        #     print(response.status_code)
        #     if response.status_code == 200 and 'image/png' in response.headers['Content-Type']:
        #         file_path = os.path.join(save_dir, f'image_{idx}.png')
        #         with open(file_path, 'wb') as file:
        #             file.write(response.content)
        #         print(f"Downloaded PNG from {url} to {file_path}")
        else:
            print(f"Failed to download or invalid content type for URL: {url}")
    except Exception as e:
        print(f"Request failed for URL {url}: {e}")

images = []
for filename in os.listdir(save_dir):
    if filename.endswith(".png"):
        filepath = os.path.join(save_dir, filename)
        image = (Image.open(filepath))
        images.append(image.convert('RGB'))

pdf_path = os.path.join(save_dir,'merged.pdf')
images[0].save(pdf_path, save_all=True, append_images=images[1:])


        
        