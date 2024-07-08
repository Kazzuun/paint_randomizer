# Paint randomiser
Periodically selects a random 7tv paint and equips it.

## Usage
Written on python 3.10 but should work on most versions.

1. Clone the repo.
   ```sh
   git clone https://github.com/Kazzuun/paint_randomizer.git
   ```
2. Install requirements.
   ```sh
   pip install -r requirements.txt
   ```
3. Copy or rename .env.example to .env and fill it with correct values.
4. Run the script.
   ```sh
   python main.py
   ```
   An interval at which it changes paints can be given
   ```sh
   python main.py <interval>
   ```