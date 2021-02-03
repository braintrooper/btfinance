<!-- PROJECT LOGO -->
<p align="center">
  <a>
    <img src="circle-cropped.ico" alt="Logo" height="138">
  </a>
  <img src="logotext.png" alt="Logo Text" position="32,78">
</p>


<hr>
<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

<hr>


<!-- ABOUT THE PROJECT -->
## About The Project 📖

This is my final project for the Harvard CS50x course. It is a website where young people can learn how the stock market works through a live and interactive stock simulator. The implementation is fairly simple in essence with minimal variables and math to reduce load times and has various plugins that are placed in the HTML pages through JS to increase user-friendliness, style, and functionality. I also plan to host this website and make it available to the public shortly, so that the main purpose of the site can be achieved.

I wanted to make a project like this to expand my knowledge of Flask and Databases and of techniques like app routing in flask, adding dynamic information in HTML through Jinja, and others. I have learned a lot in the process, and I hope you like it! 👍🏻

Key features are:
* An advanced chart displaying almost all the data needed to help you decide when and what to buy or sell.
* A smooth, hassle-free dark mode that ensures your eye-health is not compromised no matter what time you are viewing the site!
* A list of all stocks, so you can explore the various companies' shares you can buy, all in one place.

Skip to the <a href="#usage">Usage</a></li> page if you want to see how it works!

### Built With

These are the major frameworks used to build the site
* Flask
* HTML
* SQLite 3
* JavaScript
* CSS
* [Bootstrap 4.5](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [SQL, by CS50](https://github.com/cs50/libcs50)


<hr>


<!-- GETTING STARTED -->
## Getting Started

This site was planned to be hosted through Heroku, but due to a host of errors and tight time constraints, it isn't live yet. But you can still access the site through your machine by following the steps below!



### Prerequisites

* You will need an IDE with a terminal.
* A good option is the CS50 ide itself. Another good local IDE you can try is WebStorm by JetBrains
* As the site has plugins that get data from the cloud, you will need a constant internet connection to access all the features.



### Installation

1. Get an API Key by registering at [IEXCloud](https://iexcloud.com)
2. Clone the repo
   ```python
   git clone https://github.com/cs50raajvir/CS50-Final-Project.git
   ```
3. Install all the frameworks and packages
   ```python
   pip install "package name"
   ```
4. Enter your API in the terminal window
   ```python
   export API_KEY = 'your API key'
   ```

<hr>

<!-- USAGE EXAMPLES -->
## Usage

Navigate to the directory containing the {app.py} and enter the following to start the local server.
   ```python
   flask run
   ```
Click the link to open the website in your browser

### Start

Register yourself on the register page. After you are done, you will be automatically redirected to the index page. There you will find a table containing the stocks you own, which are none at the moment. Then below that, you will find a table showing the active stocks of today.
This will help you decide what and when to buy and when to sell stocks. Ok, now let's go buy some stocks, shall we?

### Quote

Here you can check the prices of the stocks. Simply type the ticker symbol of the stock you want to quote and press the big yellow button. You will find the price of one stock and also a mini chart showing the recent history of prices of the stock.

### Buy

Navigate to the buy page from the navbar. There you will find two input fields. The first one is where you have to type in the symbol of the stock you want to buy. In the next one, you have to input the number of stocks you wish to buy. Then, if you press the big green button, the transaction will take place. You can view your newly bought stock on the index page. **Yay**

### Sell

Navigate to the sell page. Here you will an input selector displaying the stocks that you own and the number of the same. Select the stock you want to sell and the number of them. Again, click the big red button to confirm the transaction.

### Index

This is the main page of the site. It consists of a table containing the stocks that you own and another table showing the most active stocks of today. The latter also can show the biggest gainers and losers, which will help you buy stocks.

_For strategies, please refer to this site [Investopedia Strategies](https://www.investopedia.com/financial-edge/0412/5-tips-on-when-to-buy-your-stock.aspx)_


<hr>

<!-- LICENSE -->
## License

Distributed under the MIT License. See [`LICENSE`](https://www.braintrooper.info) for more information.



<!-- CONTACT -->
## Contact

Raajvir Vijay - [@instagram](https://instagram.com/bluecrystalcars) - vijay.raajvir@gmail.com

edX Verified Learner - Username: [vijayraajvir](https://profile.edx.org/u/vijayraajvir)

GitHub username: [cs50raajvir](https://www.github.com/cs50raajvir)

Project Link: [https://github.com/cs50raajvir/CS50-Final_Project](https://github.com/cs50raajvir/CS50-Final_Project)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Readme Template](https://github.com/othneildrew/Best-README-Template)
* [IEXCloud - Data Provider](https://www.iexcloud.com)
* [TradingView - Charts and Ticker Tape](https://www.tradingview.com)
* [DataHub - Data Provider](https://www.datahub.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Loaders.css](https://connoratherton.com/loaders)