from libs import BeijingTiku
import sys
from libs.except_hook import except_hook

sys.excepthook = except_hook

if __name__ == "__main__":

    app = BeijingTiku()
    app.run()
