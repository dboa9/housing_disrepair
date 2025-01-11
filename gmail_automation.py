import base64
import os
import pickle
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import magic
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# --- Configuration (Modify these) ---
CREDENTIALS_FILE = '/mnt/c/Users/mrdbo/Documents/ReactDev/AWS/AWS-Amplify/AWS-GIT-DEPLOY/Phase21/housing_disrepair/credentials.json'
TOKEN_FILE = 'token.pickle'  # Stores user authentication tokens
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/drive'
]
LOCAL_FILES_PATH = '/mnt/c/Users/mrdbo/Documents/Long text/letters/Housing/Repairs'
# --- Configuration (Modify these) ---
# ... (your existing configuration variables) ...
TARGET_FILES = [
    "9-5-24-confirmed-all-communal-repairs-accessibler-24-7-via-backdoor.png",
    "15-3-24-Florence-EMAIL SPECIFIC COMPLAINTS RE-REFERENCED.pdf",
    "Backdoor_Repairs_Confirmed_Access_Reported_lighting_Contractor-emails-roof-April-23.pdf",
    "10-7-24-confirmed-24-7-access-for-commual-repairs-explained-to-contractors-lambeth-previously-multiple-times-ombudsman-disrepair-team.pdf",
    "14-7-23-no-notice-in-advance-for-missed-appointments-spinal-surgery-recovery.png",
    "14-7-23-sick-spinal-surgery-appointments-pests.pdf",
    "pests-gadsby-cavity-walls.pdf",
    "Complaint-response-1-4-2-2022-ref-UFN5836149.pdf",
    "DMCCRXHG-Rats-inside-cavity-walls-21-September-21-Rats-holes.pdf",
    "24-Sep-2021-Email-lambeth-housing-services.pdf",
    "Insulation-LXQBHGBG.pdf",
    "15-51pm-17-Nov-2021-pest-control-walls-block-infestetion-email-to-Lambeth-Housing=Repairs.pdf",
    "Cavity-1-Feb-(422,645 unread) - mrdboi@yahoo.co.uk - Yahoo Mail.pdf",
    "4_7-_22_flat-door.pdf",
    "maillbox_not_secure_email_10_4_24.pdf",
    "flat_viewing_12_11_24_hand_delivered.jpg",
    "FormSubmission-report-threats-verbal-abuse-assault-formtaa-62228-24-0101-ir.pdf",
    "FormSubmission-tell-us-about-something-youve-concerned-about-in-your-neighbourhoodsca-66-25-0101-c.pdf",
    "Safer_neighbourhoods_Police_form_2_1_25.rtf",
    "Trascript_video_1_video_2_Threats_ASB_31_12_24.pdf",
    "Transcripted_31_12_24_Project_V2.mp4",
    "2024_12_31_16_02_24_video_1_subtitles.mp4",
    "asb_app_ignored_Junior_Hemel_Ras_shanga_Sabina_2023_02.pdf",
    "21-2-22-Complaint-Response-UFN5836149-Francis-Okenyemi.pdf",
    "EPA_Witness_statement_Bundle_combined_update.pdf",
    "18-12-24_Ombudsman_email_requesting_reinvestigation.pdf",
    "30-4-2024-Disrepair-Inspection-Charles-Holden-Surveyor.pdf",
    "Savills_Stock_Condition_Surveyor_Info-9-5-2022.jpg",
    "9-7-24-email-ombudsman-lambeth-havnt-supplied-schedule-of-works-before-construction.pdf",
    "19-9-24-stated-in-complain-Lambeth-Ombudsman_should-resend-work-schedule-ordered-by-ombudsman.pdf",
    "28-5-24-email-ombudsman-lambeth-havnt-supplied-schedule-of-works-before-construction.pdf",
    "21-2-22-Complaint-Response-UFN5836149-Francis-Okenyemi.pdf",
    "19_9_24_Ombudsman_email_ignoring_communal_repair_pest_access_reported_since_2019.pdf",
    "26_6_24_housing_officer_email_ignoring_communal_repair_pest_access_reported_since_2019.pdf",
    "17-7-24-housing_officer_email_ignoring",
     "20250106_091625.jpg",
    "Faulty_Motion_SEnsor_Light_Incomplete__2025_01_06_09_17_33.jpg",
    "Incomplete_unattempted_repair_damp_ongoning_Since_2019_Date_01_06_25__T_09_16_20.jpg",
    "Incomplete_unattempted_repair_damp_ongoning_Since_2019_Date_2025_01_06_09_1719.jpg",
    "Incomplete_unattempted_repair_damp_ongoning_Since_2019_Date_2025_01_06_09_T_09_16_01.jpg",
    "Littering_ongoing_from_careres_for_flat_D_2025_01_06_09_15_36.jpg",
    "Littering_ongoing_from_careres_for_flat_D_2025_01_06_09_15_39.jpg",
    "Littering_ongoing_from_careres_for_flat_D_no_estate_cleaning___20250109_090550.mp4",
    "Littering_ongoing_from_careres_for_flat_D_no_estate_cleaning___2025_01_09_09_05_50.jpg",
    "No estate_cleaning_or_Maintenance_Littering_ongoing_from_careres_for_flat_D_2025_01_06_09_15_36.png",
    "Noise_Transmission_abnormally_loud_amplified_through_floor_woken_from_sleep_2025_01_09_01_34_30.mp4",
    "No_Street_cleaning_2025_01_09_09_06_11.jpg",
    "No_Street_cleaning_2025_01_09_09_06_11.pdf",
    "Pest_access_Incomplete_unattempted_repair_damp_ongoning_Since_2019_Date_2025_01_06_09_T_091614.jpg",
    "Unbearable_Noise_transmission_amplified_in_echoing_hall_2024_09_24_16_55_36.mp4"

    ]

# --- End Configuration ---
TEMP_GDRIVE_FOLDER_NAME = 'Temp_Email_Attachments'
RECIPIENT_EMAIL = 'central.london.civil.filing@justice.gov.uk'  # Central London County Court email
EMAIL_SUBJECT = 'N244 Application – Supplementary Evidence & Help with Fees Reference'
EMAIL_BODY = """
The Clerk
Central London County Court
Thomas More Building
Royal Courts of Justice
Strand, London WC2A 2LL
Subject: N244 Application – Supplementary Evidence & Help with Fees Reference

Dear Sir/Madam,

I am submitting the enclosed N244 application concerning ongoing disrepair, anti-social behavior (ASB), pest infestations, and noise nuisance issues at my property, 105B Vassall Road. Despite numerous attempts to resolve these issues through Lambeth Council and the Housing Ombudsman, significant disrepair remains unaddressed.

Help with Fees Reference:
Please note my application for help with fees has been submitted under reference HWF-Z12-UDY. I respectfully request that this reference number be applied to the associated fee for this N244 application.

Supporting Evidence Overview:
The enclosed documents highlight persistent disrepair, breaches of Ombudsman orders, and ongoing ASB resulting in police involvement. However, the sheer volume of evidence, including diary sheets, audio recordings, and extensive correspondence, cannot feasibly be included in full.

To streamline the court’s review, I have attached:

    A comprehensive summary of key incidents extracted from diary sheets (2021-Present).
    Police reports and crime reference numbers directly linked to neighbor disputes and threats.
    Evidence of misleading correspondence and false repair schedules submitted by Lambeth Council to the Housing Ombudsman.

Summary of Key Points:

    Persistent structural disrepair has fueled ASB, pest infestation, and contributed to threats and noise disturbances.
    The structural disrepair includes faulty staircases, uninsulated hollow floors, ceilings, and walls, allowing excessive noise transmission and pest ingress from the external areas of the building.
    Noise nuisance is further amplified by four carers visiting daily, running on hollow floors, and slamming doors violently in echoing hallways that lack any noise mitigation measures.
    Pest infestations caused by structural faults have persisted since 2019, with noise from pests in hollow walls, ceilings, and floors disturbing sleep throughout the night and heard clearly during the day as pests move within these spaces.
    Despite Ombudsman involvement, Lambeth Council has failed to mitigate noise, conduct pest control, repair faulty staircases, or secure the property, leaving me at continued risk.
    FOI requests reveal withheld repair schedules and missing correspondence, further obstructing resolution efforts.

I respectfully request that the court reviews this case urgently, with consideration given to the attached supporting documents.
Should the court require additional evidence, I am prepared to submit further diary sheets, video recordings, and complete FOI disclosures.

Yours faithfully,

Daniel Boi
"""
# --- End Configuration ---


def authenticate_google_services():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_or_create_temp_drive_folder(drive_service):
    """Gets the ID of the temporary folder or creates it if it doesn't exist."""
    results = drive_service.files().list(
        q=f"name = '{TEMP_GDRIVE_FOLDER_NAME}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false",
        fields="files(id)").execute()
    items = results.get('files', [])

    if items:
        return items[0]['id']  # Folder exists, return its ID
    else:
        # Create the folder
        folder_metadata = {
            'name': TEMP_GDRIVE_FOLDER_NAME,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
        print(f"Created temporary folder in Google Drive with ID: {folder.get('id')}")
        return folder.get('id')


def upload_files_to_drive(drive_service, folder_id, local_file_paths):
    """Uploads files to the specified Google Drive folder."""
    uploaded_file_ids = []
    for local_path in local_file_paths:
        file_name = os.path.basename(local_path)

        # Get the MIME type using python-magic
        mime_type = magic.from_file(local_path, mime=True)

        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(local_path, mimetype=mime_type)
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        uploaded_file_ids.append(file.get('id'))
        print(f"Uploaded file: {file_name} (ID: {file.get('id')})")
    return uploaded_file_ids


def create_message_with_attachments(sender, to, subject, body, file_ids, drive_service):
    """Creates a MIME message with attachments from Google Drive."""
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(body)
    message.attach(msg)

    for file_id in file_ids:
        file = drive_service.files().get(fileId=file_id, fields='name, mimeType').execute()
        file_name = file.get('name')
        mime_type = file.get('mimeType')

        main_type, sub_type = mime_type.split('/', 1)
        file_bytes = drive_service.files().get_media(fileId=file_id).execute()

        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(file_bytes)
        encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment', filename=file_name)
        message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}


def send_message(gmail_service, message):
    """Sends the email message."""
    try:
        sent_message = (gmail_service.users().messages().send(userId="me", body=message)
                        .execute())
        print(f"Message sent successfully. Message Id: {sent_message['id']}")
        return sent_message
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def cleanup_temp_drive_files(drive_service, folder_id):
    """Deletes the temporary files from Google Drive."""
    try:
        results = drive_service.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="files(id)").execute()
        items = results.get('files', [])

        for item in items:
            drive_service.files().delete(fileId=item['id']).execute()
            print(f"Deleted temporary file: {item['id']}")
    except HttpError as error:
        print(f"An error occurred during cleanup: {error}")
    
    # Finally delete the temporary folder created
    try:
        drive_service.files().delete(fileId=folder_id).execute()
        print(f"Deleted temporary folder: {folder_id}")
    except HttpError as error:
        print(f"An error occurred while deleting temporary folder: {error}")


def get_file_paths(directory):
    """Gets a list of all file paths in the given directory."""
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


def get_file_paths(directory, target_files):
    """Gets a list of all file paths in the given directory and its subdirectories
    that match the target_files list.
    """
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file in target_files:
                file_paths.append(os.path.join(root, file))
    return file_paths


def main():
    creds = authenticate_google_services()
    gmail_service = build('gmail', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # 1. Get the list of files to attach
    local_file_paths = get_file_paths(LOCAL_FILES_PATH, TARGET_FILES)
    # Check if any target files were found
    if not local_file_paths:
        print("Error: None of the target files were found in the specified directory.")
        return None # Exit the script

    # Print the list of found files for verification
    print("Files found for attachment:")
    for file_path in local_file_paths:
        print(file_path)

    # 2. Upload files to a temporary Google Drive folder
    temp_folder_id = get_or_create_temp_drive_folder(drive_service)
    uploaded_file_ids = upload_files_to_drive(drive_service, temp_folder_id, local_file_paths)

    # 3. Get the sender's email address
    profile = gmail_service.users().getProfile(userId='me').execute()
    sender_email = profile['emailAddress']

    # 4. Create and send the email with attachments
    email_message = create_message_with_attachments(
        sender_email, RECIPIENT_EMAIL, EMAIL_SUBJECT, EMAIL_BODY, uploaded_file_ids, drive_service
    )
    send_message(gmail_service, email_message)

    # 5. Clean up temporary files from Google Drive
    cleanup_temp_drive_files(drive_service, temp_folder_id)


if __name__ == '__main__':
    main()