pipeline {
  agent any

  environment {
    VENV_DIR = "${WORKSPACE}/.venv"
    PYTHON = "python3"
    PIP = "${WORKSPACE}/.venv/bin/pip"
    PY = "${WORKSPACE}/.venv/bin/python"
  }

  stages {
    stage('Checkout') {
      steps {
        echo 'Checking out code...'
        checkout scm
      }
    }

    stage('Setup Python Environment') {
      steps {
        sh '''
          set -eux
          
          # Try to create venv, if it fails, install python3-venv
          if ! ${PYTHON} -m venv "${VENV_DIR}" 2>/dev/null; then
            echo "python3-venv not available, trying to install..."
            
            # Check if we have sudo access
            if command -v sudo >/dev/null 2>&1; then
              sudo apt update
              sudo apt install -y python3-venv python3-pip
            else
              # Try without sudo (might work if already root)
              apt update
              apt install -y python3-venv python3-pip
            fi
            
            # Try creating venv again
            ${PYTHON} -m venv "${VENV_DIR}"
          fi
          
          . "${VENV_DIR}/bin/activate"
          python -m pip install --upgrade pip setuptools wheel
        '''
      }
    }

    stage('Install Dependencies') {
      steps {
        sh '''
          set -eux
          . "${VENV_DIR}/bin/activate"
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt
          else
            echo "No requirements.txt, skipping."
          fi
        '''
      }
    }

    stage('Verify Data Files') {
      steps {
        sh '''
          set -eux
          test -f "auto-mpg-new.csv"
          echo "Data file auto-mpg-new.csv found."
        '''
      }
    }

    stage('Validate Python Syntax') {
      steps {
        sh '''
          set -eux
          . "${VENV_DIR}/bin/activate"
          python -m py_compile app.py
        '''
      }
    }

    stage('Check Imports') {
      steps {
        sh '''
          set -eux
          . "${VENV_DIR}/bin/activate"
          python - <<'PYCODE'
import sys
try:
    import panel
    import pandas
    import hvplot.pandas  # noqa
    import numpy
    print('All imports successful!')
    print('Panel:', panel.__version__)
    print('Pandas:', pandas.__version__)
    print('NumPy:', numpy.__version__)
except ImportError as e:
    print('Import error:', e)
    sys.exit(1)
PYCODE
        '''
      }
    }

    stage('Validate Application') {
      steps {
        sh '''
          set -eux
          . "${VENV_DIR}/bin/activate"
          python - <<'PYCODE'
import sys, pandas as pd
try:
    df = pd.read_csv('auto-mpg-new.csv')
    print(f'Data loaded: {len(df)} rows, {len(df.columns)} cols')
    assert len(df) > 0, 'Dataset is empty'
    for col in ('mpg','horsepower'):
        assert col in df.columns, f'{col} column not found'
    print('Application validation passed!')
except Exception as e:
    print('Validation error:', e)
    sys.exit(1)
PYCODE
        '''
      }
    }

    stage('Build Report') {
      steps {
        sh '''
          set -eux
          . "${VENV_DIR}/bin/activate"
          echo "==================================="
          echo "Build Report - PINIX7 Auto MPG Dashboard"
          echo "==================================="
          echo "Build Number: ${BUILD_NUMBER}"
          echo "Build Date: $(date)"
          echo "Workspace: ${WORKSPACE}"
          echo
          echo "Environment:"
          python --version
          pip --version
          echo
          echo "Installed Packages:"
          pip list | grep -E "(panel|pandas|hvplot|numpy|bokeh|holoviews)" || true
          echo
          echo "==================================="
          echo "Build Status: SUCCESS"
          echo "==================================="
        '''
      }
    }
  }

  post {
    success {
      echo '✅ Build completed successfully!'
      echo 'To run locally on server:'
      echo ". ${VENV_DIR}/bin/activate && panel serve app.py --allow-websocket-origin=<your-host>:<port>"
    }
    failure {
      echo '❌ Build failed! Check logs above.'
    }
    always {
      archiveArtifacts artifacts: '*.csv', allowEmptyArchive: true
      // cleanWs() // aktifkan jika ingin bersih-bersih workspace setiap build
    }
  }
}
