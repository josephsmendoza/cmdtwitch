# cmdTwitch
This program allows you to bind twitch commands to terminal commands. In layman's terms, it allows twitch commands/redeems to run programs on your pc.
## WIP
This program is in its early stages, and doesn't implement any safety checks. It only binds chat commands, which are only mod-accessible, to terminal commands, which can do immense damage to your pc. If you don't understand exactly what a terminal command does, don't put it into this program.
## Usage
At the moment there is no GUI, just a json file that is generated the first time you run the program. The `username` should be the account username that the bot will send messages from and read chat with, the `channel` should be your account username, and the `password` should be generated using the provided link while signed in to the bot account. Then you need to fill out the commands you want to use, for example:
```json
"commands":{
    "!goose":"GooseDesktop.exe",
    "!ungoose":"Close Goose.bat"
}
```
At the moment, only mods can use cmdtwitch chat commands. You can use one of the popular chatbots to put these commands behind a point system by creating a chat command in your chatbot which puts a cmdtwitch chat command into chat. Redeem support is on it's way.
