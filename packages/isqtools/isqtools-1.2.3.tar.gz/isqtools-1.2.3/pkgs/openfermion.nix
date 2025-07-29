{ lib
, buildPythonPackage
, fetchPypi
, # build-system
  setuptools
  #dep
, cirq-core
, deprecation
, h5py
, networkx
, numpy
, requests
, scipy
, sympy
, ...
}:
buildPythonPackage rec {
  pname = "openfermion";
  version = "1.7.0";
  format = "setuptools";

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-Fyh2jDGLUOWKiIpGV8LoejkRECLv8y93KfPtpynagag=";
  };

  build-system = [ setuptools ];

  dependencies = [
    cirq-core
    deprecation
    h5py
    networkx
    numpy
    requests
    scipy
    sympy
  ];

  nativeBuildInputs = [ ];
  buildInputs = [ ];

  doCheck = false;

  meta = { };
}
