# simple-budget

## Installation instructions
- clone repo `git clone {repo_link}`
- `pipenv install`
- `pipenv shell`
- `python manage.py init_project`
Note: init_project might error out when running `npm run compile:tsc` if
there are no .ts files in the project.

## Django Commands
### init_project
- Run `python manage.py init_project` to run a series of commands to initalize the project

## Dev Node Commands
To automatically compile scss or ts files run:
- compile:tsc:watch
- compile:css:watch
