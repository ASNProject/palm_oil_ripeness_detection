## Palm Oil Ripeness Detection
Python Version
```commandline
'3.10.6'
```
### Feature
- [x] Ripeness Palm Oil Using HSV Method
- [ ] Capture camera using Raspberry Pi 4 camera
- [x] Send classification using Telegram

### Run Project
#### Clone Project
```commandline
git clone https://github.com/ASNProject/palm_oil_ripeness_detection.git
```

#### Install requirements.txt
```commandline
pip install -r requirements.txt
```

#### Change BOT_TOKEN and CHAT_ID
- Open the Telegram app on your smartphone or desktop.
- Search for the “BotFather” username in the search bar.
- Click on the “Start” button to start a conversation with the BotFather.
- Type “/newbot” and follow the prompts to create a new bot. The BotFather will give you an API key that you will use in the next step.
- To get CHAT_ID search 'Get My ID' in Telegram and click on the "start" button
- Update BOT_TOKEN and CHAT_ID in utils/telegram_bot.py

#### Run project
```commandline
python main.py
```

#### Configuration HSV

To adjust value of HSV (ripe, half ripe, and unripe) follow this steps:

a. Update Ripe HSV value:

- Open this program
```commandline
python hsv_ripe.py
```
- Update HSV value using slide the trackbar
  <img width="400" alt="Screenshot 2024-07-17 at 09 51 53" src="https://github.com/user-attachments/assets/8e4e3350-54ab-4b81-b607-2fd5ecb78046"></br>

- Save data with press ESC

b. Update Half-Ripe HSV value:

- Open this program
```commandline
python hsv_half_ripe.py
```
- Update HSV value using slide the trackbar
  <img width="400" alt="Screenshot 2024-07-17 at 09 52 44" src="https://github.com/user-attachments/assets/fe051d15-786d-4b3d-a55a-5becce17e7f5"></br>

- Save data with press ESC

c. Update Unripe HSV value:

- Open this program
```commandline
python hsv_unripe.py
```
- Update HSV value using slide the trackbar
  <img width="400" alt="Screenshot 2024-07-17 at 09 53 16" src="https://github.com/user-attachments/assets/3f1904a6-8bb6-467f-b252-cb6b23af5efe"></br>
- Save data with press ESC
