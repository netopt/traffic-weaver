const pyproject_toml = {
  filename: "pyproject.toml",
  updater: "./commit-and-tag-version-to-toml.js",
};

const python_module = {
  filename: "src/traffic_weaver/_version.py",
  updater: "./commit-and-tag-version-to-toml.js",
}

module.exports = {
  bumpFiles: [pyproject_toml, python_module],
  packageFiles: [pyproject_toml],
};
