# cmdTwitch
This program allows you to bind twitch commands to terminal commands. In layman's terms, it allows twitch commands/redeems to run programs on your pc.
## WIP
This program is in its early stages, and doesn't implement any safety checks. It only binds chat commands, which are only mod-accessible, to terminal commands, which can do immense damage to your pc. If you don't understand exactly what a terminal command does, don't put it into this program.
## Usage
At the moment there is no GUI, just a json file that is generated the first time you run the program. The username should be the bot (or your) account username, the nick should be your account username, and the pass should be generated using the provided link while signed in to the bot (or your) account. Then you need to fill out the commands you want to use, for example:
```json
"commands":{
    "!goose":"GooseDesktop.exe",
    "!ungoose":"Close Goose.bat"
}
```
These commands are only useable by mods. If you want regular users to trigger these commands, you should create a redeem or other bot action which sends the command into chat. Make sure you don't allow users to trigger many commands in rapid succession, as that can easily overwhelm your pc just by spawning a huge number of processes.