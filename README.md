This is a tool that searches all your uncompleted Steam badges, that have no card drops remaining, and sorts them based on how cheap it is to buy the rest of the cards.

If you have a lottt of games, it may take a little bit and also varies on your internet connection, 100 games takes about 5 minutes for me.

### Running
Make sure you have Python 3 installed and then install the packages required by running `pip install -r requirements.txt` in the folder.

Download the Chrome web driver that matches your version of Chrome [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
You can check your Chrome version by going to `chrome://version` in the address bar.

Put the chrome driver in the folder, you can change the path of the Chrome driver in `config.yml`.

Login to Steam using `login.py`.  Your username and password are **not** stored, cookies that Steam sends back are stored in the `data/` folder and you can delete them afterwards if you like.

Once you are logged in, run `main.py` and it will start going through every badge.

Once it's completed you can open up `results.html` in your web browser.

### Issues and contributing
If you have any problems you may contact me on Discord: `sexnine#6969` or you may open an issue.
Contributions are welcome, feel free to talk to me about it first :)

### License
MIT License

Copyright (c) 2021 sexnine

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.