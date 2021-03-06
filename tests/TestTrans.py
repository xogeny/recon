from recon.trans import wall2meld, dsres2meld

from recon.wall import WallReader, WallWriter
from recon.meld import MeldReader, MeldWriter

from TestWall import write_wall

from nose.tools import *
import os

def testWall2Meld():
    write_wall(verbose=True);

    wfile = os.path.join("test_output","sample.wll")
    mfile =  os.path.join("test_output","sample.mld")
    wall2meld(wfile, mfile)

    with open(os.path.join("test_output","sample.mld"), "rb") as fp:
        meld = MeldReader(fp, verbose=True)

        print "Objects:"
        for objname in meld.objects():
            obj = meld.read_object(objname)
            print "  "+objname+" = "+str(obj)

        print "Tables:"
        for tabname in meld.tables():
            table = meld.read_table(tabname)
            print "  "+tabname
            for signal in table.signals():
                print "    #"+signal+": "+str(table.data(signal))

        print "table.metadata = "+str(table.metadata)
        print "table.var_metadata = "+str(table.var_metadata)

        assert_equals(meld.metadata, {"a": "bar"})
        assert_equals(table.signals(), ["time", "x", "y", "active", "a", "b", "inactive"])
        assert_equals(table.data("time"), [0.0, 1.0, 2.0])
        assert_equals(table.metadata, {"model": "Foo"})
        assert_equals(table.var_metadata["time"], {"units": "s"})
        assert_equals(table.data("x"), [1.0, 0.0, 1.0])
        assert_equals(table.data("y"), ["2.0", "3.0", "3.0"])
        assert_equals(table.data("a"), [1.0, 2.0, 1.0])
        assert_equals(table.data("b"), ["2.0", "3.0", "3.0"])

def testDsres2Meld():
    mfile = os.path.join("test_output","dsres.mld")
    dsres2meld("tests/dsres.mat", mfile, verbose=True, compression=False)

    meld = MeldReader(mfile, verbose=True)
    print str(meld.report())

def testDsres2Meld_Compression():
    with open(os.path.join("test_output","dsres_comp.mld"), "wb") as fp:
        dsres2meld("tests/dsres.mat", fp, verbose=True, compression=True)

    with open(os.path.join("test_output","dsres_comp.mld"), "rb") as fp:
        meld = MeldReader(fp, verbose=True)
        print str(meld.report())

def testDsres2Meld_Robot():
    with open(os.path.join("test_output","dsres_robot.mld"), "wb") as fp:
        dsres2meld("tests/fullRobot.mat", fp, verbose=False, compression=False)

    with open(os.path.join("test_output","dsres.mld"), "rb") as fp:
        meld = MeldReader(fp, verbose=False)
        print str(meld.report())

def testDsres2Meld_Compression_Robot():
    with open(os.path.join("test_output","dsres_robot_comp.mld"), "wb") as fp:
        dsres2meld("tests/fullRobot.mat", fp, verbose=False)

    with open(os.path.join("test_output","dsres_comp.mld"), "rb") as fp:
        meld = MeldReader(fp, verbose=False)
        print str(meld.report())

