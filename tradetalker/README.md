[![Backend checks](https://github.com/thiswasdumb/SoftEngProject/actions/workflows/backend.yaml/badge.svg)](https://github.com/thiswasdumb/SoftEngProject/actions/workflows/backend.yaml) [![Frontend checks](https://github.com/thiswasdumb/SoftEngProject/actions/workflows/frontend.yaml/badge.svg)](https://github.com/thiswasdumb/SoftEngProject/actions/workflows/frontend.yaml)

# TradeTalker

<img src="/tradetalker/public/images/logo.png" alt="TradeTalker" width="150"/>

A financial sentiment news website built with Next.js, Flask and MySQL.

## Requirements

- [Python 3.11 or higher](https://www.python.org/downloads/)
- [Node.js 21 or higher and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- [(Optional) pnpm](https://pnpm.io/installation)

## Installation

- To run the environment, install the dependencies with `npm i` (or `pnpm i` if you wish to use pnpm.)
- Run the development server with `npm run dev` or `pnpm dev`.
- Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
- The Flask server will be running on [http://127.0.0.1:8080](http://127.0.0.1:8080).

## Backend development

- Please make sure to lint all Python code by running the `lint.sh` script before committing. This will install `pipenv` and create a pipenv virtual environment where the required packages will be installed and checks will run.

## Frontend development

- To install a Node package, run `npm install [package]`. Make sure that `pnpm-lock.yaml` is kept up to date by running `pnpm install` after a package installation.
- Please make sure to lint all JS/TS code by running `npm run lint` before committing.
