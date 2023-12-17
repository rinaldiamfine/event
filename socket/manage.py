from distutils.log import debug
import uvicorn
from app import app, configuration
import os
_basedir = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
    # uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=True, debug=True)