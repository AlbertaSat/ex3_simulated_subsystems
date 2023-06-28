## Contributing

### Branch naming conventions: 
The following branch naming conventions must be followed. Any PR not in compliance will be denied. The naming convention going is as follows:

<name_of_author>/<branch_type>/<description_of_branch>

The following is a list of possible branch types:   
- feature
- testing
- bugfix
- hotfix
- documentation

### Branching etiquette
- Branches must implement/change only a single feature. Changes related to that feature across different layers of code is acceptable.
- If you discover a bug unrelated to the feature you are working on, switch back to master, make a branch to fix the bug, then make a PR to merge that Bugfix. Chances are you aren't the only one experiencing the bug. You may rebase your development branch off the Bugfix branch.
- Branches that do not describe what they are changing will not be accepted.