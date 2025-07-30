import gettext
import os
import re
import subprocess


def get_translator(domain='messages', locale_dir=None, lang=None):
    if locale_dir is None:
        locale_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'locale',
        )
    if lang is None:
        lang = os.getenv('LANG', 'en').split('.')[0]  # Get system language

    try:
        translation = gettext.translation(
            domain,
            localedir=locale_dir,
            languages=[lang],
        )
        translation.install()
        return translation.gettext  # Returns the translation function `_()`
    except FileNotFoundError:
        return lambda s: s  # If no translation is found, return original text
    # If no translation is found, return original text


_ = get_translator()


def color_text(text, color) -> str:
    """
    Colors text based on a color string.

    Parameters
    ----------
    text : str
    Text to be placed.
    color : str
    Color of the text. Possible values: "red", "green", "yellow", "blue",
    "magenta", "cyan".

    Returns
    -------
    str
    Text with the color applied.
    """
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'reset': '\033[0m',
    }
    return f'{colors.get(color, colors["reset"])}{text}{colors["reset"]}'


def get_git_user() -> str:
    """
    Gets the Git username.

    Returns
    -------
    str or None
    Git username if found, otherwise None.
    """
    message: str = ''
    try:
        message = _('Git user is required')
        username = subprocess.check_output(
            ['git', 'config', 'user.name'], text=True
        ).strip()
        if not username:
            raise ValueError(f'{message}')
        return username
    except (subprocess.CalledProcessError, ValueError) as e:
        message = _('Error getting user from Git')
        print(color_text(f'❌ {message}: {e}', 'red'))
        return None


def check_git_status() -> bool:
    """
    Checks for changes in the Git repository.

    Returns
    -------
    bool
    True if there are changes in the repository, False otherwise.
    """
    try:
        status = subprocess.check_output(
            ['git', 'status', '--porcelain'], text=True
        ).strip()
        return bool(status)
    except subprocess.CalledProcessError as e:
        message: str = _(
            'Error checking Git status'
        )  # Erro ao verificar status do Git  # noqa: E501
        print(color_text(f'❌ {message}: {e}', 'red'))
        return False


def get_git_status() -> str | None:
    """
    Gets the status of the Git repository.

    Returns
    -------
    str or None
        String with the formatted status of the Git repository
        if found, otherwise None.
    """
    message: str = ''
    try:
        output = subprocess.check_output(
            ['git', 'status', '--porcelain'],
            text=True,
        ).strip()

        # if not output:
        #     return color_text("✔ No changes detected", "green")

        changes_not_staged = []
        changes_staged = []
        untracked_files = []

        # Process each line of output
        for line in output.split('\n'):
            status_code, file_path = line[:2].strip(), line[2:].strip()

            if status_code in {
                'M',
                'A',
                'D',
                'R',
            }:  # Modified, Added, Deleted, Renamed (Staged)  # noqa: E501
                changes_staged.append(f'{file_path}')
            elif status_code in {
                ' M',
                ' D',
            }:  # Modified or deleted (Not Staged)  # noqa: E501
                changes_not_staged.append(f'{file_path}')
            elif status_code == '??':  # Untracked files
                untracked_files.append(f'{file_path}')

        # Format the output
        result = []
        if changes_not_staged:
            message = _('Changes not staged')
            result.append(color_text(f'📋 {message}:', 'yellow'))
            result.extend(
                color_text(f'   🎯 {item}', 'yellow')
                for item in changes_not_staged
            )
            result.append('')
        if changes_staged:
            message = _('Changes staged')
            result.append(color_text(f'📝 {message}:', 'green'))
            result.extend(
                color_text(f'   🎯 {item}', 'green') for item in changes_staged
            )
            result.append('')
        if untracked_files:
            message = _('Untracked files')
            result.append(color_text(f'❌ {message}:', 'red'))
            result.extend(
                color_text(f'   🎯 {item}', 'red') for item in untracked_files
            )
            result.append('')

        return '\n'.join(result)

    except subprocess.CalledProcessError as e:
        message = _('Error checking Git status')
        return color_text(f'❌ {message}: {e}', 'red')


def is_git_flow():
    """
    Checks if the repository uses Git Flow.

    Returns
    -------
    bool
    True if the repository uses Git Flow, False otherwise.
    """
    try:
        subprocess.check_output(['git', 'flow', 'config'], text=True)
        return True
    except subprocess.CalledProcessError as e:
        message: str = _('Gitflow not installed, but push is successful')
        print(color_text(f'❌ {message}: {e}', 'red'))
        return False


def get_current_branch():
    """
    Gets the name of the current branch of the Git repository.

    Returns
    -------
    str or None
    Name of the current branch if found, otherwise None.
    """
    try:
        return subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'], text=True
        ).strip()
    except subprocess.CalledProcessError as e:
        message: str = _('Error getting current branch')
        print(color_text(f'❌ {message}: {e}', 'red'))
        return None


def add_changes():
    """
    Add all changes from the Git repository.

    ------
    subprocess.CalledProcessError
    If there was an error while adding the changes.
    """
    message: str = ''
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        message = _('All changes added')
        print(color_text(f'✔️ {message}.', 'green'))
    except subprocess.CalledProcessError as e:
        message = _('Error adding changes')
        print(color_text(f'❌ {message}: {e}', 'red'))
        raise


def create_commit(commit_type, module, commit_message, git_user):
    """
    Performs a commit to the Git repository with the specified type,
    module, and message.

    Parameters
    ----------
    commit_type : str
    Commit type:
    (feat, fix, chore, refactor, test, docs, style, ci, perf).
    module : str
    Module that the commit refers to.
    commit_message : str
    Commit message.
    git_user : str
    Git user who performed the commit.

    ------
    subprocess.CalledProcessError
    If there was an error while performing the commit.
    """
    message: str = ''
    full_commit_message = f'{commit_type}({module}): {commit_message}'
    updated_commit_message = f'{full_commit_message} (👤: {git_user})'.lower()
    try:
        subprocess.run(
            ['git', 'commit', '-m', updated_commit_message], check=True
        )
        message = _('Commit successful')
        print(color_text(f'✅ {message}!\n', 'green'))
    except subprocess.CalledProcessError as e:
        message = _('Error committing')
        print(color_text(f'❌ {message}: {e}', 'red'))
        raise


def handle_git_flow(branch):
    """
    Manages the Git Flow workflow for the specified branch.

    Parameters
    ----------
    branch : str
    Name of the branch in "type/name" format that you want to publish
    or finish.

    Prompts the user for the desired action ('publish' or 'finish') for the
    given branch and executes the appropriate Git Flow command.
    Displays success or error messages based on the result of the command
    execution.

    ------
    subprocess.CalledProcessError
    If there is an error executing the Git Flow command.
    """
    message: str = _("Do you want to 'publish' or 'finish' this branch?")
    action = (
        input(
            color_text(
                f'🛠️ {message}? (publish/finish): ',
                'blue',
            )
        )
        .strip()
        .lower()
    )
    if action == 'publish':
        try:
            subprocess.run(
                ['git', 'flow', branch.split('/')[0], 'publish'], check=True
            )
        except subprocess.CalledProcessError as e:
            message: str = _('Error publishing branch')
            print(color_text(f'❌ {message}: {e}', 'red'))
    elif action == 'finish':
        try:
            subprocess.run(
                ['git', 'flow', branch.split('/')[0], 'finish'], check=True
            )
        except subprocess.CalledProcessError as e:
            message: str = _('Error finalizing branch')
            print(color_text(f'❌ {message}: {e}', 'red'))
    else:
        message: str = _('Invalid action')
        print(color_text(f'❌ {message}!', 'red'))


def execute_push(branch):
    """
    Pushes the current branch to the remote repository.

    Parameters
    ----------
    branch : str
    Name of the branch you want to push.

    ------
    subprocess.CalledProcessError
    If there is an error during the push.
    """
    try:
        subprocess.run(['git', 'push', 'origin', branch], check=True)
    except subprocess.CalledProcessError as e:
        message: str = _('Error when pushing')
        print(color_text(f'❌ {message}: {e}', 'red'))


def remove_excess_spaces(text: str) -> str:
    """
    Removes excess spaces from text.

    Parameters
    ----------
    text : str
    Text from which to remove excess spaces.

    Returns
    -------
    str
    Text without excess spaces.
    """
    if text is None:
        return ''

    text_without_extra_space: str = re.sub(r'\s+', ' ', text)
    return text_without_extra_space.strip()


def clear_screen(stdscr):
    """Limpar a tela do terminal"""
    stdscr.clear()
    stdscr.refresh()
