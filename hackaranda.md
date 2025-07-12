# Hackaranda Tournament Framework

## Project Purpose

This repository contains a framework for running turn-based game tournaments between automated bots. The system is designed to be game-agnostic and supports running various tournament formats (like round-robin and knockout) via a command-line interface (CLI). Bots are run in isolated Docker containers and communicate with the game engine over standard I/O.

## Agent Workflow: Setup and Execution

To set up and run a game, the agent should follow these steps:

### 1. Environment Setup & Installation

**Prerequisites:** The agent must ensure Node.js and Docker are installed and that the Docker daemon is running. The `src/cli/helpers/docker.ts` file contains a function `checkDockerActive` that can be used for this verification.

**Install Dependencies:** From the root of the repository, run the command `npm install`.

**Compile Code:** Compile the TypeScript source code by running `npm run build`. This will create the distributable files in the `/dist` directory.

**Build Bot Images:** The first time the tool is used, the default bot Docker images must be built. This is handled by a setup script.

- **Entry Point:** `npm start`
- **Action:** From the main menu, select the Build Default Bots option. The underlying script is located at `src/cli/setup/index.ts`, which reads bot definitions from the `/bots` directory and builds their corresponding Docker images.

### 2. Running a Tournament or Match

The primary entry point for all operations is the main CLI script.

- **Execution Command:** `npm start`
- **Main Script:** `src/cli/index.ts`

The agent will be presented with a menu. The most relevant options for running games are:

#### Begin Tournament
- **Handler:** `src/cli/beginTournament/index.ts`
- **Configuration:** The agent will need to provide inputs for:
  - `gameType`: e.g., 'arboretum', 'tictactoe'. The available games are defined in `src/games/index.ts`.
  - `tournamentType`: e.g., 'roundRobin', 'knockout'.
  - `tournamentName`: A unique string to identify the tournament and its output folder.
  - `players`: The agent can choose to use a predefined list of bots from a JSON file. These files are located in `bots/{game_name}/`. For example, `bots/arboretum/defaultBots.json`.
  - `numberOfPlayers`: Total number of competitors. The system will fill any empty slots with default random bots.
  - `bestOf`: The number of games to be played in each matchup.
  - `messageTimeout`: The maximum time in milliseconds a bot has to respond before timing out.
  - `save`: A boolean to determine if the results and game logs should be saved to disk.

#### Begin Best Of
- **Handler:** `src/cli/beginBestOf/index.ts`
- **Configuration:** The configuration is similar to a tournament but is limited to selecting two players.

### 3. Core Logic & File Locations

#### Tournament Orchestration
The core logic for running different tournament types resides in `src/tournaments/`.
- `src/tournaments/roundRobin/index.ts` handles the logic for round-robin tournaments.
- `src/tournaments/knockout/index.ts` handles the logic for knockout tournaments.

#### Game Logic
Each game's rules, state management, and move validation are encapsulated within its own directory in `src/games/`.
The central file for any game is `src/games/{game_name}/index.ts`, which exports a `gameInterface` object (e.g., `src/games/arboretum/index.ts`).

#### Bot Handling
Bots are managed by the `BotProcess` class in `src/turnHandlers/botHandler/index.ts`. This class is responsible for spawning a bot's Docker container and managing the I/O communication.

#### Output and Results
If saving is enabled, all tournament data is written to the `tournamentResults/{game_name}/{tournamentName}/` directory.
- `results.json`: Contains the final rankings and a summary of the tournament.
- `Round{X}/{Bot1}-{Bot2}/matchupResults.json`: Contains the detailed results of a single matchup.
- `Round{X}/{Bot1}-{Bot2}/games/{game_number}.json`: A complete, replayable log of a single game.

By following this workflow and understanding the key file locations, an agentic tool can successfully set up the environment, configure and run tournaments, and parse the resulting data.