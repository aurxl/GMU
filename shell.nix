{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
      sshpass
      pandoc
      poetry
      python39
    ];

  shellHook = ''
    export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
    poetry env use $(which python)
    source $(poetry env info --path)/bin/activate
  '';

}
