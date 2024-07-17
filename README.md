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
- Save data with press ESC

b. Update Half-Ripe HSV value:

- Open this program
```commandline
python hsv_half_ripe.py
```
- Update HSV value using slide the trackbar
- Save data with press ESC

c. Update Unripe HSV value:

- Open this program
```commandline
python hsv_unripe.py
```
- Update HSV value using slide the trackbar
- Save data with press ESC
