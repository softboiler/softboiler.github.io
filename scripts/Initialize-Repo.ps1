<#.SYNOPSIS
Initialize repository.#>
. scripts/Initialize-Shell.ps1
git init

# Modify GitHub repo later on only if there were not already commits in this repo
try { git rev-parse HEAD }
catch [System.Management.Automation.NativeCommandExitException] { $fresh = $true }

git add .
git commit --no-verify -m 'Prepare template using blakeNaccarato/copier-python'
git submodule add --force --name template 'https://github.com/blakeNaccarato/copier-python.git' submodules/template
git add .
git commit --no-verify -m 'Add template and type stub submodules'
scripts/Sync-Py.ps1
Set-Env
git add .
git commit --no-verify -m 'Lock'

# Modify GitHub repo if there were not already commits in this repo
if ($fresh) {
    if (!(git remote)) {
        git remote add origin 'https://github.com/softboiler/softboiler.github.io.git'
        git branch --move --force main
    }
    gh repo edit --description "$((Get-Content '.copier-answers.yml' |
    Select-String -Pattern '^project_description:\s(.+)$').Matches.Groups[1].value)"
    gh repo edit --homepage 'https://softboiler.github.io/softboiler.github.io/'
}

git push --set-upstream origin main
