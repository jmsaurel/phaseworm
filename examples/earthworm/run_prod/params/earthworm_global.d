#  
#
#                    earthworm_global.d
#
#      !!!!   DO NOT make any changes to this file.  !!!!
#
#  The contents of this file are under the control of Earthworm Central.
#       Please direct any requested additions or changes to:
#
#             Mitch Withers    mwithers at memphis dot edu
#
#  The values defined in earthworm_global.d are critical to proper 
#  communication and data attribution among Earthworm systems around 
#  the globe. 
#
#  A copy of earthworm_global.d should be placed in your EW_PARAMS directory.
#
#  The master copy of earthworm_global.d resides in the vX.XX/environment
#  directory of this Earthworm distribution.
#

#--------------------------------------------------------------------
#                        Installation IDs
#
#   The character string <-> numerical value mapping for all
#   installations are assigned and controlled by the Earthworm 
#   Development Team at the USGS in Golden, CO.  These mappings
#   must remain globally unique in order for exchanged data 
#   to be properly attributed to the installation that created it.
#
#   0-255 are the only valid installation ids.
#
# The maximum length of installation string is 32 characters.
#
#--------------------------------------------------------------------

 Installation   INST_WILDCARD      0   # Sacred wildcard value - DO NOT CHANGE!!!
 Installation   INST_FAIRBANKS     1   # University of Alaska, Fairbanks
 Installation   INST_UW            2   # University of Washington, Seattle
 Installation   INST_MENLO         3   # USGS Menlo Park
 Installation   INST_CIT           4   # Caltech
 Installation   INST_UTAH          5   # University of Utah, Salt Lake City
 Installation   INST_MEMPHIS       6   # University of Memphis (CERI)
 Installation   INST_UNR           7   # University of Nevada, Reno
 Installation   INST_UCB           8   # University of California, Berkeley
 Installation   INST_PTWC          9   # NOAA, Pacific Tsunami Warning Center
 Installation   INST_IDA          10   # IRIS, International Deployment of Accelerometers (Scripps, UC San Diego)
 Installation   INST_NC           11   # University of North Carolina (?)
 Installation   INST_VT           12   # Virginia Tech
 Installation   INST_USNSN        13   # USGS National Seismic Network
 Installation   INST_RICKS        14   # Ricks College, BYU Idaho
 Installation   INST_HVO          15   # USGS, Hawaii Volcano Observatory
 Installation   INST_ATWC         16   # NOAA, Alaska Tsunami Warning Center
 Installation   INST_PGE          17   # Pacific Gas and Electric
 Installation   INST_PNNL         18   # DOE, Pacific Northwest National Lab
 Installation   INST_PGC          19   # Pacific Geoscience Center, Candada
 Installation   INST_AVO          20   # USGS, Alaska Volcano Observatory
 Installation   INST_BUTTE        21   # University of Montana
 Installation   INST_LAMONT       22   # LDEO, Columbia University
 Installation   INST_SC_CHA       23   # University of South Carolina, Columbia (Charleston node)
 Installation   INST_STLOUIS      24   # Saint Louis University
 Installation   INST_NMT          25   # New Mexico Tech
 Installation   INST_CVO          26   # USGS, Cascades Volcano Observatory
 Installation   INST_SC_COL       27   # University of South Carolina, Columbia
 Installation   INST_PRSN         28   # Puerto Rico Seismic Network
 Installation   INST_TEMP1        29   # Temporary for long forgotten purpose (?)
 Installation   INST_SOAPP        30   # Southern Appalachian Cooperative Seismic Network (CERI)
 Installation   INST_UO           31   # University of Oregon
 Installation   INST_USBR         32   # U.S. Bureau of Reclamation (?)
 Installation   INST_UTIG         33   # Institute for Geophysics, University of Texas, Austin
 Installation   INST_PSU          34   # Penn State University
 Installation   INST_INEL         35   # DOE, Idaho National Lab
 Installation   INST_SISMALP      36   #
 Installation   INST_MIT          37   # Massachussetts Institute of Technology
 Installation   INST_GSC          38   # Geological Survey of Canada
 Installation   INST_IRISDMC      39   # IRIS Data Management Center, Seattle
 Installation   INST_BOZEMAN      40   # Montana State University
 Installation   INST_UTK          41   # University of Tennessee, Knoxville
 Installation   INST_CDWR         42   # California Division of Water Resources 
 Installation   INST_WO           43   # Weston Observatory, Boston College
 Installation   INST_NAZ          44   # Northern Arizona University
 Installation   INST_MVO          45   #
 Installation   INST_LASN         46   # Los Alamos Seismic Network (?)
 Installation   INST_NAU          47   #
 Installation   INST_KO           48   #
 Installation   INST_DIGITEXX     49   #
 Installation   INST_DTA          50   # Digital Technology Associates
 Installation   INST_STACHELTIER  51   #
 Installation   INST_CWB          52   #
 Installation   INST_EDI          53   #
 Installation   INST_MI           54   # Michigan (?)
 Installation   INST_URBAN-HZ     55   # USGS Urban Hazards project (?)
 Installation   INST_EREBUS       56   # New Mexico Tech, Mt Erebus, Antarctica network
 Installation   INST_SGS          57   #
 Installation   INST_UNAVCO       58   # University Navstar Consortium
 Installation   INST_USGSMAG      59   # USGS National Geomagnetism Program
 Installation   INST_KACST        60   # King Abdulaziz City for Science & Technology
 Installation   INST_OVSM         61   # Ob. Vol. de la Montagne Pelee
 Installation   INST_COSO         62   #  Keith Richards-Dinger Coso Geothermalm NAWS
 Installation   INST_CGS          63   #  California Geological Survey
 Installation   INST_GEYSERS      64   #  Lawrence Berkeley Lab - Geysers Network
 Installation   INST_GSL          65   #  Guralp Systems Limited
 Installation   INST_UKY          66   #  University of Kentucky
 Installation   INST_POLARIS      67   #  POLARIS - Canada geophysical research
 Installation   INST_NISN         68   #  Norther Idaho Seismic Network- Ken Sprenke
 Installation   INST_KSU          69   #  Kansas State University
 Installation   INST_OVSG         70   # Observatoire Volcanologique et Sismologique de Guadeloupe
 Installation   INST_BSU-BOISE    71   # Network in Boise, run by Zollweg for BSU
 Installation   INST_PA           72   # Observatrio Sismico del Occidente de Panama
 Installation   INST_INGV         73   # Istituto Nazionale di Geofisica e Vulcanologia
 Installation   INST_CORISUBMOD05 74    
 Installation   INST_KARTHALA     75   # IPGP, Paris installation at Volcanological Observatory of Karthala, Comoros Islands
 Installation   INST_SSN          76   # National Earthquake Information Service of Mexico
 Installation   INST_CASC         77   # Central America Seismic Center
 Installation   INST_INSIVUMEH    78   # National Observatory of Guatemala
 Installation   INST_UNAH         79   # Universidad Nacional Autonoma de Honduras
 Installation   INST_COPECO       80   # Comision Permanente de Contingencias (Honduras equivalent to U.S. FEMA)
 Installation   INST_RSN          81   # Red Sismica Nacional operated by the Univ. of Costa Rica
 Installation   INST_UPA          82   # Universidad de Panama
 Installation   INST_ARUBA        83   # Meteorological Service Aruba
 Installation   INST_PATRAS       84   # Univ. of Patras, Patras, Greece
 Installation   INST_EDELCA       85   # ELECTRIFICACION DEL CARONI (EDELCA), Venezuala
 Installation   INST_CAYMAN       86   # Hazard Management Cayman Islands
 Installation   INST_ACP          87   # Autoridad del Canal de Panama
 Installation   INST_ECUADOR      88   # Instituto Geofisico, Quito, Ecuador
 Installation   INST_NNSN         89   # Norwegian National Seismic Network, University Of Bergen
 Installation   INST_CSIRO        90   # Commonwealth Scientific and Industrial Research Organisation, Australia
 Installation   INST_PUNA         91   # Puna HI geothermal station
 Installation   INST_ISU          92   # Instituto Sismologico Universitario at Universidad Autónoma de Santo Domingo, Dom. Rep..
 Installation   INST_UCSD         93   # UC San Diego
 Installation   INST_GATECH       94   # Georgia Tech
 Installation   INST_VSI          95   # Volcanological Survey of Indonesia
 Installation   INST_PBO          96   # UNAVCO/EarthScope PBO
 Installation   INST_DSNU         97   # Digital Seismic Network of Uzbekistan
 Installation   INST_INDRHI       98   # Instituto Nacional de Recursos Hidraulicos, Dominican Republic
 Installation   INST_TUBITAK      99   # TUBITAK Marmara Research Center, Earth and Marine Science Inst., Gebze-Kocaeli-Turkey
 Installation   INST_QUITO       100
 Installation   INST_INETER      101
 Installation   INST_CENAPRED    102
 Installation   INST_RABAUL      103
 Installation   INST_COLIMA      104
 Installation   INST_SNET        105
 Installation   INST_OVSICORI    106   # Observatorio Vulcanologia y Sismologia de Costa Rica 
 Installation   INST_PCCHIAPAS   107   # Protección Civil de Chiapas  
 Installation   INST_NIOSH       108   # The National Institute for Occupational Safety and Health, Centers for Disease Control and Prevention
 Installation   INST_NDMI        109   # National Disaster Management of India
 Installation   INST_SRU         110   # Eastern Caribbean Seismograph Network, University of the West Indies
 Installation   INST_IDEI        111   # Instituto de Ingenieria, UNAM - Mexico
 Installation   INST_DPSN        112   # Public Seismic Network on Dominica
 Installation   INST_INPRES      113   # Instituto Nacional de Prevencion Sismica, San Juan, Argentina
 Installation   INST_IGSV        114   # Instituto Geofisico Sismologico Volponi, San Juan, Argentina
 Installation   INST_ISNET       115   # RISSC-Lab, Naples - www.rissclab.unina.it
 Installation   INST_IGT         116   # Istituto Geofisico Toscano
 Installation   INST_JSN         117   # Jamaica Seismograph Network, University of the West Indies, Mona, Jamaica
 Installation   INST_NOAIG       118   # National Observatory of Athens- Institute of Geodynamics
 Installation   INST_NMI         119   # Northern Mariana Islands Volcano Observatory
 Installation   INST_FUNVISIS    120   # Fundacion Venezolana de Investiagciones Sismologicas
 Installation   INST_TA          121   # Earthscope Transportable Array for NEIC
 Installation   INST_ASAIN       122   # Antarctic Seismographic Argentinean Italian Network
 Installation   INST_RSNC        123   # SGC - Red Sismologica Nacional de Colombia
 Installation   INST_RENASS      124   # Reseau National de Surveillance Sismique (French National Network of Seismic Survey
 Installation   INST_UALR        125   # University of Arkansas, Little Rock
 Installation   INST_MYMMD       126   # Malaysian Meteorology Department
 Installation   INST_SINICA      127   # Institute of Earth Science, Academia Sinica, Taiwan
 Installation   INST_OGS         128   # Oklahoma Geological Survey 
 Installation   INST_OPGC        129   # Auvergne Seismic Network in France
 Installation   INST_PHIVOLCS    130   # Philippine Institute of Volcanology and Seismology
 Installation   INST_PCJALISCO   131   # Unidad Estatal de Proteccion Civil y Bomberos Jalisco, Mexico
 Installation   INST_CALIXTO     132   # Observatorio San Calixto, Calle Indaburo, La Paz, Bolivia
 Installation   INST_INGEMMET    133   # Instituto Geologico Minero y Metalurgico, INGEMMET, Av Canada 1470 San Borjo, Lima, Peru
 Installation   INST_OVDAS       134   # Observatorio Volcanologico de los Andes del Sur, Dinamarca 661, Temuco, Chile
 Installation   INST_SISVOL      135   # Centro de sismologia y volcanologia de Occidente, Universidad de Gudalajara, Ave Universidad 202, Puerto Vallarta, Mexico
 Installation   INST_ISLA        136   # Infrasound Laboratory in Kona Hawaii
 Installation   INST_NCPA        137   # National Center for Physical Acoustics, University of Mississippi
 Installation   INST_RESNOM      138   # Red Sismica del Noroeste de Mexico
 Installation   INST_NKU         139   # Northern Kentucky University
 Installation   INST_NEIST       140   # North East Institute of Science and Technology, Jorhat, India
 Installation   INST_PRSM        141   # Puerto Rico Strong Motion Program
 Installation   INST_METEO       142   # National Institute of Meteorology, Tunisia
 Installation   INST_RESBAN      143   # Red Sismologica de Banda ancha del Golfo de California
 Installation   INST_CSN         144   # Chilean National Seismic Network, Universidad de Chile
 Installation   INST_CIVISA      145   # Centro de Informacao e Vigilancia Sismovulcanica dos Acores (Azores, Portugal)
 Installation   INST_CENAIS      146   # National Center of Seismological Research, Cuba
 Installation   INST_NTU         147   # Dept. of Geology, National Taiwan University
 Installation   INST_HAITI       148   # Requested by Caltech for Haitian network.
 Installation   INST_OSQ         149   # Seismological Observatory of Quindio University, Columbia
 Installation   INST_RAINIERAFM  150
 Installation   INST_PARIS       151   # IPGP, Institute of Earth Physics of Paris
 Installation   INST_REDSW       152   # Red Sismologica del Suroccidente Colombiano, Universidad del Valle
 Installation   INST_KIGAM       153   # Korea Institute of Geoscience and Mineral Resources
 Installation   INST_KOREA       154   # Korea NDC
 Installation   INST_NSMP        155   # USGS National Strong Motion Program
 Installation   INST_AZGS        156   # Arizona Geological Survey
 Installation   INST_CANISIUS    157   # Canisius College, Buffalo, NY
 Installation   INST_SSAN        158   # Sandia National Labs Seismo-Acoustic Network
 Installation   INST_OHIO        159   # Ohio DNR
 Installation   INST_PSN         160   # Public Seismic Network
 Installation   INST_MEMFDL      161   # Memphis Portable
 Installation   INST_UTEP        162   # University of Texas at El Paso
 Installation   INST_ULA         163   # Universidad de los Andes, Merida - Venezuela
 Installation   INST_PPNC        164   # SGC - Observatorio Vulcanologico y Sismologico de Popayan - Colombia
 Installation   INST_MZLC        165   # SGC - Observatorio Vulcanologico y Sismologico de Manizales - Colombia
 Installation   INST_PASC        166   # SGC - Observatorio Vulcanologico y Sismologico de Pasto - Colombia
 Installation   INST_IMGG        167   # Institute of Marine Geology and Geophysics, Far Eastern Branch, Russian Academy of Sciences
 Installation   INST_CRETE       168   # Laboratory of Geophysics and Seismology at the Technological Educational Institute of Crete, Greece
 Installation   INST_KSEB        169   # Kerala State Electricity Board [India]
 Installation   INST_OVIEDO      170   # Universidad de Oviedo Geology Department, Spain
 Installation   INST_ALTAROCK    171   # AltaRock Energy, Inc
 Installation   INST_MIAMIOH     172   # Miami University in Ohio
 Installation   INST_OVPF        173   # Fournaise Volcanoe Observatory, La RÃ©union
 Installation   INST_LIS         174   # Laboratorio de Ingenieria Sismica at the Univ. of Costa Rica
 Installation   INST_IGP         175   # Geophysical Institute of Peru
 Installation   INST_USF         176   # University of South Florida, Tampa - USA
 Installation   INST_ARTA        177   # Geophysical Observatory of Arta, Djibouti
 Installation   INST_EOS         178   # Earth Observatory of Singapore, Nanyang Technological University
 Installation   INST_RIO         179   # Seismology at Observatório Nacional, Rio de Janeiro
 Installation   INST_OSV_LNX     180   # Observatorio Sismologico Vulcanologico operated (OSV) by Centro de Ciencias de la Tierra (CCT) at Universidad Veracruzana
 Installation   INST_OSV_WIN     181   # Pico de Orizaba Volano observatory operated by Centro Nacional De Prevencion De Desastres (CENAPRED) and OSV.
 Installation   INST_PHIAFDRILL  182   # AF Drill, Philippines
 Installation   INST_MTA         183   # General Directorate Of Mineral Research And Explorations, Ankara, Turkey
 Installation   INST_UNAM        184   # Second id for Instituto de Ingenieria, UNAM - Mexico
 Installation   INST_REVOSIMA    185   # Mayotte seismic and volcanic monitoring network

# NEXT

# the INST_UNKNOWN is for those who wish to run earthworm and will not exchange
# messages with other installations.  Think of it as the ip private network
# such as 192.168 subnet.
 Installation   INST_UNKNOWN     255



#--------------------------------------------------------------------------
#                          Message Types
#
#  Define all message name/message-type pairs that will be global
#  to all Earthworm systems.
#
#  VALID numbers are:
#
#   0- 99 Message types 0-99 are defined in the file earthworm_global.d.
#         These numbers are reserved by Earthworm Central to label types 
#         of messages which may be exchanged between installations. These 
#         string/value mappings must be global to all Earthworm systems 
#         in order for exchanged messages to be properly interpreted.
#         
#
#  OFF-LIMITS numbers:
#
# 100-255 Message types 100-255 are defined in each installation's  
#         earthworm.d file, under the control of each Earthworm 
#         installation. These values should be used to label messages
#         which remain internal to an Earthworm system or installation.
# 
#         
# The maximum length of the type string is 32 characters.
#             
#--------------------------------------------------------------------------

# Global Earthworm message-type mappings (0-99):
 Message  TYPE_WILDCARD          0  # wildcard value - DO NOT CHANGE!!!   
 Message  TYPE_ADBUF             1  # multiplexed waveforms from DOS adsend
 Message  TYPE_ERROR             2  # error message
 Message  TYPE_HEARTBEAT         3  # heartbeat message
 Message  TYPE_TRACE2_COMP_UA    4  # compressed waveforms from compress_UA, with SCNL
#Message  TYPE_NANOBUF           5  # single-channel waveforms from nanometrics
 Message  TYPE_ACK               6  # acknowledgment sent by import to export
 Message  TYPE_PICK_SCNL         8  # P-wave arrival time (with location code) 
 Message  TYPE_CODA_SCNL         9  # coda info (plus station/loc code) from pick_ew 
 Message  TYPE_PICK2K           10  # P-wave arrival time (with 4 digit year) 
                                    #   from pick_ew 
 Message  TYPE_CODA2K           11  # coda info (plus station code) from pick_ew 
#Message  TYPE_PICK2            12  # P-wave arrival time from picker & pick_ew
#Message  TYPE_CODA2            13  # coda info from picker & pick_ew
 Message  TYPE_HYP2000ARC       14  # hyp2000 (Y2K hypoinverse) event archive  
                                    #   msg from eqproc/eqprelim
 Message  TYPE_H71SUM2K         15  # hypo71-format hypocenter summary msg 
                                    #   (with 4-digit year) from eqproc/eqprelim
#Message  TYPE_HINVARC          17  # hypoinverse event archive msg from 
                                    #   eqproc/eqprelim
#Message  TYPE_H71SUM           18  # hypo71-format summary msg from
                                    #   eqproc/eqprelim
 Message  TYPE_TRACEBUF2        19  # single-channel waveforms with channels 
                                    #   identified with sta,comp,net,loc (SCNL)
 Message  TYPE_TRACEBUF         20  # single-channel waveforms from NT adsend, 
                                    #   getdst2, nano2trace, rcv_ew, import_ida...
 Message  TYPE_LPTRIG           21  # single-channel long-period trigger from 
                                    #   lptrig & evanstrig
 Message  TYPE_CUBIC            22  # cubic-format summary msg from cubic_msg
 Message  TYPE_CARLSTATRIG      23  # single-channel trigger from carlstatrig
#Message  TYPE_TRIGLIST         24  # trigger-list msg (used by tracesave modules)
                                    #   from arc2trig, trg_assoc, carlsubtrig
 Message  TYPE_TRIGLIST2K       25  # trigger-list msg (with 4-digit year) used 
                                    #   by tracesave modules from arc2trig, 
                                    #   trg_assoc, carlsubtrig
 Message  TYPE_TRACE_COMP_UA    26  # compressed waveforms from compress_UA
#Message  TYPE_STRONGMOTION     27  # single-instrument peak accel, peak velocity,
                                    #   peak displacement, spectral acceleration 
 Message  TYPE_MAGNITUDE        28  # event magnitude: summary plus station info
 Message  TYPE_STRONGMOTIONII   29  # event strong motion parameters
 Message  TYPE_LOC_GLOBAL       30  # Global location message used by NEIC & localmag
 Message  TYPE_LPTRIG_SCNL      31  # single-channel long-period trigger from 
                                    #   lptrig & evanstrig (with location code)
 Message  TYPE_CARLSTATRIG_SCNL 32  # single-channel trigger from carlstatrig (with loc)
 Message  TYPE_TRIGLIST_SCNL    33  # trigger-list msg (with 4-digit year) used 
                                    #   by tracesave modules from arc2trig,  
                                    #   trg_assoc, carlsubtrig (with location code)
 Message  TYPE_TD_AMP           34  # time-domain reduced-rate amplitude summary
                                    #   produced by CISN RAD software & ada2ring
 Message  TYPE_MSEED            35  # Miniseed data record
 Message  TYPE_NOMAGNITUDE      36  # no event magnitude generated by localmag

 Message  TYPE_NAMED_EVENT	94  # TWC message for Windows compat
 Message  TYPE_HYPOTWC          95  # ATWC message
 Message  TYPE_PICK_GLOBAL      96  # ATWC message
 Message  TYPE_PICKTWC          97  # ATWC message
 Message  TYPE_ALARM            98  # ATWC message

#      !!!!   DO NOT make any changes to this file.  !!!!
