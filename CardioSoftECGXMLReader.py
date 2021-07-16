import xmltodict
import numpy as np
import matplotlib.pyplot as plt

class CardioSoftECGXMLReader:
    """ Extract voltage data from a CardioSoftECG XML file """

    def __init__(self, path, encoding="ISO8859-1"):
        with open(path, 'rb') as xml:
            self.Data = xmltodict.parse(xml.read().decode(encoding))['CardiologyXML']

            if 'StripData' in self.Data:
                self.StripData = self.Data['StripData']
                self.FullDisclosure = False

                self.SamplingRate = int(self.StripData['SampleRate']['#text'])
                self.NumLeads = int(self.StripData['NumberOfLeads'])
                self.WaveformData = self.StripData['WaveformData']

                self.Segmentations = {}

                try:
                    self.Segmentations['Pon'] = int(self.Data['RestingECGMeasurements']['POnset']['#text'])
                except:
                    self.Segmentations['Pon'] = float('NaN')

                try:
                    self.Segmentations['Poff'] = int(self.Data['RestingECGMeasurements']['POffset']['#text'])
                except:
                    self.Segmentations['Poff'] = float('NaN')

                try:
                    self.Segmentations['QRSon'] = int(self.Data['RestingECGMeasurements']['QOnset']['#text'])
                except:
                    self.Segmentations['QRSon'] = float('NaN')

                try:
                    self.Segmentations['QRSoff'] = int(self.Data['RestingECGMeasurements']['QOffset']['#text'])
                except:
                    self.Segmentations['QRSoff'] = float('NaN')

                try:
                    self.Segmentations['Toff'] = int(self.Data['RestingECGMeasurements']['TOffset']['#text'])
                except:
                    self.Segmentations['Toff'] = False


            elif 'FullDisclosure' in self.Data:
                self.StripData = False
                self.FullDisclosure = self.Data['FullDisclosure']

                self.SamplingRate = int(self.FullDisclosure['SampleRate']['#text'])
                self.NumLeads = int(self.FullDisclosure['NumberOfChannels'])
                self.FullDisclosureData = self.FullDisclosure['FullDisclosureData']['#text']
                self.Segmentations = False


            self.LeadVoltages = self.makeLeadVoltages()

    def makeLeadVoltages(self):

        leads = {}

        if not self.FullDisclosure:
            for lead in self.WaveformData:
                lead_name = lead['@lead']
                lead_voltages = np.array([int(volt) for volt in lead['#text'].split(',')])
                leads[lead_name] = lead_voltages

        elif not self.StripData:
            voltages_str = self.FullDisclosureData.split(',')

            voltage_lines = []
            voltage_line = []
            for volt in voltages_str:
                if '\n' in volt:
                    voltage_lines.append(voltage_line)
                    voltage_line = []
                    voltage_line.append(int(volt))

                elif volt == '':
                    voltage_lines.append(voltage_line)

                else:
                    voltage_line.append(int(volt))

            LeadOrder = self.FullDisclosure['LeadOrder'].split(',')

            for lead_name in LeadOrder:
                leads[lead_name] = []

            for lead_num in np.arange(0, self.NumLeads):
                for i in np.arange(lead_num, len(voltage_lines), self.NumLeads):
                    leads[LeadOrder[lead_num]] = leads[LeadOrder[lead_num]] + voltage_lines[i]
                leads[LeadOrder[lead_num]] = np.array(leads[LeadOrder[lead_num]])

        return leads

    def getVoltages(self):
        voltage_array = []
        for lead in self.LeadVoltages:
            if  len(voltage_array) == 0:
                voltage_array = np.transpose(self.LeadVoltages[lead][np.newaxis])
            else:
                voltage_array = np.hstack((voltage_array, np.transpose(self.LeadVoltages[lead][np.newaxis])))

        return voltage_array

    def plotLead(self, lead):
        plt.plot(self.LeadVoltages[lead])
        plt.show()
