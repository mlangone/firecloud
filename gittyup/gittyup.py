import sys

import formatters
import github
import releasenotes


def _estimate_next_version(notes):
    last_version = github.find_last_release(repo)
    return releasenotes.estimate_next_version(last_version, notes)


if __name__ == '__main__':
    repo = 'firebase/firebase-admin-dotnet'
    pulls = [ pull for pull in github.find_pulls_since_last_release(repo) if pull.has_release_notes ]
    if not pulls:
        print('Could not find any pull requests labeled with release-notes')
        sys.exit(1)

    print('Extracting release notes from {0} pull requests...'.format(len(pulls)))
    notes = []
    for pull in pulls:
        print('{0}: {1}'.format(pull.number, pull.title))
        notes.extend(releasenotes.get_release_notes_from_pull(pull))
    print()

    next_version = _estimate_next_version(notes)

    print('Devsite release notes')
    print('=====================')
    print(formatters.DevsiteFormatter(next_version).printable_output(notes))

    print('Github release notes')
    print('====================')
    print(formatters.GitHubFormatter(next_version).printable_output(notes))
