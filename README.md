[![Backend checks](https://github.com/thiswasdumb/SoftEngProject/actions/workflows/backend.yaml/badge.svg)](https://github.com/thiswasdumb/SoftEngProject/actions/workflows/backend.yaml) [![Frontend checks](https://github.com/thiswasdumb/SoftEngProject/actions/workflows/frontend.yaml/badge.svg)](https://github.com/thiswasdumb/SoftEngProject/actions/workflows/frontend.yaml)

# Group 1 - CS261 Group Project

## Members: 
- Serene Alrawi 
- Shayan Borhani Yazdi 
- Louis Hudson 
- Gabriel Hughes 
- Hao-Yen Tang 
- Alara Tindall
- Xun Khang Tan

<br>
<img src="/tradetalker/public/images/logo.png" alt="TradeTalker" width="150"/>

## Requirements
- [Python 3.11 or higher](https://www.python.org/downloads/)
    - Make sure `pip` and `setuptools` are installed and upgraded to the latest version by running `pip3 install --upgrade pip setuptools`.
- [Node.js LTS or higher and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
    - Note: the latest versions of Node.js may output a warning when the website is running.
- [MySQL 8 or higher](https://dev.mysql.com/downloads/mysql/])
    - For macOS Homebrew users, run `brew install mysql`.
    - For Linux, you should use the package manager specific to your distribution.
- [(Optional) pnpm](https://pnpm.io/installation)

## Installation
- Clone the repository by running `git clone https://github.com/thiswasdumb/SoftEngProject.git`.
- Enter the project directory with `cd tradetalker` and install the dependencies with `npm i` (or `pnpm i` if you wish to use pnpm.)
- Setup the MySQL server:
    - Start the server. (On macOS, run `mysql.server start`)
    - Access the server by running `mysql -u root`.
    - Create the `tradetalkerdb` database. (`CREATE DATABASE tradetalkerdb;`)
    - Exit the server by running `exit`.

- Run the development server with `npm run dev` or `pnpm dev`.
- Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
- The Flask server will be running on [http://127.0.0.1:8080](http://127.0.0.1:8080).
- When done, stop the MySQL server. (On macOS, run `mysql.server stop`)

## Development
Further details about how to develop the project can be found in the [project readme](https://github.com/thiswasdumb/SoftEngProject/blob/main/tradetalker/README.md).