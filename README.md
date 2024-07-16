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
