import subprocess
import sys

import inquirer
from prompt_toolkit import HTML, prompt

from .utils import (
    add_changes,
    check_git_status,
    color_text,
    create_commit,
    execute_push,
    get_current_branch,
    get_git_status,
    get_git_user,
    get_translator,
    handle_git_flow,
    is_git_flow,
    remove_excess_spaces,
)

_ = get_translator()


def git_commit():  # noqa: PLR0912, PLR0915
    message: str = ''
    message_yes: str = _('y')
    message_no: str = _('n')
    try:
        message = _('Starting commit process')
        print(color_text(f'\n🚀 {message}. 🚀\n', 'cyan'))

        def check_status():
            if not check_git_status():
                message = _('No changes to commit')
                print(color_text(f'✅ {message}.', 'green'))
                return sys.exit(0)

        git_status = get_git_status()
        if git_status:
            print(color_text(git_status, 'yellow'))

        message = _('Do you want to add all changes')
        add_all = (
            input(
                color_text(
                    f'📌 {message}? '
                    f'(✅ {message_yes} / ❌ {message_no}) '
                    f'[{message_yes}]: ',
                    'yellow',
                )
            )
            .strip()
            .lower()
            or f'{message_yes}'
        )

        if add_all == message_yes:
            try:
                message: str = _('Pulling latest changes...')
                print(color_text(f'🔄 {message}', 'cyan'))
                result = subprocess.run(
                    ['git', 'pull'],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                print(color_text(result.stdout, 'green'))

            except subprocess.CalledProcessError as err:
                stderr = err.stderr.strip()

                if 'no tracking information' in stderr.lower():
                    current_branch = get_current_branch()
                    message: str = _(
                        'The current branch is not linked to a remote'
                    )
                    print(color_text(f'❌ {message}', 'red'))
                    message: str = _(
                        'Run the following command to configure the remote branch:'  # noqa: E501
                    )
                    print(color_text(f'📌 {message}', 'yellow'))
                    print(
                        color_text(
                            '   git branch --set-upstream-to=origin/'
                            f'{current_branch} {current_branch}',
                            'cyan',
                        )
                    )
                    sys.exit(1)

                message: str = _('Conflict or error when pulling!')
                print(color_text(f'❌ {message}', 'red'))
                print(color_text(stderr, 'red'))
                sys.exit(1)

            add_changes()
        elif add_all == message_no:
            message = _('Manually add the changes and run the command again')
            print(color_text(f'❌ {message}.', 'red'))
            return sys.exit(0)
        else:
            message = _('Invalid option')
            print(color_text(f'❌ {message}!', 'red'))
            return check_status()

        check_status()

        def commit_type_input():
            feat: str = _('New functionality')
            fix: str = _('Bug fix')
            refactor: str = _('Code refactoring')
            docs: str = _('Documentation update')
            style: str = _('Style changes')
            perf: str = _('Performance improvements')
            test: str = _('Test addition/correction')
            chore: str = _('Configuration changes')
            ci: str = _('Changes in continuous integration')

            commit_type_choices: list[str] = [
                {'name': f'✨ feat - {feat}', 'value': 'feat'},
                {'name': f'🐛 fix - {fix}', 'value': 'fix'},
                {'name': f'🛠️ refactor - {refactor}', 'value': 'refactor'},
                {'name': f'📖 docs - {docs}', 'value': 'docs'},
                {'name': f'🎨 style - {style}', 'value': 'style'},
                {'name': f'🚀 perf - {perf}', 'value': 'perf'},
                {'name': f'✅ test - {test}', 'value': 'test'},
                {'name': f'⚙️ chore - {chore}', 'value': 'chore'},
                {'name': f'💚 ci - {ci}', 'value': 'ci'},
            ]
            message = _('Choose commit type')

            try:
                questions = [
                    inquirer.List(
                        'commit_type',
                        message=message,
                        choices=[
                            commit['name'] for commit in commit_type_choices
                        ],
                        carousel=True,
                    ),
                ]

                answers = inquirer.prompt(questions)

                if not answers:
                    raise KeyboardInterrupt

                if answers and 'commit_type' in answers:
                    selected_commit_type = next(
                        commit['value']
                        for commit in commit_type_choices
                        if commit['name'] == answers['commit_type']
                    )
                    return selected_commit_type
                else:
                    message = _('Invalid commit type')
                    print(color_text(f'❌ {message}', 'red'))
                    return commit_type_input()

            except KeyboardInterrupt:
                message = _('Process interrupted. Exiting...')
                print(color_text(f'🚩 {message}', 'red'))
                return sys.exit(0)

            except Exception as error:
                message = _('Unexpected error occurred')
                print(color_text(f'❌ {message}: {error}', 'red'))
                return sys.exit(1)

        commit_type = commit_type_input()

        def module_input():
            message = _(
                'Which module was changed? (example: core, api, models): '
            )
            module = remove_excess_spaces(
                (
                    prompt(HTML(f'<ansimagenta>🗂️ {message} </ansimagenta>'))
                    .strip()
                    .lower()
                )
            ).replace(' ', '_')
            if not module:
                message = _('Module is mandatory')
                print(color_text(f'❌ {message}', 'red'))
                return module_input()
            return module

        module = module_input()

        def commit_message_input():
            message = _('Enter commit message')
            commit_message = remove_excess_spaces(
                prompt(HTML(f'<ansigreen>📝 {message}: </ansigreen>')).strip()
            )
            if not commit_message:
                message = _('Commit message is mandatory')
                print(color_text(f'❌ {message}!', 'red'))
                return commit_message_input()
            return commit_message

        commit_message = commit_message_input()

        git_user = get_git_user()
        if git_user is None:
            message = _('Error: Git username not set')
            print(color_text(f'❌ {message}!', 'red'))
            return

        def send_commit_input():
            message = _('Do you want to send the commit')
            send_commit = input(
                color_text(
                    f'🚀 {message}? '
                    f'(✅ {message_yes} / ❌ {message_no}) '
                    f'[{message_yes}]: ',
                    'yellow',
                )
            ).strip().lower() or {message_yes}

            if send_commit == message_yes:
                return True
            if send_commit == message_no:
                return False
            else:
                message = _('Invalid option')
                print(color_text(f'❌ {message}!', 'red'))
                return send_commit_input()

        if send_commit_input():
            create_commit(commit_type, module, commit_message, git_user)
        else:
            message = _('Commit canceled')
            print(color_text(f'❌ {message}.', 'red'))

        def push_input():
            message = _('Do you want to push to the repository')
            push = input(
                color_text(
                    f'🚀 {message}? '
                    f'(✅ {message_yes} / ❌ {message_no}) '
                    f'[{message_yes}]: ',
                    'yellow',
                )
            ).strip().lower() or {message_yes}

            if push == message_yes:
                current_branch = get_current_branch()
                if is_git_flow() and current_branch:
                    if (
                        current_branch.startswith('feature/')
                        or current_branch.startswith('hotfix/')
                        or current_branch.startswith('release/')
                    ):
                        handle_git_flow(current_branch)
                    else:
                        execute_push(current_branch)
                else:
                    execute_push(current_branch)
                return True
            if push == message_no:
                message = _('Push canceled')
                print(color_text(f'❌ {message}.', 'red'))
                return False
            else:
                message = _('Invalid option')
                print(color_text(f'❌ {message}!', 'red'))
                return push_input()

        push_input()

    except KeyboardInterrupt:
        message = _('Leaving...')
        print(color_text(f'\n 🚩 {message}', 'red'))
        sys.exit(0)

    except Exception as error:
        message = _('Unexpected error')
        print(color_text(f'❌ {message}: {error}', 'red'))
        sys.exit(1)
