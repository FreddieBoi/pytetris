import sys
import getopt
from pytetris import __version__, __package__, Game

usage = """\
Usage: pytetris [OPTION]

       -v --version  Display version information
       -h --help     Display this text.
       
       Run without any flags to play.
"""

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv", ["help", "version"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print "\n    "+str(err)+"\n" # will print something like "option -a not recognized"
        print usage
        sys.exit(2)
    if len(opts) > 1:
        print "\n    "+"only 1 option at a time is allowed"+"\n"
        print usage
        sys.exit(2)
    for o, a in opts:
        if o in ("-v", "--version"):
            #Print info
            print __package__ + " v" + __version__
            sys.exit()
        elif o in ("-h", "--help"):
            #Print help
            print usage
            sys.exit()
        else:
            assert False, "unhandled option"
    
    #Start it up!
    Main().run()
                        
class Main(object):

    #Handle exiting actions
    def quit(self):
        print "terminating.."
        sys.exit()

    #Restart the game
    def restart(self):
        print "restarting.."
        self.run()
        
    def run(self):
        print "running.."
        self.game = Game(self)
        self.game.run()
        return self.game
        
    def get_game(self):
        return self.game
        
if __name__ == '__main__':
    main()
