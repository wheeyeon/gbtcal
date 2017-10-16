// This is the name given to the virtual environment for
// this build
venv_name = "testing-gbtcal-env"

def installPythonPackages() {

    sh """virtualenv -p /opt/local/bin/python2.7 ${venv_name}
    source ${venv_name}/bin/activate
    pip install -U pip setuptools
    pip install -r requirements.txt"""
}

def testPython() {
    sh """source ./${venv_name}/bin/activate
    cd src
    nosetests --nocapture test_calibrator.py"""
}

node {
    stage('cleanup') {
        deleteDir()
    }

    stage('checkout') {
        checkout scm
    }

    stage('install') {
        try {
            installPythonPackages()
        } catch(error) {
            notify(failure, 'An error has occurred during the <b>install</b> stage.')
            throw(error)
        }
    }

    stage('test') {
        try {
            testPython()
        } catch(error) {
            notify(failure, 'An error has occurred during the <b>test</b> stage.')
            throw(error)
        }
    }    
}    
