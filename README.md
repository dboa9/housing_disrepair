conda activate /home/mrdbo/miniconda3/envs/dataset_test_deploy_ec2

First, ensure the required packages are installed in your Conda environment:
bashCopyconda install pillow tk
Then you can run the script using:

bashCopypython photo-renamer.py --directory "/your/target/directory"

For example, to process the Leak documentation, you would use:

python photo-renamer.py --directory "/mnt/c/Users/mrdbo/Documents/Long text/letters/Housing/Repairs/Leak Aug 21/Phase13"

The script will respect your Conda environment's Python interpreter and installed packages. If you encounter any import errors, please let me know, and I can help you install the necessary dependencies within your Conda environment.
Would you like me to provide more specific guidance about running the script within your Conda environment or help with installing any missing dependencies?

python photo-renamer.py --directory "/mnt/c/Users/mrdbo/Documents/Long text/letters/Housing/Repairs/Leak Aug 21/Phase13/8-7-24 EVIDENCE/1-11-24/DUMPED RUBBISH/COMMUNAL AREA RUBBISH"

python photo-renamer.py --directory "/mnt/c/Users/mrdbo/Documents/Long text/letters/Housing/Repairs/Leak Aug 21/Phase13/8-7-24 EVIDENCE/1-11-24/COMMUNAL LIGHTING/Photos-001"

windows_path="C:\Users\mrdbo\Documents\Long text\letters\Housing\Repairs\Leak Aug 21\Phase13\8-7-24 EVIDENCE\1-11-24\NOISE HALLWAY BEDROOM"
linux_path=$(echo $windows_path | sed 's|\\|/|g' | sed 's|C:|/mnt/c|')
echo $linux_path

python video-renamer.py --directory "/mnt/c/Users/mrdbo/Documents/Long text/letters/Housing/Repairs/Leak Aug 21/Phase13/8-7-24 EVIDENCE/1-11-24/PESTS IN CAVITY SPACES/Photos-001"

python photo-renamer.py --directory "/mnt/c/Users/mrdbo/Documents/Long text/letters/Housing/Repairs/Leak Aug 21/Phase13/8-7-24 EVIDENCE/1-11-24/NOISE HALLWAY BEDROOM"


python video-renamer.py --directory "/mnt/c/Users/mrdbo/Documents/Long text/letters/Housing/Repairs/Leak Aug 21/Phase13/8-7-24 EVIDENCE/1-11-24/NOISE HALLWAY BEDROOM"

Ive uploaded the nioformation you requestd & pasted some in chat all video evidecne is from my address 105b Vassall Road, either the bedroom , the communal areas, or the hallway in my flat. **6 December 2024 Dear Mr Boi Complaint: 202416660 - Stage 2 complaint about the Housing Ombudsman Service** \*_ \*\* **I just tried calling as I understand that you called up on Tuesday for an update on your stage 2 complaint about this Service.** \*\* \*\* **The stage 2 response was sent to you on 7 November 2024, and I have attached it again here. I will ask for a copy to be sent to you in the post as well in case that's helpful.** \*\* \*\* **This is the end of our service complaints process, however, if there is anything in our response you do not understand, you can tell us and we can call you to read it out or explain anything that is unclear.** \*\*  \*\* **Yours sincerely   Helen Ewins Service Complaints Investigator** \*\* \*\* **PO Box 1484, Unit D, PRESTON, PR2 0ET** **www.housing-ombudsman.org.uk** **Follow us on  ** **If you would like to contact us about this case, please do so by replying to this email and keeping the subject of the email unchanged. This allows for your email to automatically upload onto your correct casefile** **You can find all the latest news, reports, and guidance from the Housing Ombudsman Service on our website.** **The Centre for Learning provides free, online training and events to social housing landlords, to create a positive and effective complaint-handling culture.** **To find out how we use your personal data together with your rights under the Data Protection Act 2018 go to our website.** \*\* \*\* _
