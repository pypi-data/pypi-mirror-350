import os
import sys

from .utils import get_git_user, get_translator

_ = get_translator()

HOOKS_DIR = '.git/hooks'
HOOK_NAME = 'commit-msg'
HOOK_PATH = os.path.join(HOOKS_DIR, HOOK_NAME)
GIT_USER = get_git_user()

# Expressão regular ajustada para garantir compatibilidade no shell
COMMIT_REGEX = r'^(feat|fix|chore|refactor|test|docs|style|ci|perf)(\([a-zA-Z0-9_\-]+\))?: .{1,72}$|^.{1,72}$'  # noqa: E501

TYPES_DESCRIPTION = """
✅ Conventional Commit Examples:
    - feat(api): add user authentication
    - fix(ui): correct button alignment
    - chore(deps): update dependency versions
    - refactor(core): optimize database queries
    - docs(readme): update installation guide
"""

HOOK_SCRIPT = f"""#!/bin/sh
COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")


if echo "$COMMIT_MSG" | grep -qE '^!'; then
    exit 0
fi


if [ -z "$COMMIT_MSG" ]; then
    echo "❌ Commit message cannot be empty!"
    exit 1
fi


if ! echo "$COMMIT_MSG" | grep -E "^(feat|fix|chore|refactor|test|docs|style|ci|perf)(\\([a-zA-Z0-9_\\-]+\\))?: .{{1,72}}$|^.{1, 72}$"; then
    echo "❌ Invalid commit message! Use Conventional Commits pattern."
    echo "{TYPES_DESCRIPTION}"
    exit 1
fi


GIT_USER=$(git config --get user.name)
[ -z "$GIT_USER" ] && GIT_USER="Unknown User"


CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)


if echo "$CURRENT_BRANCH" | grep -Eq "^(feature|hotfix|release)/"; then
    echo "\\nCo-authored-by: $GIT_USER" >> "$COMMIT_MSG_FILE"
fi
"""  # noqa: E501


def setup_git_hook():
    """Configura o hook de commit-msg para validar mensagens."""
    if not os.path.exists(HOOKS_DIR):
        message: str = _(
            '.git/hooks directory not found. Please run inside a Git repository.'  # noqa: E501
        )
        print(f'❌ {message}')
        sys.exit(1)

    with open(HOOK_PATH, 'w', encoding='utf-8') as hook_file:
        hook_file.write(HOOK_SCRIPT)

    os.chmod(HOOK_PATH, 0o755)  # Make the hook executable  # nosec
    message: str = _('Commit-msg hook successfully configured!')
    print(f'✅ {message}')
