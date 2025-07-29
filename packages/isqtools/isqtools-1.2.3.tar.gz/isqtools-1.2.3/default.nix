{ lib
, buildPythonPackage
  # build-system
, hatchling
  # dependencies
, numpy
, requests
, autograd
  # gitignore
, gitignoreSource
, ...
}:
buildPythonPackage rec {
  pname = "isqtools";
  version = "1.2.3";
  src = gitignoreSource ./.;

  pyproject = true;

  build-system = [ hatchling ];
  dependencies = [ numpy autograd requests ];
  nativeBuildInputs = [ ];
  buildInputs = [ ];

  doCheck = false;

  meta = { };
}
