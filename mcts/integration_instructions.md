# MCTS Bot Integration Instructions

## Successfully Created: MCTS Bot Subfolder

The MCTS bot has been set up in a clean subfolder structure to avoid merge conflicts:

```
/home/ed/majestic_maple/
├── mcts/                  # MCTS Bot subfolder
│   ├── Dockerfile         # Configured for dependency installation
│   ├── index.py          # Entry point (unchanged)
│   ├── readLine.py       # Modified to use MCTSBot
│   ├── requirements.txt  # Math optimization packages
│   ├── mcts_bot.py      # MCTS algorithm implementation
│   ├── mcts_node.py     # Tree node structure
│   ├── move_evaluator.py # Move evaluation logic
│   ├── data_structures.py # Shared data types
│   ├── placement.py     # Valid placement logic
│   └── scoring.py       # Scoring system
├── Dockerfile           # Original bot Docker config
├── index.py            # Original bot entry point
├── readLine.py         # Original bot I/O handler
└── [other files...]    # Original bot files
```

## Integration Steps

### 1. Build the MCTS Docker Image
```bash
cd /home/ed/majestic_maple
sudo docker build -t majestic-maple-mcts ./mcts
```

### 2. Register in Hackaranda Framework
Add to `/home/ed/Hackaranda/bots/arboretum/defaultBots.json`:
```json
{
  "dockerId": "majestic-maple-mcts",
  "identifier": "Majestic Maple MCTS (montey branch)"
}
```

### 3. Test the Bot
```bash
cd /home/ed/Hackaranda
npm start
# Select "Begin Best Of"
# Choose "Majestic Maple MCTS" from bot list
```

## Key Changes Made

### Modified readLine.py
- **Import**: Changed from `scoring` to `mcts_bot`
- **Function**: Renamed `randomIsh()` to `mctsMove()`
- **Logic**: Uses `MCTSBot.choose_move()` for subTurn 2 (play phase)
- **Fallback**: Graceful error handling with random move fallback
- **Time Limit**: Set to 1.15 seconds per move

### Dependencies Added
- numpy, scipy, numba, statsmodels, scikit-learn
- All math optimization packages for MCTS performance

## Conflict-Free Development

### Current Status
- ✅ **Zero merge conflicts**: Separate directories prevent any conflicts
- ✅ **Independent development**: MCTS bot can be developed without affecting main branch
- ✅ **A/B testing ready**: Both bots can run simultaneously in tournaments
- ✅ **Framework compliant**: Follows Hackaranda bot registration patterns

### Original Bot Preserved
The original bot files in `/home/ed/majestic_maple/` remain unchanged:
- Can still build with: `docker build -t majestic-maple .`
- Can still register as: `"dockerId": "majestic-maple"`
- No interference with other branch development

## Next Steps

1. **Test Build**: Run `sudo docker build -t majestic-maple-mcts ./mcts`
2. **Register Bot**: Add entry to Hackaranda bot registry
3. **Run Tournaments**: Compare MCTS vs original bot performance
4. **Iterate**: Improve MCTS parameters based on results

## Tournament Comparison Setup

Both bots can compete against each other:
```json
[
  {
    "dockerId": "majestic-maple",
    "identifier": "Majestic Maple (Original)"
  },
  {
    "dockerId": "majestic-maple-mcts", 
    "identifier": "Majestic Maple MCTS"
  }
]
```

This setup allows direct performance comparison between approaches while maintaining completely separate codebases.