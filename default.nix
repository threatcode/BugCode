# Running nix-build will build will build Bugcode using the current directory
# as source. Untracked or modified files will be used
(import ./release.nix { useLastCommit = false; }).bugcode-server
