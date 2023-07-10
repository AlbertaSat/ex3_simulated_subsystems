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

### Code styling
- All python files in this repository must follow pylint coding format and style. An automatic workflow action will test your code against theses standards automatically upon any request to merge with main. It is suggested to install a pylint linter extension in your IDE of choice to write code that follows these standards as you go. 
- Ensure that every source file written has associated 'author' and 'copyright' metadata included in the file (for now it is found in the bottom, two lines after all code). Because these items will exist in every source file pylint is explicitly told to ignore them
