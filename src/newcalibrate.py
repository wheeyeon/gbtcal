import numpy

class Calibrate(object):
    def calibrate():
        pass
    # def __init__(self, attenuator):
    #     self.attenuator = attenuator

    # def attenuate(self, table, pol, feed=None):
    #     if not self.attenuator:
    #         raise ValueError("No attenuator instance provided! "
    #                          "Only non-attenuated calibrations "
    #                          "are possible")
    #     self.attenuator.attenuate(table, pol, feed)

class InterStreamCalibrate(Calibrate):
    def calibrate():
        pass

# class IntraStreamCalibrate(Calibrate):
#     def calibrate():
#         pass

class InterBeamCalibrate(InterStreamCalibrate):
    def getSigRefFeeds(self, table):
        feeds = table.getUnique('FEED')
        trackBeam = table.meta['TRCKBEAM']

        if len(feeds) < 2:
            raise ValueError("Must have at least two feeds to determine "
                             "the tracking/reference feeds")
        if len(feeds) > 2:
            wprint("More than two feeds provided; selecting second feed as "
                   "reference feed!")

        if trackBeam == feeds[0]:
            sig = feeds[0]
            ref = feeds[1]
        else:
            sig = feeds[1]
            ref = feeds[0]

        return sig, ref

    def attenuate(self, table, pol=None):
        sigFeed, refFeed  = self.getSigRefFeeds(table)
        attenSigData = self.attenuate(table, pol, feed=sigFeed)
        attenRefData = self.attenuate(table, pol, feed=refFeed)
        return attenSigData, attenRefData

class OofCalibrate(InterBeamCalibrate):
    def calibrate(self, table, calTable):
        sigFeed, refFeed  = self.getSigRefFeeds(table)
        sigFeedTcal = table.query(FEED=sigFeed)['FACTOR'][0]
        refFeedTcal = table.query(FEED=refFeed)['FACTOR'][0]

        tcalQuot = refFeedTcal / sigFeedTcal

        sigFeedCalib = calTable.query(FEED=sigFeed)['DATA'][0]
        refFeedCalib = calTable.query(FEED=refFeed)['DATA'][0]

        # OOF gets this backwards, so so will us
        # TODO: We are not really sure why this arrangement works, but it does
        return (refFeedCalib * tcalQuot) - sigFeedCalib


class BeamSubtractionDBA(InterBeamCalibrate):
    def calibrate(self, sigFeedCalData, refFeedCalData):
        """Here we're just finding the difference between the two beams"""
        return sigFeedCalData - refFeedCalData


class InterPolAverage(InterStreamCalibrate):
    def calibrate(self, data):
        if len(data) != 2:
            raise ValueError("InterPolAverage requires exactly two polarizations to be given")

        return numpy.mean(data['DATA'], axis=0)
