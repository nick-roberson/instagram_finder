
## Setup

Install all dependencies:
```
> pip install poetry
> poetry install
```

If you add any dependencies run:
```
> poetry add <package name> && poetry update && poetry install
```


# Usage

Before you even run this script you must login with `instaloader` and then pass your profile:
```
% instaloader --login guy.dinner
Session file does not exist yet - Logging in.
Enter Instagram password for guy.dinner: 
Logged in as guy.dinner.
Saved session to /Users/nicholas/.config/instaloader/session-guy.dinner.
No targets were specified, thus nothing has been downloaded.=
```
Here I am given the file `/Users/nicholas/.config/instaloader/session-guy.dinner` to use as my `--session-file` argument in the script.

Get similar users between two profiles:
```
> poetry run python code/cli.py get-similar\
    --username guy.dinner \
    --target-user cpgreenman \
    --min-followers 700 \
    --max-followers 30000
```

Scrape web itself to get related accounts for a user:
```commandline
> poetry run python code/cli.py get-related \
    --username guy.dinner
```