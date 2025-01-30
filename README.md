# rcode-lab

Laborotary works with Radiacode spectrometer.

Uses OstapHEP software package. For more information see: https://github.com/OstapHEP/ostap.

## eff_calib

A standard sources has been used. Setups are shown at attached photos.

Spectra can be found in `spectra/sources/`

Sources:
  * Cs-137 (activity of  9.2 kBq as on 2019-10-18)
  * Eu-150 (activity of 38.2 kBq as on 2019-10-18)
  * Co-60  (activity of 25.2 kBq as on 2019-10-18)

Scripts:
  * `draw.py` - draw raw spectrum in channels (without energy calibration)
  * `draw_wo_bkg.py` - perform backgound subtruction



