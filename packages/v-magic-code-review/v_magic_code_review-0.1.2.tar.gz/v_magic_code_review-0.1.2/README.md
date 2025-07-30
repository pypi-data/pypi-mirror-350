# 📖 Guide

## 1️⃣ Install

1. install `brew`: https://brew.sh/

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. install `pipx`

```
brew install pipx
pipx ensurepath
```

3. install `v-cr`

```
pipx install v-magic-code-review
```

## 2️⃣ Setup environment variables

```
export JIRA_HOST=your jira host
export JIRA_TOKEN=your jira token

export CONFLUENCE_HOST=your confluence host
export CONFLUENCE_TOKEN=your confluence token

export GITLAB_HOST=your gitlab host
export GITLAB_TOKEN=your gitlab token

export GEMINI_COOKIE_SECURE_1PSID=get_from_browser_cookie
export GEMINI_COOKIE_SECURE_1PSIDTS=get_from_browser_cookie
```

## 3️⃣ Usage

```
v-cr ORI-100000
```

### Command Options

```
$ v-cr -h
usage: v-cr [-h] [--mr-id MR_ID] [--only-code] [-c] [-d] [-v] [JIRA_KEY]

Magic Code Review

positional arguments:
  JIRA_KEY           jira issue key

options:
  -h, --help         show this help message and exit
  --mr-id MR_ID      merge request id
  --only-code        only review code diff
  -c, --copy-prompt  copy prompt to clipboard
  -d, --debug
  -v, --version
```

# 🤝 Contributing

1. install `poetry`

```
brew install poetry
```

2. install virtualenv and dependencies

```
poetry install --with dev
```
