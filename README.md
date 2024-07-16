## Palm Oil Ripeness Detection
### Feature
- [x] Ripeness Palm Oil Using HSV Method
- [ ] Capture camera using Raspberry Pi 4 camera
- [x] Send classification using Telegram

### Run Project
- Clone Project
```commandline
git clone https://github.com/ASNProject/palm_oil_ripeness_detection.git
```

- Install requirements.txt
```commandline
pip install -r requirements.txt
```

- Change BOT_TOKEN and CHAT_ID
1. Open the Telegram app on your smartphone or desktop.
2. Search for the “BotFather” username in the search bar.
3. Click on the “Start” button to start a conversation with the BotFather.
4. Type “/newbot” and follow the prompts to create a new bot. The BotFather will give you an API key that you will use in the next step.
5. To get CHAT_ID search 'Get My ID' in Telegram and click on the "start" button
6. Update BOT_TOKEN and CHAT_ID in utils/telegram_bot.py

- Run project
```commandline
python main.py
```
