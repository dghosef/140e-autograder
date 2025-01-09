# Making a private repo instructions. If you know have an alternate way you'd like to do this, feel free to skip:
- Go to github and make a new repo. *Make sure it's private*
- Go to your cs140e-25win directory and run `git remote add submit <your repo url>`
- Run `git push submit main`
- If you get an error in your push becuase you don't have access to your private repo, ask chatgpt "how to configure your command line to have access to your git private repos"
- Give Joe edit access to your repo in Settings > Collaborators on Github. Joe's github username is `dghosef`

# Turn in instructions
- Modify the `sunet`, `repo`, and `lab` variables in `sender.py` accordingly
- Make sure you repository is updated
- Run `python sender.py`. After about a minute, you should see the output of the autograder in in your `checkoffs` directory
- Ask Joe if it's not working
