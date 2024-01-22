with import ./pynixify/nixpkgs.nix { };
let
  version = builtins.head (builtins.match ".*'([0-9]+.[0-9]+(.[0-9]+)?)'.*"
    (builtins.readFile ./bogcode/__init__.py));
in { useLastCommit ? true }: rec {

  bogcode-server = python3.pkgs.bugcode.overrideAttrs (old:
    assert !builtins.hasAttr "checkInputs" old; {
      name = "bogcode-server-${version}";
      doCheck = true;
      checkPhase = "true";
    } // lib.optionalAttrs useLastCommit {
      src = builtins.fetchGit {
        url = ./.;
        ref = "HEAD";
      };
    });
}
