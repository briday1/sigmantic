# Sigmantic Project

Sigmantic is a signal processing project focused on geolocation and tracking using TDOA (Time Difference of Arrival) and FDOA (Frequency Difference of Arrival) techniques. The project provides a modular framework for signal processing, estimation, and multilateration.

## Tech Stack

- **Language:** Python 3
- **Core Libraries:**
  - numpy - Numerical computing
  - scipy - Scientific computing
  - sympy - Symbolic mathematics
  - matplotlib - Visualization
  - plantuml - Diagram generation

## Project Structure

- `blocks/` - Signal processing blocks and estimators
  - `base.py` - Base classes for processing blocks
  - `matched_filter.py` - Matched filter implementation
  - `tdoa_estimator.py` - Time Difference of Arrival estimator
  - `fdoa_estimator.py` - Frequency Difference of Arrival estimator
  - `multilaterator.py` - Multilateration algorithms
- `chain/` - Processing chain implementation
  - `chain.py` - Chain orchestration and data flow
- `symbolic/` - Symbolic mathematics for predictions
  - `prediction.py` - Prediction algorithms
- `demo/` - Demonstration and test data
  - `synth_data.py` - Synthetic data generation
  - `run_demo.py` - Demo runner
  - `chain_diagram.puml` - PlantUML diagram for chain visualization

## Coding Guidelines

### General Principles
- Write clear, modular, and reusable code
- Follow Python PEP 8 style guidelines
- Use type hints where appropriate for better code clarity
- Keep functions focused on a single responsibility

### Naming Conventions
- Use `snake_case` for functions, variables, and file names
- Use `PascalCase` for class names
- Use descriptive names that clearly indicate purpose

### Documentation
- Include docstrings for all public classes and functions
- Document parameters, return values, and any exceptions raised
- Add inline comments for complex algorithms or non-obvious logic

### Signal Processing Best Practices
- Validate input dimensions and data types
- Handle edge cases (e.g., empty arrays, invalid configurations)
- Use numpy/scipy efficiently, avoiding Python loops where possible
- Document assumptions about signal formats and coordinate systems

## Build, Test, and Validation

### Building
- Install dependencies: `pip install -r requirements.txt`
- Generate diagrams: `make diagram`

### Testing
- Currently, the project uses manual testing through demo scripts
- Run demos: `python demo/run_demo.py`
- Generate synthetic test data: `python demo/synth_data.py`

### Validation
- Ensure code runs without errors on demo data
- Verify numerical accuracy of estimations
- Check visualization outputs for correctness

## Development Workflow

1. Make changes to the relevant module in `blocks/`, `chain/`, or `symbolic/`
2. Test changes using the demo scripts
3. Update documentation if adding new features or changing interfaces
4. Generate diagrams if modifying the processing chain

## Resources

- **numpy documentation:** https://numpy.org/doc/
- **scipy documentation:** https://scipy.org/doc/
- **sympy documentation:** https://docs.sympy.org/
- **TDOA/FDOA Geolocation:** Standard techniques for passive geolocation using signal timing and frequency differences
- **Multilateration:** Mathematical technique for determining position from multiple distance measurements
