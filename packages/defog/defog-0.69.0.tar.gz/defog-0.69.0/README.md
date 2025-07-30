# Defog Python

[![tests](https://github.com/defog-ai/defog-python/actions/workflows/main.yml/badge.svg)](https://github.com/defog-ai/defog-python/actions/workflows/main.yml)

Defog converts your natural language text queries into SQL and other machine readable code. This library allows you to easily integrate Defog into your python application, and has a CLI to help you get started.

## Important
We now recommend using [defog-desktop](https://github.com/defog-ai/defog-desktop) instead of using this repo directly.

https://user-images.githubusercontent.com/4327467/236758074-042bc5d7-4452-46ce-bb26-e2da2a0223c6.mp4

# CLI

## Installation
For a generic installation with Postgres or Redshift binaries, use
`pip install --upgrade defog`

For a Snowflake installation, use
`pip install --upgrade 'defog[snowflake]'`

For a MySQL installation, use
`pip install --upgrade 'defog[mysql]'`

For a BigQuery installation, use
`pip install --upgrade 'defog[bigquery]'`

For a Databricks installation, use
`pip install --upgrade 'defog[databricks]'`

For a SQLServer installation, use
`pip install --upgrade 'defog[sqlserver]'`

## API Key
You can get your API key by going to [https://defog.ai/signup](https://defog.ai/signup) and creating an account. If you fail to verify your email, you can email us at support(at)defog.ai

## Connection Setup
You can either use our command line interface (CLI), which will take you through the setup step-by-step, or pass it in explicitly in python to the `Defog` class. The CLI uses the python api's behind the hood, and is just an interactive wrapper over it that does some extra validation on your behalf.

To get started, you can run the following CLI command, which will prompt you for your defog api key, database type, and the corresponding database credentials required.
```
defog init
```
If this is your first time running, we will write these information into a json config file, which will be stored in `~/.defog/connection.json`. If we detect a file present already, we will ask you if you intend to re-initialize the file. You can always delete the file and `defog init` all over again. Note that your credentials are _never_ sent to defog's servers.
Once you have setup the connection settings, we will ask you for the names of the tables that you would like to register (space separated), generate the schema for each of them, upload the schema to defog, and print out the filename of a CSV with your metadata. If you do not wish to provide those at this point, you can exit this prompt by hitting `ctrl+c`

## Generating your schema

To include tables in Defog's indexed, you can run the following to generate column descriptions for your tables and columns:
```
defog gen <table1> <table2> ...
```
This will generate a CSV file that is stored locally on your disk.

## Updating Schema

If you would like to edit the auto-generate column descriptions, just edit the CSV and run the following to update the schema with defog:
```
defog update <csv_filename>
```

## Querying

You can now run queries directly:
```
defog query "<your query>"
```
Happy querying!

## Glossary

You might notice that sometimes our model fails to take into account some prior context for your own domain, eg converting certain fields into different types, joining certain tables, how to perform string matching, etc. To give the model a standard set of instructions attached to each query, you can pass us a `glossary`, which is basically just a string blob of up to 1000 characters that gives our model more specific instructions. You can manage your glossary using the following commands:
```
defog glossary update <path/to/glossary.txt>  # Update your glossary
defog glossary get                             # Get your current glossary
defog glossary delete                          # Delete your glossary
```

## Golden Queries

In certain cases where the generated query follows a complex pattern, you can provide certain examples to our model to help it generate according to your desired patterns. You can manage your golden queries using the following commands:
```
defog golden get <json|csv>                    # Get your golden queries in JSON or CSV format
defog golden add <path/to/golden_queries.json> # Add golden queries from a JSON or CSV file
defog golden delete <path/to/golden_queries.json|all> # Delete specific golden queries or all of them
```
Note that when adding golden queries, the json/csv file provided needs to have the following keys/columns:
- prev_question (optional): the existing question in the database if we're replacing a golden question-query pair
- prev_sql (optional): the existing SQL in the database if we're replacing a golden question-query pair
- question: the new question
- sql: the new SQL

## Deploying
You can deploy a defog server as a cloud function using the following command:
```
defog deploy <gcp|aws> [function_name]         # Deploy to GCP or AWS, optionally specifying the function name
```

## Quota

You can check your quota usage per month by running:
```
defog quota
```
Free-tier users have 1000 queries per month, while premium users have unlimited queries.

# Python Client
You can use the API from within Python as below
```py
from defog import Defog
# your credentials are never sent to our server, and always run locally
defog = Defog() # your credentials will automatically be loaded if you have initialized defog already
question = "question asked by a user"
# run chat version of query
results = defog.run_query(
  question=question,
)
print(results)
```

# Testing
For developers who want to test or add tests for this client, you can run:
```
pytest tests
```
Note that we will transfer the existing .defog/connection.json file over to /tmp (if at all), and transfer the original file back once the tests are done to avoid messing with the original config.
If submitting a PR, please use the `black` linter to lint your code. You can add it as a git hook to your repo by running the command below:
```bash
echo -e '#!/bin/sh\n#\n# Run linter before commit\nblack $(git rev-parse --show-toplevel)' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

# Publishing to pypi

```bash
# creates a publishable package, locally
python setup.py sdist

# uploads it to pypi
twine upload dist/defog-[your-version-number].tar.gz
```