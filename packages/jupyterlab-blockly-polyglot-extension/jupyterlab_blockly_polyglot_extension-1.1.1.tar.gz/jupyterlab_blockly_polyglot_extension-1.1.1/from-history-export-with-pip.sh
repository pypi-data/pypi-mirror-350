# Optional argument for output file (defaults to environment.yml)
output_file="${1:-environment.yml}"

# Extract installed pip packages (with colon)
pip_packages=$(conda env export | grep -A9999 ".*- pip:" | grep -v "^prefix: ")

# Export conda environment with history (without builds) and store in a variable
conda_env=$(conda env export --from-history | grep -v "^prefix: ")

# Check if conda env already includes "- pip" line (without colon)
if ! grep -q "  - pip" <<<"$conda_env"; then
  # Add the line with correct indentation if missing
  conda_env=$(printf '%s\n  - pip' "$conda_env")
fi

# Combine conda env and pip packages into a single YAML string
environment_yml="${conda_env}\n${pip_packages}"

# Write the combined YAML to the specified or default file
echo -e "$environment_yml" > "$output_file"

# Print a success message
echo "Exported environment to: $output_file"
