import sys

import uvicorn

sys.exit(uvicorn.run("test_ta_da.main:app", reload=True))
