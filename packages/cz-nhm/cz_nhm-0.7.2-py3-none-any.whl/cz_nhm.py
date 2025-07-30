# !/usr/bin/env python
# encoding: utf-8
from collections import OrderedDict, namedtuple

from commitizen import defaults as cz_defaults
from commitizen.cz.base import BaseCommitizen
from commitizen.cz.utils import multiple_line_breaker, required_validator

# CHANGE TYPES =========================================================================

ChangeType = namedtuple(
    'ChangeType', ['short_name', 'display_name', 'bump_type', 'description']
)

change_types = [
    ChangeType('BREAKING CHANGE', 'Breaking Changes', 'MAJOR', None),
    ChangeType('feat', 'Feature', 'MINOR', 'a new feature'),
    ChangeType('fix', 'Fix', 'PATCH', 'a bug fix'),
    ChangeType(
        'refactor',
        'Refactor',
        'PATCH',
        'a code change that neither fixes a bug nor adds a feature',
    ),
    ChangeType(
        'perf', 'Performance', 'PATCH', 'a code change that improves performance'
    ),
    ChangeType('docs', 'Docs', 'PATCH', 'documentation-only changes'),
    ChangeType('style', 'Style', 'PATCH', 'whitespace, formatting, etc'),
    ChangeType('test', 'Tests', 'PATCH', 'adds or fixes tests'),
    ChangeType(
        'build',
        'Build System(s)',
        'PATCH',
        'changes in build systems (e.g. pip or docker)',
    ),
    ChangeType(
        'ci', 'CI System(s)', None, 'changes in CI systems (e.g. github actions)'
    ),
    ChangeType(
        'chore', 'Chores/Misc', None, 'miscellaneous tasks like tidying up files'
    ),
    ChangeType('new', None, 'MINOR', 'explicitly bumps minor version'),
    ChangeType('patch', None, 'PATCH', 'explicitly bumps patch version'),
    ChangeType('bump', None, None, None),
    ChangeType('revert', None, None, None),
    ChangeType(
        'ui',
        'Minor UI Changes',
        'PATCH',
        'very minor UI fixes e.g. adding a contact email',
    ),
]


# PARSERS ==============================================================================


def parse_subject(text):
    """
    Strip input and ensure that it is not empty.
    """
    if isinstance(text, str):
        text = text.strip('.').strip()

    return required_validator(text, msg='Subject is required.')


def parse_issues(text):
    """
    Extract a list of issues from the input.
    """
    if isinstance(text, str):
        return [i.strip().strip('#') for i in text.split(',') if i != '']
    return []


def parse_scope(text):
    if not text:
        return

    scope = text.strip().split()
    if len(scope) == 1:
        return scope[0]

    return '-'.join(scope)


# COMMITIZEN CLASS =====================================================================


class NHMCz(BaseCommitizen):
    bump_pattern = cz_defaults.BUMP_PATTERN
    bump_map = OrderedDict(
        [(r'^.+!$', 'MAJOR')]
        + [(f'^{c.short_name}', c.bump_type) for c in change_types if c.bump_type]
    )
    bump_map_major_version_zero = OrderedDict(
        [
            (pattern, bump_type.replace('MAJOR', 'MINOR'))
            for pattern, bump_type in bump_map.items()
        ]
    )
    commit_parser = rf'^(?P<change_type>{"|".join([c.short_name for c in change_types if c.display_name])})(?:\((?P<scope>[^)\r\n]+)\))?: (?P<message>[^\n]+)'
    changelog_pattern = (
        rf'^({"|".join([c.short_name for c in change_types if c.display_name])})'
    )
    change_type_map = {
        c.short_name: c.display_name for c in change_types if c.display_name
    }
    change_type_order = [c.display_name for c in change_types if c.display_name]

    def questions(self) -> list:
        questions = [
            {
                'type': 'list',
                'name': 'prefix',
                'message': 'Select the type of change you are committing:',
                'choices': [
                    {
                        'value': c.short_name,
                        'name': f'{c.short_name}: {c.description}',
                    }
                    for c in change_types
                    if c.description
                ],
            },
            {
                'type': 'confirm',
                'name': 'is_breaking_change',
                'message': 'Is this a BREAKING CHANGE?',
                'default': False,
            },
            {
                'type': 'input',
                'name': 'scope',
                'filter': parse_scope,
                'message': 'What is the scope of this change? (press [enter] to skip)',
            },
            {
                'type': 'input',
                'name': 'subject',
                'filter': parse_subject,
                'message': 'Write a short and imperative summary of the code changes: (lower case and no period)',
            },
            {
                'type': 'input',
                'name': 'issues',
                'filter': parse_issues,
                'message': 'What issues does this commit close? (comma separated; press [enter] to skip)',
            },
            {
                'type': 'input',
                'name': 'body',
                'filter': multiple_line_breaker,
                'message': 'Provide additional contextual information about the commit, particularly any breaking '
                'changes: (use "|" for a new line; press [enter] to skip)',
            },
        ]
        return questions

    def message(self, answers: dict) -> str:
        prefix = answers['prefix']
        is_breaking_change = answers.get('is_breaking_change', False)
        scope = answers.get('scope')
        subject = answers.get('subject')
        issues = answers.get('issues', [])
        body = answers.get('body')

        message = f'{prefix}'
        if scope:
            message += f'({scope})'
        message += f': {subject}'
        if body:
            message += f'\n\n{body}'
        if is_breaking_change:
            # repeat the subject so the changelog can pick it up
            message += f'\n\nBREAKING CHANGE: {subject}'
        if len(issues) > 0:
            message += f'\n\nCloses: #{", #".join(issues)}'

        return message

    def example(self) -> str:
        """
        Used by cz example.
        """
        return (
            'fix(actions): make it stop doing the thing'
            '\n\n'
            'This action was doing a thing it was not supposed to'
            '\n\n'
            'Closes: #1, #3'
        )

    def schema(self) -> str:
        """
        Used by cz schema.
        """
        return (
            '<type>(<scope>): <subject>\n'
            '<BLANK LINE>\n'
            '<body>\n'
            '<BLANK LINE>\n'
            'BREAKING CHANGE: <subject>\n'
            '<BLANK LINE>\n'
            'Closes: <issues>'
        )

    def schema_pattern(self) -> str:
        return (
            r'(?s)'  # To explictly make . match new line
            rf'({"|".join([c for c in change_types if c.short_name != "BREAKING CHANGE"])})'  # type
            r'(\(\S+\))?!?:'  # scope
            r'( [^\n\r]+)'  # subject
            r'((\n\n.*)|(\s*))?$'
        )

    def changelog_message_builder_hook(self, parsed_message, commit):
        # ignore dist package build commits
        if (
            parsed_message['change_type'] == 'chore'
            and parsed_message['scope'] == 'dist'
        ):
            return False
        return parsed_message
