# Explorations of the REF 2021 submission data

Notes
- `Not specified - PP ADDED` is a category added during pre-processing to all string fields to replace missing values

## `Outputs` data

#### All records

    Read data/processed/Outputs_ppreprocessed.csv.gz: 185354 records
    
                                          Records  Records (%)
    Output type name                                          
    Journal article                        154826        83.53
    Authored book                           11801         6.37
    Chapter in book                          9475         5.11
    Conference contribution                  2272         1.23
    Edited book                              2135         1.15
    Other                                    1146         0.62
    Exhibition                                751         0.41
    Research report for external body         431         0.23
    Composition                               430         0.23
    Working paper                             390         0.21
    Artefact                                  378         0.20
    Digital or visual media                   360         0.19
    Scholarly edition                         329         0.18
    Performance                               312         0.17
    Design                                    119         0.06
    Website content                            67         0.04
    Translation                                38         0.02
    Patent/ published patent application       37         0.02
    Research data sets and databases           31         0.02
    Devices and products                       14         0.01
    Software                                   11         0.01



    
![png](study_files/study_4_1.png)
    


    
                                               Records  Records (%)
    Open access status                                             
    Compliant                                    85913        46.35
    Out of scope for open access requirements    58482        31.55
    Not specified - PP ADDED                     24174        13.04
    Technical exception                           4879         2.63
    Deposit exception                             4748         2.56
    Exception within 3 months of publication      2581         1.39
    Not compliant                                 2401         1.30
    Access exception                              1166         0.63
    Other exception                               1010         0.54



    
![png](study_files/study_4_3.png)
    


#### Records with `Output type` as _Software_

    Read data/processed/subsets/Outputs_ppreprocessed_type_software.csv.gz: 11 records
    
                              Records  Records (%)
    Open access status                            
    Not specified - PP ADDED       11       100.00
    
                              Records  Records (%)
    Interdisciplinary                             
    Not specified - PP ADDED        8        72.73
    Yes                             3        27.27
    
                                    Records  Records (%)
    Institution name                                    
    University College London             2        18.18
    University of Exeter                  2        18.18
    University of Ulster                  1         9.09
    Leeds Beckett University              1         9.09
    The University of Manchester          1         9.09
    University of Edinburgh               1         9.09
    Heriot-Watt University                1         9.09
    University of Cambridge               1         9.09
    University of the Arts, London        1         9.09
    
                                                    Records  Records (%)
    Main panel name                                                     
    Arts and humanities                                   6        54.55
    Social sciences                                       3        27.27
    Physical sciences, engineering and mathematics        2        18.18
    
                              Records  Records (%)
    Citations applicable                          
    Not specified - PP ADDED        9        81.82
    Yes                             2        18.18
    
                               Records  Records (%)
    Supplementary information                      
    Not specified - PP ADDED        11       100.00


#### Records with software terms in `Title`

    Read data/processed/subsets/Outputs_ppreprocessed_title_software_terms.csv.gz: 888 records
    
                                               Records  Records (%)
    Open access status                                             
    Compliant                                      463        52.14
    Out of scope for open access requirements      306        34.46
    Not specified - PP ADDED                        38         4.28
    Technical exception                             18         2.03
    Deposit exception                               18         2.03
    Access exception                                15         1.69
    Not compliant                                   12         1.35
    Exception within 3 months of publication        11         1.24
    Other exception                                  7         0.79
    
                              Records  Records (%)
    Interdisciplinary                             
    Not specified - PP ADDED      745        83.90
    Yes                           143        16.10
    
                                                    Records  Records (%)
    Main panel name                                                     
    Physical sciences, engineering and mathematics      503        56.64
    Medicine, health and life sciences                  211        23.76
    Social sciences                                     110        12.39
    Arts and humanities                                  64         7.21
    
                                                                       Records  Records (%)
    Institution name                                                                       
    University College London                                               41         4.62
    University of Oxford                                                    38         4.28
    Imperial College of Science, Technology and Medicine                    29         3.27
    University of Edinburgh                                                 26         2.93
    University of Southampton                                               26         2.93
    The University of Birmingham                                            22         2.48
    The University of Manchester                                            21         2.36
    The University of Warwick                                               21         2.36
    University of Bristol                                                   20         2.25
    Cardiff University / Prifysgol Caerdydd                                 20         2.25
    University of Cambridge                                                 19         2.14
    The University of Lancaster                                             19         2.14
    University of Nottingham, The                                           18         2.03
    Loughborough University                                                 18         2.03
    The University of Leeds                                                 18         2.03
    University of Greenwich                                                 17         1.91
    The University of Huddersfield                                          15         1.69
    University of Glasgow                                                   15         1.69
    City, University of London                                              14         1.58
    Brunel University London                                                14         1.58
    University of Portsmouth                                                13         1.46
    University of Sussex                                                    13         1.46
    The University of Bath                                                  13         1.46
    University of York                                                      13         1.46
    University of Ulster                                                    12         1.35
    University of Strathclyde                                               11         1.24
    University of Newcastle upon Tyne                                       11         1.24
    The University of Sheffield                                             11         1.24
    King's College London                                                   10         1.13
    Swansea University / Prifysgol Abertawe                                 10         1.13
    University of Durham                                                     9         1.01
    Middlesex University                                                     8         0.90
    Queen's University of Belfast                                            8         0.90
    Glasgow Caledonian University                                            8         0.90
    Queen Mary University of London                                          8         0.90
    Bournemouth University                                                   8         0.90
    The University of Leicester                                              8         0.90
    University of Northumbria at Newcastle                                   8         0.90
    University of the West of Scotland                                       8         0.90
    Coventry University                                                      8         0.90
    University of Exeter                                                     8         0.90
    University of the West of England, Bristol                               8         0.90
    De Montfort University                                                   7         0.79
    The University of Essex                                                  7         0.79
    University of Lincoln                                                    7         0.79
    The University of Bradford                                               7         0.79
    Aston University                                                         6         0.68
    Birkbeck College                                                         6         0.68
    Sheffield Hallam University                                              6         0.68
    Manchester Metropolitan University                                       6         0.68
    University of St Andrews                                                 6         0.68
    The University of Kent                                                   6         0.68
    Nottingham Trent University                                              6         0.68
    The Open University                                                      6         0.68
    Oxford Brookes University                                                6         0.68
    The University of Liverpool                                              6         0.68
    University of Salford, The                                               5         0.56
    The University of Hull                                                   5         0.56
    University of Plymouth                                                   5         0.56
    Birmingham City University                                               5         0.56
    Abertay University                                                       5         0.56
    The University of East Anglia                                            5         0.56
    Kingston University                                                      5         0.56
    Heriot-Watt University                                                   5         0.56
    University of Hertfordshire                                              5         0.56
    The University of Surrey                                                 5         0.56
    The University of Reading                                                4         0.45
    Royal Holloway and Bedford New College                                   4         0.45
    London School of Hygiene and Tropical Medicine                           4         0.45
    University of Central Lancashire                                         4         0.45
    Leeds Beckett University                                                 4         0.45
    Cranfield University                                                     4         0.45
    Goldsmiths' College                                                      4         0.45
    Robert Gordon University                                                 4         0.45
    University of Brighton                                                   4         0.45
    University of East London                                                4         0.45
    University of Wolverhampton                                              4         0.45
    Edinburgh Napier University                                              4         0.45
    University of Stirling                                                   4         0.45
    University of Chester                                                    3         0.34
    The University of Westminster                                            3         0.34
    University of Bedfordshire                                               3         0.34
    Aberystwyth University / Prifysgol Aberystwyth                           3         0.34
    Teesside University                                                      3         0.34
    The Royal Veterinary College                                             2         0.23
    University of Aberdeen                                                   2         0.23
    Bangor University / Prifysgol Bangor                                     2         0.23
    Wrexham Glyndŵr University / Prifysgol Glyndŵr Wrecsam                   2         0.23
    London South Bank University                                             2         0.23
    Liverpool Hope University                                                2         0.23
    SRUC                                                                     2         0.23
    University of Dundee                                                     2         0.23
    Liverpool John Moores University                                         2         0.23
    University of Northampton, The                                           2         0.23
    The University of Cumbria                                                2         0.23
    The Metanoia Institute                                                   1         0.11
    University of Sunderland                                                 1         0.11
    Falmouth University                                                      1         0.11
    University of South Wales / Prifysgol De Cymru                           1         0.11
    Institute of Cancer Research: Royal Cancer Hospital (The)                1         0.11
    University of the Highlands and Islands                                  1         0.11
    University of Derby                                                      1         0.11
    University of the Arts, London                                           1         0.11
    The London School of Economics and Political Science                     1         0.11
    Harper Adams University                                                  1         0.11
    St. George's Hospital Medical School                                     1         0.11
    Cardiff Metropolitan University / Prifysgol Metropolitan Caerdydd        1         0.11
    Staffordshire University                                                 1         0.11
    Anglia Ruskin University Higher Education Corporation                    1         0.11
    Bath Spa University                                                      1         0.11
    Leeds Arts University                                                    1         0.11

