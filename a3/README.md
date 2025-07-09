The implementation satisfies the following:
- **Termination**: The election completes in finite time.
- **Uniqueness**: Exactly one leader is elected.
- **Agreement**: All nodes agree on the same leader.

## Files

- `myleprocess.py`: Python script that runs a single node in the election ring.
- `config1.txt`, `config2.txt`, `config3.txt`: Configuration files for each node.
- `log1.txt`, `log2.txt`, `log3.txt`: Logs from each node showing election progress.
- `README.md`: This file.

# Terminal 1
python3 myleprocess.py config1.txt

# Terminal 2
python3 myleprocess.py config2.txt

# Terminal 3
python3 myleprocess.py config3.txt

Outputs are visible in their respective log files
