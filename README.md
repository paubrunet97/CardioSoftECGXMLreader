# CardioSoftECGXMLreader

Python class for reading CardioSoft ECG XML files. Extracts lead voltages with and info contained in the XML file created by CardioSoft.

```python
from CardioSoftECGXMLreader import CardioSoftECGXMLreader

a = CardioSoftECGXMLReader('filename.XML') #Create a CardioSoftECGXMLreader class

a.getVoltages() # Extract voltages as an array of size (samplesize, 12)

a.plotLead('LeadName') # Plot a lead
```
