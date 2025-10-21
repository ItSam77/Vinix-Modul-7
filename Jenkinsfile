pipeline {
    agent any
    
    environment {
        // Python virtual environment path
        VENV_DIR = 'venv'
        // Python executable
        PYTHON = 'python'
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
                echo 'Setting up Python virtual environment...'
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv ${VENV_DIR}
                            . ${VENV_DIR}/bin/activate
                            pip install --upgrade pip
                        '''
                    } else {
                        bat '''
                            python -m venv %VENV_DIR%
                            call %VENV_DIR%\\Scripts\\activate.bat
                            python -m pip install --upgrade pip
                        '''
                    }
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                script {
                    if (isUnix()) {
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            call %VENV_DIR%\\Scripts\\activate.bat
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }
        
        stage('Verify Data Files') {
            steps {
                echo 'Verifying required data files exist...'
                script {
                    if (isUnix()) {
                        sh '''
                            if [ ! -f "auto-mpg-new.csv" ]; then
                                echo "Error: auto-mpg-new.csv not found!"
                                exit 1
                            fi
                            echo "Data file auto-mpg-new.csv found."
                        '''
                    } else {
                        bat '''
                            if not exist "auto-mpg-new.csv" (
                                echo Error: auto-mpg-new.csv not found!
                                exit /b 1
                            )
                            echo Data file auto-mpg-new.csv found.
                        '''
                    }
                }
            }
        }
        
        stage('Validate Python Syntax') {
            steps {
                echo 'Validating Python syntax...'
                script {
                    if (isUnix()) {
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            python -m py_compile app.py
                        '''
                    } else {
                        bat '''
                            call %VENV_DIR%\\Scripts\\activate.bat
                            python -m py_compile app.py
                        '''
                    }
                }
            }
        }
        
        stage('Check Imports') {
            steps {
                echo 'Checking if all imports are available...'
                script {
                    if (isUnix()) {
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            python -c "
import sys
try:
    import panel
    import pandas
    import hvplot.pandas
    import numpy
    print('All imports successful!')
    print(f'Panel version: {panel.__version__}')
    print(f'Pandas version: {pandas.__version__}')
    print(f'NumPy version: {numpy.__version__}')
except ImportError as e:
    print(f'Import error: {e}')
    sys.exit(1)
"
                        '''
                    } else {
                        bat '''
                            call %VENV_DIR%\\Scripts\\activate.bat
                            python -c "import sys; import panel; import pandas; import hvplot.pandas; import numpy; print('All imports successful!'); print(f'Panel version: {panel.__version__}'); print(f'Pandas version: {pandas.__version__}'); print(f'NumPy version: {numpy.__version__}')"
                        '''
                    }
                }
            }
        }
        
        stage('Validate Application') {
            steps {
                echo 'Validating application can load...'
                script {
                    if (isUnix()) {
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            python -c "
import sys
import pandas as pd

# Test data loading
try:
    df = pd.read_csv('auto-mpg-new.csv')
    print(f'Data loaded successfully: {len(df)} rows, {len(df.columns)} columns')
    
    # Basic validation
    assert len(df) > 0, 'Dataset is empty'
    assert 'mpg' in df.columns, 'mpg column not found'
    assert 'horsepower' in df.columns, 'horsepower column not found'
    
    print('Application validation passed!')
except Exception as e:
    print(f'Validation error: {e}')
    sys.exit(1)
"
                        '''
                    } else {
                        bat '''
                            call %VENV_DIR%\\Scripts\\activate.bat
                            python -c "import sys; import pandas as pd; df = pd.read_csv('auto-mpg-new.csv'); print(f'Data loaded successfully: {len(df)} rows'); print('Application validation passed!')"
                        '''
                    }
                }
            }
        }
        
        stage('Build Report') {
            steps {
                echo 'Generating build report...'
                script {
                    if (isUnix()) {
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            echo "==================================="
                            echo "Build Report - PINIX7 Auto MPG Dashboard"
                            echo "==================================="
                            echo "Build Number: ${BUILD_NUMBER}"
                            echo "Build Date: $(date)"
                            echo "Workspace: ${WORKSPACE}"
                            echo ""
                            echo "Environment:"
                            python --version
                            pip --version
                            echo ""
                            echo "Installed Packages:"
                            pip list | grep -E "(panel|pandas|hvplot|numpy|bokeh|holoviews)"
                            echo ""
                            echo "==================================="
                            echo "Build Status: SUCCESS"
                            echo "==================================="
                        '''
                    } else {
                        bat '''
                            call %VENV_DIR%\\Scripts\\activate.bat
                            echo ===================================
                            echo Build Report - PINIX7 Auto MPG Dashboard
                            echo ===================================
                            echo Build Number: %BUILD_NUMBER%
                            echo Build Date: %DATE% %TIME%
                            echo Workspace: %WORKSPACE%
                            echo.
                            echo Environment:
                            python --version
                            pip --version
                            echo.
                            echo Installed Packages:
                            pip list | findstr /i "panel pandas hvplot numpy bokeh holoviews"
                            echo.
                            echo ===================================
                            echo Build Status: SUCCESS
                            echo ===================================
                        '''
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo '✅ Build completed successfully!'
            echo 'The PINIX7 Auto MPG Dashboard is ready to deploy.'
            echo 'To run the dashboard manually: panel serve app.py'
        }
        failure {
            echo '❌ Build failed! Please check the logs above.'
        }
        always {
            echo 'Cleaning up...'
            // Archive build artifacts if needed
            archiveArtifacts artifacts: '*.csv', allowEmptyArchive: true
        }
    }
}

