# WARNING: This file was automatically generated. You should avoid editing it.
# If you run pynixify again, the file will be either overwritten or
# deleted, and you will lose the changes you made to it.

{ buildPythonPackage, fetchPypi, lib }:

buildPythonPackage rec {
  pname = "werkzeug";
  version = "2.0.3";

  src = fetchPypi {
    inherit version;
    pname = "Werkzeug";
    sha256 = "0g1dh9is2l5axsn0skdswm5in5j1n0l9wz06nrj22lkw0pzzhqxq";
  };

  # TODO FIXME
  doCheck = false;

  meta = with lib; { };
}
