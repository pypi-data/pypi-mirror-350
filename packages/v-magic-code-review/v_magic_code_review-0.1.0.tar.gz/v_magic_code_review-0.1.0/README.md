# Install system command

1. install `brew`: https://brew.sh/

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. install `poetry`

```
brew install poetry
```

3. install `pipx`

```
brew install pipx
pipx ensurepath
```

4. install `v-magic-code-review` and `v-cr`

```
cd v-magic-code-review
```

```
make install
```

# Setup environment variables

```
export JIRA_TOKEN=your_jira_token
export CONFLUENCE_TOKEN=your_wiki_access_token
export GITLAB_TOKEN=your_gitlab_access_token
export GEMINI_COOKIE_SECURE_1PSID=get_from_browser_cookie
export GEMINI_COOKIE_SECURE_1PSIDTS=get_from_browser_cookie
```

# Usage

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
