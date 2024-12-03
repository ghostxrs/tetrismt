[![Apache License 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

# Tetris

Tetris is a classic puzzle game where you strategically rotate and drop tetrominoes to clear lines.

This implementation is built using `Python` and utilizes the following technologies:

- `Django` framework for the backend.
- `Jinja2` as a template engine for rendering frontend views.
- `Threading` module:
   - `Rlock()` ensures synchronized access for shared resources.
   - `Timer()` updates the game field on the frontend.

**The application deployed and running on the **`SAP Business Technology Platform`** (SAP BTP), utilizing the **`Cloud Foundry`** service.**

## How To Play

### Game Controls:

- <kbd>↑</kbd> - Rotate figure clockwise.
- <kbd>←</kbd> - Move figure left (one cell).
- <kbd>→</kbd> - Move figure right (one cell).
- <kbd>↓</kbd> - Soft drop (move figure down one cell). Hold for continuous soft drop.


## Browser Game

[Play](https://tetris.cfapps.us10-001.hana.ondemand.com/)

## CLI Game

### Download the game:

There are two ways to download the game:

1. **Clone the repository using Git:**
   
    ```bash
    git clone https://github.com/cult2rologist/TETRIS.git
    ```

    *Use code with caution.*

2. **Download the ZIP archive from GitHub:**
   
    - Go to the GitHub repository: [Tetris](https://github.com/cult2rologist/TETRIS/tree/main)
    - Click "Code" -> "Download ZIP"
    - Extract the downloaded ZIP file.

### Run the game:

1. Open your terminal and navigate to the extracted folder.
2. Run the game using: 
   
    ```bash
    python tetris.py
    ```

3. Make your moves using the keyboard arrows (refer to the instructions above).

## Dependencies

This game requires Python 3.x to run.
```
Django==5.0.3
keyboard
gunicorn
```

## Contributors

- Ilya Makeev
- [Micellius](https://github.com/micellius) as a Mentor

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/cult2rologist/TETRIS/blob/main/LICENCE) file for details.
