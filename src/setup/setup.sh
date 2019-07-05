mkdir ~/performance_tracker-worktree
mkdir ~/performance_tracker-worktree/logs
mkdir ~/performance_tracker-gitdir
git init --bare ~/performance_tracker-gitdir
cp post-receive.sample ~/performance_tracker-gitdir/hooks/post-receive
chmod +x ~/performance_tracker-gitdir/hooks/post-receive
echo "Bare git repo setup to receive pushes in ~/performance_tracker-gitdir and deploy"
