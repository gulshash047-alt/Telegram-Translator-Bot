# 1. Project Name
Translator Bot — a Telegram chat bot for automatic text translation via API with history storage.

# 2. Project Description
This chat bot was developed as a final project for the "Python Programming" course. It is designed for rapid automatic translation of user text messages into several popular languages. The bot automatically detects the source language of the input text, translates it into the chosen target language using an external API, and saves the query history to a local database. The bot supports a full interactive dialogue and is resilient to various input errors.

# 3. Technologies Used
* **Programming Language:** Python 3.10+
* **Libraries:** pyTelegramBotAPI, deep-translator
* **Database:** SQLite3
* **Tools:** PyCharm, GitHub

# 4. Installation Instructions
1. Clone the repository:
   
   git clone https://github.com/gulshash047-alt/Telegram-Translator-Bot.git
   
3. Open the project folder in PyCharm or any other code editor.
4. Install the required dependencies from the requirements.txt file:
pip install -r requirements.txt

# 5. Deployment and Launch Instructions
1. Insert your bot token obtained from @BotFather into the TOKEN variable in the bot.py file.
2. Run the bot using the terminal command:

   pyhon bot.py
   
3. Open Telegram and send the /start command.
   
# 6. Examples of Chat Bot Operation
* /start — Greeting, user initialization, displaying the current target language, and opening the command menu.
* /help — Displays a detailed user guide with rules: instructions on sending words or sentences for translation, changing settings, viewing the last 5 translations from history, and checking available languages.
* /languages — Displaying interactive Reply buttons right below the input field to select the target translation language (English, Russian, Kazakh, Turkish, German, French)
* /history — Accessing the SQLite database to fetch and display the last 5 translations performed by the user.
* Sending regular text — The bot accepts any text message, automatically detects its source language, immediately provides the translation into the chosen language via API, and logs the entry into the database history.

# 7. Interface Screenshots
All screenshots of the bot interface are saved in the root folder of the repository:
* ![start..PNG](screenshots/start..PNG) — Bot launch, greeting message, and main menu. 
* ![lanгг..PNG](screenshots/lan%D0%B3%D0%B3..PNG) — Interactive language selection buttons interface.
* ![turkisн transl.PNG](screenshots/turkis%D0%BD%20transl.PNG) — Successful text translation into Turkish.
* ![немис transl.PNG](screenshots/%D0%BD%D0%B5%D0%BC%D0%B8%D1%81%20transl.PNG) — Successful text translation into German.  
* ![Нistory.PNG](screenshots/%D0%9Distory.PNG) — Fetching and displaying translation history from the database.
* ![Неlp.PNG](screenshots/%D0%9D%D0%B5lp.PNG) — Displaying the user guide and command list (Help).
